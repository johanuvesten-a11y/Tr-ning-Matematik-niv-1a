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

# -- PLOTLY RIT-FUNKTION (Pilar exakt i spetsen!) --
def rita_plotly_graf(f, visa_facit=False, q_vis_type='vis_none', trace_x=None, trace_y=None, trace_alla_x=None):
    fig = go.Figure()
    
    # Skapa x och y värden
    x_plot = np.linspace(-10, 10, 400)
    y_plot = f(x_plot)
    
    # Huvudgrafen (blå linje). hoverinfo='skip' stänger av muspekaren här.
    fig.add_trace(go.Scatter(
        x=x_plot, y=y_plot, mode='lines', 
        line=dict(color='blue', width=2), 
        hoverinfo='skip'
    ))
    
    # Rita in facit-linjerna om man har svarat
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

    # ==========================================
    # MANUELLA SIFFROR LÄNGS MED AXLARNA
    # ==========================================
    tick_vals = [-10, -5, 5, 10]
    
    # Siffror för x-axeln
    fig.add_trace(go.Scatter(
        x=tick_vals, y=[-0.6]*4, mode='text', text=[str(v) for v in tick_vals],
        textposition='bottom center', showlegend=False, hoverinfo='skip', textfont=dict(color='black', size=14)
    ))
    # Siffror för y-axeln
    fig.add_trace(go.Scatter(
        x=[-0.6]*4, y=tick_vals, mode='text', text=[str(v) for v in tick_vals],
        textposition='middle left', showlegend=False, hoverinfo='skip', textfont=dict(color='black', size=14)
    ))
    # Origo (0)
    fig.add_trace(go.Scatter(
        x=[-0.4], y=[-0.6], mode='text', text=['0'],
        textposition='bottom left', showlegend=False, hoverinfo='skip', textfont=dict(color='black', size=14)
    ))

   # Gemensamma inställningar (rutnät)
    axis_layout = dict(
        range=[-10.8, 10.8], 
        zeroline=True, zerolinewidth=3, zerolinecolor='black',  # Fetare axlar (ökad från 2 till 3)
        showgrid=True, gridwidth=2, gridcolor='#cccccc',        # Fetare huvudrutnät (ökad från 1 till 2)
        minor=dict(dtick=1, gridwidth=2, gridcolor='#e0e0e0'),  # Fetare under-rutnät (ökad från 1 till 2)
        showticklabels=False, 
        fixedrange=True 
    )

    # ==========================================
    # PILAR OCH AXLARNAS NAMN (Nu i spetsen!)
    # ==========================================
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
            # Pil och namn för x-axeln (Spetsen flyttad ut till 10.8)
            dict(x=10.8, y=0, ax=9.8, ay=0, xref='x', yref='y', axref='x', ayref='y', **pil_inst),
            dict(x=10.8, y=-0.5, text="x", showarrow=False, xref='x', yref='y', font=dict(size=16, color='black')),
            
            # Pil och namn för y-axeln (Spetsen flyttad ut till 10.8)
            dict(x=0, y=10.8, ax=0, ay=9.8, xref='x', yref='y', axref='x', ayref='y', **pil_inst),
            dict(x=-0.5, y=10.8, text="y", showarrow=False, xref='x', yref='y', font=dict(size=16, color='black'))
        ]
    )
    return fig
# -- 2. Algebraisk Funktion --
def skapa_alg_func_uppgift(niva):
    while True:
        if niva == 1:
            typ = random.choice(['f_a', 'f_x_C'])
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
                    st.session_state.alg_funktion = f"{f_str}"
                    st.session_state.alg_svar = svar
                    break
                    
            else: # f(x) = C
                b = random.choice([1, 1, 2, 3, 4]) 
                a_coeff = random.choice([-4, -3, -2, -1, 1, 2, 3, 4])
                m = random.randint(-15, 15)
                x = random.randint(-20, 20) * b 
                if b == 1:
                    k_str = "x" if a_coeff == 1 else ("-x" if a_coeff == -1 else f"{a_coeff}x")
                    C = a_coeff*x + m
                    term_x = k_str
                else:
                    if a_coeff == 1: term_x = f"\\frac{{{x}}}{{{b}}}"
                    elif a_coeff == -1: term_x = f"-\\frac{{{x}}}{{{b}}}"
                    else: term_x = f"\\frac{{{a_coeff}x}}{{{b}}}"
                    C = int((a_coeff*x)/b + m)
                m_str = f" + {m}" if m > 0 else (f" - {-m}" if m < 0 else "")
                f_str = f"{term_x}{m_str}"
                
                if abs(x) <= 100 and abs(C) <= 100:
                    st.session_state.alg_fraga = f"Bestäm x om f(x) = {C}"
                    st.session_state.alg_funktion = f"{f_str}"
                    st.session_state.alg_svar = x
                    break
                    
        else: # Niva 2
            typ = random.choice(['f_f_a', 'f_f_x_C'])
            k = random.choice([-3, -2, -1, 2, 3])
            m = random.randint(-10, 10)
            k_str = "x" if k == 1 else ("-x" if k == -1 else f"{k}x")
            m_str = f" + {m}" if m > 0 else (f" - {-m}" if m < 0 else "")
            f_str = f"{k_str}{m_str}"
            
            if typ == 'f_f_a':
                a = random.randint(-8, 8)
                inner = k*a + m
                svar = k*inner + m
                if abs(svar) <= 100:
                    st.session_state.alg_fraga = f"Bestäm f(f({a}))"
                    st.session_state.alg_funktion = f"{f_str}"
                    st.session_state.alg_svar = svar
                    break
            else:
                x = random.randint(-12, 12)
                inner = k*x + m
                C = k*inner + m
                if abs(x) <= 100 and abs(C) <= 100:
                    st.session_state.alg_fraga = f"Bestäm x om f(f(x)) = {C}"
                    st.session_state.alg_funktion = f"{f_str}"
                    st.session_state.alg_svar = x
                    break

# -- 3. Ekvationer --
def skapa_ekv_uppgift(niva):
    while True:
        x = random.randint(-10, 10)
        def formatera_sida(k, m):
            if k == 1: k_str = "x"
            elif k == -1: k_str = "-x"
            else: k_str = f"{k}x"
            if m > 0: return f"{k_str} + {m}"
            elif m < 0: return f"{k_str} - {-m}"
            else: return k_str

        if niva == 1:
            a = random.choice([-5, -4, -3, -2, 2, 3, 4, 5])
            c = random.choice([-5, -4, -3, -2, 2, 3, 4, 5])
            if a == c: continue 
            b = random.randint(-20, 20)
            d = a*x + b - c*x
            VL = formatera_sida(a, b)
            HL = formatera_sida(c, d)
            st.session_state.ekv_str = f"{VL} = {HL}"
            st.session_state.ekv_svar = x
            break
        else:
            a = random.choice([-4, -3, -2, 2, 3, 4])
            c = random.choice([-5, -4, -3, -2, 2, 3, 4, 5])
            if a == c: continue
            b = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            d = a*(x + b) - c*x
            b_str = f"+ {b}" if b > 0 else f"- {-b}"
            VL = f"{a}(x {b_str})"
            HL = formatera_sida(c, d)
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

    typ = random.choice(['minus_parentes', 'mult_parentes', 'konstant_parentes', 'faktorisera'])
    
    if typ == 'minus_parentes':
        st.session_state.alg_rubrik = "Förenkla uttrycket:"
        c = random.choice([2, 3, 4])
        A = random.randint(-5, 5)
        B = random.randint(-5, 5)
        A_str = f"+ {A}" if A > 0 else (f"- {-A}" if A < 0 else "")
        B_str = f"+ {B}" if B > 0 else (f"- {-B}" if B < 0 else "")
        st.session_state.alg_uttryck_str = f"(x {A_str}) - ({c}x {B_str})"
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
st.sidebar.info("Välj ett område ovan för att starta!")

# ==========================================
# MODUL 1: Funktioner grafisk lösning
# ==========================================
if vald_kategori == "Funktioner: Grafisk lösning":
    st.title("Grafisk avläsning av funktioner")

    if 'niva' not in st.session_state:
        st.session_state.niva = 1
    if 'graf_fraga' not in st.session_state:
        skapa_graf_uppgift(st.session_state.niva)
        st.session_state.graf_uppgift_nr = 1
    if 'submitted_ans' not in st.session_state:
        st.session_state.submitted_ans = False
    if 'svar_status' not in st.session_state:
        st.session_state.svar_status = None

    col_graf, col_kontroller = st.columns([1.2, 1], gap="large")

    with col_graf:
        # Använd Plotly istället för Matplotlib!
        fig = rita_plotly_graf(
            f = st.session_state.graf_f,
            visa_facit = st.session_state.submitted_ans,
            q_vis_type = st.session_state.get('q_type_vis', 'vis_none'),
            trace_x = st.session_state.get('trace_x'),
            trace_y = st.session_state.get('trace_y'),
            trace_alla_x = st.session_state.get('trace_alla_x')
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with col_kontroller:
        st.subheader("Inställningar")
        aktuellt_index = 0 if st.session_state.niva == 1 else 1
        ny_niva = st.radio("Välj svårighetsgrad:", [1, 2], horizontal=True, index=aktuellt_index, key="graf_niva_val")
        if ny_niva != st.session_state.niva:
            st.session_state.niva = ny_niva
            st.session_state.submitted_ans = False
            skapa_graf_uppgift(st.session_state.niva)
            st.session_state.graf_uppgift_nr += 1
            st.rerun()
            
        st.divider() 
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

    col_uppgift, col_installningar = st.columns([1.5, 1], gap="large")
    with col_installningar:
        st.subheader("Inställningar")
        ny_niva = st.radio("Välj svårighetsgrad:", [1, 2], horizontal=True, index=0 if st.session_state.alg_niva==1 else 1, key="alg_niva_val")
        if ny_niva != st.session_state.alg_niva:
            st.session_state.alg_niva = ny_niva
            st.session_state.alg_rattat = False
            st.session_state.alg_uppgift_nr += 1
            skapa_alg_func_uppgift(st.session_state.alg_niva)
            st.rerun()
            
    with col_uppgift:
        st.markdown("<div style='text-align: center; font-size: 20px; color: gray;'>Givet funktionen:</div>", unsafe_allow_html=True)
        st.latex(f"f(x) = {st.session_state.alg_funktion}")
        st.markdown(f"<div style='text-align: center; font-size: 32px; color: #0056b3; margin-bottom: 25px;'>{st.session_state.alg_fraga}</div>", unsafe_allow_html=True)
        svar = st.text_input("Skriv in ditt svar (heltal):", key=f"alg_input_{st.session_state.alg_uppgift_nr}")
        
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

    col_uppgift, col_installningar = st.columns([1.5, 1], gap="large")
    with col_installningar:
        st.subheader("Inställningar")
        ny_niva = st.radio("Välj svårighetsgrad:", [1, 2], horizontal=True, index=0 if st.session_state.ekv_niva==1 else 1, key="ekv_niva_val")
        if ny_niva != st.session_state.ekv_niva:
            st.session_state.ekv_niva = ny_niva
            st.session_state.ekv_rattat = False
            st.session_state.ekv_uppgift_nr += 1
            skapa_ekv_uppgift(st.session_state.ekv_niva)
            st.rerun()
            
    with col_uppgift:
        st.markdown("<div style='text-align: center; font-size: 20px; color: gray;'>Lös ekvationen:</div>", unsafe_allow_html=True)
        st.latex(st.session_state.ekv_str)
        st.write("")
        svar = st.text_input("Vad är x? (Svara med ett heltal):", key=f"ekv_input_{st.session_state.ekv_uppgift_nr}")
        
        k1, k2 = st.columns(2)
        with k1:
            if st.button("Rätta svar", type="primary", use_container_width=True):
                st.session_state.ekv_rattat = True
                if svar.strip() != "":
                    try:
                        if int(svar.strip()) == st.session_state.ekv_svar: st.session_state.ekv_status = 'ratt'
                        else: st.session_state.ekv_status = 'fel'
                    except ValueError: st.session_state.ekv_status = 'format'
                else: st.session_state.ekv_status = 'tom'
        with k2:
            if st.button("Ny ekvation", use_container_width=True):
                st.session_state.ekv_rattat = False
                st.session_state.ekv_uppgift_nr += 1
                skapa_ekv_uppgift(st.session_state.ekv_niva)
                st.rerun()

        if st.session_state.get('ekv_rattat', False):
            if st.session_state.ekv_status == 'ratt': st.success("✅ Helt rätt! Snyggt jobbat.")
            elif st.session_state.ekv_status == 'fel': st.error(f"❌ Tyvärr fel. Rätt svar var: {st.session_state.ekv_svar}")
            elif st.session_state.ekv_status == 'format': st.warning("⚠️ Svaret ska vara ett heltal.")
            elif st.session_state.ekv_status == 'tom': st.warning("Skriv in ett svar först.")

# ==========================================
# MODUL 4: Algebra
# ==========================================
elif vald_kategori == "Algebra":
    st.title("Förenkla och faktorisera uttryck")
    if 'alg_uttryck_uppgift_nr' not in st.session_state: st.session_state.alg_uttryck_uppgift_nr = 0
    if 'alg_uttryck_str' not in st.session_state: skapa_alg_uttryck_uppgift(1)

    col_uppgift, col_installningar = st.columns([1.5, 1], gap="large")
    with col_installningar:
        st.subheader("Inställningar")
        st.info("Nivå 2 är tillfälligt dold.")
            
    with col_uppgift:
        st.markdown(f"<div style='text-align: center; font-size: 20px; color: gray;'>{st.session_state.alg_rubrik}</div>", unsafe_allow_html=True)
        st.latex(st.session_state.alg_uttryck_str)
        st.write("")
        valt_svar = st.radio("Välj rätt alternativ:", st.session_state.alg_uttryck_alternativ, index=None, key=f"alg_uttryck_val_{st.session_state.alg_uttryck_uppgift_nr}")
        
        k1, k2 = st.columns(2)
        with k1:
            if st.button("Rätta svar", type="primary", use_container_width=True):
                st.session_state.alg_uttryck_rattat = True
                if valt_svar is not None:
                    if valt_svar.strip() == st.session_state.alg_uttryck_svar.strip(): st.session_state.alg_uttryck_status = 'ratt'
                    else: st.session_state.alg_uttryck_status = 'fel'
                else: st.session_state.alg_uttryck_status = 'tom'
        with k2:
            if st.button("Ny uppgift", use_container_width=True):
                st.session_state.alg_uttryck_rattat = False
                st.session_state.alg_uttryck_uppgift_nr += 1
                skapa_alg_uttryck_uppgift(1)
                st.rerun()
                
        if st.session_state.get('alg_uttryck_rattat', False):
            if st.session_state.alg_uttryck_status == 'ratt': st.success("✅ Helt rätt! Bra jobbat!")
            elif st.session_state.alg_uttryck_status == 'fel': st.error(f"❌ Tyvärr fel. Rätt svar var: {st.session_state.alg_uttryck_svar}")
            elif st.session_state.alg_uttryck_status == 'tom': st.warning("Välj ett alternativ innan du klickar på Rätta.")

# ==========================================
# MODUL 5: Blandat (Slumpas)
# ==========================================
elif vald_kategori == "Blandat (Slumpas)":
    st.title("Blandade uppgifter - Träna på allt!")

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
            skapa_alg_uttryck_uppgift(1)

    if 'blandat_typ' not in st.session_state:
        st.session_state.blandat_niva = 1
        ny_blandad_uppgift()

    col_uppgift, col_installningar = st.columns([1.5, 1], gap="large")

    with col_installningar:
        st.subheader("Inställningar")
        aktuellt_index = 0 if st.session_state.blandat_niva == 1 else 1
        ny_niva = st.radio("Välj svårighetsgrad:", [1, 2], horizontal=True, index=aktuellt_index, key="blandat_niva_val")
        if ny_niva != st.session_state.blandat_niva:
            st.session_state.blandat_niva = ny_niva
            ny_blandad_uppgift()
            st.rerun()

    with col_uppgift:
        if st.session_state.blandat_typ == 'graf':
            st.markdown(f"<div style='font-size: 24px; font-weight: bold; color: #0056b3; margin-bottom: 20px; text-align: center;'>{st.session_state.graf_fraga}</div>", unsafe_allow_html=True)
            
            # Plotly istället för Matplotlib här också!
            fig = rita_plotly_graf(
                f = st.session_state.graf_f,
                visa_facit = st.session_state.get('blandat_rattat', False),
                q_vis_type = st.session_state.get('q_type_vis', 'vis_none'),
                trace_x = st.session_state.get('trace_x'),
                trace_y = st.session_state.get('trace_y'),
                trace_alla_x = st.session_state.get('trace_alla_x')
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

            antal_svar = len(st.session_state.graf_ratt_svar)
            svar_lista = []
            for i in range(antal_svar):
                svar = st.text_input(f"Svar {i+1}:" if antal_svar > 1 else "Svar:", key=f"blandat_graf_in_{st.session_state.blandat_id}_{i}")
                svar_lista.append(svar)

        elif st.session_state.blandat_typ == 'alg_func':
            st.markdown("<div style='text-align: center; font-size: 20px; color: gray;'>Givet funktionen:</div>", unsafe_allow_html=True)
            st.latex(f"f(x) = {st.session_state.alg_funktion}")
            st.markdown(f"<div style='text-align: center; font-size: 32px; color: #0056b3; margin-bottom: 25px;'>{st.session_state.alg_fraga}</div>", unsafe_allow_html=True)
            svar = st.text_input("Svar (heltal):", key=f"blandat_algf_in_{st.session_state.blandat_id}")

        elif st.session_state.blandat_typ == 'ekv':
            st.markdown("<div style='text-align: center; font-size: 20px; color: gray;'>Lös ekvationen:</div>", unsafe_allow_html=True)
            st.latex(st.session_state.ekv_str)
            svar = st.text_input("Vad är x? (Heltal):", key=f"blandat_ekv_in_{st.session_state.blandat_id}")

        elif st.session_state.blandat_typ == 'alg_uttryck':
            st.markdown(f"<div style='text-align: center; font-size: 20px; color: gray;'>{st.session_state.alg_rubrik}</div>", unsafe_allow_html=True)
            st.latex(st.session_state.alg_uttryck_str)
            valt_svar = st.radio("Välj rätt alternativ:", st.session_state.alg_uttryck_alternativ, index=None, key=f"blandat_algu_in_{st.session_state.blandat_id}")

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
                elif st.session_state.blandat_typ == 'alg_uttryck': ratt_txt = st.session_state.alg_uttryck_svar
                st.error(f"❌ Tyvärr fel. Rätt svar var: {ratt_txt}")
            elif st.session_state.blandat_status == 'format':
                st.warning("⚠️ Svaret är i fel format (se till att använda siffror, och inte 'x=').")
            elif st.session_state.blandat_status == 'tom':
                st.warning("Vänligen fyll i ett svar innan du rättar.")
