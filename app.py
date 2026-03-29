import streamlit as st
import numpy as np
import random
import math
import plotly.graph_objects as go

# --- Ställ in sidans layout till bred ---
st.set_page_config(layout="wide", page_title="Matematikträning")

# --- Specialdesign (CSS) ---
st.markdown("""
<style>
input[type="text"] {
    font-size: 24px !important;
    font-weight: bold !important;
    text-align: center !important;
    padding: 15px !important;
}
.stTextInput label p {
    font-size: 18px !important;
    font-weight: bold !important;
}
.stAlert p {
    font-size: 18px !important;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# GEMENSAMMA MATEMATIK-FUNKTIONER
# ==========================================

# -- 1. Grafisk Funktion --
def generera_funktion():
    typ = random.choice(['linjar', 'kvadratisk', 'kubisk', 'exponential', 'sinus'])
    if typ == 'linjar':
        k = random.choice([-2, -1.5, -1, -0.5, 0.5, 1, 1.5, 2])
        m = random.randint(-4, 4)
        return lambda x: k * x + m
    elif typ == 'kvadratisk':
        a = random.choice([-1, -0.5, 0.5, 1])
        h = random.randint(-3, 3)
        v = random.randint(-4, 4)
        return lambda x: a * (x - h)**2 + v
    elif typ == 'kubisk':
        a = random.choice([-0.5, -0.25, 0.25, 0.5])
        h = random.randint(-2, 2)
        v = random.randint(-3, 3)
        return lambda x: a * (x - h)**3 + v
    elif typ == 'exponential':
        bas = random.choice([2.0, 0.5])
        a = random.choice([-2, -1, 1, 2])
        h = random.randint(-2, 2)
        v = random.randint(-4, 4)
        return lambda x: a * (bas ** (x - h)) + v
    elif typ == 'sinus':
        a = random.randint(2, 4) * random.choice([-1, 1])
        period = random.choice([0.25, 0.5]) 
        h = random.randint(-2, 2)
        v = random.randint(-2, 2)
        return lambda x: a * np.sin(np.pi * period * (x - h)) + v

def skapa_graf_uppgift(niva):
    for _ in range(100): 
        f = generera_funktion()
        giltiga_punkter = []
        for x_val in [i / 2 for i in range(-16, 17)]:
            y_val = f(x_val)
            if abs(y_val) <= 10 and round(y_val * 2, 4).is_integer():
                giltiga_punkter.append((round(x_val, 4), round(y_val, 4)))
                
        if not giltiga_punkter:
            continue 

        if niva == 1:
            target_x, target_y = random.choice(giltiga_punkter)
            fraga_typ = random.choice(['hitta_y', 'hitta_x'])
            if fraga_typ == 'hitta_y':
                fraga = f"Bestäm f({target_x:g})"
                ratt_svar = [target_y]
                st.session_state.q_type_vis = 'vis_find_y'
                st.session_state.trace_x = target_x
                st.session_state.trace_y = target_y
            else:
                target_y_snygg = target_y + 0.0 
                alla_x = list(set([p[0] for p in giltiga_punkter if p[1] == target_y]))
                if len(alla_x) > 3: continue 
                fraga = f"Bestäm ett värde på x så att f(x) = {target_y_snygg:g}"
                ratt_svar = sorted(alla_x)
                st.session_state.q_type_vis = 'vis_find_x'
                st.session_state.trace_y = target_y
                st.session_state.trace_alla_x = alla_x
            break 
            
        else:
            fraga_typ = random.choice(['f_x_plus_c', 'f_f_c', 'f_a_op_f_b', 'f_kx'])
            st.session_state.q_type_vis = 'vis_none'

            if fraga_typ == 'f_x_plus_c':
                hel_punkter = [p for p in giltiga_punkter if round(p[1], 4).is_integer()]
                if not hel_punkter: continue
                target_x, target_y = random.choice(hel_punkter)
                c = random.choice([-3, -2, -1, 1, 2, 3])
                c_str = f"+ {c}" if c > 0 else f"- {abs(c)}"
                alla_mål_x = [p[0] for p in giltiga_punkter if p[1] == target_y]
                if len(alla_mål_x) > 3: continue 
                target_y_snygg = target_y + 0.0
                fraga = f"Bestäm x om f(x {c_str}) = {target_y_snygg:g}"
                ratt_svar = sorted([tx - c for tx in alla_mål_x])
                st.session_state.q_type_vis = 'vis_find_x'
                st.session_state.trace_y = target_y
                st.session_state.trace_alla_x = alla_mål_x
                break
                
            elif fraga_typ == 'f_f_c':
                valid_c = []
                for x_val in range(-8, 9):
                    y1 = f(x_val)
                    if round(y1, 4).is_integer() and -8 <= y1 <= 8:
                        y2 = f(y1)
                        if abs(y2) <= 10 and round(y2 * 2, 4).is_integer():
                            valid_c.append(x_val)
                if not valid_c: continue 
                c = random.choice(valid_c)
                y1 = round(f(c), 4)
                y2 = round(f(y1), 4)
                ratt_svar = [y2]
                fraga = f"Bestäm f(f({c}))"
                break
                
            elif fraga_typ == 'f_a_op_f_b':
                hel_punkter = [p for p in giltiga_punkter if round(p[1], 4).is_integer() and round(p[0], 4).is_integer()]
                if len(hel_punkter) < 2: continue
                p1, p2 = random.sample(hel_punkter, 2)
                op = random.choice(['+', '-'])
                if op == '+': svar = p1[1] + p2[1]
                else: svar = p1[1] - p2[1]
                fraga = f"Bestäm f({p1[0]:g}) {op} f({p2[0]:g})"
                ratt_svar = [svar]
                break
                
            elif fraga_typ == 'f_kx':
                mål_y = random.choice([p[1] for p in giltiga_punkter])
                alla_mål_x = [p[0] for p in giltiga_punkter if p[1] == mål_y]
                if len(alla_mål_x) > 3: continue 
                k_val = random.choice([2, -2])
                mojliga_svar = [x / k_val for x in alla_mål_x]
                if all(round(s * 2, 4).is_integer() and abs(s) <= 20 for s in mojliga_svar):
                    k_str = f"{k_val:g}"
                    mål_y_snygg = mål_y + 0.0
                    fraga = f"Bestäm x om f({k_str}x) = {mål_y_snygg:g}"
                    ratt_svar = sorted(mojliga_svar)
                    st.session_state.q_type_vis = 'vis_find_x'
                    st.session_state.trace_y = mål_y
                    st.session_state.trace_alla_x = alla_mål_x
                    break
                else:
                    continue
    else:
        f = lambda x: x
        fraga = "Bestäm f(1)"
        ratt_svar = [1.0]

    st.session_state.graf_f = f
    st.session_state.graf_fraga = fraga.replace('.', ',')
    st.session_state.graf_ratt_svar = [round(ans, 4) + 0.0 for ans in ratt_svar]

# -- PLOTLY RIT-FUNKTION --
def rita_plotly_graf(f, visa_facit=False, q_vis_type='vis_none', trace_x=None, trace_y=None, trace_alla_x=None):
    fig = go.Figure()
    
    x_plot = np.linspace(-10, 10, 400)
    y_plot = f(x_plot)
    
    fig.add_trace(go.Scatter(
        x=x_plot, y=y_plot, mode='lines', 
        line=dict(color='blue', width=2), 
        hoverinfo='skip'
    ))
    
    if visa_facit:
        if q_vis_type == 'vis_find_y':
            tx, ty = trace_x, trace_y
            fig.add_trace(go.Scatter(
                x=[tx, tx, 0], y=[0, ty, ty], 
                mode='lines+markers', line=dict(color='red', dash='dash', width=2), 
                marker=dict(size=8, color='red'), showlegend=False, hoverinfo='skip'
            ))
        elif q_vis_type == 'vis_find_x':
            ty = trace_y
            ax_list = trace_alla_x
            if ax_list:
                min_ax, max_ax = min(ax_list + [0]), max(ax_list + [0])
                fig.add_trace(go.Scatter(
                    x=[min_ax, max_ax], y=[ty, ty], 
                    mode='lines', line=dict(color='red', dash='dash', width=2), showlegend=False, hoverinfo='skip'
                ))
                for ax_v in ax_list:
                    fig.add_trace(go.Scatter(
                        x=[ax_v, ax_v], y=[ty, 0], 
                        mode='lines+markers', line=dict(color='red', dash='dash', width=2), 
                        marker=dict(size=8, color='red'), showlegend=False, hoverinfo='skip'
                    ))

    tick_vals = [-10, -5, 5, 10]
    fig.add_trace(go.Scatter(
        x=tick_vals, y=[-0.6]*4, mode='text', text=[str(v) for v in tick_vals],
        textposition='bottom center', showlegend=False, hoverinfo='skip', textfont=dict(color='black', size=14)
    ))
    fig.add_trace(go.Scatter(
        x=[-0.6]*4, y=tick_vals, mode='text', text=[str(v) for v in tick_vals],
        textposition='middle left', showlegend=False, hoverinfo='skip', textfont=dict(color='black', size=14)
    ))
    fig.add_trace(go.Scatter(
        x=[-0.4], y=[-0.6], mode='text', text=['0'],
        textposition='bottom left', showlegend=False, hoverinfo='skip', textfont=dict(color='black', size=14)
    ))

    axis_layout = dict(
        range=[-10.8, 10.8], 
        zeroline=True, zerolinewidth=3, zerolinecolor='black', 
        showgrid=True, gridwidth=2, gridcolor='#cccccc', 
        minor=dict(dtick=1, gridwidth=2, gridcolor='#e0e0e0'), 
        showticklabels=False, 
        fixedrange=True 
    )

    pil_inst = dict(showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2, arrowcolor='black')
    
    fig.update_layout(
        xaxis=axis_layout,
        yaxis=axis_layout,
        showlegend=False,
        margin=dict(l=20, r=20, t=20, b=20),
        height=550,
        plot_bgcolor='white',
        hovermode=False,
        dragmode=False,
        annotations=[
            dict(x=10.8, y=0, ax=9.8, ay=0, xref='x', yref='y', axref='x', ayref='y', **pil_inst),
            dict(x=10.8, y=-0.5, text="x", showarrow=False, xref='x', yref='y', font=dict(size=16, color='black')),
            dict(x=0, y=10.8, ax=0, ay=9.8, xref='x', yref='y', axref='x', ayref='y', **pil_inst),
            dict(x=-0.5, y=10.8, text="y", showarrow=False, xref='x', yref='y', font=dict(size=16, color='black'))
        ]
    )
    return fig

# -- 2. Algebraisk Funktion --
def skapa_alg_func_uppgift(niva):
    while True:
        if niva == 1:
            # Ny typ tillagd: 'f_x_C_kvadrat'
            typ = random.choice(['f_a', 'f_x_C', 'f_x_C_kvadrat'])
            
            if typ == 'f_a':
                func_type = random.choice(['linjar', 'kvadratisk', 'exponential'])
                a = random.randint(-10, 10)
                if func_type == 'linjar':
                    k = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
                    m = random.randint(-10, 10)
                    svar = k*a + m
                    k_str = "x" if k == 1 else ("-x" if k == -1 else f"{k}x")
                    m_str = f" + {m}" if m > 0 else (f" - {-m}" if m < 0 else "")
                    f_str = f"{k_str}{m_str}"
                elif func_type == 'kvadratisk':
                    k = random.choice([-3, -2, -1, 1, 2, 3])
                    m = random.randint(-10, 10)
                    a = random.randint(-5, 5) 
                    svar = k*(a**2) + m
                    k_str = "x^2" if k == 1 else ("-x^2" if k == -1 else f"{k}x^2")
                    m_str = f" + {m}" if m > 0 else (f" - {-m}" if m < 0 else "")
                    f_str = f"{k_str}{m_str}"
                else:
                    bas = random.choice([2, 3])
                    a = random.randint(0, 4) 
                    k = random.choice([-3, -2, -1, 1, 2, 3])
                    svar = k * (bas**a)
                    if k == 1: f_str = f"{bas}^x"
                    elif k == -1: f_str = f"-{bas}^x"
                    else: f_str = f"{k} \cdot {bas}^x"
                
                if abs(svar) <= 100:
                    st.session_state.alg_fraga = f"Bestäm f({a})"
                    st.session_state.alg_funktion = f"f(x) = {f_str}"
                    st.session_state.alg_svar = svar
                    break
                    
            elif typ == 'f_x_C_kvadrat':
                # NY: Lös f(x) = C för andragradsfunktioner (endast positivt x för att få ett unikt svar)
                x = random.randint(1, 10) # Bara positiva x
                k = random.choice([-3, -2, -1, 1, 2, 3])
                m = random.randint(-15, 15)
                C = k*(x**2) + m
                k_str = "x^2" if k == 1 else ("-x^2" if k == -1 else f"{k}x^2")
                m_str = f" + {m}" if m > 0 else (f" - {-m}" if m < 0 else "")
                f_str = f"{k_str}{m_str}"
                
                if abs(C) <= 300:
                    st.session_state.alg_fraga = f"Bestäm det positiva värdet på x om f(x) = {C}"
                    st.session_state.alg_funktion = f"f(x) = {f_str}"
                    st.session_state.alg_svar = x
                    break
                    
            else: # f(x) = C (Linjär)
                b = random.choice([1, 1, 2, 3, 4]) 
                a_coeff = random.choice([-4, -3, -2, -1, 1, 2, 3, 4])
                
                if b > 1 and abs(a_coeff) % b == 0:
                    continue

                m = random.randint(-15, 15)
                x = random.randint(-20, 20) * b 
                if b == 1:
                    k_str = "x" if a_coeff == 1 else ("-x" if a_coeff == -1 else f"{a_coeff}x")
                    C = a_coeff*x + m
                    term_x = k_str
                else:
                    if a_coeff == 1: term_x = f"\\frac{{x}}{{{b}}}"
                    elif a_coeff == -1: term_x = f"-\\frac{{x}}{{{b}}}"
                    else: term_x = f"\\frac{{{a_coeff}x}}{{{b}}}"
                    
                    C = int((a_coeff*x)/b + m)
                m_str = f" + {m}" if m > 0 else (f" - {-m}" if m < 0 else "")
                f_str = f"{term_x}{m_str}"
                
                if abs(x) <= 100 and abs(C) <= 100:
                    st.session_state.alg_fraga = f"Bestäm x om f(x) = {C}"
                    st.session_state.alg_funktion = f"f(x) = {f_str}"
                    st.session_state.alg_svar = x
                    break
                    
        else: # Niva 2 
            typ = random.choice(['f_f_a', 'f_f_x_C', 'f_g_a', 'f_likamed_g'])
            
            # Hjälpfunktion för att formatera kx + m snyggt
            def formatera_linjar(k, m):
                k_str = "x" if k == 1 else ("-x" if k == -1 else f"{k}x")
                if m == 0: return k_str
                m_str = f" + {m}" if m > 0 else f" - {-m}"
                return f"{k_str}{m_str}"

            if typ in ['f_f_a', 'f_f_x_C']:
                # Din ursprungliga logik för f(f(x))
                k = random.choice([-3, -2, -1, 2, 3])
                m = random.randint(-10, 10)
                f_str = formatera_linjar(k, m)
                
                if typ == 'f_f_a':
                    a = random.randint(-8, 8)
                    inner = k*a + m
                    svar = k*inner + m
                    if abs(svar) <= 150:
                        st.session_state.alg_fraga = f"Bestäm f(f({a}))"
                        st.session_state.alg_funktion = f"f(x) = {f_str}"
                        st.session_state.alg_svar = svar
                        break
                else: # f_f_x_C
                    x = random.randint(-12, 12)
                    inner = k*x + m
                    C = k*inner + m
                    if abs(x) <= 100 and abs(C) <= 150:
                        st.session_state.alg_fraga = f"Bestäm x om f(f(x)) = {C}"
                        st.session_state.alg_funktion = f"f(x) = {f_str}"
                        st.session_state.alg_svar = x
                        break
                        
            elif typ == 'f_g_a':
                # NY: Två funktioner, bestäm f(g(a))
                k1 = random.choice([-4, -3, -2, -1, 2, 3, 4])
                m1 = random.randint(-10, 10)
                k2 = random.choice([-4, -3, -2, -1, 2, 3, 4])
                m2 = random.randint(-10, 10)
                
                a = random.randint(-5, 5)
                g_a = k2*a + m2
                svar = k1*g_a + m1
                
                f_str = formatera_linjar(k1, m1)
                g_str = formatera_linjar(k2, m2)
                
                st.session_state.alg_fraga = f"Bestäm f(g({a}))"
                st.session_state.alg_funktion = f"f(x) = {f_str} \quad \text{{och}} \quad g(x) = {g_str}"
                st.session_state.alg_svar = svar
                break
                
            elif typ == 'f_likamed_g':
                # NY: Lös ekvationen f(x) = g(x)
                x = random.randint(-10, 10)
                k1 = random.choice([-5, -4, -3, -2, 2, 3, 4, 5])
                k2 = random.choice([-5, -4, -3, -2, 2, 3, 4, 5])
                if k1 == k2: continue # Måste ha olika lutning för att få ett unikt x
                
                m1 = random.randint(-15, 15)
                # Anpassar m2 så att ekvationen går jämnt upp med vårt slumpade x
                m2 = (k1 - k2)*x + m1 
                
                f_str = formatera_linjar(k1, m1)
                g_str = formatera_linjar(k2, m2)
                
                st.session_state.alg_fraga = "Bestäm x om f(x) = g(x)"
                st.session_state.alg_funktion = f"f(x) = {f_str} \quad \text{{och}} \quad g(x) = {g_str}"
                st.session_state.alg_svar = x
                break
# -- 3. Ekvationer --
def formatera_sida(k, m):
    if k == 1: k_str = "x"
    elif k == -1: k_str = "-x"
    elif k == 0: k_str = ""
    else: k_str = f"{k}x"
    
    if k == 0: return str(m)
    if m > 0: return f"{k_str} + {m}"
    elif m < 0: return f"{k_str} - {-m}"
    else: return k_str

def skapa_ekv_uppgift(niva):
    while True:
        x = random.randint(-10, 10)
        
        if niva == 1:
            typ = random.choice(['tvosteg', 'division', 'bada_sidor', 'enkel_parentes'])
            
            if typ == 'tvosteg':
                a = random.choice([-5, -4, -3, -2, -1, 2, 3, 4, 5])
                b = random.randint(-15, 15)
                c = a * x + b
                st.session_state.ekv_str = f"{formatera_sida(a, b)} = {c}"
                st.session_state.ekv_svar = x
                break
                
            elif typ == 'division':
                a = random.choice([2, 3, 4, 5])
                # Måste se till att divisionen går jämnt upp
                x = random.randint(-6, 6) * a 
                b = random.randint(-10, 10)
                c = int(x / a) + b
                b_str = f" + {b}" if b > 0 else (f" - {-b}" if b < 0 else "")
                st.session_state.ekv_str = f"\\frac{{x}}{{{a}}}{b_str} = {c}"
                st.session_state.ekv_svar = x
                break
                
            elif typ == 'bada_sidor':
                a = random.choice([-5, -4, -3, -2, 2, 3, 4, 5])
                c_coeff = random.choice([-5, -4, -3, -2, 2, 3, 4, 5])
                if a == c_coeff: continue 
                b = random.randint(-20, 20)
                d = a * x + b - c_coeff * x
                st.session_state.ekv_str = f"{formatera_sida(a, b)} = {formatera_sida(c_coeff, d)}"
                st.session_state.ekv_svar = x
                break
                
            elif typ == 'enkel_parentes':
                a = random.choice([-5, -4, -3, -2, 2, 3, 4, 5])
                b = random.choice([-5, -4, -3, -2, 1, 2, 3, 4, 5])
                c = a * (x + b)
                b_str = f"+ {b}" if b > 0 else f"- {-b}"
                st.session_state.ekv_str = f"{a}(x {b_str}) = {c}"
                st.session_state.ekv_svar = x
                break

        else: # Niva 2
            # Nu finns 5 olika tuffa ekvationstyper som lottas fram!
            typ = random.choice(['nuvarande', 'parenteser_bada', 'gemensam_namnare', 'x_i_namnare', 'gomda_forstagrads'])
            
            if typ == 'nuvarande':
                A = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
                C = random.choice([2, 3, 4, 5])
                val_VL = random.randint(-10, 10)
                B = C * val_VL - A * x
                if abs(A) % C == 0 and abs(B) % C == 0: continue
                E = random.choice([1, 2, 3, 4, 5])
                F = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
                op = random.choice(['+', '-'])
                if op == '+': D = val_VL - E * (x + F)
                else: D = val_VL + E * (x + F)
                
                if A == 1: A_str = "x"
                elif A == -1: A_str = "-x"
                else: A_str = f"{A}x"
                
                if B > 0: B_str = f" + {B}"
                elif B < 0: B_str = f" - {-B}"
                else: B_str = ""
                
                VL = f"\\frac{{{A_str}{B_str}}}{{{C}}}"
                E_str = "" if E == 1 else str(E)
                F_str = f"+ {F}" if F > 0 else f"- {-F}"
                HL = f"{D} {op} {E_str}(x {F_str})"
                
                st.session_state.ekv_str = f"{VL} = {HL}"
                st.session_state.ekv_svar = x
                break
                
            elif typ == 'parenteser_bada':
                A = random.choice([2, 3, 4, 5])
                D = random.choice([2, 3, 4, 5])
                if A == D: continue
                B = random.choice([-5, -4, -3, -2, 1, 2, 3, 4, 5])
                E = random.choice([-5, -4, -3, -2, 1, 2, 3, 4, 5])
                C = D*x + D*E - A*x - A*B
                B_str = f"+ {B}" if B > 0 else f"- {-B}"
                E_str = f"+ {E}" if E > 0 else f"- {-E}"
                C_str = f" + {C}" if C > 0 else (f" - {-C}" if C < 0 else "")
                
                VL = f"{A}(x {B_str}){C_str}"
                HL = f"{D}(x {E_str})"
                
                st.session_state.ekv_str = f"{VL} = {HL}"
                st.session_state.ekv_svar = x
                break
                
            elif typ == 'gemensam_namnare':
                B = random.choice([2, 3, 4])
                D = random.choice([2, 3, 4])
                if B == D: continue
                A = random.randint(-5, 5)
                x_term1 = random.randint(-3, 3) * B
                x = x_term1 - A
                C = random.randint(-5, 5)
                val_VL1 = (x + A) / B
                val_VL2 = (x + C) / D
                E = val_VL1 + val_VL2
                if not E.is_integer(): continue 
                E = int(E)
                A_str = f"+ {A}" if A > 0 else (f"- {-A}" if A < 0 else "")
                C_str = f"+ {C}" if C > 0 else (f"- {-C}" if C < 0 else "")
                VL = f"\\frac{{x {A_str}}}{{{B}}} + \\frac{{x {C_str}}}{{{D}}}"
                
                st.session_state.ekv_str = f"{VL} = {E}"
                st.session_state.ekv_svar = x
                break
                
            elif typ == 'x_i_namnare':
                B = random.choice([-5, -4, -3, -2, 1, 2, 3, 4, 5])
                x = random.randint(-10, 10)
                if x + B == 0: continue 
                C = random.choice([-4, -3, -2, -1, 2, 3, 4])
                A = C * (x + B)
                B_str = f"+ {B}" if B > 0 else f"- {-B}"
                VL = f"\\frac{{{A}}}{{x {B_str}}}"
                
                st.session_state.ekv_str = f"{VL} = {C}"
                st.session_state.ekv_svar = x
                break
                
            elif typ == 'gomda_forstagrads':
                A = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
                B = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
                C = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
                
                # Om x-termerna tar ut varandra helt på båda sidor går det inte att lösa för x
                if A + B == C: continue 
                
                # Räkna ut konstanten D så att ekvationen stämmer med vårt slumpade x
                D = (A + B - C) * x + A * B
                
                A_str = f"+ {A}" if A > 0 else f"- {-A}"
                B_str = f"+ {B}" if B > 0 else f"- {-B}"
                
                if C == 1: C_str = "+ x"
                elif C == -1: C_str = "- x"
                elif C > 0: C_str = f"+ {C}x"
                else: C_str = f"- {-C}x"
                
                if D > 0: D_str = f"+ {D}"
                elif D < 0: D_str = f"- {-D}"
                else: D_str = ""
                
                VL = f"(x {A_str})(x {B_str})"
                HL = f"x^2 {C_str} {D_str}".strip()
                
                st.session_state.ekv_str = f"{VL} = {HL}"
                st.session_state.ekv_svar = x
                break
# -- 4. Algebra Uttryck --
def skapa_alg_uttryck_uppgift(niva=1):
    def formatera_svar(k2, k, m):
        res = ""
        if k2 == 1: res += "x^2"
        elif k2 == -1: res += "-x^2"
        elif k2 != 0: res += f"{k2}x^2"
        if k != 0:
            if k == 1: res += " + x" if res else "x"
            elif k == -1: res += " - x" if res else "-x"
            elif k > 0: res += f" + {k}x" if res else f"{k}x"
            elif k < 0: res += f" - {-k}x" if res else f"{k}x"
        if m != 0:
            if m > 0: res += f" + {m}" if res else f"{m}"
            elif m < 0: res += f" - {-m}" if res else f"{m}"
        if res == "": return "0"
        return res

    if niva == 1:
        typ = random.choice(['minus_parentes', 'mult_parentes', 'konstant_parentes', 'faktorisera'])
        
        if typ == 'minus_parentes':
            st.session_state.alg_rubrik = "Förenkla uttrycket:"
            c = random.choice([2, 3, 4])
            A = random.randint(-5, 5)
            B = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            
            if A == 0:
                del_1 = "x"
            else:
                A_str = f"+ {A}" if A > 0 else f"- {-A}"
                del_1 = f"(x {A_str})"
                
            B_str = f"+ {B}" if B > 0 else f"- {-B}"
            st.session_state.alg_uttryck_str = f"{del_1} - ({c}x {B_str})"
            
            svar_ratt = formatera_svar(0, 1 - c, A - B)
            d1 = formatera_svar(0, 1 - c, A + B) 
            d2 = formatera_svar(0, 1 + c, A - B) 
            d3 = formatera_svar(0, 1 + c, A + B) 
            
        elif typ == 'konstant_parentes':
            st.session_state.alg_rubrik = "Förenkla uttrycket:"
            a = random.randint(2, 5)
            c = random.randint(2, 5)
            A = random.choice([-4, -3, -2, 2, 3, 4])
            B = random.choice([-4, -3, -2, 2, 3, 4])
            A_str = f"+ {A}" if A > 0 else f"- {-A}"
            B_str = f"+ {B}" if B > 0 else f"- {-B}"
            op = random.choice(['+', '-'])
            if op == '-':
                st.session_state.alg_uttryck_str = f"{a}(x {A_str}) - {c}(x {B_str})"
                svar_ratt = formatera_svar(0, a - c, a*A - c*B)
                d1 = formatera_svar(0, a - c, a*A + c*B)
                d2 = formatera_svar(0, a - c, a*A - B)
                d3 = formatera_svar(0, a + c, a*A - c*B)
            else:
                st.session_state.alg_uttryck_str = f"{a}(x {A_str}) + {c}(x {B_str})"
                svar_ratt = formatera_svar(0, a + c, a*A + c*B)
                d1 = formatera_svar(0, a + c, a*A - c*B)
                d2 = formatera_svar(0, a + c, a*A + B)
                d3 = formatera_svar(0, a - c, a*A + c*B)
                
        elif typ == 'mult_parentes':
            st.session_state.alg_rubrik = "Förenkla uttrycket:"
            A = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            B = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            A_str = f"+ {A}" if A > 0 else f"- {-A}"
            B_str = f"+ {B}" if B > 0 else f"- {-B}"
            st.session_state.alg_uttryck_str = f"(x {A_str})(x {B_str})"
            svar_ratt = formatera_svar(1, A + B, A * B)
            d1 = formatera_svar(1, A - B, A * B)
            d2 = formatera_svar(1, A + B, -(A * B))
            d3 = formatera_svar(1, -A - B, A * B)

        elif typ == 'faktorisera':
            st.session_state.alg_rubrik = "Faktorisera uttrycket så långt som möjligt:"
            k = random.choice([2, 3, 4, 5, 6, 7]) 
            a = random.choice([2, 3, 4, 5, 6])
            b = random.choice([1, 2, 3, 4, 5, 6])
            while math.gcd(a, b) != 1:
                b = random.randint(1, 6)
            A = k * a
            B = k * b
            op = random.choice(['+', '-'])
            st.session_state.alg_uttryck_str = f"{A}x {op} {B}"
            svar_ratt = f"{k}({a}x {op} {b})"
            d1 = f"{k}({a}x {op} {B})"  
            d2 = f"{a}({k}x {op} {b})" 
            d3 = f"{k}x({a} {op} {b})" if op == '+' else f"{k}x({a} - {b})"

    else: # Nivå 2
        typ = random.choice(['faktorisera_avancerat', 'mult_parentes_koeff', 'flersteg', 'rationell'])
        
        if typ == 'faktorisera_avancerat':
            st.session_state.alg_rubrik = "Faktorisera uttrycket så långt som möjligt:"
            c = random.choice([2, 3, 4, 5]) 
            a = random.choice([2, 3, 4, 5])
            b = random.choice([1, 2, 3, 4, 5])
            while math.gcd(a, b) != 1:
                b = random.randint(1, 5)
            
            var_typ = random.choice(['xy', 'x2'])
            op = random.choice(['+', '-'])
            A = c * a
            B = c * b
            
            if var_typ == 'xy':
                st.session_state.alg_uttryck_str = f"{A}xy {op} {B}x"
                svar_ratt = f"{c}x({a}y {op} {b})"
                d1 = f"{c}({a}xy {op} {b}x)"     
                d2 = f"x({A}y {op} {B})"         
                d3 = f"{c}x({a}y {op} {B})"      
            else:
                st.session_state.alg_uttryck_str = f"{A}x^2 {op} {B}x"
                svar_ratt = f"{c}x({a}x {op} {b})"
                d1 = f"{c}({a}x^2 {op} {b}x)"    
                d2 = f"x({A}x {op} {B})"         
                d3 = f"{c}x({a}x {op} {B})"      

        elif typ == 'mult_parentes_koeff':
            st.session_state.alg_rubrik = "Förenkla uttrycket:"
            a = random.choice([2, 3, 4])
            c = random.choice([2, 3, 4])
            b = random.choice([-4, -3, -2, -1, 1, 2, 3, 4])
            d = random.choice([-4, -3, -2, -1, 1, 2, 3, 4])
            b_str = f"+ {b}" if b > 0 else f"- {-b}"
            d_str = f"+ {d}" if d > 0 else f"- {-d}"
            
            st.session_state.alg_uttryck_str = f"({a}x {b_str})({c}x {d_str})"
            svar_ratt = formatera_svar(a*c, a*d + b*c, b*d)
            d1 = formatera_svar(a*c, 0, b*d) 
            d2 = formatera_svar(a*c, a*d - b*c, b*d) 
            d3 = formatera_svar(a+c, a*d + b*c, b*d) 

        elif typ == 'flersteg':
            st.session_state.alg_rubrik = "Förenkla uttrycket:"
            a = random.choice([2, 3])
            b = random.choice([-4, -3, 2, 3, 4])
            c = random.choice([-3, -2, -1, 1, 2, 3])
            d = random.choice([-3, -2, -1, 1, 2, 3])
            b_str = f"+ {b}" if b > 0 else f"- {-b}"
            c_str = f"+ {c}" if c > 0 else f"- {-c}"
            d_str = f"+ {d}" if d > 0 else f"- {-d}"
            
            st.session_state.alg_uttryck_str = f"x({a}x {b_str}) - (x {c_str})(x {d_str})"
            svar_ratt = formatera_svar(a - 1, b - (c + d), -(c * d))
            d1 = formatera_svar(a - 1, b - (c + d), c * d) 
            d2 = formatera_svar(a - 1, b + c + d, -(c * d)) 
            d3 = formatera_svar(a + 1, b - (c + d), -(c * d)) 

        elif typ == 'rationell':
            st.session_state.alg_rubrik = "Förenkla uttrycket:"
            C = random.choice([2, 3, 4, 5])
            a = random.choice([-4, -3, -2, 2, 3, 4])
            b = random.choice([-5, -4, -3, -2, 2, 3, 4, 5])
            B_str = f"+ {b*C}" if b*C > 0 else f"- {-b*C}"
            
            st.session_state.alg_uttryck_str = f"\\frac{{{a*C}x^2 {B_str}x}}{{{C}x}}"
            b_svar = f"+ {b}" if b > 0 else f"- {-b}"
            svar_ratt = f"{a}x {b_svar}"
            B_fel = f"+ {b*C}" if b*C > 0 else f"- {-b*C}"
            
            d1 = f"{a}x^2 {b_svar}" 
            d2 = f"{a}x {B_fel}"    
            d3 = f"{a*C}x {b_svar}"   

    svar_ratt_latex = f"${svar_ratt}$"
    alternativ = list(set([svar_ratt_latex, f"${d1}$", f"${d2}$", f"${d3}$"]))
    while len(alternativ) < 4:
        alternativ.append(alternativ[0].replace("$", " $", 1)) 
        alternativ = list(set(alternativ))
    
    random.shuffle(alternativ)
    st.session_state.alg_uttryck_alternativ = alternativ
    st.session_state.alg_uttryck_svar = svar_ratt_latex

# --- MENYSYSTEM ---
st.sidebar.title("Välj Träningsläge")
vald_kategori = st.sidebar.radio("Vad vill du träna på?", [
    "Funktioner: Grafisk lösning",
    "Funktioner: Algebraisk lösning",
    "Ekvationer",
    "Algebra",
    "Blandat (Slumpas)"
])

if 'aktuell_kategori' not in st.session_state:
    st.session_state.aktuell_kategori = vald_kategori

if st.session_state.aktuell_kategori != vald_kategori:
    for key in list(st.session_state.keys()):
        if key != 'aktuell_kategori':
            del st.session_state[key]
    st.session_state.aktuell_kategori = vald_kategori
    st.rerun()

st.sidebar.divider()

# ==========================================
# MODUL 1: Funktioner grafisk lösning
# ==========================================
if vald_kategori == "Funktioner: Grafisk lösning":
    st.title("Grafisk avläsning av funktioner")

    if 'niva' not in st.session_state: st.session_state.niva = 1
    if 'graf_fraga' not in st.session_state:
        skapa_graf_uppgift(st.session_state.niva)
        st.session_state.graf_uppgift_nr = 1
    if 'submitted_ans' not in st.session_state: st.session_state.submitted_ans = False
    if 'svar_status' not in st.session_state: st.session_state.svar_status = None

    # INSTÄLLNINGAR I SIDOFÄLTET
    with st.sidebar:
        st.subheader("Inställningar")
        aktuellt_index = 0 if st.session_state.niva == 1 else 1
        ny_niva = st.radio("Välj svårighetsgrad:", [1, 2], horizontal=True, index=aktuellt_index, key="graf_niva_val")
        if ny_niva != st.session_state.niva:
            st.session_state.niva = ny_niva
            st.session_state.submitted_ans = False
            skapa_graf_uppgift(st.session_state.niva)
            st.session_state.graf_uppgift_nr += 1
            st.rerun()

    # LAYOUT
    col_vanster, col_hoger = st.columns([1.2, 1], gap="large")

    with col_vanster:
        fig = rita_plotly_graf(
            f = st.session_state.graf_f,
            visa_facit = st.session_state.submitted_ans,
            q_vis_type = st.session_state.get('q_type_vis', 'vis_none'),
            trace_x = st.session_state.get('trace_x'),
            trace_y = st.session_state.get('trace_y'),
            trace_alla_x = st.session_state.get('trace_alla_x')
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with col_hoger:
        st.subheader("Uppgift")
        st.markdown(f"<div style='font-size: 32px; font-weight: bold; color: #0056b3; margin-bottom: 20px;'>{st.session_state.graf_fraga}</div>", unsafe_allow_html=True)
        
        antal_svar = len(st.session_state.graf_ratt_svar)
        svar_lista = []
        for i in range(antal_svar):
            etikett = f"Svar {i+1}:" if antal_svar > 1 else "Skriv ditt svar här:"
            svar = st.text_input(etikett, key=f"graf_input_{st.session_state.graf_uppgift_nr}_{i}")
            svar_lista.append(svar)
            
        st.write("") 
        k1, k2 = st.columns(2)
        with k1:
            if st.button("Rätta svar", type="primary", use_container_width=True):
                st.session_state.submitted_ans = True
                if all(s.strip() != "" for s in svar_lista):
                    try:
                        anv_svar_float = [round(float(s.strip().replace(',', '.')), 4) for s in svar_lista]
                        if sorted(anv_svar_float) == st.session_state.graf_ratt_svar:
                            st.session_state.svar_status = 'ratt'
                        else:
                            st.session_state.svar_status = 'fel'
                    except ValueError:
                        st.session_state.svar_status = 'varning_format'
                else:
                    st.session_state.svar_status = 'varning_tom'
                st.rerun()
        with k2:
            if st.button("Ny graf", use_container_width=True):
                st.session_state.submitted_ans = False
                st.session_state.svar_status = None
                skapa_graf_uppgift(st.session_state.niva)
                st.session_state.graf_uppgift_nr += 1
                st.rerun()
                
        if st.session_state.submitted_ans:
            if st.session_state.svar_status == 'ratt': st.success("✅ Helt rätt! Snyggt jobbat.")
            elif st.session_state.svar_status == 'fel':
                svar_str = ' och '.join([f"{a:g}".replace('.', ',') for a in st.session_state.graf_ratt_svar])
                st.error(f"❌ Tyvärr fel. Rätt svar var: {svar_str}")
            elif st.session_state.svar_status == 'varning_format': st.warning("⚠️ Ange bara siffror (t.ex. 2, -3, eller 1,5).")
            elif st.session_state.svar_status == 'varning_tom': st.warning("Fyll i alla rutor innan du rättar.")

# ==========================================
# MODUL 2: Funktioner algebraisk lösning
# ==========================================
elif vald_kategori == "Funktioner: Algebraisk lösning":
    st.title("Algebraisk lösning av funktioner")
    
    if 'alg_niva' not in st.session_state: st.session_state.alg_niva = 1
    if 'alg_uppgift_nr' not in st.session_state: st.session_state.alg_uppgift_nr = 0
    if 'alg_fraga' not in st.session_state: skapa_alg_func_uppgift(st.session_state.alg_niva)

    # INSTÄLLNINGAR I SIDOFÄLTET
    with st.sidebar:
        st.subheader("Inställningar")
        ny_niva = st.radio("Välj svårighetsgrad:", [1, 2], horizontal=True, index=0 if st.session_state.alg_niva==1 else 1, key="alg_niva_val_func")
        if ny_niva != st.session_state.alg_niva:
            st.session_state.alg_niva = ny_niva
            st.session_state.alg_rattat = False
            st.session_state.alg_uppgift_nr += 1
            skapa_alg_func_uppgift(st.session_state.alg_niva)
            st.rerun()

    # LAYOUT
    col_vanster, col_hoger = st.columns([1.2, 1], gap="large")
            
    with col_vanster:
        st.markdown("<div style='text-align: center; font-size: 20px; color: gray; margin-top: 50px;'>Givet funktionen:</div>", unsafe_allow_html=True)
        st.latex(f"f(x) = {st.session_state.alg_funktion}")
        
    with col_hoger:
        st.subheader("Uppgift")
        st.markdown("<p style='font-size: 14px; font-style: italic; color: #666; margin-bottom: 5px;'>Lös gärna på papper och skriv in ditt svar.</p>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size: 32px; font-weight: bold; color: #0056b3; margin-bottom: 25px;'>{st.session_state.alg_fraga}</div>", unsafe_allow_html=True)
        svar = st.text_input("Skriv in ditt svar (heltal):", key=f"alg_input_{st.session_state.alg_uppgift_nr}")
        
        st.write("")
        k1, k2 = st.columns(2)
        with k1:
            if st.button("Rätta svar", type="primary", use_container_width=True):
                st.session_state.alg_rattat = True
                if svar.strip() != "":
                    try:
                        if int(svar.strip()) == st.session_state.alg_svar: st.session_state.alg_status = 'ratt'
                        else: st.session_state.alg_status = 'fel'
                    except ValueError: st.session_state.alg_status = 'format'
                else: st.session_state.alg_status = 'tom'
                st.rerun()
        with k2:
            if st.button("Ny uppgift", use_container_width=True):
                st.session_state.alg_rattat = False
                st.session_state.alg_uppgift_nr += 1
                skapa_alg_func_uppgift(st.session_state.alg_niva)
                st.rerun()

        if st.session_state.get('alg_rattat', False):
            if st.session_state.alg_status == 'ratt': st.success("✅ Helt rätt! Bra jobbat.")
            elif st.session_state.alg_status == 'fel': st.error(f"❌ Tyvärr fel. Rätt svar var: {st.session_state.alg_svar}")
            elif st.session_state.alg_status == 'format': st.warning("⚠️ Svaret ska vara ett heltal.")
            elif st.session_state.alg_status == 'tom': st.warning("Skriv in ett svar först.")

# ==========================================
# MODUL 3: Ekvationer
# ==========================================
elif vald_kategori == "Ekvationer":
    st.title("Lös ekvationerna")
    
    if 'ekv_niva' not in st.session_state: st.session_state.ekv_niva = 1
    if 'ekv_uppgift_nr' not in st.session_state: st.session_state.ekv_uppgift_nr = 0
    if 'ekv_str' not in st.session_state: skapa_ekv_uppgift(st.session_state.ekv_niva)

    with st.sidebar:
        st.subheader("Inställningar")
        ny_niva = st.radio("Välj svårighetsgrad:", [1, 2], horizontal=True, index=0 if st.session_state.ekv_niva==1 else 1, key="ekv_niva_val")
        if ny_niva != st.session_state.ekv_niva:
            st.session_state.ekv_niva = ny_niva
            st.session_state.ekv_rattat = False
            st.session_state.ekv_uppgift_nr += 1
            skapa_ekv_uppgift(st.session_state.ekv_niva)
            st.rerun()

    col_vanster, col_hoger = st.columns([1.2, 1], gap="large")
            
    with col_vanster:
        st.markdown("<div style='text-align: center; font-size: 20px; color: gray; margin-top: 50px;'>Lös ekvationen:</div>", unsafe_allow_html=True)
        st.latex(st.session_state.ekv_str)
        
    with col_hoger:
        st.subheader("Uppgift")
        st.markdown("<p style='font-size: 14px; font-style: italic; color: #666; margin-bottom: 5px;'>Lös gärna på papper och skriv in ditt svar.</p>", unsafe_allow_html=True)
        svar = st.text_input("Vad är x? (Svara med ett heltal):", key=f"ekv_input_{st.session_state.ekv_uppgift_nr}")
        
        st.write("")
        k1, k2 = st.columns(2)
        with k1:
            if st.button("Rätta svar", type="primary", use_container_width=True):
                st.session_state.ekv_rattat = True
                if svar.strip() != "":
                    try:
                        if int(svar.strip()) == st.session_state.ekv_svar: 
                            st.session_state.ekv_status = 'ratt'
                        else: 
                            st.session_state.ekv_status = 'fel'
                    except ValueError: 
                        st.session_state.ekv_status = 'format'
                else: 
                    st.session_state.ekv_status = 'tom'
                st.rerun()
        with k2:
            if st.button("Ny ekvation", use_container_width=True):
                st.session_state.ekv_rattat = False
                st.session_state.ekv_uppgift_nr += 1
                skapa_ekv_uppgift(st.session_state.ekv_niva)
                st.rerun()

        if st.session_state.get('ekv_rattat', False):
            if st.session_state.ekv_status == 'ratt': st.success("✅ Helt rätt! Bra jobbat.")
            elif st.session_state.ekv_status == 'fel': st.error(f"❌ Tyvärr fel. Rätt svar var: {st.session_state.ekv_svar}")
            elif st.session_state.ekv_status == 'format': st.warning("⚠️ Svaret ska vara ett heltal.")
            elif st.session_state.ekv_status == 'tom': st.warning("Skriv in ett svar först.")

# ==========================================
# MODUL 4: Algebra 
# ==========================================
elif vald_kategori == "Algebra":
    st.title("Förenkla och faktorisera algebraiska uttryck")
    
    if 'alg_utt_niva' not in st.session_state: st.session_state.alg_utt_niva = 1
    if 'alg_utt_nr' not in st.session_state: st.session_state.alg_utt_nr = 0
    if 'alg_uttryck_str' not in st.session_state: 
        skapa_alg_uttryck_uppgift(st.session_state.alg_utt_niva)

    with st.sidebar:
        st.subheader("Inställningar")
        aktuellt_index = 0 if st.session_state.alg_utt_niva == 1 else 1
        ny_niva = st.radio("Välj svårighetsgrad:", [1, 2], horizontal=True, index=aktuellt_index, key="alg_utt_niva_val")
        
        if ny_niva != st.session_state.alg_utt_niva:
            st.session_state.alg_utt_niva = ny_niva
            st.session_state.alg_utt_rattat = False
            st.session_state.alg_utt_nr += 1
            skapa_alg_uttryck_uppgift(st.session_state.alg_utt_niva)
            st.rerun()

    col_vanster, col_hoger = st.columns([1.2, 1], gap="large")
            
    with col_vanster:
        st.markdown(f"<div style='text-align: center; font-size: 20px; color: gray; margin-top: 50px;'>{st.session_state.alg_rubrik}</div>", unsafe_allow_html=True)
        st.latex(st.session_state.alg_uttryck_str)
        
    with col_hoger:
        st.subheader("Välj rätt alternativ")
        st.markdown("<p style='font-size: 14px; font-style: italic; color: #666; margin-bottom: 5px;'>Lös gärna på papper och välj ditt svar.</p>", unsafe_allow_html=True)
        
        valt_svar = st.radio("Alternativ:", st.session_state.alg_uttryck_alternativ, key=f"alg_radio_{st.session_state.alg_utt_nr}", label_visibility="collapsed")
        
        st.write("")
        k1, k2 = st.columns(2)
        
        with k1:
            if st.button("Rätta svar", type="primary", use_container_width=True):
                st.session_state.alg_utt_rattat = True
                if valt_svar is not None:
                    if valt_svar.strip() == st.session_state.alg_uttryck_svar.strip():
                        st.session_state.alg_utt_status = 'ratt'
                    else:
                        st.session_state.alg_utt_status = 'fel'
                else:
                    st.session_state.alg_utt_status = 'tom'
                st.rerun()
                
        with k2:
            if st.button("Ny uppgift", use_container_width=True):
                st.session_state.alg_utt_rattat = False
                st.session_state.alg_utt_nr += 1
                skapa_alg_uttryck_uppgift(st.session_state.alg_utt_niva)
                st.rerun()

        if st.session_state.get('alg_utt_rattat', False):
            if st.session_state.alg_utt_status == 'ratt': 
                st.success("✅ Helt rätt! Bra jobbat.")
            elif st.session_state.alg_utt_status == 'fel': 
                st.error(f"❌ Tyvärr fel. Rätt svar var exakt: {st.session_state.alg_uttryck_svar}")
            elif st.session_state.alg_utt_status == 'tom': 
                st.warning("Vänligen välj ett alternativ först.")

# ==========================================
# MODUL 5: Blandat (Slumpas)
# ==========================================
elif vald_kategori == "Blandat (Slumpas)":
    st.title("Blandade uppgifter - Träna på allt!")

    if 'blandat_niva' not in st.session_state: st.session_state.blandat_niva = 1

    def ny_blandad_uppgift():
        st.session_state.blandat_typ = random.choice(['graf', 'alg_func', 'ekv', 'alg_uttryck'])
        niva = st.session_state.get('blandat_niva', 1)
        st.session_state.blandat_id = st.session_state.get('blandat_id', 0) + 1
        st.session_state.blandat_rattat = False
        st.session_state.blandat_status = None
        st.session_state.submitted_ans = False 
        
        if st.session_state.blandat_typ == 'graf':
            skapa_graf_uppgift(niva)
        elif st.session_state.blandat_typ == 'alg_func':
            skapa_alg_func_uppgift(niva)
        elif st.session_state.blandat_typ == 'ekv':
            skapa_ekv_uppgift(niva)
        elif st.session_state.blandat_typ == 'alg_uttryck':
            # Skickar med 'niva' här istället för 1, så att nivå 2-algebran kommer med!
            skapa_alg_uttryck_uppgift(niva)

    with st.sidebar:
        st.subheader("Inställningar")
        aktuellt_index = 0 if st.session_state.blandat_niva == 1 else 1
        ny_niva = st.radio("Välj svårighetsgrad:", [1, 2], horizontal=True, index=aktuellt_index, key="blandat_niva_val")
        if ny_niva != st.session_state.blandat_niva:
            st.session_state.blandat_niva = ny_niva
            ny_blandad_uppgift()
            st.rerun()

    if 'blandat_typ' not in st.session_state:
        ny_blandad_uppgift()

    col_vanster, col_hoger = st.columns([1.2, 1], gap="large")

    with col_vanster:
        if st.session_state.blandat_typ == 'graf':
            fig = rita_plotly_graf(
                f = st.session_state.graf_f,
                visa_facit = st.session_state.get('blandat_rattat', False),
                q_vis_type = st.session_state.get('q_type_vis', 'vis_none'),
                trace_x = st.session_state.get('trace_x'),
                trace_y = st.session_state.get('trace_y'),
                trace_alla_x = st.session_state.get('trace_alla_x')
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        elif st.session_state.blandat_typ == 'alg_func':
            st.markdown("<div style='text-align: center; font-size: 20px; color: gray; margin-top: 50px;'>Givet funktionen:</div>", unsafe_allow_html=True)
            st.latex(f"f(x) = {st.session_state.alg_funktion}")

        elif st.session_state.blandat_typ == 'ekv':
            st.markdown("<div style='text-align: center; font-size: 20px; color: gray; margin-top: 50px;'>Lös ekvationen:</div>", unsafe_allow_html=True)
            st.latex(st.session_state.ekv_str)

        elif st.session_state.blandat_typ == 'alg_uttryck':
            st.markdown(f"<div style='text-align: center; font-size: 20px; color: gray; margin-top: 50px;'>{st.session_state.alg_rubrik}</div>", unsafe_allow_html=True)
            st.latex(st.session_state.alg_uttryck_str)

    with col_hoger:
        st.subheader("Uppgift")
        
        # Visar instruktionstexten för alla förutom grafer där det kanske inte är ett måste med papper
        if st.session_state.blandat_typ in ['alg_func', 'ekv']:
            st.markdown("<p style='font-size: 14px; font-style: italic; color: #666; margin-bottom: 5px;'>Lös gärna på papper och skriv in ditt svar.</p>", unsafe_allow_html=True)
        elif st.session_state.blandat_typ == 'alg_uttryck':
            st.markdown("<p style='font-size: 14px; font-style: italic; color: #666; margin-bottom: 5px;'>Lös gärna på papper och välj ditt svar.</p>", unsafe_allow_html=True)
            
        svar_lista = []
        svar = ""
        valt_svar = None

        if st.session_state.blandat_typ == 'graf':
            st.markdown(f"<div style='font-size: 32px; font-weight: bold; color: #0056b3; margin-bottom: 20px;'>{st.session_state.graf_fraga}</div>", unsafe_allow_html=True)
            antal_svar = len(st.session_state.graf_ratt_svar)
            for i in range(antal_svar):
                tmp_svar = st.text_input(f"Svar {i+1}:" if antal_svar > 1 else "Ditt svar:", key=f"blandat_graf_in_{st.session_state.blandat_id}_{i}")
                svar_lista.append(tmp_svar)

        elif st.session_state.blandat_typ == 'alg_func':
            st.markdown(f"<div style='font-size: 32px; font-weight: bold; color: #0056b3; margin-bottom: 25px;'>{st.session_state.alg_fraga}</div>", unsafe_allow_html=True)
            svar = st.text_input("Svar (heltal):", key=f"blandat_algf_in_{st.session_state.blandat_id}")

        elif st.session_state.blandat_typ == 'ekv':
            st.markdown("<div style='font-size: 32px; font-weight: bold; color: transparent; margin-bottom: 25px;'>&nbsp;</div>", unsafe_allow_html=True) 
            svar = st.text_input("Vad är x? (Heltal):", key=f"blandat_ekv_in_{st.session_state.blandat_id}")

        elif st.session_state.blandat_typ == 'alg_uttryck':
            valt_svar = st.radio("Välj rätt alternativ:", st.session_state.alg_uttryck_alternativ, index=None, key=f"blandat_algu_in_{st.session_state.blandat_id}", label_visibility="collapsed")

        st.write("")
        
        k1, k2 = st.columns(2)
        with k1:
            if st.button("Rätta svar", type="primary", use_container_width=True, key=f"btn_ratt_{st.session_state.blandat_id}"):
                st.session_state.blandat_rattat = True
                
                if st.session_state.blandat_typ == 'graf':
                    if all(s.strip() != "" for s in svar_lista):
                        try:
                            anv_svar_float = sorted([round(float(s.strip().replace(',', '.')), 4) for s in svar_lista])
                            st.session_state.blandat_status = 'ratt' if anv_svar_float == st.session_state.graf_ratt_svar else 'fel'
                        except ValueError: st.session_state.blandat_status = 'format'
                    else: st.session_state.blandat_status = 'tom'
                        
                elif st.session_state.blandat_typ in ['alg_func', 'ekv']:
                    if svar.strip() != "":
                        try:
                            ratt_svar = st.session_state.alg_svar if st.session_state.blandat_typ == 'alg_func' else st.session_state.ekv_svar
                            st.session_state.blandat_status = 'ratt' if int(svar.strip()) == ratt_svar else 'fel'
                        except ValueError: st.session_state.blandat_status = 'format'
                    else: st.session_state.blandat_status = 'tom'
                        
                elif st.session_state.blandat_typ == 'alg_uttryck':
                    if valt_svar is not None:
                        st.session_state.blandat_status = 'ratt' if valt_svar.strip() == st.session_state.alg_uttryck_svar.strip() else 'fel'
                    else: st.session_state.blandat_status = 'tom'
                st.rerun()

        with k2:
            if st.button("Nästa uppgift", use_container_width=True, key=f"btn_ny_{st.session_state.blandat_id}"):
                ny_blandad_uppgift()
                st.rerun()

        if st.session_state.get('blandat_rattat', False):
            if st.session_state.blandat_status == 'ratt':
                st.success("✅ Helt rätt! Grymt!")
            elif st.session_state.blandat_status == 'fel':
                if st.session_state.blandat_typ == 'graf': ratt_txt = ' och '.join([f"{a:g}".replace('.', ',') for a in st.session_state.graf_ratt_svar])
                elif st.session_state.blandat_typ == 'alg_func': ratt_txt = st.session_state.alg_svar
                elif st.session_state.blandat_typ == 'ekv': ratt_txt = st.session_state.ekv_svar
                elif st.session_state.blandat_typ == 'alg_uttryck': ratt_txt = f"uttrycket som är exakt {st.session_state.alg_uttryck_svar}"
                st.error(f"❌ Tyvärr fel. Rätt svar var: {ratt_txt}")
            elif st.session_state.blandat_status == 'format':
                st.warning("⚠️ Svaret är i fel format (ange bara siffror).")
            elif st.session_state.blandat_status == 'tom':
                st.warning("Vänligen fyll i ett svar innan du rättar.")
