import streamlit as st
from fractions import Fraction
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
from models import Uppgift

def formatera_polynom(termer):
    """Formaterar en lista med termer till ett snyggt polynom som en sträng."""
    if not termer:
        return "0"
    res = str(termer[0])
    for term in termer[1:]:
        if str(term).startswith("-"):
            res += f" - {str(term)[1:]}"
        else:
            res += f" + {term}"
    return res

def formatera_kr(b):
    """Formaterar belopp till ett snyggt format med tusentalsavskiljare (mellanslag)."""
    return f"{b:,.0f}".replace(",", " ")

def visa_infobox(text: str, style: str = "info"):
    """Visar en formaterad infobox (t.ex. för lösningar eller tips)."""
    farger = {
        "info": "#e7f3fe",
        "success": "#d4edda",
        "warning": "#fff3cd",
        "error": "#f8d7da"
    }
    bg_color = farger.get(style, "#f8f9fa")
    st.markdown(
        f'<div style="background-color: {bg_color}; padding: 10px; border-radius: 5px; margin-bottom: 10px;">{text}</div>',
        unsafe_allow_html=True
    )

def ratta_svar(u: Uppgift, input_svar: any) -> str:
    """Rättar svaret baserat på uppgiftens svarstyp och det förväntade svaret."""
    # Hantera tomma inmatningar
    if input_svar is None or input_svar == "":
        return "fel"
        
    svarstyp = u.svarstyp
    ratt = u.ratt_svar

    try:
        if svarstyp == "string_math":
            # Använd Sympy för att utvärdera om två algebraiska uttryck är ekvivalenta
            transformations = (standard_transformations + (implicit_multiplication_application,))
            expr_input = parse_expr(str(input_svar).replace(",", "."), transformations=transformations)
            expr_ratt = parse_expr(str(ratt).replace(",", "."), transformations=transformations)
            if sp.simplify(expr_input - expr_ratt) == 0:
                return "ratt"
            else:
                return "fel"
                
        elif svarstyp == "fraction":
            # Hantera bråktal
            in_frac = Fraction(str(input_svar).replace(",", ".").strip())
            ratt_frac = Fraction(str(ratt).strip())
            if in_frac == ratt_frac:
                return "ratt"
            else:
                return "fel"
                
        elif svarstyp == "float":
            # Tolerans för flyttal
            in_float = float(str(input_svar).replace(",", ".").strip())
            ratt_float = float(ratt)
            if abs(in_float - ratt_float) < 1e-5:
                return "ratt"
            else:
                return "fel"
                
        else: # "string", "int", "flerval", etc.
            if str(input_svar).strip().lower() == str(ratt).strip().lower():
                return "ratt"
            else:
                return "fel"
    except Exception:
        # Fångar upp formateringsfel från användaren (t.ex. bokstäver i ett fält för bråktal)
        return "fel"

def hantera_svar():
    """Hämtar inmatat värde och sätter rättningsstatus i session_state."""
    if 'current_input' in st.session_state and 'aktuell_uppgift' in st.session_state:
        inmatning = st.session_state.current_input
        u = st.session_state.aktuell_uppgift
        
        status = ratta_svar(u, inmatning)
        st.session_state.svar_status = status
        st.session_state.senaste_svar = inmatning
