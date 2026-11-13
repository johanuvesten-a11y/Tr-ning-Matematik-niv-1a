import streamlit as st
from fractions import Fraction
import sympy as sp
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
)
from models import Uppgift


def formatera_polynom(termer):
    res = ""
    for koeff, var in termer:
        if koeff == 0:
            continue
        if var == "":
            term_str = str(abs(koeff))
        else:
            term_str = var if abs(koeff) == 1 else f"{abs(koeff)}{var}"

        if res == "":
            res += f"-{term_str}" if koeff < 0 else term_str
        else:
            res += f" - {term_str}" if koeff < 0 else f" + {term_str}"
    return res if res != "" else "0"


def formatera_kr(b):
    return f"{int(round(b)):,}".replace(",", "\xa0")


def visa_infobox(text: str, style: str):
    colors = {
        "blue": ("#0056b3", "#f8f9fa"),
        "green": ("#28a745", "#e9ecef"),
        "pink": ("#e83e8c", "#fce4ec"),
        "purple": ("#8B008B", "#f3e5f5"),
    }
    border_color, bg_color = colors.get(style, ("#333", "#f4f4f4"))
    st.markdown(
        f"<div style='font-size: 22px; font-weight: bold; color: #333; margin-top: 30px; "
        f"background-color: {bg_color}; padding: 25px; border-radius: 10px; "
        f"border-left: 6px solid {border_color};'>{text}</div>",
        unsafe_allow_html=True,
    )


def ratta_svar(u: Uppgift, input_svar) -> str:
    if u.input_typ == "flera_text":
        if all(s.strip() != "" for s in input_svar):
            try:
                anv_svar_float = sorted([round(float(s.strip().replace(",", ".")), 4) for s in input_svar])
                return "ratt" if anv_svar_float == u.ratt_svar else "fel"
            except ValueError:
                return "format"
        return "tom"

    elif u.input_typ == "text":
        if input_svar.strip() != "":
            try:
                if u.svarstyp == "int":
                    svar_clean = input_svar.strip().replace(" ", "").replace("\xa0", "")
                    return "ratt" if int(svar_clean) == u.ratt_svar else "fel"

                elif u.svarstyp in ["float", "procent"]:
                    svar_clean = (
                        input_svar.strip()
                        .replace(",", ".")
                        .replace(" ", "")
                        .replace("\xa0", "")
                        .replace("%", "")
                    )
                    return "ratt" if abs(float(svar_clean) - float(u.ratt_svar)) < 0.001 else "fel"

                elif u.svarstyp == "fraction":
                    svar_clean = input_svar.strip().replace(" ", "").replace("\xa0", "").replace(",", ".")
                    return "ratt" if Fraction(svar_clean) == Fraction(str(u.ratt_svar)) else "fel"

                elif u.svarstyp == "ratio":
                    svar_clean = input_svar.strip().replace(" ", "").replace("\xa0", "")
                    if ":" not in svar_clean:
                        return "format_ratio"
                    return "ratt" if svar_clean == str(u.ratt_svar) else "fel"

                elif u.svarstyp == "string_math":
                    svar_clean = input_svar.replace(",", ".").replace(" ", "").replace("\xa0", "").replace("^", "**")
                    try:
                        transformations = standard_transformations + (implicit_multiplication_application,)
                        expr_elev = parse_expr(svar_clean, transformations=transformations)
                        ratt_svar_str = str(u.ratt_svar).replace(" ", "").replace("^", "**")
                        expr_facit = parse_expr(ratt_svar_str, transformations=transformations)
                        return "ratt" if sp.simplify(expr_elev - expr_facit) == 0 else "fel"
                    except Exception:
                        return "format"

                elif u.svarstyp == "kalkyl_formel":
                    svar_clean = input_svar.strip().replace(" ", "").replace("\xa0", "").lower()
                    if not svar_clean.startswith("="):
                        return "format_saknar_likamed"
                    godkanda = [s.lower() for s in (u.ratt_svar_lista or [])]
                    return "ratt" if svar_clean in godkanda else "fel"

                elif u.svarstyp == "string":
                    svar_clean = str(input_svar).strip()
                    return "ratt" if svar_clean.lower() == str(u.ratt_svar).strip().lower() else "fel"
            except ValueError:
                return "format"
        return "tom"

    elif u.input_typ in ["radio", "selectbox"]:
        if input_svar is not None and input_svar != "Välj svar...":
            return "ratt" if str(input_svar).strip() == str(u.ratt_svar).strip() else "fel"
        return "tom"

    return "fel"


def hantera_svar():
    st.session_state.rattat = True
    u = st.session_state.aktiv_uppgift
    uid = st.session_state.uppgift_id

    if u.input_typ == "flera_text":
        input_svar = [st.session_state.get(f"input_{uid}_{i}", "") for i in range(len(u.ratt_svar))]
    else:
        input_svar = st.session_state.get(f"input_single_{uid}")
        if input_svar is None:
            input_svar = "Välj svar..." if u.input_typ == "selectbox" else ""

    st.session_state.svar_status = ratta_svar(u, input_svar)
