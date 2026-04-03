import streamlit as st
import numpy as np
import random
import math
import plotly.graph_objects as go
from fractions import Fraction

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
# 1. MATEMATIKGENERATORER (Returnerar data)
# ==========================================

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

def rita_plotly_graf(f, visa_facit=False, q_vis_type='vis_none', trace_x=None, trace_y=None, trace_alla_x=None):
    fig = go.Figure()
    x_plot = np.linspace(-10, 10, 400)
    y_plot = f(x_plot)
    fig.add_trace(go.Scatter(
        x=x_plot, y=y_plot, mode='lines', line=dict(color='blue', width=2), hoverinfo='skip'
    ))
    if visa_facit:
        if q_vis_type == 'vis_find_y':
            tx, ty = trace_x, trace_y
            fig.add_trace(go.Scatter(
                x=[tx, tx, 0], y=[0, ty, ty], mode='lines+markers', line=dict(color='red', dash='dash', width=2), 
                marker=dict(size=8, color='red'), showlegend=False, hoverinfo='skip'
            ))
        elif q_vis_type == 'vis_find_x':
            ty = trace_y
            ax_list = trace_alla_x
            if ax_list:
                min_ax, max_ax = min(ax_list + [0]), max(ax_list + [0])
                fig.add_trace(go.Scatter(
                    x=[min_ax, max_ax], y=[ty, ty], mode='lines', line=dict(color='red', dash='dash', width=2), showlegend=False, hoverinfo='skip'
                ))
                for ax_v in ax_list:
                    fig.add_trace(go.Scatter(
                        x=[ax_v, ax_v], y=[ty, 0], mode='lines+markers', line=dict(color='red', dash='dash', width=2), 
                        marker=dict(size=8, color='red'), showlegend=False, hoverinfo='skip'
                    ))

    tick_vals = [-10, -5, 5, 10]
    fig.add_trace(go.Scatter(
        x=tick_vals, y=[-0.6]*4, mode='text', text=[str(v) for v in tick_vals], textposition='bottom center', showlegend=False, hoverinfo='skip', textfont=dict(color='black', size=14)
    ))
    fig.add_trace(go.Scatter(
        x=[-0.6]*4, y=tick_vals, mode='text', text=[str(v) for v in tick_vals], textposition='middle left', showlegend=False, hoverinfo='skip', textfont=dict(color='black', size=14)
    ))
    fig.add_trace(go.Scatter(
        x=[-0.4], y=[-0.6], mode='text', text=['0'], textposition='bottom left', showlegend=False, hoverinfo='skip', textfont=dict(color='black', size=14)
    ))

    axis_layout = dict(
        range=[-10.8, 10.8], zeroline=True, zerolinewidth=3, zerolinecolor='black', showgrid=True, gridwidth=2, gridcolor='#cccccc', 
        minor=dict(dtick=1, gridwidth=2, gridcolor='#e0e0e0'), showticklabels=False, fixedrange=True 
    )
    pil_inst = dict(showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2, arrowcolor='black')
    
    fig.update_layout(
        xaxis=axis_layout, yaxis=axis_layout, showlegend=False, margin=dict(l=20, r=20, t=20, b=20), height=550, plot_bgcolor='white', hovermode=False, dragmode=False,
        annotations=[
            dict(x=10.8, y=0, ax=9.8, ay=0, xref='x', yref='y', axref='x', ayref='y', **pil_inst),
            dict(x=10.8, y=-0.5, text="x", showarrow=False, xref='x', yref='y', font=dict(size=16, color='black')),
            dict(x=0, y=10.8, ax=0, ay=9.8, xref='x', yref='y', axref='x', ayref='y', **pil_inst),
            dict(x=-0.5, y=10.8, text="y", showarrow=False, xref='x', yref='y', font=dict(size=16, color='black'))
        ]
    )
    return fig

def skapa_graf_uppgift(niva):
    for _ in range(100): 
        f = generera_funktion()
        giltiga_punkter = []
        for x_val in [i / 2 for i in range(-16, 17)]:
            y_val = f(x_val)
            if abs(y_val) <= 10 and round(y_val * 2, 4).is_integer():
                giltiga_punkter.append((round(x_val, 4), round(y_val, 4)))
                
        if not giltiga_punkter: continue 

        if niva == 1:
            target_x, target_y = random.choice(giltiga_punkter)
            fraga_typ = random.choice(['hitta_y', 'hitta_x'])
            if fraga_typ == 'hitta_y':
                fraga = f"Bestäm f({target_x:g})"
                ratt_svar = [target_y]
                q_type_vis = 'vis_find_y'
                return {
                    "graf_f": f, "q_type_vis": q_type_vis, "trace_x": target_x, "trace_y": target_y,
                    "fraga": fraga.replace('.', ','), "ratt_svar": [round(ans, 4) + 0.0 for ans in ratt_svar],
                    "input_typ": "flera_text", "svarstyp": "array_float"
                }
            else:
                target_y_snygg = target_y + 0.0 
                alla_x = list(set([p[0] for p in giltiga_punkter if p[1] == target_y]))
                if len(alla_x) > 3: continue 
                fraga = f"Bestäm ett värde på x så att f(x) = {target_y_snygg:g}"
                ratt_svar = sorted(alla_x)
                q_type_vis = 'vis_find_x'
                return {
                    "graf_f": f, "q_type_vis": q_type_vis, "trace_y": target_y, "trace_alla_x": alla_x,
                    "fraga": fraga.replace('.', ','), "ratt_svar": [round(ans, 4) + 0.0 for ans in ratt_svar],
                    "input_typ": "flera_text", "svarstyp": "array_float"
                }
        else:
            fraga_typ = random.choice(['f_x_plus_c', 'f_f_c', 'f_a_op_f_b', 'f_kx'])
            q_type_vis = 'vis_none'

            if fraga_typ == 'f_x_plus_c':
                hel_punkter = [p for p in giltiga_punkter if round(p[1], 4).is_integer()]
                if not hel_punkter: continue
                target_x, target_y = random.choice(hel_punkter)
                c = random.choice([-3, -2, -1, 1, 2, 3])
                c_str = f"+ {c}" if c > 0 else f"- {abs(c)}"
                alla_mål_x = [p[0] for p in giltiga_punkter if p[1] == target_y]
                if len(alla_mål_x) > 3: continue 
                fraga = f"Bestäm x om f(x {c_str}) = {target_y + 0.0:g}"
                ratt_svar = sorted([tx - c for tx in alla_mål_x])
                return {"graf_f": f, "q_type_vis": 'vis_find_x', "trace_y": target_y, "trace_alla_x": alla_mål_x, "fraga": fraga.replace('.', ','), "ratt_svar": [round(ans, 4) + 0.0 for ans in ratt_svar], "input_typ": "flera_text", "svarstyp": "array_float"}
                
            elif fraga_typ == 'f_f_c':
                valid_c = []
                for x_val in range(-8, 9):
                    y1 = f(x_val)
                    if round(y1, 4).is_integer() and -8 <= y1 <= 8:
                        y2 = f(y1)
                        if abs(y2) <= 10 and round(y2 * 2, 4).is_integer(): valid_c.append(x_val)
                if not valid_c: continue 
                c = random.choice(valid_c)
                ratt_svar = [round(f(round(f(c), 4)), 4)]
                fraga = f"Bestäm f(f({c}))"
                return {"graf_f": f, "q_type_vis": q_type_vis, "fraga": fraga.replace('.', ','), "ratt_svar": [round(ans, 4) + 0.0 for ans in ratt_svar], "input_typ": "flera_text", "svarstyp": "array_float"}
                
            elif fraga_typ == 'f_a_op_f_b':
                hel_punkter = [p for p in giltiga_punkter if round(p[1], 4).is_integer() and round(p[0], 4).is_integer()]
                if len(hel_punkter) < 2: continue
                p1, p2 = random.sample(hel_punkter, 2)
                op = random.choice(['+', '-'])
                svar = p1[1] + p2[1] if op == '+' else p1[1] - p2[1]
                fraga = f"Bestäm f({p1[0]:g}) {op} f({p2[0]:g})"
                ratt_svar = [svar]
                return {"graf_f": f, "q_type_vis": q_type_vis, "fraga": fraga.replace('.', ','), "ratt_svar": [round(svar, 4) + 0.0], "input_typ": "flera_text", "svarstyp": "array_float"}
                
            elif fraga_typ == 'f_kx':
                mål_y = random.choice([p[1] for p in giltiga_punkter])
                alla_mål_x = [p[0] for p in giltiga_punkter if p[1] == mål_y]
                if len(alla_mål_x) > 3: continue 
                k_val = random.choice([2, -2])
                mojliga_svar = [x / k_val for x in alla_mål_x]
                if all(round(s * 2, 4).is_integer() and abs(s) <= 20 for s in mojliga_svar):
                    fraga = f"Bestäm x om f({k_val:g}x) = {mål_y + 0.0:g}"
                    return {"graf_f": f, "q_type_vis": 'vis_find_x', "trace_y": mål_y, "trace_alla_x": alla_mål_x, "fraga": fraga.replace('.', ','), "ratt_svar": [round(ans, 4) + 0.0 for ans in sorted(mojliga_svar)], "input_typ": "flera_text", "svarstyp": "array_float"}

def skapa_alg_func_uppgift(niva):
    while True:
        if niva == 1:
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
                    return {"info_text": "Givet funktionen:", "latex_text": f"f(x) = {f_str}", "fraga": f"Bestäm f({a})", "ratt_svar": svar, "input_typ": "text", "svarstyp": "int", "undertext": "Lös gärna på papper och skriv in ditt svar."}
                    
            elif typ == 'f_x_C_kvadrat':
                x = random.randint(1, 10) 
                k = random.choice([-3, -2, -1, 1, 2, 3])
                m = random.randint(-15, 15)
                C = k*(x**2) + m
                k_str = "x^2" if k == 1 else ("-x^2" if k == -1 else f"{k}x^2")
                m_str = f" + {m}" if m > 0 else (f" - {-m}" if m < 0 else "")
                
                if abs(C) <= 300:
                    return {"info_text": "Givet funktionen:", "latex_text": f"f(x) = {k_str}{m_str}", "fraga": f"Bestäm det positiva värdet på x om f(x) = {C}", "ratt_svar": x, "input_typ": "text", "svarstyp": "int", "undertext": "Lös gärna på papper och skriv in ditt svar."}
                    
            else: # Linjär
                b = random.choice([1, 1, 2, 3, 4]) 
                a_coeff = random.choice([-4, -3, -2, -1, 1, 2, 3, 4])
                if b > 1 and abs(a_coeff) % b == 0: continue
                m = random.randint(-15, 15)
                x = random.randint(-20, 20) * b 
                if b == 1:
                    C = a_coeff*x + m
                    term_x = "x" if a_coeff == 1 else ("-x" if a_coeff == -1 else f"{a_coeff}x")
                else:
                    term_x = f"\\frac{{x}}{{{b}}}" if a_coeff == 1 else (f"-\\frac{{x}}{{{b}}}" if a_coeff == -1 else f"\\frac{{{a_coeff}x}}{{{b}}}")
                    C = int(round((a_coeff*x)/b + m))
                m_str = f" + {m}" if m > 0 else (f" - {-m}" if m < 0 else "")
                
                if abs(x) <= 100 and abs(C) <= 100:
                    return {"info_text": "Givet funktionen:", "latex_text": f"f(x) = {term_x}{m_str}", "fraga": f"Bestäm x om f(x) = {C}", "ratt_svar": x, "input_typ": "text", "svarstyp": "int", "undertext": "Lös gärna på papper och skriv in ditt svar."}
                    
        else: # Niva 2 
            def formatera_linjar(k, m):
                k_str = "x" if k == 1 else ("-x" if k == -1 else f"{k}x")
                if m == 0: return k_str
                return f"{k_str} + {m}" if m > 0 else f"{k_str} - {-m}"

            typ = random.choice(['f_f_a', 'f_f_x_C', 'f_g_a', 'f_likamed_g'])
            if typ in ['f_f_a', 'f_f_x_C']:
                k = random.choice([-3, -2, -1, 2, 3])
                m = random.randint(-10, 10)
                if typ == 'f_f_a':
                    a = random.randint(-8, 8)
                    svar = k*(k*a + m) + m
                    if abs(svar) <= 150:
                        return {"info_text": "Givet funktionen:", "latex_text": f"f(x) = {formatera_linjar(k, m)}", "fraga": f"Bestäm f(f({a}))", "ratt_svar": svar, "input_typ": "text", "svarstyp": "int", "undertext": "Lös gärna på papper och skriv in ditt svar."}
                else:
                    x = random.randint(-12, 12)
                    C = k*(k*x + m) + m
                    if abs(x) <= 100 and abs(C) <= 150:
                        return {"info_text": "Givet funktionen:", "latex_text": f"f(x) = {formatera_linjar(k, m)}", "fraga": f"Bestäm x om f(f(x)) = {C}", "ratt_svar": x, "input_typ": "text", "svarstyp": "int", "undertext": "Lös gärna på papper och skriv in ditt svar."}
            elif typ == 'f_g_a':
                k1 = random.choice([-4, -3, -2, -1, 2, 3, 4])
                m1 = random.randint(-10, 10)
                k2 = random.choice([-4, -3, -2, -1, 2, 3, 4])
                m2 = random.randint(-10, 10)
                a = random.randint(-5, 5)
                svar = k1*(k2*a + m2) + m1
                return {"info_text": "Givet funktionen:", "latex_text": f"f(x) = {formatera_linjar(k1, m1)} \\quad \\text{{och}} \\quad g(x) = {formatera_linjar(k2, m2)}", "fraga": f"Bestäm f(g({a}))", "ratt_svar": svar, "input_typ": "text", "svarstyp": "int", "undertext": "Lös gärna på papper och skriv in ditt svar."}
            elif typ == 'f_likamed_g':
                x = random.randint(-10, 10)
                k1 = random.choice([-5, -4, -3, -2, 2, 3, 4, 5])
                k2 = random.choice([-5, -4, -3, -2, 2, 3, 4, 5])
                if k1 == k2: continue 
                m1 = random.randint(-15, 15)
                m2 = (k1 - k2)*x + m1 
                return {"info_text": "Givet funktionen:", "latex_text": f"f(x) = {formatera_linjar(k1, m1)} \\quad \\text{{och}} \\quad g(x) = {formatera_linjar(k2, m2)}", "fraga": "Bestäm x om f(x) = g(x)", "ratt_svar": x, "input_typ": "text", "svarstyp": "int", "undertext": "Lös gärna på papper och skriv in ditt svar."}

def skapa_ekv_uppgift(niva):
    def formatera_sida(k, m):
        k_str = "x" if k == 1 else ("-x" if k == -1 else (f"{k}x" if k != 0 else ""))
        if k == 0: return str(m)
        if m > 0: return f"{k_str} + {m}"
        elif m < 0: return f"{k_str} - {-m}"
        else: return k_str

    while True:
        x = random.randint(-10, 10)
        if niva == 1:
            typ = random.choice(['tvosteg', 'division', 'bada_sidor', 'enkel_parentes'])
            if typ == 'tvosteg':
                a = random.choice([-5, -4, -3, -2, -1, 2, 3, 4, 5])
                b = random.randint(-15, 15)
                ekv = f"{formatera_sida(a, b)} = {a * x + b}"
            elif typ == 'division':
                a = random.choice([2, 3, 4, 5])
                x = random.randint(-6, 6) * a 
                b = random.randint(-10, 10)
                b_str = f" + {b}" if b > 0 else (f" - {-b}" if b < 0 else "")
                ekv = f"\\frac{{x}}{{{a}}}{b_str} = {int(round(x / a)) + b}"
            elif typ == 'bada_sidor':
                a = random.choice([-5, -4, -3, -2, 2, 3, 4, 5])
                c_coeff = random.choice([-5, -4, -3, -2, 2, 3, 4, 5])
                if a == c_coeff: continue 
                b = random.randint(-20, 20)
                ekv = f"{formatera_sida(a, b)} = {formatera_sida(c_coeff, a * x + b - c_coeff * x)}"
            elif typ == 'enkel_parentes':
                a = random.choice([-5, -4, -3, -2, 2, 3, 4, 5])
                b = random.choice([-5, -4, -3, -2, 1, 2, 3, 4, 5])
                b_str = f"+ {b}" if b > 0 else f"- {-b}"
                ekv = f"{a}(x {b_str}) = {a * (x + b)}"
        else:
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
                D = val_VL - E * (x + F) if op == '+' else val_VL + E * (x + F)
                A_str = "x" if A == 1 else ("-x" if A == -1 else f"{A}x")
                B_str = f" + {B}" if B > 0 else (f" - {-B}" if B < 0 else "")
                E_str = "" if E == 1 else str(E)
                F_str = f"+ {F}" if F > 0 else f"- {-F}"
                ekv = f"\\frac{{{A_str}{B_str}}}{{{C}}} = {D} {op} {E_str}(x {F_str})"
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
                ekv = f"{A}(x {B_str}){C_str} = {D}(x {E_str})"
            elif typ == 'gemensam_namnare':
                B = random.choice([2, 3, 4])
                D = random.choice([2, 3, 4])
                if B == D: continue
                A = random.randint(-5, 5)
                x = random.randint(-3, 3) * B - A
                C = random.randint(-5, 5)
                E = (x + A) / B + (x + C) / D
                if not E.is_integer(): continue 
                A_str = f"+ {A}" if A > 0 else (f"- {-A}" if A < 0 else "")
                C_str = f"+ {C}" if C > 0 else (f"- {-C}" if C < 0 else "")
                ekv = f"\\frac{{x {A_str}}}{{{B}}} + \\frac{{x {C_str}}}{{{D}}} = {int(round(E))}"
            elif typ == 'x_i_namnare':
                B = random.choice([-5, -4, -3, -2, 1, 2, 3, 4, 5])
                x = random.randint(-10, 10)
                if x + B == 0: continue 
                C = random.choice([-4, -3, -2, -1, 2, 3, 4])
                B_str = f"+ {B}" if B > 0 else f"- {-B}"
                ekv = f"\\frac{{{C * (x + B)}}}{{x {B_str}}} = {C}"
            elif typ == 'gomda_forstagrads':
                A = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
                B = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
                C = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
                if A + B == C: continue 
                D = (A + B - C) * x + A * B
                A_str = f"+ {A}" if A > 0 else f"- {-A}"
                B_str = f"+ {B}" if B > 0 else f"- {-B}"
                C_str = "+ x" if C == 1 else ("- x" if C == -1 else (f"+ {C}x" if C > 0 else f"- {-C}x"))
                D_str = f"+ {D}" if D > 0 else (f"- {-D}" if D < 0 else "")
                ekv = f"(x {A_str})(x {B_str}) = x^2 {C_str} {D_str}".strip()

        return {
            "info_text": "Lös ekvationen:",
            "latex_text": ekv,
            "fraga": "Vad är x? (Svara med ett heltal):",
            "ratt_svar": x,
            "input_typ": "text",
            "svarstyp": "int",
            "undertext": "Lös gärna på papper och skriv in ditt svar."
        }

def skapa_alg_uttryck_uppgift(niva):
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

    while True:
        if niva == 1:
            typ = random.choice(['minus_parentes', 'mult_parentes', 'konstant_parentes', 'faktorisera'])
            if typ == 'minus_parentes':
                c = random.choice([2, 3, 4])
                B = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
                alg_uttryck_str = f"x - ({c}x {f'+ {B}' if B > 0 else f'- {-B}'})"
                svar_ratt = formatera_svar(0, 1 - c, -B)
                d1 = formatera_svar(0, 1 - c, B) 
                d2 = formatera_svar(0, 1 + c, -B) 
                d3 = formatera_svar(0, -c, -B) 
            elif typ == 'konstant_parentes':
                a, c = random.randint(2, 5), random.randint(2, 5)
                A, B = random.choice([-4, -3, -2, 2, 3, 4]), random.choice([-4, -3, -2, 2, 3, 4])
                alg_uttryck_str = f"{a}(x {f'+ {A}' if A > 0 else f'- {-A}'}) - {c}(x {f'+ {B}' if B > 0 else f'- {-B}'})"
                svar_ratt = formatera_svar(0, a - c, a*A - c*B)
                d1 = formatera_svar(0, a - c, a*A + c*B)
                d2 = formatera_svar(0, a + c, a*A - c*B)
                d3 = formatera_svar(0, a - c, a*A - B)
            elif typ == 'mult_parentes':
                A = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
                B = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
                alg_uttryck_str = f"(x {f'+ {A}' if A > 0 else f'- {-A}'})(x {f'+ {B}' if B > 0 else f'- {-B}'})"
                svar_ratt = formatera_svar(1, A + B, A * B)
                d1 = formatera_svar(1, 0, A * B)
                d2 = formatera_svar(1, A + B, A + B)
                d3 = formatera_svar(1, A * B, A * B)
            elif typ == 'faktorisera':
                k = random.choice([2, 3, 4, 5, 6, 7]) 
                a = random.choice([2, 3, 4, 5, 6])
                b = random.choice([1, 2, 3, 4, 5, 6])
                while math.gcd(a, b) != 1: b = random.randint(1, 6)
                op = random.choice(['+', '-'])
                alg_uttryck_str = f"{k * a}x {op} {k * b}"
                svar_ratt = f"{k}({a}x {op} {b})"
                d1 = f"{a}({k}x {op} {b})"  
                d2 = f"{k}({a}x {op} {k * b})" 
                d3 = f"{k}x({a} {op} {b})" if op == '+' else f"{k}x({a} - {b})"

        else: # Nivå 2
            typ = random.choice(['faktorisera_avancerat', 'mult_parentes_koeff', 'flersteg', 'rationell', 'likhet_parentes'])
            
            if typ == 'likhet_parentes':
                while True:
                    A = random.choice([2, 3, 4, 5])
                    D = random.choice([2, 3, 4, 5])
                    if A == D: continue
                    
                    E = random.choice([-5, -4, -3, -2, 2, 3, 4, 5])
                    F = random.choice([-10, -9, -8, -7, -6, -5, -4, -3, -2, 2, 3, 4, 5, 6, 7, 8, 9, 10])
                    
                    # För att B och C ska bli heltal måste A dela D*E och D*F
                    if (D * E) % A == 0 and (D * F) % A == 0:
                        B = (D * E) // A
                        C = (D * F) // A
                        break
                        
                B_str = "x" if B == 1 else ("-x" if B == -1 else f"{B}x")
                C_str = f"+ {C}" if C > 0 else f"- {-C}"
                VL = f"{A}({B_str} {C_str})"
                
                HL = f"{D}( \\dots )"
                alg_uttryck_str = f"{VL} = {HL}"
                
                E_str = "x" if E == 1 else ("-x" if E == -1 else f"{E}x")
                F_str = f"+ {F}" if F > 0 else f"- {-F}"
                svar_ratt = f"{E_str} {F_str}"
                
                return {
                    "info_text": "Skriv ett uttryck i parentesen så att likheten gäller:",
                    "latex_text": alg_uttryck_str,
                    "undertext": "Svara på formen ax + b (t.ex. 6x - 15).",
                    "fraga": "Vad ska stå i parentesen?",
                    "ratt_svar": svar_ratt,
                    "input_typ": "text",
                    "svarstyp": "string_math"
                }

            elif typ == 'faktorisera_avancerat':
                c, a = random.choice([2, 3, 4, 5]), random.choice([2, 3, 4, 5])
                b = random.choice([1, 2, 3, 4, 5])
                while math.gcd(a, b) != 1: b = random.randint(1, 5)
                var_typ, op = random.choice(['xy', 'x2']), random.choice(['+', '-'])
                if var_typ == 'xy':
                    alg_uttryck_str = f"{c * a}xy {op} {c * b}x"
                    svar_ratt = f"{c}x({a}y {op} {b})"
                    d1, d2, d3 = f"{a}x({c}y {op} {b})", f"{c}({a}xy {op} {b}x)", f"{c}xy({a} {op} {b})"      
                else:
                    alg_uttryck_str = f"{c * a}x^2 {op} {c * b}x"
                    svar_ratt = f"{c}x({a}x {op} {b})"
                    d1, d2, d3 = f"{a}x({c}x {op} {b})", f"{c}({a}x^2 {op} {b}x)", f"{c}x^2({a} {op} {b})"      
            elif typ == 'mult_parentes_koeff':
                a, c = random.choice([2, 3, 4]), random.choice([2, 3, 4])
                b, d = random.choice([-4, -3, -2, -1, 1, 2, 3, 4]), random.choice([-4, -3, -2, -1, 1, 2, 3, 4])
                alg_uttryck_str = f"({a}x {f'+ {b}' if b > 0 else f'- {-b}'})({c}x {f'+ {d}' if d > 0 else f'- {-d}'})"
                svar_ratt = formatera_svar(a*c, a*d + b*c, b*d)
                d1 = formatera_svar(a*c, 0, b*d) 
                d2 = formatera_svar(a*c, a*d + b*c, b+d) 
                d3 = formatera_svar(a+c, a*d + b*c, b*d) 
            elif typ == 'flersteg':
                a = random.choice([2, 3])
                b, c, d = random.choice([-4, -3, 2, 3, 4]), random.choice([-3, -2, -1, 1, 2, 3]), random.choice([-3, -2, -1, 1, 2, 3])
                alg_uttryck_str = f"x({a}x {f'+ {b}' if b > 0 else f'- {-b}'}) - (x {f'+ {c}' if c > 0 else f'- {-c}'})(x {f'+ {d}' if d > 0 else f'- {-d}'})"
                svar_ratt = formatera_svar(a - 1, b - (c + d), -(c * d))
                d1 = formatera_svar(a - 1, b - (c + d), c * d) 
                d2 = formatera_svar(a + 1, b - (c + d), -(c * d)) 
                d3 = formatera_svar(a - 1, b + c + d, -(c * d)) 
            elif typ == 'rationell':
                C = random.choice([2, 3, 4, 5])
                a, b = random.choice([-4, -3, -2, 2, 3, 4]), random.choice([-5, -4, -3, -2, 2, 3, 4, 5])
                B_str = f"+ {b*C}" if b*C > 0 else f"- {-b*C}"
                alg_uttryck_str = f"\\frac{{{a*C}x^2 {B_str}x}}{{{C}x}}"
                b_svar = f"+ {b}" if b > 0 else f"- {-b}"
                svar_ratt = f"{a}x {b_svar}"
                B_fel = f"+ {b*C}" if b*C > 0 else f"- {-b*C}"
                d1 = f"{a}x^2 {b_svar}"
                d2 = f"{a*C}x {b_svar}"
                d3 = f"{a}x {B_fel}"
                
        svar_ratt_latex = f"${svar_ratt}$"
        alternativ = [svar_ratt_latex, f"${d1}$", f"${d2}$", f"${d3}$"]
        
        # Säkerställ att vi får 4 HELT unika svarsalternativ, annars slumpar loopen om direkt
        if len(set(alternativ)) == 4:
            break
            
    random.shuffle(alternativ)

    return {
        "info_text": "Förenkla uttrycket:" if typ != 'faktorisera' and typ != 'faktorisera_avancerat' else "Faktorisera uttrycket så långt som möjligt:",
        "latex_text": alg_uttryck_str,
        "undertext": "Lös gärna på papper och välj ditt svar.",
        "fraga": "Välj rätt alternativ:",
        "ratt_svar": svar_ratt_latex,
        "alternativ": alternativ,
        "input_typ": "radio",
        "svarstyp": "string"
    }

def skapa_lan_uppgift(niva):
    def formatera_kr(b): return f"{int(round(b)):,}".replace(",", " ")
    
    if niva == 1:
        typ = random.choice(['arsranta', 'manadsranta', 'rak_amortering'])
        if typ == 'arsranta':
            kapital, ranta = random.choice([15000, 20000, 35000, 50000, 80000, 150000]), random.choice([3, 4, 5, 6, 7, 8])
            return {"info_box_blue": f"Du lånar {formatera_kr(kapital)} kr av banken med en årsränta på {ranta} %.", "fraga": "Hur mycket får du betala i ränta under det första året? (Svara i kr)", "ratt_svar": int(round(kapital * (ranta / 100))), "input_typ": "text", "svarstyp": "int", "suffix": "kr"}
        elif typ == 'manadsranta':
            kapital, ranta = random.choice([12000, 24000, 36000, 60000, 120000]), random.choice([3, 4, 5, 6, 7, 8])
            return {"info_box_blue": f"Du tar ett lån på {formatera_kr(kapital)} kr. Årsräntan är {ranta} %.", "fraga": "Hur stor blir räntekostnaden för den allra första månaden? (Svara i kr)", "ratt_svar": int(round((kapital * (ranta / 100)) / 12)), "input_typ": "text", "svarstyp": "int", "suffix": "kr"}
        elif typ == 'rak_amortering':
            ar, amort = random.choice([2, 3, 4, 5, 10]), random.choice([500, 1000, 1500, 2000, 2500])
            return {"info_box_blue": f"Du lånar {formatera_kr(amort * ar * 12)} kr som ska betalas tillbaka med rak amortering under {ar} år.", "fraga": "Hur mycket ska du amortera varje månad? (Svara i kr)", "ratt_svar": amort, "input_typ": "text", "svarstyp": "int", "suffix": "kr"}
    else:
        typ = random.choice(['manadskostnad_1', 'manadskostnad_2', 'snabblan'])
        if typ in ['manadskostnad_1', 'manadskostnad_2']:
            p = random.choice([{"K": 60000, "ar": 5, "amort": 1000, "rantor": [3, 6, 9]}, {"K": 120000, "ar": 5, "amort": 2000, "rantor": [3, 6, 9]}, {"K": 72000, "ar": 3, "amort": 2000, "rantor": [3, 4, 5, 6]}])
            ranta, avgift = random.choice(p["rantor"]), random.choice([25, 35, 45])
            if typ == 'manadskostnad_1':
                svar = int(round(p["amort"] + (p["K"] * (ranta / 100)) / 12 + avgift))
                return {"info_box_blue": f"Du köper en bil för {formatera_kr(p['K'])} kr på avbetalning. Lånet har rak amortering över {p['ar']} år och en årsränta på {ranta} %. Banken tar också ut en aviseringsavgift på {avgift} kr/månad.", "fraga": "Vad blir din TOTALA månadskostnad den första månaden? (Svara i kr)", "ratt_svar": svar, "input_typ": "text", "svarstyp": "int", "suffix": "kr"}
            else: 
                svar = int(round(p["amort"] + ((p["K"] - p["amort"]) * (ranta / 100)) / 12 + avgift))
                return {"info_box_blue": f"Du tar ett lån på {formatera_kr(p['K'])} kr med rak amortering över {p['ar']} år och en årsränta på {ranta} %. Aviseringsavgiften är {avgift} kr/månad.", "fraga": "När du ska betala din ANDRA faktura har lånet minskat. Vad blir din TOTALA månadskostnad den andra månaden? (Svara i kr)", "ratt_svar": svar, "input_typ": "text", "svarstyp": "int", "suffix": "kr"}
        elif typ == 'snabblan':
            kapital, manadsranta, upplagg, avi = random.choice([3000, 4000, 5000, 8000]), random.choice([2, 3, 4, 5]), random.choice([295, 395, 495]), random.choice([35, 45, 55])
            return {"info_box_blue": f"Du tar ett snabblån på {formatera_kr(kapital)} kr som ska betalas tillbaka i sin helhet efter exakt en månad. Uppläggningsavgiften är {upplagg} kr, aviseringsavgiften {avi} kr och månadsräntan är {manadsranta} %.", "fraga": "Hur mycket måste du totalt betala tillbaka när månaden är slut? (Svara i kr)", "ratt_svar": int(round(kapital + kapital * (manadsranta / 100) + upplagg + avi)), "input_typ": "text", "svarstyp": "int", "suffix": "kr"}

def skapa_ff_uppgift(niva):
    if niva == 1:
        typ = random.choice(['berakna_ff', 'nytt_pris', 'hitta_procent'])
        if typ == 'berakna_ff':
            riktning, procent = random.choice(['ökar', 'minskar']), round(random.uniform(1.5, 80.5), 1) if random.choice([True, False]) else random.randint(5, 80)
            return {"info_box_green": f"Ett pris {riktning} med {f'{procent:g}'.replace('.', ',')} %.", "fraga": "Vad blir förändringsfaktorn? (Svara med decimaltal)", "ratt_svar": round(1 + (procent / 100) if riktning == 'ökar' else 1 - (procent / 100), 4), "input_typ": "text", "svarstyp": "float"}
        elif typ == 'hitta_procent':
            riktning, procent = random.choice(['ökar', 'minskar']), round(random.uniform(1.5, 95.5), 1) if random.choice([True, False]) else random.randint(5, 95)
            ff = 1 + (procent / 100) if riktning == 'ökar' else 1 - (procent / 100)
            return {"info_box_green": f"En förändringsfaktor är {f'{round(ff, 4):g}'.replace('.', ',')}.", "fraga": "Vilken procentuell förändring motsvarar detta? (En sänkning svaras med minus, t.ex. -12,5)", "ratt_svar": procent if riktning == 'ökar' else -procent, "input_typ": "text", "svarstyp": "procent"}
        elif typ == 'nytt_pris':
            startpris, riktning, procent = random.choice([100, 200, 250, 400, 500, 800, 1000, 1500]), random.choice(['höjs', 'sänks']), random.choice([10, 15, 20, 25, 30, 40, 50, 12.5])
            return {"info_box_green": f"En vara kostar {startpris} kr. Priset {riktning} med {f'{procent:g}'.replace('.', ',')} %.", "fraga": "Vad blir det nya priset? (Svara i hela kronor)", "ratt_svar": int(round(startpris * (1 + procent / 100))) if riktning == 'höjs' else int(round(startpris * (1 - procent / 100))), "input_typ": "text", "svarstyp": "int", "suffix": "kr"}
    else:
        typ = random.choice(['hitta_gammalt', 'upprepad_procent'])
        if typ == 'hitta_gammalt':
            gammalt_pris, procent, riktning = random.choice([400, 500, 800, 1000, 1200, 1500, 2000]), random.choice([10, 20, 25, 30, 40, 50]), random.choice(['höjs', 'sänks'])
            nytt_pris = int(round(gammalt_pris * (1 + procent / 100))) if riktning == 'höjs' else int(round(gammalt_pris * (1 - procent / 100)))
            return {"info_box_green": f"Efter att priset på en vara {riktning} med {procent} % kostar den nu {nytt_pris} kr.", "fraga": "Vad kostade varan från början? (Svara i hela kronor)", "ratt_svar": gammalt_pris, "input_typ": "text", "svarstyp": "int", "suffix": "kr"}
        elif typ == 'upprepad_procent':
            p1, p2 = random.choice([10, 20, 25, 30]), random.choice([10, 20, 25, 30])
            r1, r2 = random.choice(['ökar', 'minskar']), random.choice(['ökar', 'minskar'])
            f1 = (1 + p1/100) if r1 == 'ökar' else (1 - p1/100)
            f2 = (1 + p2/100) if r2 == 'ökar' else (1 - p2/100)
            return {"info_box_green": f"Priset på en produkt {r1} först med {p1} % och {r2} därefter med {p2} %.", "fraga": "Vad är den totala förändringsfaktorn för båda ändringarna tillsammans? (Svara med decimaltal)", "ratt_svar": round(f1 * f2, 4), "input_typ": "text", "svarstyp": "float"}

def rita_traddiagram(grenar, farg1, farg2):
    fig = go.Figure()
    nodes_x, nodes_y = [0.5, 0.25, 0.75, 0.125, 0.375, 0.625, 0.875], [1, 0.5, 0.5, 0, 0, 0, 0]
    edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)]
    for i, (start, end) in enumerate(edges):
        fig.add_trace(go.Scatter(x=[nodes_x[start], nodes_x[end]], y=[nodes_y[start], nodes_y[end]], mode='lines', line=dict(color='black', width=2), hoverinfo='skip'))
        forskjutning = 0.65
        fig.add_annotation(x=nodes_x[start] + forskjutning * (nodes_x[end] - nodes_x[start]), y=nodes_y[start] + forskjutning * (nodes_y[end] - nodes_y[start]), text=f"<b>{grenar[i]}</b>", showarrow=False, font=dict(size=18, color='red' if grenar[i] == 'x' else '#0056b3'), bgcolor="white", borderpad=2)
    fig.add_trace(go.Scatter(x=nodes_x, y=nodes_y, mode='markers+text', marker=dict(size=40, color='white', line=dict(color='black', width=2)), text=[f"<b>{lbl}</b>" for lbl in ["Start", farg1, farg2, farg1, farg2, farg1, farg2]], textposition="middle center", hoverinfo='skip'))
    fig.add_annotation(x=-0.05, y=0.5, text="<b>Dragning 1</b>", showarrow=False, font=dict(size=14, color="gray"), xanchor="right")
    fig.add_annotation(x=-0.05, y=0, text="<b>Dragning 2</b>", showarrow=False, font=dict(size=14, color="gray"), xanchor="right")
    fig.update_layout(xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.3, 1.05]), yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.2, 1.1]), margin=dict(l=10, r=10, t=10, b=10), height=400, plot_bgcolor='white', showlegend=False, hovermode=False, dragmode=False)
    return fig

def skapa_slump_uppgift(niva):
    if niva == 1:
        typ = random.choice(['flerval_uppstallning', 'berakna_enkla', 'enkel_dragning', 'tarning_mynt', 'trad_berakna', 'trad_saknas'])
        if typ == 'trad_berakna':
            A, B = random.randint(3, 6), random.randint(3, 6)
            tot = A + B
            p1, p2, p3, p4, p5, p6 = Fraction(A, tot), Fraction(B, tot), Fraction(A-1, tot-1), Fraction(B, tot-1), Fraction(A, tot-1), Fraction(B-1, tot-1)
            gren_texter = [f"{p.numerator}/{p.denominator}" for p in [p1, p2, p3, p4, p5, p6]]
            fraga_val = random.choice(['två röda', 'två blå', 'exakt en av varje färg'])
            ratt_svar = p1 * p3 if fraga_val == 'två röda' else (p2 * p6 if fraga_val == 'två blå' else (p1 * p4) + (p2 * p5))
            return {"info_box_pink": f"I en påse finns {A} röda och {B} blå kulor. Träddiagrammet visar vad som kan hända om du drar två kulor utan återläggning.", "plotly_fig": rita_traddiagram(gren_texter, "Röd", "Blå"), "fraga": f"Vad är sannolikheten att du drar {fraga_val}? (Svara i bråkform)", "ratt_svar": ratt_svar, "input_typ": "text", "svarstyp": "fraction", "undertext": "Svara i bråkform med ett snedstreck (t.ex. 3/8). Bråket behöver inte vara förkortat maximalt."}
        elif typ == 'trad_saknas':
            A, B = random.randint(3, 7), random.randint(3, 7)
            tot = A + B
            fractions = [Fraction(A, tot), Fraction(B, tot), Fraction(A-1, tot-1), Fraction(B, tot-1), Fraction(A, tot-1), Fraction(B-1, tot-1)]
            gren_texter = [f"{p.numerator}/{p.denominator}" for p in fractions]
            saknad_idx = random.randint(0, 5)
            ratt_svar = fractions[saknad_idx]
            gren_texter[saknad_idx] = "x"
            return {"info_box_pink": f"I en påse finns {A} röda och {B} blå kulor. Du drar två kulor utan återläggning.", "plotly_fig": rita_traddiagram(gren_texter, "Röd", "Blå"), "fraga": "Ett värde i träddiagrammet har bytts ut mot 'x'. Vilket bråktal ska stå istället för x i diagrammet?", "ratt_svar": ratt_svar, "input_typ": "text", "svarstyp": "fraction", "undertext": "Svara i bråkform med ett snedstreck (t.ex. 3/8). Bråket behöver inte vara förkortat maximalt."}
        elif typ == 'flerval_uppstallning':
            A, B = random.randint(3, 7), random.randint(3, 7)
            tot = A + B
            ratt = f"\\frac{{{A}}}{{{tot}}} \\cdot \\frac{{{A-1}}}{{{tot-1}}}"
            alt = [ratt, f"\\frac{{{A}}}{{{tot}}} \\cdot \\frac{{{A}}}{{{tot}}}", f"\\frac{{{A}}}{{{tot}}} + \\frac{{{A-1}}}{{{tot-1}}}", f"\\frac{{{A}}}{{{tot}}} \\cdot \\frac{{{A-1}}}{{{tot}}}"]
            random.shuffle(alt)
            return {"info_box_pink": f"I en påse finns {A} röda och {B} gröna godisbitar. Du drar två godisbitar slumpmässigt utan att titta.", "fraga": "Vilken beräkning ger sannolikheten att du får två röda godisbitar?", "ratt_svar": f"${ratt}$", "alternativ": [f"${a}$" for a in alt], "input_typ": "radio", "svarstyp": "string", "undertext": "Välj det alternativ som visar rätt uträkning."}
        elif typ == 'berakna_enkla':
            tot = random.randint(4, 12)
            vinst, nit = 1, tot - 1
            return {"info_box_pink": f"Ett lyckohjul har {tot} lika stora fält. Endast {vinst} av fälten ger vinst och {nit} ger nit. Du snurrar hjulet två gånger.", "fraga": "Vad är sannolikheten att du vinner på båda snurren?", "ratt_svar": Fraction(vinst, tot) * Fraction(vinst, tot), "input_typ": "text", "svarstyp": "fraction", "undertext": "Svara i bråkform med ett snedstreck (t.ex. 3/8). Bråket behöver inte vara förkortat maximalt."}
        elif typ == 'enkel_dragning':
            farg1_plur, farg1_sing = random.choice([('röda', 'röd'), ('gröna', 'grön'), ('blåa', 'blå')])
            farg2_plur, farg2_sing = random.choice([('gula', 'gul'), ('svarta', 'svart'), ('vita', 'vit')])
            A, B = random.randint(3, 8), random.randint(3, 8)
            return {"info_box_pink": f"I en påse finns {A} {farg1_plur} och {B} {farg2_plur} kulor. Du drar en kula utan att titta.", "fraga": f"Vad är sannolikheten att du drar en {farg1_sing} kula?", "ratt_svar": Fraction(A, A+B), "input_typ": "text", "svarstyp": "fraction", "undertext": "Svara i bråkform med ett snedstreck (t.ex. 3/8). Bråket behöver inte vara förkortat maximalt."}
        elif typ == 'tarning_mynt':
            tarning_events = [("ett jämnt tal", Fraction(3, 6)), ("ett udda tal", Fraction(3, 6)), ("mer än 4", Fraction(2, 6)), ("mindre än 3", Fraction(2, 6)), ("mer än 2", Fraction(4, 6)), ("mindre än 5", Fraction(4, 6))] + [(f"en {i}:a", Fraction(1, 6)) for i in range(1, 7)]
            valt_tarning_event, tarning_prob = random.choice(tarning_events)
            target_mynt = random.choice(['krona', 'klave'])
            return {"info_box_pink": "Du kastar en vanlig sexsidig tärning och singlar ett mynt.", "fraga": f"Vad är sannolikheten att du får {valt_tarning_event} och {target_mynt}?", "ratt_svar": tarning_prob * Fraction(1, 2), "input_typ": "text", "svarstyp": "fraction", "undertext": "Svara i bråkform med ett snedstreck (t.ex. 3/8). Bråket behöver inte vara förkortat maximalt."}
    else:
        typ = random.choice(['komplement_oberoende', 'komplement_beroende', 'flera_vagar', 'tarning_summa'])
        if typ == 'komplement_oberoende':
            kast = random.choice([3, 4])
            return {"info_box_pink": f"Du kastar en vanlig sexsidig tärning {kast} gånger i rad.", "fraga": "Vad är sannolikheten att du slår minst en sexa?", "ratt_svar": Fraction(1, 1) - (Fraction(5, 6) ** kast), "input_typ": "text", "svarstyp": "fraction", "undertext": "Svara i bråkform med ett snedstreck (t.ex. 3/8). Bråket behöver inte vara förkortat maximalt."}
        elif typ == 'komplement_beroende':
            vinst, nit = random.randint(2, 4), random.randint(8, 15)
            tot = vinst + nit
            return {"info_box_pink": f"I en skål ligger {tot} lotter. {vinst} är vinstlotter och {nit} är nitlotter. Du drar två lotter utan att titta.", "fraga": "Vad är sannolikheten att du får minst en vinstlott?", "ratt_svar": Fraction(1, 1) - (Fraction(nit, tot) * Fraction(nit-1, tot-1)), "input_typ": "text", "svarstyp": "fraction", "undertext": "Svara i bråkform med ett snedstreck (t.ex. 3/8). Bråket behöver inte vara förkortat maximalt."}
        elif typ == 'flera_vagar':
            A, B = random.randint(3, 6), random.randint(3, 6)
            return {"info_box_pink": f"I en ask finns {A} röda och {B} blå bollar. Du drar två bollar slumpmässigt utan återläggning.", "fraga": "Vad är sannolikheten att du får exakt en av varje färg?", "ratt_svar": Fraction(2 * A * B, (A + B) * (A + B - 1)), "input_typ": "text", "svarstyp": "fraction", "undertext": "Svara i bråkform med ett snedstreck (t.ex. 3/8). Bråket behöver inte vara förkortat maximalt."}
        elif typ == 'tarning_summa':
            summan = random.randint(4, 10)
            gynsamma = sum(1 for i in range(1, 7) for j in range(1, 7) if i + j == summan)
            return {"info_box_pink": "Du kastar två vanliga sexsidiga tärningar.", "fraga": f"Vad är sannolikheten att tärningarnas summa blir exakt {summan}?", "ratt_svar": Fraction(gynsamma, 36), "input_typ": "text", "svarstyp": "fraction", "undertext": "Svara i bråkform med ett snedstreck (t.ex. 3/8). Bråket behöver inte vara förkortat maximalt."}

def rita_stat_graf(x, y):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='markers', marker=dict(size=10, color='#8B008B', opacity=0.7), hoverinfo='skip'))
    fig.update_layout(xaxis=dict(range=[0, 100], showticklabels=False, showgrid=False, zeroline=False, showline=False), yaxis=dict(range=[0, 160], showticklabels=False, showgrid=False, zeroline=False, showline=False), margin=dict(l=20, r=20, t=20, b=20), height=450, plot_bgcolor='white', hovermode=False, dragmode=False)
    fig.add_annotation(x=100, y=0, xref='x', yref='y', ax=0, ay=0, axref='x', ayref='y', showarrow=True, arrowhead=2, arrowsize=1.5, arrowwidth=2, arrowcolor='black')
    fig.add_annotation(x=0, y=160, xref='x', yref='y', ax=0, ay=0, axref='x', ayref='y', showarrow=True, arrowhead=2, arrowsize=1.5, arrowwidth=2, arrowcolor='black')
    return fig

def skapa_stat_uppgift(niva=1):
    typ = random.choice(['spridning', 'konf_overlapp', 'konf_baklanges', 'konf_urval', 'konf_falskt'])
    if typ == 'spridning':
        num_points = random.randint(40, 60)
        x = np.random.uniform(10, 90, num_points)
        korr = random.choice(['Stark positiv', 'Svag positiv', 'Stark negativ', 'Svag negativ', 'Ingen korrelation'])
        if korr == 'Stark positiv': y = 1.5 * x + np.random.normal(0, 6, num_points)
        elif korr == 'Svag positiv': y = 1.5 * x + np.random.normal(0, 25, num_points)
        elif korr == 'Stark negativ': y = -1.5 * x + 150 + np.random.normal(0, 6, num_points)
        elif korr == 'Svag negativ': y = -1.5 * x + 150 + np.random.normal(0, 25, num_points)
        else: y = np.random.uniform(10, 90, num_points)
        return {"info_text_italic": "Kika på spridningsdiagrammet ovan.", "plotly_fig": rita_stat_graf(x, y), "fraga": "Vilken typ av korrelation visar diagrammet?", "ratt_svar": korr, "alternativ": ['Välj svar...', 'Stark positiv', 'Svag positiv', 'Stark negativ', 'Svag negativ', 'Ingen korrelation'], "input_typ": "selectbox", "svarstyp": "string"}
    elif typ == 'konf_overlapp':
        A = random.randint(14, 25)
        B, fm = A - random.randint(1, 3), random.randint(2, 4)
        overlapp = (A - fm) <= (B + fm)
        ratt = "Vi kan inte vara helt säkra på vilket parti som är störst, eftersom felmarginalerna överlappar." if overlapp else "Parti A är med största sannolikhet större än Parti B, eftersom felmarginalerna inte överlappar."
        alts = [ratt, "Parti A är garanterat större än Parti B." if overlapp else "Vi kan inte vara säkra på vilket parti som är störst, eftersom felmarginalerna överlappar.", "Parti A har ökat mer än Parti B sedan förra valet.", f"Parti A kommer att få exakt {A} % av rösterna i valet."]
        random.shuffle(alts)
        return {"info_box_purple": f"En väljarbarometer visar att Parti A får {A} % och Parti B får {B} % av väljarstödet. Felmarginalen är ±{fm} procentenheter för båda partierna vid 95 % konfidensgrad.", "fraga": "Vilken slutsats kan dras med 95 % säkerhet?", "ratt_svar": ratt, "alternativ": alts, "input_typ": "radio", "svarstyp": "string"}
    elif typ == 'konf_baklanges':
        resultat, fm = round(random.uniform(4.0, 12.0), 1), round(random.uniform(1.5, 3.5), 1)
        ratt = f"Resultatet var {f'{resultat:g}'.replace('.', ',')} % med en felmarginal på ±{f'{fm:g}'.replace('.', ',')} procentenheter."
        alts = [ratt, f"Resultatet var {f'{round(resultat+fm, 1):g}'.replace('.', ',')} % med en felmarginal på ±{f'{round(fm*2, 1):g}'.replace('.', ',')} procentenheter.", f"Resultatet var {f'{round(resultat-fm, 1):g}'.replace('.', ',')} % med en felmarginal på ±{f'{round(resultat+fm, 1):g}'.replace('.', ',')} procentenheter.", f"Resultatet var {f'{resultat:g}'.replace('.', ',')} % med en felmarginal på ±{f'{round(fm/2, 1):g}'.replace('.', ',')} procentenheter."]
        random.shuffle(alts)
        return {"info_box_purple": f"Ett 95 % konfidensintervall för andelen defekta produkter i en fabrik anges till {f'{round(resultat-fm, 1):g}'.replace('.', ',')}-{f'{round(resultat+fm, 1):g}'.replace('.', ',')}%.", "fraga": "Vad var resultatet i själva stickprovet, och vad var felmarginalen?", "ratt_svar": ratt, "alternativ": alts, "input_typ": "radio", "svarstyp": "string"}
    elif typ == 'konf_urval':
        fm = round(random.uniform(3.0, 5.0), 1)
        ratt = "Fråga betydligt fler personer i nästa undersökning."
        alts = [ratt, "Fråga färre personer så att risken för felräkning minskar.", "Ändra konfidensgraden till 100 % istället för 95 %.", "Bara fråga personer som de vet är insatta i politiken."]
        random.shuffle(alts)
        return {"info_box_purple": f"En tidning publicerar en opinionsundersökning men tycker att felmarginalen på ±{f'{fm:g}'.replace('.', ',')} % gör resultatet för osäkert. De vill ha ett snävare (mindre) konfidensintervall nästa månad.", "fraga": "Vad är det bästa sättet för dem att minska felmarginalen rent statistiskt?", "ratt_svar": ratt, "alternativ": alts, "input_typ": "radio", "svarstyp": "string"}
    elif typ == 'konf_falskt':
        resultat, fm = random.randint(55, 75), random.randint(2, 4)
        ratt = f"Mellan {resultat - fm} % och {resultat + fm} % av eleverna *som tillfrågades* vill ha längre raster."
        alts = [ratt, f"Det sanna värdet för hela skolan ligger med 95 % säkerhet mellan {resultat - fm} % och {resultat + fm} %.", f"I det faktiska stickprovet svarade exakt {resultat} % att de vill ha längre raster.", "Även om intervallet är brett, finns det en risk att det sanna värdet ligger utanför intervallet."]
        random.shuffle(alts)
        return {"info_box_purple": f"En undersökning visar att {resultat} % av eleverna på en stor skola vill ha längre raster. Undersökningen har en felmarginal på ±{fm} procentenheter vid 95 % konfidensgrad.", "fraga": "Vilket av följande påståenden är FALSKT (felaktigt)?", "ratt_svar": ratt, "alternativ": alts, "input_typ": "radio", "svarstyp": "string"}

# ==========================================
# 2. LOGIK FÖR ATT GENERERA NY UPPGIFT
# ==========================================

KATEGORIER = {
    "Funktioner: Grafisk lösning": skapa_graf_uppgift,
    "Funktioner: Algebraisk lösning": skapa_alg_func_uppgift,
    "Ekvationer": skapa_ekv_uppgift,
    "Algebra": skapa_alg_uttryck_uppgift,
    "Lån och ränta": skapa_lan_uppgift,
    "Förändringsfaktor": skapa_ff_uppgift,
    "Sannolikhetslära": skapa_slump_uppgift,
    "Statistik": skapa_stat_uppgift
}

TITLAR = {
    "Funktioner: Grafisk lösning": "Grafisk avläsning av funktioner",
    "Funktioner: Algebraisk lösning": "Algebraisk lösning av funktioner",
    "Ekvationer": "Lös ekvationerna",
    "Algebra": "Förenkla och faktorisera algebraiska uttryck",
    "Lån och ränta": "Beräkna Lån och Ränta",
    "Förändringsfaktor": "Träna på Förändringsfaktor",
    "Sannolikhetslära": "Träna på Sannolikhetslära",
    "Statistik": "Tolka Statistik och Diagram",
    "Blandat (Slumpas)": "Blandade uppgifter - Träna på allt!"
}

def generera_ny_uppgift():
    st.session_state.rattat = False
    st.session_state.svar_status = None
    st.session_state.uppgift_id = st.session_state.get('uppgift_id', 0) + 1
    
    kat = st.session_state.aktuell_kategori
    niva = st.session_state.niva
    
    if kat == "Blandat (Slumpas)":
        tillgangliga_kategorier = list(KATEGORIER.keys())
        # Om nivå 2 är vald, plocka bort Statistik från hatten
        if niva == 2:
            tillgangliga_kategorier.remove("Statistik")
            
        valbar_kat = random.choice(tillgangliga_kategorier)
        u = KATEGORIER[valbar_kat](niva)
        u['visnings_kategori'] = valbar_kat # För att veta vilken färg vi ska använda etc.
    else:
        u = KATEGORIER[kat](niva)
        u['visnings_kategori'] = kat
        
    st.session_state.aktiv_uppgift = u

# ==========================================
# 3. MENYSYSTEM
# ==========================================
st.sidebar.title("Välj Träningsläge")
vald_kategori = st.sidebar.radio("Vad vill du träna på?", list(KATEGORIER.keys()) + ["Blandat (Slumpas)"])

if 'aktuell_kategori' not in st.session_state or st.session_state.aktuell_kategori != vald_kategori:
    st.session_state.aktuell_kategori = vald_kategori
    st.session_state.niva = 1
    generera_ny_uppgift()
    st.rerun()

st.sidebar.divider()
st.sidebar.subheader("Inställningar")

# Endast nivå 1 för statistik
if vald_kategori == "Statistik":
    ny_niva = st.sidebar.radio("Välj svårighetsgrad:", [1], horizontal=True, index=0)
else:
    ny_niva = st.sidebar.radio("Välj svårighetsgrad:", [1, 2], horizontal=True, index=st.session_state.niva - 1)

if ny_niva != st.session_state.niva:
    st.session_state.niva = ny_niva
    generera_ny_uppgift()
    st.rerun()

# ==========================================
# 4. UNIVERSELL UI-RENDERING
# ==========================================
u = st.session_state.aktiv_uppgift
st.title(TITLAR[st.session_state.aktuell_kategori])

col_vanster, col_hoger = st.columns([1.2, 1], gap="large")

with col_vanster:
    # 1. Grafisk Plot
    if u.get('graf_f') is not None:
        fig = rita_plotly_graf(
            f = u['graf_f'],
            visa_facit = st.session_state.rattat,
            q_vis_type = u.get('q_type_vis', 'vis_none'),
            trace_x = u.get('trace_x'),
            trace_y = u.get('trace_y'),
            trace_alla_x = u.get('trace_alla_x')
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
    # 2. Plotly fig (träd, spridning)
    if u.get('plotly_fig') is not None:
        st.plotly_chart(u['plotly_fig'], use_container_width=True, config={'displayModeBar': False})

    # 3. Text/Latex content
    if 'info_text' in u:
        st.markdown(f"<div style='text-align: center; font-size: 20px; color: gray; margin-top: 50px;'>{u['info_text']}</div>", unsafe_allow_html=True)
    if 'latex_text' in u:
        st.latex(u['latex_text'])
    
    # 4. Färgade informationsboxar
    if 'info_box_blue' in u:
        st.markdown(f"<div style='font-size: 22px; font-weight: bold; color: #333; margin-top: 30px; background-color: #f8f9fa; padding: 25px; border-radius: 10px; border-left: 6px solid #0056b3;'>{u['info_box_blue']}</div>", unsafe_allow_html=True)
    if 'info_box_green' in u:
        st.markdown(f"<div style='font-size: 22px; font-weight: bold; color: #333; margin-top: 30px; background-color: #e9ecef; padding: 25px; border-radius: 10px; border-left: 6px solid #28a745;'>{u['info_box_green']}</div>", unsafe_allow_html=True)
    if 'info_box_pink' in u:
        st.markdown(f"<div style='font-size: 22px; font-weight: bold; color: #333; margin-top: 30px; background-color: #fce4ec; padding: 25px; border-radius: 10px; border-left: 6px solid #e83e8c;'>{u['info_box_pink']}</div>", unsafe_allow_html=True)
    if 'info_box_purple' in u:
        st.markdown(f"<div style='font-size: 22px; font-weight: bold; color: #333; margin-top: 30px; background-color: #f3e5f5; padding: 25px; border-radius: 10px; border-left: 6px solid #8B008B;'>{u['info_box_purple']}</div>", unsafe_allow_html=True)
    if 'info_text_italic' in u:
        st.markdown(f"<div style='font-size: 20px; font-style: italic; color: gray;'>{u['info_text_italic']}</div>", unsafe_allow_html=True)

with col_hoger:
    st.subheader("Uppgift")
    if 'undertext' in u:
        st.markdown(f"<p style='font-size: 14px; font-style: italic; color: #666; margin-bottom: 5px;'>{u['undertext']}</p>", unsafe_allow_html=True)
        
    # Färgkodning beroende på kategori
    q_color = "#0056b3"
    if u['visnings_kategori'] == "Förändringsfaktor": q_color = "#28a745"
    elif u['visnings_kategori'] == "Sannolikhetslära": q_color = "#e83e8c"
    elif u['visnings_kategori'] == "Statistik": q_color = "#8B008B"
    
    # Transparent utfyllnad om ekvation är ensam på vänstersidan
    if u['visnings_kategori'] == "Ekvationer":
        st.markdown("<div style='font-size: 32px; font-weight: bold; color: transparent; margin-bottom: 25px;'>&nbsp;</div>", unsafe_allow_html=True) 
    else:
        st.markdown(f"<div style='font-size: 26px; font-weight: bold; color: {q_color}; margin-bottom: 25px;'>{u['fraga']}</div>", unsafe_allow_html=True)
    
    # Generera Inmatningsfält
    input_svar = None
    uid = st.session_state.uppgift_id
    if u['input_typ'] == 'flera_text':
        input_svar = []
        for i in range(len(u['ratt_svar'])):
            etikett = f"Svar {i+1}:" if len(u['ratt_svar']) > 1 else "Ditt svar:"
            input_svar.append(st.text_input(etikett, key=f"input_{uid}_{i}"))
    elif u['input_typ'] == 'text':
        input_svar = st.text_input("Ditt svar:", key=f"input_text_{uid}")
    elif u['input_typ'] == 'radio':
        input_svar = st.radio("Alternativ:", u['alternativ'], index=None, label_visibility="collapsed", key=f"input_radio_{uid}")
    elif u['input_typ'] == 'selectbox':
        input_svar = st.selectbox("Välj ett alternativ:", u['alternativ'], label_visibility="collapsed", key=f"input_select_{uid}")
        
    st.write("")
    
    # Knappar
    k1, k2 = st.columns(2)
    with k1:
        if st.button("Rätta svar", type="primary", use_container_width=True):
            st.session_state.rattat = True
            status = 'fel'
            
            # Validering
            if u['input_typ'] == 'flera_text':
                if all(s.strip() != "" for s in input_svar):
                    try:
                        anv_svar_float = sorted([round(float(s.strip().replace(',', '.')), 4) for s in input_svar])
                        status = 'ratt' if anv_svar_float == u['ratt_svar'] else 'fel'
                    except ValueError: status = 'format'
                else: status = 'tom'
                    
            elif u['input_typ'] == 'text':
                if input_svar.strip() != "":
                    try:
                        if u['svarstyp'] == 'int':
                            svar_clean = input_svar.strip().replace(" ", "")
                            status = 'ratt' if int(svar_clean) == u['ratt_svar'] else 'fel'
                        elif u['svarstyp'] in ['float', 'procent']:
                            svar_clean = input_svar.strip().replace(",", ".").replace(" ", "").replace("%", "")
                            status = 'ratt' if abs(float(svar_clean) - u['ratt_svar']) < 0.001 else 'fel'
                        elif u['svarstyp'] == 'fraction':
                            svar_clean = input_svar.strip().replace(" ", "").replace(",", ".")
                            status = 'ratt' if Fraction(svar_clean) == u['ratt_svar'] else 'fel'
                        elif u['svarstyp'] == 'string_math':
                            # Rensar inmatning och gör den smidigare att utvärdera för Algebrauttryck
                            svar_clean = input_svar.replace(" ", "").lower()
                            ratt_clean = str(u['ratt_svar']).replace(" ", "").lower()
                            if svar_clean.startswith("+"): svar_clean = svar_clean[1:]
                            if svar_clean.startswith("1x"): svar_clean = "x" + svar_clean[2:]
                            if svar_clean.startswith("-1x"): svar_clean = "-x" + svar_clean[3:]
                            svar_clean = svar_clean.replace("+1x", "+x").replace("-1x", "-x")
                            status = 'ratt' if svar_clean == ratt_clean else 'fel'
                    except ValueError: status = 'format'
                else: status = 'tom'
                    
            elif u['input_typ'] in ['radio', 'selectbox']:
                if input_svar is not None and input_svar != 'Välj svar...':
                    status = 'ratt' if str(input_svar).strip() == str(u['ratt_svar']).strip() else 'fel'
                else: status = 'tom'
                    
            st.session_state.svar_status = status
            st.rerun()
            
    with k2:
        if st.button("Nästa uppgift", use_container_width=True):
            generera_ny_uppgift()
            st.rerun()
            
    # Återkoppling
    if st.session_state.rattat:
        status = st.session_state.svar_status
        if status == 'ratt':
            st.success("✅ Helt rätt! Snyggt jobbat.")
        elif status == 'fel':
            # Formatera rätt svar för utskrift
            if u['svarstyp'] == 'array_float':
                ratt_txt = ' och '.join([f"{a:g}".replace('.', ',') for a in u['ratt_svar']])
            elif u['svarstyp'] == 'fraction':
                ratt_txt = f"{u['ratt_svar'].numerator}/{u['ratt_svar'].denominator}"
            elif u['svarstyp'] in ['float', 'procent']:
                ratt_txt = f"{u['ratt_svar']:g}".replace('.', ',')
            elif u['svarstyp'] == 'string_math':
                ratt_txt = str(u['ratt_svar'])
            else:
                ratt_txt = str(u['ratt_svar'])
                
            if u.get('suffix'): ratt_txt += f" {u['suffix']}"
            if u['svarstyp'] == 'procent': ratt_txt += " %"
            
            st.error(f"❌ Tyvärr fel. Rätt svar var:\n\n {ratt_txt}")
        elif status == 'format':
            if u['svarstyp'] in ['float', 'procent']:
                st.warning("⚠️ Svaret är i fel format (skriv bara siffror/decimaltal, t.ex. 1,25).")
            elif u['svarstyp'] == 'int':
                st.warning("⚠️ Svaret ska vara ett heltal.")
            elif u['svarstyp'] == 'fraction':
                st.warning("⚠️ Skriv svaret som ett bråk, till exempel 3/8.")
            else:
                st.warning("⚠️ Svaret är i fel format.")
        elif status == 'tom':
            if u['input_typ'] in ['radio', 'selectbox']:
                st.warning("Vänligen välj ett alternativ i listan.")
            else:
                st.warning("Vänligen fyll i ett svar innan du rättar.")
