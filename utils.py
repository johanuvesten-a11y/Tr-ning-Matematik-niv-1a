import math
import re
import streamlit as st
from sympy import simplify, expand, SympifyError
from sympy.parsing.sympy_parser import (
    parse_expr, 
    standard_transformations, 
    implicit_multiplication_application, 
    convert_xor
)

def visa_infobox(text: str, style: str):
    """
    Renderar en snygg informationsruta i Streamlit.
    style kan vara 'info', 'warning', eller 'success'.
    """
    colors = {
        "info": {"bg": "#e7f3fe", "border": "#b3d4fc", "icon": "ℹ️"},
        "warning": {"bg": "#fff3cd", "border": "#ffeeba", "icon": "⚠️"},
        "success": {"bg": "#d4edda", "border": "#c3e6cb", "icon": "✅"}
    }
    c = colors.get(style, colors["info"])
    
    html = f"""
    <div style="background-color: {c['bg']}; border-left: 5px solid {c['border']}; padding: 15px; margin: 10px 0; border-radius: 5px;">
        <strong>{c['icon']} Info:</strong><br>{text}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def formatera_polynom(termer):
    """
    Hjälpfunktion för att bygga snygga matematiska uttryck som strängar.
    Förväntar sig en lista med tupler: [(koefficient, "variabel")], t.ex. [(1, "x^2"), (-3, "x"), (2, "")]
    """
    uttryck = []
    for i, (c, v) in enumerate(termer):
        if c == 0:
            continue
            
        if i == 0:
            tecken = "-" if c < 0 else ""
            c_abs = abs(c)
        else:
            tecken = " - " if c < 0 else " + "
            c_abs = abs(c)
            
        if c_abs == 1 and v != "":
            uttryck.append(f"{tecken}{v}")
        else:
            uttryck.append(f"{tecken}{c_abs}{v}")
            
    res = "".join(uttryck)
    return res if res else "0"

def ratta_svar(u, input_svar):
    """
    Huvudfunktion för att rätta elevens svar baserat på svarstypen i Uppgift-objektet.
    Returnerar 'ratt', 'fel', 'tom', 'format', 'format_saknar_x', 'format_saknar_y' eller 'ej_forenklad'.
    """
    if not input_svar:
        return 'tom'
        
    if isinstance(input_svar, list):
        if any(not s or str(s).strip() == "" for s in input_svar):
            return 'tom'
    elif isinstance(input_svar, str) and input_svar.strip() == "":
        return 'tom'

    typ = u.svarstyp

    # --- Hantera svar med flera fält (listor) ---
    if typ in ['ekvationssystem', 'punkt', 'ordered_float']:
        try:
            svar = [float(s.replace(',', '.').replace(' ', '')) for s in input_svar]
            if len(svar) == len(u.ratt_svar):
                for s, r in zip(svar, u.ratt_svar):
                    if not math.isclose(s, r, abs_tol=u.tolerans):
                        return 'fel'
                return 'ratt'
            return 'fel'
        except ValueError:
            return 'format'

    # --- Hantera text/strängfält ---
    if isinstance(input_svar, str):
        svar_clean = str(input_svar).replace(',', '.').strip()
        
        # Enkla strängar
        if typ == 'string':
            return 'ratt' if svar_clean.lower() == str(u.ratt_svar).lower() else 'fel'
            
        # Numeriska värden
        if typ in ['float', 'int', 'procent']:
            try:
                val = float(svar_clean.replace('%', ''))
                if math.isclose(val, float(u.ratt_svar), abs_tol=u.tolerans):
                    return 'ratt'
                return 'fel'
            except ValueError:
                return 'format'
                
        # Flera flyttal i samma textruta (t.ex. "2 och 4")
        if typ == 'array_float':
            try:
                svar_parts = [float(p.strip()) for p in re.split(r'[,;\s]+(?:och\s+)?', svar_clean) if p.strip()]
                if len(svar_parts) != len(u.ratt_svar): 
                    return 'fel'
                    
                svar_parts.sort()
                ratt_sort = sorted(u.ratt_svar)
                for s, r in zip(svar_parts, ratt_sort):
                    if not math.isclose(s, float(r), abs_tol=u.tolerans): 
                        return 'fel'
                return 'ratt'
            except ValueError:
                return 'format'

        # --- Matematiska uttryck via SymPy ---
        if typ in ['string_math', 'ekvation_x', 'ekvation_linje', 'faktoriserad']:
            
            # Formatkrav för symmetrilinjer
            if typ == 'ekvation_x':
                if not svar_clean.startswith('x='):
                    svar_clean_test = svar_clean.replace(' ', '')
                    if svar_clean_test.startswith('x='):
                        svar_clean = svar_clean_test
                    elif '=' in svar_clean_test and svar_clean_test.split('=')[0] == 'x':
                        svar_clean = svar_clean_test
                    else:
                        return 'format_saknar_x'
                svar_clean = svar_clean.replace('x=', '').strip()
                    
            # Formatkrav för linjens ekvation
            if typ == 'ekvation_linje':
                if not svar_clean.replace(' ', '').startswith('y='):
                    return 'format_saknar_y'
                svar_clean = svar_clean.replace(' ', '').replace('y=', '').strip()
                     
            # Begränsning mot onödiga parenteser
            if u.krav_inga_parenteser:
                if '(' in svar_clean or ')' in svar_clean:
                    return 'ej_forenklad'
                    
            transformations = (standard_transformations + (implicit_multiplication_application, convert_xor))
            
            try:
                expr_elev = parse_expr(svar_clean, transformations=transformations)
                
                # Rensa y= från rättningsnyckeln om det finns
                ratt_str = str(u.ratt_svar).replace('y=', '').replace('x=', '').strip()
                expr_ratt = parse_expr(ratt_str, transformations=transformations)
                
                if typ == 'faktoriserad':
                    if expand(expr_elev) == expand(expr_ratt):
                        return 'ratt'
                    return 'fel'

                diff = simplify(expr_elev - expr_ratt)
                if diff == 0:
                    return 'ratt'
                return 'fel'
                
            except (SympifyError, ValueError, TypeError):
                return 'format'
                
    # Fallback om inga andra villkor uppfylls
    if input_svar == u.ratt_svar:
        return 'ratt'
    return 'fel'
