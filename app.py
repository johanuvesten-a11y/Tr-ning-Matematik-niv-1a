import streamlit as st
import numpy as np
import random
import math
import plotly.graph_objects as go
from fractions import Fraction
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

# --- Ställ in sidans layout till bred ---
st.set_page_config(layout="wide", page_title="Matematikträning")

# --- Specialdesign (CSS) ---
st.markdown("""
<style>
input[type="text"] {
    font-size: 14px !important;
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
# 0. HJÄLPFUNKTIONER FÖR FORMATERING & RÄTTNING
# ==========================================

def formatera_polynom(termer):
    """
    Hjälpfunktion för att formatera algebraiska termer till snygg text (t.ex. tar bort 1x, hanterar minus).
    termer: En lista med tupler (koefficient, 'variabelsträng'), t.ex. [(3, 'x^2'), (-1, 'x'), (5, '')]
    """
    res = ""
    for koeff, var in termer:
        if koeff == 0:
            continue
        
        # Formatera koefficienten (siffran)
        if var == "":
            term_str = str(abs(koeff))
        else:
            if abs(koeff) == 1:
                term_str = var
            else:
                term_str = f"{abs(koeff)}{var}"
        
        # Hantera tecken och bygga ihop strängen
        if res == "":
            if koeff < 0:
                res += f"-{term_str}"
            else:
                res += term_str
        else:
            if koeff < 0:
                res += f" - {term_str}"
            else:
                res += f" + {term_str}"
                
    return res if res != "" else "0"

def formatera_kr(b): 
    return f"{int(round(b)):,}".replace(",", " ")

def ratta_svar(u, input_svar):
    """
    Centraliserad logik för att rätta alla uppgiftstyper.
    Returnerar status som en sträng: 'ratt', 'fel', 'format', 'format_ratio', 'format_saknar_likamed', 'tom'
    """
    if u['input_typ'] == 'flera_text':
        if all(s.strip() != "" for s in input_svar):
            try:
                anv_svar_float = sorted([round(float(s.strip().replace(',', '.')), 4) for s in input_svar])
                return 'ratt' if anv_svar_float == u['ratt_svar'] else 'fel'
            except ValueError: 
                return 'format'
        else: 
            return 'tom'
            
    elif u['input_typ'] == 'text':
        if input_svar.strip() != "":
            try:
                if u['svarstyp'] == 'int':
                    svar_clean = input_svar.strip().replace(" ", "")
                    return 'ratt' if int(svar_clean) == u['ratt_svar'] else 'fel'
                
                elif u['svarstyp'] in ['float', 'procent']:
                    svar_clean = input_svar.strip().replace(",", ".").replace(" ", "").replace("%", "")
                    return 'ratt' if abs(float(svar_clean) - float(u['ratt_svar'])) < 0.001 else 'fel'
                
                elif u['svarstyp'] == 'fraction':
                    svar_clean = input_svar.strip().replace(" ", "").replace(",", ".")
                    return 'ratt' if Fraction(svar_clean) == u['ratt_svar'] else 'fel'
                
                elif u['svarstyp'] == 'ratio':
                    svar_clean = input_svar.strip().replace(" ", "")
                    if ":" not in svar_clean:
                        return 'format_ratio'
                    else:
                        return 'ratt' if svar_clean == str(u['ratt_svar']) else 'fel'
                
                elif u['svarstyp'] == 'string_math':
                    # Ersätt vanliga knasigheter som komma och mellanslag
                    svar_clean = input_svar.replace(",", ".").replace(" ", "").replace("^", "**")
                    try:
                        # Använd sympy med "implicit_multiplication"
                        transformations = (standard_transformations + (implicit_multiplication_application,))
                        expr_elev = parse_expr(svar_clean, transformations=transformations)
                        ratt_svar_str = str(u['ratt_svar']).replace(" ", "").replace("^", "**")
                        expr_facit = parse_expr(ratt_svar_str, transformations=transformations)
                        
                        # Förenkla skillnaden. Är den noll är uttrycken exakt likvärdiga.
                        if sp.simplify(expr_elev - expr_facit) == 0:
                            return 'ratt'
                        else:
                            return 'fel'
                    except Exception:
                        return 'format'
                
                elif u['svarstyp'] == 'kalkyl_formel':
                    svar_clean = input_svar.strip().replace(" ", "").lower()
                    if not svar_clean.startswith("="):
                        return 'format_saknar_likamed'
                    else:
                        godkanda = [s.lower() for s in u.get('ratt_svar_lista', [])]
                        return 'ratt' if svar_clean in godkanda else 'fel'
                        
                elif u['svarstyp'] == 'string':
                    svar_clean = str(input_svar).strip()
                    return 'ratt' if svar_clean.lower() == str(u['ratt_svar']).strip().lower() else 'fel'

            except ValueError: 
                return 'format'
        else: 
            return 'tom'
            
    elif u['input_typ'] in ['radio', 'selectbox']:
        if input_svar is not None and input_svar != 'Välj svar...':
            return 'ratt' if str(input_svar).strip() == str(u['ratt_svar']).strip() else 'fel'
        else: 
            return 'tom'
    
    return 'fel'

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
                    f_str = formatera_polynom([(k, 'x'), (m, '')])
                elif func_type == 'kvadratisk':
                    k = random.choice([-3, -2, -1, 1, 2, 3])
                    m = random.randint(-10, 10)
                    svar = k*(a**2) + m
                    f_str = formatera_polynom([(k, 'x^2'), (m, '')])
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
                f_str = formatera_polynom([(k, 'x^2'), (m, '')])
                
                if abs(C) <= 300:
                    return {"info_text": "Givet funktionen:", "latex_text": f"f(x) = {f_str}", "fraga": f"Bestäm det positiva värdet på x om f(x) = {C}", "ratt_svar": x, "input_typ": "text", "svarstyp": "int", "undertext": "Lös gärna på papper och skriv in ditt svar."}
                    
            else: # Linjär
                b = random.choice([1, 1, 2, 3, 4]) 
                a_coeff = random.choice([-4, -3, -2, -1, 1, 2, 3, 4])
                if b > 1 and abs(a_coeff) % b == 0: continue
                m = random.randint(-15, 15)
                x = random.randint(-20, 20) * b 
                if b == 1:
                    C = a_coeff*x + m
                    f_str = formatera_polynom([(a_coeff, 'x'), (m, '')])
                else:
                    term_x = f"\\frac{{x}}{{{b}}}" if a_coeff == 1 else (f"-\\frac{{x}}{{{b}}}" if a_coeff == -1 else f"\\frac{{{a_coeff}x}}{{{b}}}")
                    C = int(round((a_coeff*x)/b + m))
                    m_str = f" + {m}" if m > 0 else (f" - {-m}" if m < 0 else "")
                    f_str = f"{term_x}{m_str}"
                
                if abs(x) <= 100 and abs(C) <= 100:
                    return {"info_text": "Givet funktionen:", "latex_text": f"f(x) = {f_str}", "fraga": f"Bestäm x om f(x) = {C}", "ratt_svar": x, "input_typ": "text", "svarstyp": "int", "undertext": "Lös gärna på papper och skriv in ditt svar."}
                    
        else: # Niva 2 
            def formatera_linjar(k, m):
                return formatera_polynom([(k, 'x'), (m, '')])

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
        return formatera_polynom([(k, 'x'), (m, '')])

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
        return formatera_polynom([(k2, 'x^2'), (k, 'x'), (m, '')])

    while True:
        if niva == 1:
            typ = random.choice(['minus_parentes', 'mult_parentes', 'konstant_parentes', 'faktorisera', 'forhallande_blanda', 'forhallande_forenkla'])
            
            if typ == 'forhallande_blanda':
                A, B = random.randint(1, 3), random.randint(2, 5)
                if A == B: B += 1
                k = random.randint(2, 6)
                saft, vatten = A * k, B * k
                total = saft + vatten
                fraga_vatten = random.choice([True, False])
                info = f"Du ska blanda saft och vatten i förhållandet {A}:{B}. Du häller i {saft} dl koncentrerad saft."
                if fraga_vatten:
                    fraga = "Hur många deciliter (dl) vatten ska du blanda med?"
                    svar = vatten
                else:
                    fraga = "Hur många deciliter (dl) färdigblandad saft får du totalt?"
                    svar = total
                return {"info_box_blue": info, "fraga": fraga, "ratt_svar": svar, "input_typ": "text", "svarstyp": "int", "suffix": "dl", "undertext": "Svara med ett heltal."}
                
            elif typ == 'forhallande_forenkla':
                A, B = random.randint(2, 6), random.randint(2, 6)
                while math.gcd(A, B) != 1 or A == B:
                    A, B = random.randint(2, 6), random.randint(2, 6)
                k = random.randint(3, 8)
                killar, tjejer = A * k, B * k
                if random.choice([True, False]):
                    info = f"I en klass finns det {killar} killar och {tjejer} tjejer."
                    fraga = "Vilket är förhållandet mellan antalet killar och tjejer?"
                else:
                    info = f"I en fruktskål ligger {killar} äpplen och {tjejer} päron."
                    fraga = "Vilket är förhållandet mellan antalet äpplen och päron?"
                return {"info_box_blue": info, "fraga": fraga, "ratt_svar": f"{A}:{B}", "input_typ": "text", "svarstyp": "ratio", "undertext": "Svara på enklaste form med ett kolon (t.ex. 2:3)."}
                
            elif typ == 'minus_parentes':
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
            typ = random.choice(['faktorisera_avancerat', 'mult_parentes_koeff', 'flersteg', 'rationell', 'likhet_parentes', 'forhallande_dela_total', 'forhallande_tre_parter'])
            
            if typ == 'forhallande_dela_total':
                A, B = random.randint(2, 7), random.randint(2, 7)
                while math.gcd(A, B) != 1 or A == B:
                    A, B = random.randint(2, 7), random.randint(2, 7)
                k = random.choice([50, 100, 200, 500])
                total = (A + B) * k
                info = f"Två personer ska dela på {total} kr i förhållandet {A}:{B} (den första får {A} delar, den andra får {B} delar)."
                if random.choice([True, False]):
                    fraga = "Hur många kronor får den som får den STÖRSTA andelen?"
                    svar = max(A, B) * k
                else:
                    fraga = "Hur många kronor får den som får den MINSTA andelen?"
                    svar = min(A, B) * k
                return {"info_box_blue": info, "fraga": fraga, "ratt_svar": svar, "input_typ": "text", "svarstyp": "int", "suffix": "kr", "undertext": "Svara med ett heltal."}

            elif typ == 'forhallande_tre_parter':
                A, B, C = random.randint(1, 4), random.randint(1, 4), random.randint(1, 4)
                while A == B and B == C:
                    C = random.randint(1, 4)
                k = random.randint(3, 8)
                
                recept_typ = random.choice(['marinad', 'betong'])
                if recept_typ == 'marinad':
                    info = f"Ett recept på marinad anger förhållandet mellan olja, soja och vinäger till {A}:{B}:{C}. Du gör en stor sats och använder {A*k} msk olja."
                    delar = [('soja', B*k), ('vinäger', C*k)]
                    vald_del = random.choice(delar)
                    fraga = f"Hur många matskedar {vald_del[0]} ska du använda?"
                    suffix = "msk"
                else:
                    info = f"För att blanda en viss sorts betong är förhållandet mellan cement, grus och sand {A}:{B}:{C}. Du använder {A*k} kg cement."
                    delar = [('grus', B*k), ('sand', C*k)]
                    vald_del = random.choice(delar)
                    fraga = f"Hur många kg {vald_del[0]} ska du använda?"
                    suffix = "kg"
                return {"info_box_blue": info, "fraga": fraga, "ratt_svar": vald_del[1], "input_typ": "text", "svarstyp": "int", "suffix": suffix, "undertext": "Svara med ett heltal."}

            elif typ == 'likhet_parentes':
                while True:
                    A = random.choice([2, 3, 4, 5])
                    D = random.choice([2, 3, 4, 5])
                    if A == D: continue
                    
                    E = random.choice([-5, -4, -3, -2, 2, 3, 4, 5])
                    F = random.choice([-10, -9, -8, -7, -6, -5, -4, -3, -2, 2, 3, 4, 5, 6, 7, 8, 9, 10])
                    
                    if (D * E) % A == 0 and (D * F) % A == 0:
                        B = (D * E) // A
                        C = (D * F) // A
                        break
                        
                VL = f"{A}({formatera_polynom([(B, 'x'), (C, '')])})"
                HL = f"{D}( \dots )"
                alg_uttryck_str = f"{VL} = {HL}"
                svar_ratt = formatera_polynom([(E, 'x'), (F, '')])
                
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
    
    if niva == 1:
        typ = random.choice(['arsranta', 'manadsranta', 'rak_amortering', 'kalkylblad_varde', 'kalkylblad_formel'])
        if typ == 'arsranta':
            kapital, ranta = random.choice([15000, 20000, 35000, 50000, 80000, 150000]), random.choice([3, 4, 5, 6, 7, 8])
            return {"info_box_blue": f"Du lånar {formatera_kr(kapital)} kr av banken med en årsränta på {ranta} %.", "fraga": "Hur mycket får du betala i ränta under det första året? (Svara i kr)", "ratt_svar": int(round(kapital * (ranta / 100))), "input_typ": "text", "svarstyp": "int", "suffix": "kr"}
        elif typ == 'manadsranta':
            kapital, ranta = random.choice([12000, 24000, 36000, 60000, 120000]), random.choice([3, 4, 5, 6, 7, 8])
            return {"info_box_blue": f"Du tar ett lån på {formatera_kr(kapital)} kr. Årsräntan är {ranta} %.", "fraga": "Hur stor blir räntekostnaden för den allra första månaden? (Svara i kr)", "ratt_svar": int(round((kapital * (ranta / 100)) / 12)), "input_typ": "text", "svarstyp": "int", "suffix": "kr"}
        elif typ == 'rak_amortering':
            ar, amort = random.choice([2, 3, 4, 5, 10]), random.choice([500, 1000, 1500, 2000, 2500])
            return {"info_box_blue": f"Du lånar {formatera_kr(amort * ar * 12)} kr som ska betalas tillbaka med rak amortering under {ar} år.", "fraga": "Hur mycket ska du amortera varje månad? (Svara i kr)", "ratt_svar": amort, "input_typ": "text", "svarstyp": "int", "suffix": "kr"}
        elif typ in ['kalkylblad_varde', 'kalkylblad_formel']:
            kapital = random.choice([60000, 120000, 240000])
            ranta = random.choice([3, 4, 5, 6])
            amort = random.choice([1000, 2000, 3000])
            manadsranta_kr = int(round(kapital * (ranta / 100) / 12))
            
            tabell_html = f"""
            <div style="overflow-x: auto; margin-top: 10px; margin-bottom: 20px;">
                <table style="width: 100%; border-collapse: collapse; font-family: sans-serif; font-size: 14px; background-color: white; border: 1px solid #ccc;">
                    <thead>
                        <tr style="background-color: #f1f3f4; border-bottom: 2px solid #ccc;">
                            <th style="padding: 8px; border: 1px solid #ccc; width: 40px;"></th>
                            <th style="padding: 8px; border: 1px solid #ccc; text-align: center; color: #333;">A</th>
                            <th style="padding: 8px; border: 1px solid #ccc; text-align: center; color: #333;">B</th>
                            <th style="padding: 8px; border: 1px solid #ccc; text-align: center; color: #333;">C</th>
                            <th style="padding: 8px; border: 1px solid #ccc; text-align: center; color: #333;">D</th>
                            <th style="padding: 8px; border: 1px solid #ccc; text-align: center; color: #333;">E</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <th style="background-color: #f1f3f4; padding: 8px; border: 1px solid #ccc; text-align: center; color: #333;">1</th>
                            <td style="padding: 8px; border: 1px solid #ccc; font-weight: bold; text-align: center;">Lånebelopp</td>
                            <td style="padding: 8px; border: 1px solid #ccc; font-weight: bold; text-align: center;">Räntesats</td>
                            <td style="padding: 8px; border: 1px solid #ccc; font-weight: bold; text-align: center;">Räntekostnad<br>/mån</td>
                            <td style="padding: 8px; border: 1px solid #ccc; font-weight: bold; text-align: center;">Amortering</td>
                            <td style="padding: 8px; border: 1px solid #ccc; font-weight: bold; text-align: center;">Månads-<br>kostnad</td>
                        </tr>
                        <tr>
                            <th style="background-color: #f1f3f4; padding: 8px; border: 1px solid #ccc; text-align: center; color: #333;">2</th>
                            <td style="padding: 8px; border: 1px solid #ccc; text-align: center;">{formatera_kr(kapital)}</td>
                            <td style="padding: 8px; border: 1px solid #ccc; text-align: center;">{ranta} %</td>
                            <td style="padding: 8px; border: 1px solid #ccc; text-align: center; color: gray; font-style: italic;">[tom]</td>
                            <td style="padding: 8px; border: 1px solid #ccc; text-align: center;">{formatera_kr(amort)}</td>
                            <td style="padding: 8px; border: 1px solid #ccc; text-align: center; color: gray; font-style: italic;">[tom]</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            """
            
            subtyp = random.choice(['C2', 'E2'])
            
            if typ == 'kalkylblad_varde':
                if subtyp == 'C2':
                    return {
                        "info_box_blue": "Titta på kalkylarket nedan:",
                        "html_table": tabell_html,
                        "fraga": "I cell C2 skriver du in formeln: `=A2*B2/12`. Vilket värde kommer att visas i cell C2 när du trycker på Enter? (Svara i kr)",
                        "ratt_svar": manadsranta_kr,
                        "input_typ": "text",
                        "svarstyp": "int",
                        "suffix": "kr"
                    }
                else:
                    return {
                        "info_box_blue": f"Titta på kalkylarket nedan. Tänk dig att du redan har räknat ut att räntekostnaden i cell C2 blev {formatera_kr(manadsranta_kr)} kr.",
                        "html_table": tabell_html,
                        "fraga": "I cell E2 skriver du in formeln: `=C2+D2`. Vilket värde kommer att visas i cell E2? (Svara i kr)",
                        "ratt_svar": manadsranta_kr + amort,
                        "input_typ": "text",
                        "svarstyp": "int",
                        "suffix": "kr"
                    }
            else: # formel
                if subtyp == 'C2':
                    return {
                        "info_box_blue": "Titta på kalkylarket nedan:",
                        "html_table": tabell_html,
                        "fraga": "Vilken formel ska du skriva in i cell C2 för att kalkylarket ska räkna ut räntekostnaden för en månad?",
                        "ratt_svar_lista": [
                            '=a2*b2/12', '=b2*a2/12', '=a2*(b2/100)/12', '=(a2*b2)/12',
                            '=a2/12*b2', '=b2/12*a2', '=a2*b2/100/12', '=(a2*b2/100)/12',
                            '=b2*a2/100/12', '=a2*(b2/12)', '=(a2/12)*b2', '=(b2/12)*a2'
                        ],
                        "ratt_svar_visning": "=A2*B2/12",
                        "ratt_svar": "=A2*B2/12",
                        "input_typ": "text",
                        "svarstyp": "kalkyl_formel"
                    }
                else:
                    return {
                        "info_box_blue": "Titta på kalkylarket nedan:",
                        "html_table": tabell_html,
                        "fraga": "Vilken formel ska du skriva in i cell E2 för att kalkylarket ska räkna ut den totala månadskostnaden?",
                        "ratt_svar_lista": ['=c2+d2', '=d2+c2'],
                        "ratt_svar_visning": "=C2+D2",
                        "ratt_svar": "=C2+D2",
                        "input_typ": "text",
                        "svarstyp": "kalkyl_formel"
                    }
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
        typ = random.choice(['berakna_ff', 'nytt_pris', 'hitta_procent', 'index_berakna', 'index_nytt_varde', 'index_procentuell_forandring'])
        
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
            
        elif typ == 'index_berakna':
            P0 = random.choice([50, 100, 200, 250, 400, 500])
            idx_val = random.choice([110, 120, 125, 130, 140, 150])
            P1 = int(P0 * idx_val / 100)
            info = f"Ett basår kostade en specifik vara {P0} kr. Några år senare kostar samma vara {P1} kr."
            return {"info_box_green": info, "fraga": "Vilket index har varan det senare året? (Svara med ett heltal)", "ratt_svar": idx_val, "input_typ": "text", "svarstyp": "int"}
            
        elif typ == 'index_nytt_varde':
            P0 = random.choice([100, 200, 500, 1000, 2000, 5000])
            idx_val = random.choice([112, 115, 120, 130, 140, 150])
            P1 = int(P0 * idx_val / 100)
            info = f"En vara kostade {P0} kr under basåret (då index alltid är 100). Ett senare år är index för varan {idx_val}."
            return {"info_box_green": info, "fraga": "Vad kostar varan det senare året? (Svara i kr)", "ratt_svar": P1, "input_typ": "text", "svarstyp": "int", "suffix": "kr"}
            
        elif typ == 'index_procentuell_forandring':
            ans = random.choice(range(5, 155, 5)) 
            i1 = random.randint(5, 15) * 20 
            i2 = int(round(i1 * (1 + ans / 100.0)))
            info = f"Index för en viss vara var {i1} år 1 och {i2} år 2."
            return {"info_box_green": info, "fraga": "Med hur många procent ökade priset från år 1 till år 2?", "ratt_svar": ans, "input_typ": "text", "svarstyp": "procent"}
            
    else:
        typ = random.choice(['hitta_gammalt', 'upprepad_procent', 'index_byta_basar', 'index_reallon'])
        
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
            
        elif typ == 'index_byta_basar':
            komb = [(120, 144, 120), (120, 150, 125), (125, 150, 120), (140, 168, 120), (150, 180, 120), (150, 195, 130)]
            old_i2, old_i3, new_i3 = random.choice(komb)
            info = f"I en indextabell är index 100 för år 1, {old_i2} för år 2, och {old_i3} för år 3. Man bestämmer sig sedan för att byta basår till år 2."
            return {"info_box_green": info, "fraga": "Vilket index får år 3 i den nya tabellen?", "ratt_svar": new_i3, "input_typ": "text", "svarstyp": "int"}
            
        elif typ == 'index_reallon':
            kpi = random.choice([110, 120, 125, 140, 150])
            lon_faktor = random.choice([1.05, 1.1, 1.15, 1.2])
            base_lon = random.choice([20000, 25000, 30000, 35000])
            new_lon = int(base_lon * (kpi/100) * lon_faktor)
            reallon = int(new_lon / (kpi / 100))
            info = f"År 1 är KPI 100 och din månadslön är {base_lon} kr. År 2 är KPI {kpi} och din lön har ökat till {new_lon} kr."
            return {"info_box_green": info, "fraga": "Vad är din lön år 2 omräknad till penningvärdet för år 1 (så kallad reallön)?", "ratt_svar": reallon, "input_typ": "text", "svarstyp": "int", "suffix": "kr"}

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
        # DYNAMISK LOGIK: Slumpa mellan 4 olika scenarier (alltid 95 % konfidensgrad)
        scenario = random.choice(['minska_fm', 'öka_n_effekt', 'minska_n_effekt', 'jamfora_tva_n'])
        fm = round(random.uniform(3.0, 5.0), 1)
        
        if scenario == 'minska_fm':
            ratt = "Fråga betydligt fler personer i nästa undersökning."
            alts = [ratt, "Fråga färre personer så att risken för felräkning minskar.", "Bara fråga personer som de vet är insatta i ämnet.", "Ställa frågan på ett annat sätt så att fler svarar ja."]
            info = f"En tidning publicerar en opinionsundersökning men tycker att felmarginalen på ±{f'{fm:g}'.replace('.', ',')} procentenheter gör resultatet för osäkert. De vill ha ett snävare (mindre) konfidensintervall nästa månad."
            fraga = "Vad är det bästa sättet för dem att minska felmarginalen rent statistiskt?"
            
        elif scenario == 'öka_n_effekt':
            ratt = "Felmarginalen minskar och intervallet blir snävare."
            alts = [ratt, "Felmarginalen ökar och intervallet blir bredare.", "Felmarginalen påverkas inte alls av antalet tillfrågade.", "Resultatet i själva stickprovet ändras."]
            info = "Ett undersökningsföretag brukar fråga 1 000 personer i sina mätningar. Till nästa mätning bestämmer de sig för att ställa samma fråga till 3 000 personer istället. Båda beräknas med 95 % konfidensgrad."
            fraga = "Vad händer med felmarginalen när de ökar antalet tillfrågade på detta sätt?"
            
        elif scenario == 'minska_n_effekt':
            ratt = "Felmarginalen ökar (intervallet blir bredare)."
            alts = [ratt, "Felmarginalen minskar (intervallet blir snävare).", "Felmarginalen påverkas inte, så länge det är exakt samma fråga.", "Undersökningen blir helt ogiltig och kan inte användas alls."]
            info = "En forskare skickar ut en enkät till 2 000 personer, men får en väldigt låg svarsfrekvens och bara 400 personer svarar. Hon beräknar ett 95 % konfidensintervall baserat på de 400 svaren."
            fraga = "Hur blir felmarginalen nu, jämfört med om alla 2 000 hade svarat?"
            
        elif scenario == 'jamfora_tva_n':
            ratt = "Undersökning A har en större felmarginal än Undersökning B."
            alts = [ratt, "Undersökning B har en större felmarginal än Undersökning A.", "De har exakt samma felmarginal eftersom båda har 95 % konfidensgrad.", "Det går inte att säga vilken felmarginal som är störst utan att veta vad folk svarade."]
            info = "Två olika tidningar gör varsin undersökning om samma sak. Båda använder 95 % konfidensgrad. Undersökning A frågar 500 slumpmässigt valda personer. Undersökning B frågar 2 500 slumpmässigt valda personer."
            fraga = "Vilket påstående om undersökningarnas felmarginal är sant?"

        random.shuffle(alts)
        return {"info_box_purple": info, "fraga": fraga, "ratt_svar": ratt, "alternativ": alts, "input_typ": "radio", "svarstyp": "string"}
        
    elif typ == 'konf_falskt':
        resultat, fm = random.randint(55, 75), random.randint(2, 4)
        ratt = f"Mellan {resultat - fm} % och {resultat + fm} % av eleverna *som tillfrågades* vill ha längre raster."
        alts = [ratt, f"Det sanna värdet för hela skolan ligger med 95 % säkerhet mellan {resultat - fm} % och {resultat + fm} %.", f"I det faktiska stickprovet svarade exakt {resultat} % att de vill ha längre raster.", "Även om intervallet är brett, finns det en risk att det sanna värdet ligger utanför intervallet."]
        random.shuffle(alts)
        return {"info_box_purple": f"En undersökning visar att {resultat} % av eleverna på en stor skola vill ha längre raster. Undersökningen har en felmarginal på ±{fm} procentenheter vid 95 % konfidensgrad.", "fraga": "Vilket av följande påståenden är FALSKT (felaktigt)?", "ratt_svar": ratt, "alternativ": alts, "input_typ": "radio", "svarstyp": "string"}

def skapa_problemlosning_uppgift(niva):
    namn_lista = ["Charlie", "Kim", "Ali", "Maja", "Sami", "Robin", "Nilo", "Alex", "Noa", "Elsa", "Viktor"]
    
    if niva == 1:
        typ = random.choice([
            'hyra_fordon', 'vardeminskning', 'pannkakor_proportion', 'valuta_omvandling', 
            'jamfora_abonnemang', 'vattenlackage', 'upprepad_procent_rea', 
            'enhetsomvandling_regn', 'formel_kokpunkt', 'enkel_tidszon_resa'
        ])
        
        if typ == 'hyra_fordon':
            namn = random.choice(namn_lista)
            fordon = random.choice(["bil", "minibuss", "skåpbil", "husbil"])
            start = random.randint(3, 10) * 100
            mil_kost = random.randint(2, 6) * 10
            
            ratt = f"y = {mil_kost}x + {start}"
            alt1 = f"y = {start}x + {mil_kost}"
            alt2 = f"y = {mil_kost} + x + {start}"
            alt3 = f"y = {mil_kost}x + {start}x"
            
            alts = [f"${ratt}$", f"${alt1}$", f"${alt2}$", f"${alt3}$"]
            random.shuffle(alts)
            
            info = f"{namn} ska hyra en {fordon}. Startavgiften är {start} kr. Dessutom kostar det {mil_kost} kr för varje mil hen kör."
            return {
                "info_box_blue": info,
                "fraga": "Vilken formel beskriver den totala kostnaden y kr för x mil som körs?",
                "ratt_svar": f"${ratt}$",
                "alternativ": alts,
                "input_typ": "radio",
                "svarstyp": "string",
                "undertext": "Lös uppgiften med huvudräkning (utan miniräknare)."
            }
            
        elif typ == 'vardeminskning':
            fordon = random.choice(["bil", "båt", "husvagn", "traktor", "motorcykel"])
            pris = random.randint(15, 60) * 10000
            procent = random.randint(10, 25)
            ff = round((100 - procent) / 100.0, 2)
            
            info = f"En {fordon} kostar {formatera_kr(pris)} kr i inköpspris. Värdet minskar med {procent} % per år."
            
            return {
                "info_box_blue": info,
                "fraga": "Skriv ett uttryck som beskriver värdet i kronor x år efter inköp.",
                "ratt_svar": f"{pris}*{ff}**x",
                "input_typ": "text",
                "svarstyp": "string_math",
                "undertext": "Ange uttrycket med x som variabel och ^ för upphöjt till (t.ex. 500*0,8^x).\nLös uppgiften med huvudräkning (utan miniräknare)."
            }
            
        elif typ == 'pannkakor_proportion':
            kombinationer = [
                (4, 200, 6),   # 200 / 2 * 3 = 300
                (6, 300, 4),   # 300 / 3 * 2 = 200
                (8, 400, 6),   # 400 / 4 * 3 = 300
                (6, 400, 9),   # 400 / 2 * 3 = 600
                (10, 500, 15), # 500 / 2 * 3 = 750
                (4, 200, 10),  # 200 / 2 * 5 = 500
                (6, 150, 10)   # 150 / 3 * 5 = 250
            ]
            personer_start, mjol, personer_mal = random.choice(kombinationer)
            svar = int((mjol / personer_start) * personer_mal)
            
            info = f"Ett recept för {personer_start} portioner kräver {mjol} gram mjöl."
            return {
                "info_box_blue": info,
                "fraga": f"Hur mycket mjöl krävs om man ska laga {personer_mal} portioner?",
                "ratt_svar": svar,
                "input_typ": "text",
                "svarstyp": "int",
                "suffix": "gram",
                "undertext": "Lös uppgiften med huvudräkning (utan miniräknare)."
            }
            
        elif typ == 'valuta_omvandling':
            namn1, namn2 = random.sample(namn_lista, 2)
            valuta_kombos = [
                ("thailändska baht", "THB", 750, 3000, 500, 2000),
                ("danska kronor", "DKK", 600, 400, 900, 600),
                ("euro", "EUR", 800, 80, 600, 60),
                ("amerikanska dollar", "USD", 1500, 150, 1000, 100),
                ("brittiska pund", "GBP", 1200, 100, 900, 75),
                ("tjeckiska koruna", "CZK", 400, 1000, 600, 1500),
                ("japanska yen", "JPY", 600, 8000, 900, 12000)
            ]
            valuta_namn, valuta_kod, sek_A, val_A, sek_B, val_B = random.choice(valuta_kombos)
            
            info = f"{namn1} växlar {sek_A} kr till {valuta_namn} ({valuta_kod}) och får {formatera_kr(val_A)} {valuta_kod}.<br><br>{namn2} växlar {sek_B} kr till samma kurs."
            return {
                "info_box_blue": info,
                "fraga": f"Hur mycket får {namn2}?",
                "ratt_svar": val_B,
                "input_typ": "text",
                "svarstyp": "int",
                "suffix": valuta_kod,
                "undertext": "Lös uppgiften med huvudräkning (utan miniräknare)."
            }

        elif typ == 'enkel_tidszon_resa':
            resmal_lista = [
                {"stad": "London", "bas_tim": 2, "bas_min": 30, "tidsskillnad": -1},
                {"stad": "New York", "bas_tim": 8, "bas_min": 30, "tidsskillnad": -6},
                {"stad": "Tokyo", "bas_tim": 13, "bas_min": 20, "tidsskillnad": 8},
                {"stad": "Bangkok", "bas_tim": 11, "bas_min": 0, "tidsskillnad": 6},
                {"stad": "Dubai", "bas_tim": 6, "bas_min": 10, "tidsskillnad": 3}
            ]

            destination = random.choice(resmal_lista)
            avresa_h = random.randint(6, 22)
            avresa_m = random.choice([0, 10, 20, 30, 40, 50])

            extra_min = random.choice([-20, -10, 0, 10, 20, 30])
            total_restid_m = destination["bas_tim"] * 60 + destination["bas_min"] + extra_min

            restid_h = total_restid_m // 60
            restid_m_rest = total_restid_m % 60

            start_minuter = avresa_h * 60 + avresa_m
            ankomst_svensk_tid = start_minuter + total_restid_m
            ankomst_lokal_tid = ankomst_svensk_tid + (destination["tidsskillnad"] * 60)
            ankomst_lokal_tid = ankomst_lokal_tid % (24 * 60)

            ankomst_h = ankomst_lokal_tid // 60
            ankomst_m = ankomst_lokal_tid % 60

            avresa_str = f"{avresa_h:02d}:{avresa_m:02d}"
            restid_str = f"{restid_h}h {restid_m_rest}min"
            
            if destination['tidsskillnad'] > 0:
                diff_str = f"+{destination['tidsskillnad']}h"
            else:
                diff_str = f"{destination['tidsskillnad']}h"

            info = f"Du reser från Stockholm kl. {avresa_str} och resan till {destination['stad']} tar {restid_str}."
            fraga = f"Vad är klockan lokalt i {destination['stad']} när du landar om tidsskillnaden är {diff_str}? (Svara i formatet HH:MM)"
            svar = f"{ankomst_h:02d}:{ankomst_m:02d}"

            return {
                "info_box_blue": info,
                "fraga": fraga,
                "ratt_svar": svar,
                "input_typ": "text",
                "svarstyp": "string",
                "undertext": "Svara med klockslag i formatet HH:MM (till exempel 08:30 eller 15:00)."
            }

        elif typ == 'jamfora_abonnemang':
            R_B = random.choice([30, 40, 50])
            R_A = R_B + random.choice([20, 30, 40])
            visits = random.choice([4, 5, 6, 8, 10])
            F_A = random.choice([100, 150, 200, 250])
            F_B = F_A + visits * (R_A - R_B)
            
            info = f"Du funderar på att skaffa gymkort.<br><br>&bull; <b>Gym A</b> tar {F_A} kr i fast månadsavgift och sedan {R_A} kr per träningspass.<br>&bull; <b>Gym B</b> tar {F_B} kr i fast månadsavgift och sedan {R_B} kr per träningspass."
            return {
                "info_box_blue": info,
                "fraga": "Vid exakt hur många träningspass under en månad kostar de båda gymmen lika mycket?",
                "ratt_svar": visits,
                "input_typ": "text",
                "svarstyp": "int",
                "suffix": "pass",
                "undertext": "Lös uppgiften på papper (utan miniräknare)."
            }

        elif typ == 'vattenlackage':
            start_vol = random.randint(10, 50) * 10
            leak = random.randint(2, 8)
            info = f"En vattentunna innehåller från början {start_vol} liter vatten. Det har gått hål i botten och tunnan läcker därefter {leak} liter per minut."
            return {
                "info_box_blue": info,
                "fraga": "Skriv ett algebraiskt uttryck för volymen vatten (i liter) som finns kvar i tunnan efter t minuter.",
                "ratt_svar": f"{start_vol} - {leak}*t",
                "input_typ": "text",
                "svarstyp": "string_math",
                "undertext": "Använd t som variabel. Lös uppgiften med huvudräkning (utan miniräknare)."
            }

        elif typ == 'upprepad_procent_rea':
            rea1 = random.choice([20, 30, 40])
            rea2 = random.choice([10, 20, 25])
            rabatt_total = 100 - 100 * (1 - rea1/100.0) * (1 - rea2/100.0)
            
            info = f"En klädbutik har en stor utförsäljning med {rea1} % rabatt på alla varor i butiken. Eftersom du är VIP-medlem får du dessutom ytterligare {rea2} % rabatt i kassan på det redan sänkta priset."
            return {
                "info_box_blue": info,
                "fraga": "Hur stor blir den TOTALA rabatten i procent från varans ursprungspris?",
                "ratt_svar": int(round(rabatt_total)),
                "input_typ": "text",
                "svarstyp": "procent",
                "suffix": "%",
                "undertext": "Lös uppgiften med huvudräkning (utan miniräknare)."
            }

        elif typ == 'enhetsomvandling_regn':
            area = random.choice([50, 100, 150, 200, 500])
            regn = random.choice([2, 5, 8, 10, 12, 15])
            svar = area * regn
            info = f"Ett kraftigt regnoväder drar in och det faller {regn} mm regn över ett platt tak som har arean {area} m²."
            return {
                "info_box_blue": info,
                "fraga": "Hur många liter vatten har det fallit på taket?",
                "ratt_svar": svar,
                "input_typ": "text",
                "svarstyp": "int",
                "suffix": "liter",
                "undertext": "Lös uppgiften med huvudräkning (utan miniräknare)."
            }

        elif typ == 'formel_kokpunkt':
            fraga_typ = random.choice(['hitta_t', 'hitta_h'])
            if fraga_typ == 'hitta_t':
                h = random.choice([1500, 3000, 4500, 6000])
                t = int(100 - h / 300)
                info = f"Vattnets kokpunkt <i>t</i> (i °C) beror på höjden över havet <i>h</i> (i meter) enligt formeln:<br><br><b>t = 100 - h/300</b><br><br>Du befinner dig på ett berg på {formatera_kr(h)} meters höjd."
                fraga = "Vid vilken temperatur kokar vattnet där du är?"
                svar = t
                suffix = "°C"
            else:
                t = random.choice([80, 85, 90, 95])
                h = (100 - t) * 300
                info = f"Vattnets kokpunkt <i>t</i> (i °C) beror på höjden över havet <i>h</i> (i meter) enligt formeln:<br><br><b>t = 100 - h/300</b><br><br>Du kokar vatten uppe på ett berg och märker att det börjar koka redan vid {t} °C."
                fraga = "På ungefär vilken höjd över havet befinner du dig?"
                svar = h
                suffix = "meter"
                
            return {
                "info_box_blue": info,
                "fraga": fraga,
                "ratt_svar": svar,
                "input_typ": "text",
                "svarstyp": "int",
                "suffix": suffix,
                "undertext": "Lös uppgiften med huvudräkning (utan miniräknare)."
            }

    else: # Nivå 2
        typ = random.choice([
            'pizza_brak', 'algebraisk_forstaelse', 'monster_stickor', 'tolka_uttryck_rabatt', 
            'tidsvinst_hastighet', 'area_uttryck', 'medelfart', 'relativ_procent', 'valgorenhet'
        ])
        
        if typ == 'pizza_brak':
            namn1, namn2 = random.sample(namn_lista, 2)
            A_den = random.choice([3, 4, 5])
            B_den = random.choice([2, 3])
            
            kvar_1 = Fraction(1, 1) - Fraction(1, A_den)
            ata_2 = Fraction(1, B_den) * kvar_1
            kvar_total = kvar_1 - ata_2
            
            info = f"{namn1} och {namn2} köper en stor pizza tillsammans. {namn1} äter upp 1/{A_den} av hela pizzan. Senare äter {namn2} upp 1/{B_den} av det som är kvar."
            return {
                "info_box_blue": info,
                "fraga": "Hur stor andel av HELA pizzan finns sedan kvar?",
                "ratt_svar": kvar_total,
                "input_typ": "text",
                "svarstyp": "fraction",
                "undertext": "Lös uppgiften med huvudräkning (utan miniräknare).\nSvara i bråkform med ett snedstreck (t.ex. 3/8)."
            }
            
        elif typ == 'algebraisk_forstaelse':
            namn1, namn2 = random.sample(namn_lista, 2)
            proc_okning = random.choice([15, 20, 25, 30, 40])
            dec_okning = round(proc_okning / 100.0, 2)
            
            info = f"{namn1} väger <i>a</i> kg och {namn2} väger <i>b</i> kg. Du vet att följande samband gäller:<br><br><b>a + {str(dec_okning).replace('.', ',')}a = b</b>"
            
            ratt1 = f"{namn2} väger {proc_okning} % mer än {namn1}"
            ratt2 = f"{namn2}s vikt är {str(round(1+dec_okning, 2)).replace('.', ',')} gånger {namn1}s vikt"
            
            fel1 = f"{namn1} väger {proc_okning} % mer än {namn2}"
            fel2 = f"{namn1} väger {str(dec_okning).replace('.', ',')} kg mer än {namn2}"
            fel3 = f"{namn2} väger {str(dec_okning).replace('.', ',')} kg mer än {namn1}"
            fel4 = f"{namn1}s vikt är {str(round(1+dec_okning, 2)).replace('.', ',')} gånger {namn2}s vikt"
            
            valt_ratt = random.choice([ratt1, ratt2])
            alts_visning = random.sample([valt_ratt, fel1, random.choice([fel2, fel3]), fel4], 4)
            
            return {
                "info_box_blue": info,
                "fraga": "Vilket av följande alternativ stämmer alltid?",
                "ratt_svar": valt_ratt,
                "alternativ": alts_visning,
                "input_typ": "radio",
                "svarstyp": "string",
                "undertext": "Lös uppgiften med huvudräkning (utan miniräknare)."
            }
            
        elif typ == 'monster_stickor':
            k = random.randint(2, 5)
            m = random.randint(1, 4)
            f1, f2, f3 = k*1 + m, k*2 + m, k*3 + m
            
            info = f"Ett mönster byggs med tändstickor.<br><br>&bull; Figur 1 består av {f1} stickor.<br>&bull; Figur 2 består av {f2} stickor.<br>&bull; Figur 3 består av {f3} stickor."
            svar_ratt = f"{k}*n + {m}"
            
            return {
                "info_box_blue": info,
                "fraga": "Skriv ett generellt algebraiskt uttryck för antalet stickor i figur n.",
                "ratt_svar": svar_ratt,
                "input_typ": "text",
                "svarstyp": "string_math",
                "undertext": "Lös uppgiften med huvudräkning (utan miniräknare).\nAnvänd n som variabel. Svara med ett uttryck, till exempel 6n + 2."
            }
            
        elif typ == 'tolka_uttryck_rabatt':
            engangs = random.randint(5, 8) * 10 - 1
            klipp = engangs * 10 - random.randint(10, 20) * 10
            
            varianter = [
                (f"(10 &middot; {engangs} - {klipp}) / 10", "Hur mycket man i snitt sparar per badtillfälle med rabattkortet."),
                (f"{klipp} / 10", "Vad ett bad kostar per gång med rabattkortet."),
                (f"10 &middot; {engangs} - {klipp}", "Hur mycket rabatt man får totalt för alla 10 gånger."),
                (f"{klipp} / {engangs}", "Hur många gånger man måste bada för att tjäna in rabattkortet.")
            ]
            valt_uttryck, ratt_svar_text = random.choice(varianter)
            
            info = f"I simhallen kostar en engångsentré {engangs} kr. Man kan också köpa ett rabattkort för 10 gånger som kostar {klipp} kr.<br><br>En person beräknar följande:<br><b>{valt_uttryck}</b>"
            alts = [v[1] for v in varianter]
            random.shuffle(alts)
            
            return {
                "info_box_blue": info,
                "fraga": "Förklara vad personen har beräknat genom att välja rätt svarsalternativ.",
                "ratt_svar": ratt_svar_text,
                "alternativ": alts,
                "input_typ": "radio",
                "svarstyp": "string",
                "undertext": "Läs uttrycket noggrant och fundera på vad uträkningen faktiskt ger för svar.<br>Lös uppgiften med huvudräkning (utan miniräknare)."
            }

        elif typ == 'tidsvinst_hastighet':
            combos = [
                (30, 60, 90, 10), (40, 80, 120, 10), (60, 90, 120, 10),
                (20, 60, 80, 5), (10, 40, 60, 5)
            ]
            s, v1, v2, t = random.choice(combos)
            info = f"I en tidningsartikel presenteras en formel för att beräkna tidsskillnaden <i>t</i> (i minuter) om man kör en viss sträcka <i>s</i> (i km) med två olika hastigheter:<br><br><b>t = (1/v<sub>1</sub> - 1/v<sub>2</sub>) &middot; s &middot; 60</b><br><br>Du brukar köra till jobbet med hastigheten {v1} km/h, men funderar på hur mycket tid du tjänar på att istället köra {v2} km/h. Sträckan till jobbet är {s} km."
            return {
                "info_box_blue": info,
                "fraga": "Hur många minuter tjänar du på att köra i den snabbare hastigheten?",
                "ratt_svar": t,
                "input_typ": "text",
                "svarstyp": "int",
                "suffix": "min",
                "undertext": "Sätt in siffrorna i formeln och räkna. Lös uppgiften med papper och penna."
            }

        elif typ == 'area_uttryck':
            L = random.randint(2, 6) * 10
            info = f"En bonde ska bygga en rektangulär hage till sina djur. Hagen ska byggas mot en lång, rak ladugårdsvägg, så bonden behöver bara bygga staket på tre av sidorna. Bonden har totalt {L} meter staket att använda.<br><br>Sidorna som är vinkelräta (går rakt ut) från väggen kallas för <i>x</i>."
            
            ratt = f"x({L} - 2x)"
            alt1 = f"x({L} - x)"
            alt2 = f"x(2x - {L})"
            alt3 = f"x(\\frac{{{L}}}{{2}} - x)"
            alts = [f"${ratt}$", f"${alt1}$", f"${alt2}$", f"${alt3}$"]
            random.shuffle(alts)
            
            return {
                "info_box_blue": info,
                "fraga": "Vilket av följande uttryck beskriver hagens area (i kvadratmeter) beroende på x?",
                "ratt_svar": f"${ratt}$",
                "alternativ": alts,
                "input_typ": "radio",
                "svarstyp": "string",
                "undertext": "Börja gärna med att rita en figur på papper."
            }
            
        elif typ == 'medelfart':
            s = random.choice([30, 60, 120])
            v1 = random.choice([20, 30, 40, 60])
            v2 = random.choice([10, 15, 20, 30])
            
            # Vi vill ha olika hastigheter och en snygg division
            while v1 <= v2 or (s % v1 != 0) or (s % v2 != 0):
                v1 = random.choice([20, 30, 40, 60])
                v2 = random.choice([10, 15, 20, 30])
            
            t1 = s / v1
            t2 = s / v2
            tot_s = 2 * s
            tot_t = t1 + t2
            medelfart = int(tot_s / tot_t)
            
            namn = random.choice(namn_lista)
            fordon = random.choice(['cyklar', 'kör moped', 'kör elsparkcykel'])
            info = f"{namn} {fordon} till en ort som ligger {s} km bort. På ditvägen är medelhastigheten {v1} km/h. På hemvägen är det motvind och medelhastigheten blir bara {v2} km/h."
            
            return {
                "info_box_blue": info,
                "fraga": "Vad är medelhastigheten för HELA resan (dit och hem)?",
                "ratt_svar": medelfart,
                "input_typ": "text",
                "svarstyp": "int",
                "suffix": "km/h",
                "undertext": "Lös gärna med huvudräkning."
            }

        elif typ == 'relativ_procent':
            namn1, namn2, namn3 = random.sample(namn_lista, 3)
            # Fasta snygga procentkombinationer som ger jämna svar
            combos = [
                (40, 20, 75),  # 140 / 80 = 1.75 (+75%)
                (50, 25, 100), # 150 / 75 = 2.0 (+100%)
                (20, 40, 100), # 120 / 60 = 2.0 (+100%)
                (80, 10, 100), # 180 / 90 = 2.0 (+100%)
                (10, 45, 100)  # 110 / 55 = 2.0 (+100%)
            ]
            p_mer, p_mindre, p_svar = random.choice(combos)
            sak = random.choice(['vinner pengar i ett lotteri', 'får lön för ett sommarjobb', 'säljer jultidningar'])
            
            info = f"Tre vänner {sak}.<br><br>&bull; {namn1} får {p_mer} % <b>mer</b> än {namn2}.<br>&bull; {namn3} får {p_mindre} % <b>mindre</b> än {namn2}."
            
            return {
                "info_box_blue": info,
                "fraga": f"Hur många procent MER får {namn1} jämfört med {namn3}?",
                "ratt_svar": p_svar,
                "input_typ": "text",
                "svarstyp": "int",
                "suffix": "%",
                "undertext": "Lös med huvudräkning."
            }

        elif typ == 'valgorenhet':
            pop_milj = random.choice([5, 10, 20])
            items = random.choice([50000, 100000, 200000])
            price = random.choice([200, 400, 500])
            effektivitet = random.choice([80, 50])
            
            total_items_cost = items * price
            total_needed = total_items_cost / (effektivitet / 100.0)
            per_person = int(total_needed / (pop_milj * 1000000))
            
            sak = random.choice(['nödpaket', 'vaccindoser', 'varma filtar'])
            info = f"I ett land med {pop_milj} miljoner invånare startas en insamling för att köpa {formatera_kr(items)} {sak}. Varje styck kostar {price} kr.<br><br>På grund av administrativa kostnader går dock bara {effektivitet} % av de insamlade pengarna till själva inköpen (resten försvinner på vägen)."
            
            return {
                "info_box_blue": info,
                "fraga": "Hur mycket måste varje invånare i landet i genomsnitt skänka för att målet ska nås?",
                "ratt_svar": per_person,
                "input_typ": "text",
                "svarstyp": "int",
                "suffix": "kr",
                "undertext": "Lös gärna med papper och penna."
            }

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
    "Statistik": skapa_stat_uppgift,
    "Problemlösning": skapa_problemlosning_uppgift
}

TITLAR = {
    "Funktioner: Grafisk lösning": "Grafisk avläsning av funktioner",
    "Funktioner: Algebraisk lösning": "Algebraisk lösning av funktioner",
    "Ekvationer": "Lös ekvationerna",
    "Algebra": "Algebra & Förhållanden",
    "Lån och ränta": "Beräkna Lån och Ränta",
    "Förändringsfaktor": "Träna på Förändringsfaktor",
    "Sannolikhetslära": "Träna på Sannolikhetslära",
    "Statistik": "Tolka Statistik och Diagram",
    "Problemlösning": "Problemlösning & Lästal",
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
        if niva == 2:
            tillgangliga_kategorier.remove("Statistik")
            
        valbar_kat = random.choice(tillgangliga_kategorier)
        u = KATEGORIER[valbar_kat](niva)
        u['visnings_kategori'] = valbar_kat 
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
        
    if u.get('plotly_fig') is not None:
        st.plotly_chart(u['plotly_fig'], use_container_width=True, config={'displayModeBar': False})

    if 'info_text' in u:
        st.markdown(f"<div style='text-align: center; font-size: 20px; color: gray; margin-top: 50px;'>{u['info_text']}</div>", unsafe_allow_html=True)
    if 'latex_text' in u:
        st.latex(u['latex_text'])
    
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
        
    if 'html_table' in u:
        st.write("")
        st.markdown(u['html_table'], unsafe_allow_html=True)

with col_hoger:
    st.subheader("Uppgift")
    if 'undertext' in u:
        st.markdown(f"<p style='font-size: 14px; font-style: italic; color: #666; margin-bottom: 5px;'>{u['undertext'].replace(chr(10), '<br>')}</p>", unsafe_allow_html=True)
        
    q_color = "#0056b3"
    if u['visnings_kategori'] == "Förändringsfaktor": q_color = "#28a745"
    elif u['visnings_kategori'] == "Sannolikhetslära": q_color = "#e83e8c"
    elif u['visnings_kategori'] == "Statistik": q_color = "#8B008B"
    elif u['visnings_kategori'] == "Problemlösning": q_color = "#d35400"
    
    if u['visnings_kategori'] == "Ekvationer":
        st.markdown("<div style='font-size: 32px; font-weight: bold; color: transparent; margin-bottom: 25px;'>&nbsp;</div>", unsafe_allow_html=True) 
    else:
        st.markdown(f"<div style='font-size: 26px; font-weight: bold; color: {q_color}; margin-bottom: 25px;'>{u['fraga']}</div>", unsafe_allow_html=True)
    
    uid = st.session_state.uppgift_id
    rattat = st.session_state.get('rattat', False)
    status = st.session_state.get('svar_status', None)

    if rattat and status == 'ratt':
        st.success("✅ Helt rätt! Snyggt jobbat.")
        if st.button("Nästa uppgift", type="primary", use_container_width=True, key=f"next_{uid}"):
            generera_ny_uppgift()
            st.rerun()
    else:
        # Om eleven inte svarat rätt än, visa svarsformuläret
        with st.form(key=f"form_{uid}"):
            input_svar = None
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
            submit_btn = st.form_submit_button("Rätta svar", use_container_width=True)
            
            # Vid klick eller Enter
            if submit_btn:
                st.session_state.rattat = True
                st.session_state.svar_status = ratta_svar(u, input_svar)
                st.rerun()

        # Feedback för fel och format visas under formuläret
        if rattat and status != 'ratt':
            if status == 'fel':
                if u['svarstyp'] == 'array_float':
                    ratt_txt = ' och '.join([f"{a:g}".replace('.', ',') for a in u['ratt_svar']])
                elif u['svarstyp'] == 'fraction':
                    ratt_txt = f"{u['ratt_svar'].numerator}/{u['ratt_svar'].denominator}"
                elif u['svarstyp'] in ['float', 'procent']:
                    ratt_txt = f"{float(u['ratt_svar']):g}".replace('.', ',')
                elif u['svarstyp'] == 'kalkyl_formel':
                    ratt_txt = u['ratt_svar_visning']
                elif u['svarstyp'] == 'string_math':
                    ratt_txt = str(u['ratt_svar']).replace("**", "^").replace("*", " \cdot ")
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
                elif u['svarstyp'] == 'string_math':
                    st.warning("⚠️ Ditt uttryck är tyvärr felaktigt formaterat och kan inte rättas matematiskt.")
                else:
                    st.warning("⚠️ Svaret är i fel format.")
            elif status == 'format_ratio':
                st.warning("⚠️ Svara med ett kolon mellan siffrorna, till exempel 3:4.")
            elif status == 'format_saknar_likamed':
                st.warning("⚠️ Formler i kalkylark måste alltid börja med ett likamedstecken (=).")
            elif status == 'tom':
                if u['input_typ'] in ['radio', 'selectbox']:
                    st.warning("Vänligen välj ett alternativ i listan.")
                else:
                    st.warning("Vänligen fyll i ett svar innan du rättar.")
            
            # En "hoppa över"-knapp om de tröttnar på att gissa
            st.write("")
            if st.button("Hoppa över / Nästa uppgift", use_container_width=True, key=f"skip_{uid}"):
                generera_ny_uppgift()
                st.rerun()
