import random
import streamlit as st
from models import Uppgift
from utils import visa_infobox, hantera_svar
from graphics import rita_plotly_graf, rita_traddiagram, rita_stat_graf
from generators import (
    skapa_graf_uppgift,
    skapa_alg_func_uppgift,
    skapa_ekv_uppgift,
    skapa_alg_uttryck,
    skapa_lan,
    skapa_ff,
    skapa_index,
    skapa_slump,
    skapa_stat_uppgift,
    skapa_procent,
    skapa_problemlosning,
)

# --- Ställ in sidans layout till bred ---
st.set_page_config(layout="wide", page_title="Matematikträning Ma1a")

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
# KATEGORIER OCH TITLAR
# ==========================================
KATEGORIER = {
    "Funktioner: Grafisk lösning": skapa_graf_uppgift,
    "Funktioner: Algebraisk lösning": skapa_alg_func_uppgift,
    "Ekvationer": skapa_ekv_uppgift,
    "Algebra": skapa_alg_uttryck,
    "Lån och ränta": skapa_lan,
    "Förändringsfaktor": skapa_ff,
    "Index": skapa_index,
    "Sannolikhetslära": skapa_slump,
    "Statistik": skapa_stat_uppgift,
    "Procent vs Procentenheter": skapa_procent,
    "Problemlösning": skapa_problemlosning,
}

TITLAR = {
    "Funktioner: Grafisk lösning": "Grafisk avläsning av funktioner",
    "Funktioner: Algebraisk lösning": "Algebraisk lösning av funktioner",
    "Ekvationer": "Lös ekvationerna",
    "Algebra": "Algebra & Förhållanden",
    "Lån och ränta": "Beräkna Lån och Ränta",
    "Förändringsfaktor": "Träna på Förändringsfaktor",
    "Index": "Index och Prisutveckling",
    "Sannolikhetslära": "Träna på Sannolikhetslära",
    "Statistik": "Tolka Statistik och Diagram",
    "Procent vs Procentenheter": "Procent och Procentenheter",
    "Problemlösning": "Problemlösning & Lästal",
    "Träning till halvkursprov": "Träning inför halvkursprov",
    "Blandat (Slumpas)": "Blandade uppgifter - Träna på allt!",
}


def generera_ny_uppgift():
    st.session_state.rattat = False
    st.session_state.svar_status = None
    st.session_state.uppgift_id = st.session_state.get("uppgift_id", 0) + 1

    kat = st.session_state.aktuell_kategori
    niva = st.session_state.niva

    if kat == "Blandat (Slumpas)":
        tillgangliga = list(KATEGORIER.keys())
        valbar_kat = random.choice(tillgangliga)
        u = KATEGORIER[valbar_kat](niva)
        if u is not None:
            u.visnings_kategori = valbar_kat

    elif kat == "Träning till halvkursprov":
        halvkursprov_kategorier = [
            "Ekvationer",
            "Algebra",
            "Lån och ränta",
            "Förändringsfaktor",
            "Index",
            "Procent vs Procentenheter",
        ]
        valbar_kat = random.choice(halvkursprov_kategorier)
        u = KATEGORIER[valbar_kat](niva)
        if u is not None:
            u.visnings_kategori = valbar_kat

    else:
        u = KATEGORIER[kat](niva)
        if u is not None:
            u.visnings_kategori = kat

    st.session_state.aktiv_uppgift = u


# ==========================================
# MENYSYSTEM (SIDOPANEL)
# ==========================================
st.sidebar.title("Välj Träningsläge")
vald_kategori = st.sidebar.radio(
    "Vad vill du träna på?",
    list(KATEGORIER.keys()) + ["Träning till halvkursprov", "Blandat (Slumpas)"],
)

if "aktuell_kategori" not in st.session_state or st.session_state.aktuell_kategori != vald_kategori:
    st.session_state.aktuell_kategori = vald_kategori
    st.session_state.niva = 1
    generera_ny_uppgift()
    st.rerun()

st.sidebar.divider()
st.sidebar.subheader("Inställningar")
ny_niva = st.sidebar.radio(
    "Välj svårighetsgrad:",
    [1, 2],
    horizontal=True,
    index=st.session_state.niva - 1,
)

if ny_niva != st.session_state.niva:
    st.session_state.niva = ny_niva
    generera_ny_uppgift()
    st.rerun()


# ==========================================
# UNIVERSELL UI-RENDERING
# ==========================================
u: Uppgift = st.session_state.get("aktiv_uppgift")
st.title(TITLAR[st.session_state.aktuell_kategori])

if u is None:
    st.warning("Denna kategori saknar ännu uppgiftskod (kontrollera funktionen i generators/).")
    st.stop()

col_vanster, col_hoger = st.columns([1.2, 1], gap="large")

with col_vanster:
    # 1. Funktionsgraf
    if u.graf_f is not None:
        tx = [u.trace_x] if (st.session_state.rattat and u.trace_x is not None) else None
        ty = [u.trace_y] if (st.session_state.rattat and u.trace_y is not None) else None
        fig = rita_plotly_graf(
            f=u.graf_f,
            visa_facit=st.session_state.rattat,
            q_vis_type=u.q_type_vis,
            trace_x=tx,
            trace_y=ty,
            trace_alla_x=u.trace_alla_x,
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False}, theme=None)

    # 2. Färdigt Plotly-diagram (t.ex. kuber)
    if u.plotly_fig is not None:
        st.plotly_chart(u.plotly_fig, use_container_width=True, config={"displayModeBar": False}, theme=None)

    # 3. Statistik- eller träddiagram från extra_data
    if "stat_graf" in u.extra_data:
        fig_stat = rita_stat_graf(**u.extra_data["stat_graf"])
        st.plotly_chart(fig_stat, use_container_width=True, config={"displayModeBar": False}, theme=None)

    if u.extra_data.get("visa_traddiagram"):
        fig_trad = rita_traddiagram(
            grenar=[],
            farg1=u.extra_data.get("farg1", "#1f77b4"),
            farg2=u.extra_data.get("farg2", "#ff7f0e"),
        )
        st.plotly_chart(fig_trad, use_container_width=True, config={"displayModeBar": False}, theme=None)

    # 4. Text, LaTeX, Infobox och Tabell
    if u.info_text:
        st.markdown(
            f"<div style='text-align: center; font-size: 20px; color: gray; margin-top: 50px;'>{u.info_text}</div>",
            unsafe_allow_html=True,
        )
    if u.latex_text:
        st.latex(u.latex_text)

    if u.info_box_text and u.info_box_style:
        visa_infobox(u.info_box_text, u.info_box_style)

    if u.info_text_italic:
        st.markdown(
            f"<div style='font-size: 20px; font-style: italic; color: gray;'>{u.info_text_italic}</div>",
            unsafe_allow_html=True,
        )

    if u.html_table:
        st.write("")
        st.markdown(u.html_table, unsafe_allow_html=True)

with col_hoger:
    st.subheader("Uppgift")
    if u.undertext:
        st.markdown(
            f"<p style='font-size: 14px; font-style: italic; color: #666; margin-bottom: 5px;'>{u.undertext.replace(chr(10), '<br>')}</p>",
            unsafe_allow_html=True,
        )

    q_color = "#0056b3"
    if u.visnings_kategori == "Förändringsfaktor":
        q_color = "#28a745"
    elif u.visnings_kategori == "Sannolikhetslära":
        q_color = "#e83e8c"
    elif u.visnings_kategori == "Statistik":
        q_color = "#8B008B"
    elif u.visnings_kategori == "Problemlösning":
        q_color = "#d35400"

    if u.visnings_kategori == "Ekvationer":
        st.markdown(
            "<div style='font-size: 32px; font-weight: bold; color: transparent; margin-bottom: 25px;'>&nbsp;</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"<div style='font-size: 26px; font-weight: bold; color: {q_color}; margin-bottom: 25px;'>{u.fraga}</div>",
            unsafe_allow_html=True,
        )

    uid = st.session_state.uppgift_id
    rattat = st.session_state.get("rattat", False)
    status = st.session_state.get("svar_status", None)

    if rattat and status == "ratt":
        st.success("✅ Helt rätt! Snyggt jobbat.")
        if st.button("Nästa uppgift", type="primary", use_container_width=True, key=f"next_{uid}"):
            generera_ny_uppgift()
            st.rerun()
    else:
        with st.form(key=f"form_{uid}"):
            if u.input_typ == "flera_text":
                for i in range(len(u.ratt_svar)):
                    etikett = f"Svar {i + 1}:" if len(u.ratt_svar) > 1 else "Ditt svar:"
                    st.text_input(etikett, key=f"input_{uid}_{i}")
            elif u.input_typ == "text":
                st.text_input("Ditt svar:", key=f"input_single_{uid}")
            elif u.input_typ == "radio":
                st.radio(
                    "Alternativ:",
                    u.alternativ,
                    index=None,
                    label_visibility="collapsed",
                    key=f"input_single_{uid}",
                )
            elif u.input_typ == "selectbox":
                st.selectbox(
                    "Välj ett alternativ:",
                    u.alternativ,
                    index=0,
                    label_visibility="collapsed",
                    key=f"input_single_{uid}",
                )

            st.write("")
            st.form_submit_button("Rätta svar", use_container_width=True, on_click=hantera_svar)

        if rattat and status != "ratt":
            if status == "fel":
                if u.svarstyp == "array_float":
                    ratt_txt = " och ".join([f"{a:g}".replace(".", ",") for a in u.ratt_svar])
                elif u.svarstyp == "fraction" and hasattr(u.ratt_svar, "numerator"):
                    ratt_txt = f"{u.ratt_svar.numerator}/{u.ratt_svar.denominator}"
                elif u.svarstyp in ["float", "procent"]:
                    ratt_txt = f"{float(u.ratt_svar):g}".replace(".", ",")
                elif u.svarstyp == "kalkyl_formel":
                    ratt_txt = u.ratt_svar_visning
                elif u.svarstyp == "string_math":
                    ratt_txt = str(u.ratt_svar).replace("**", "^").replace("*", " · ")
                else:
                    ratt_txt = str(u.ratt_svar)

                if u.suffix:
                    ratt_txt += f"\xa0{u.suffix}"
                if u.svarstyp == "procent":
                    ratt_txt += "\xa0%"

                st.error(f"❌ Tyvärr fel. Rätt svar var:\n\n {ratt_txt}")

            elif status == "format":
                if u.svarstyp in ["float", "procent"]:
                    st.warning("⚠️ Svaret är i fel format (skriv bara siffror/decimaltal, t.ex. 1,25).")
                elif u.svarstyp == "int":
                    st.warning("⚠️ Svaret ska vara ett heltal.")
                elif u.svarstyp == "fraction":
                    st.warning("⚠️ Skriv svaret som ett bråk, till exempel 3/8.")
                elif u.svarstyp == "string_math":
                    st.warning("⚠️ Ditt uttryck är tyvärr felaktigt formaterat och kan inte rättas matematiskt.")
                else:
                    st.warning("⚠️ Svaret är i fel format.")
            elif status == "format_ratio":
                st.warning("⚠️ Svara med ett kolon mellan siffrorna, till exempel 3:4.")
            elif status == "format_saknar_likamed":
                st.warning("⚠️ Formler i kalkylark måste alltid börja med ett likamedstecken (=).")
            elif status == "tom":
                if u.input_typ in ["radio", "selectbox"]:
                    st.warning("Vänligen välj ett alternativ i listan.")
                else:
                    st.warning("Vänligen fyll i ett svar innan du rättar.")

            st.write("")
            if st.button("Hoppa över / Nästa uppgift", use_container_width=True, key=f"skip_{uid}"):
                generera_ny_uppgift()
                st.rerun()
