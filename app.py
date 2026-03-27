import streamlit as st
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import numpy as np
import random

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

# --- MENYSYSTEM ---
st.sidebar.title("Välj Träningsläge")
vald_kategori = st.sidebar.radio("Vad vill du träna på?", [
    "Funktioner: Grafisk lösning",
    "Funktioner: Algebraisk lösning",
    "Ekvationer",
    "Algebra",
    "Blandat (Slumpas)"
])

# Rensa minnet om man byter kategori i menyn
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

    def ny_uppgift():
        if 'fraga_nr' not in st.session_state:
            st.session_state.fraga_nr = 1
        else:
            st.session_state.fraga_nr += 1
            
        niva = st.session_state.get('niva', 1)
        st.session_state.submitted_ans = False
        st.session_state.svar_status = None
            
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
                    
                    if op == '+':
                        svar = p1[1] + p2[1]
                    else:
                        svar = p1[1] - p2[1]
                        
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

        st.session_state.f = f
        st.session_state.fraga = fraga.replace('.', ',')
        st.session_state.ratt_svar = [round(ans, 4) + 0.0 for ans in ratt_svar]

    if 'niva' not in st.session_state:
        st.session_state.niva = 1
    if 'fraga_nr' not in st.session_state:
        ny_uppgift()
    if 'submitted_ans' not in st.session_state:
        st.session_state.submitted_ans = False
    if 'svar_status' not in st.session_state:
        st.session_state.svar_status = None

    st.title("Grafisk avläsning av funktioner")

    col_graf, col_kontroller = st.columns([1.2, 1], gap="large")

    with col_graf:
        fig, ax = plt.subplots(figsize=(5, 5))
        x_plot = np.linspace(-10, 10, 400)
        y_plot = st.session_state.f(x_plot)

        ax.plot(x_plot, y_plot, linewidth=1.5, color='blue')

        ax.grid(True, which='both', linestyle='-', linewidth=0.5, color='gray', alpha=0.5)
        
        ax.spines['left'].set_position('zero')
        ax.spines['left'].set_linewidth(2.0) 
        ax.spines['left'].set_color('black') 

        ax.spines['bottom'].set_position('zero')
        ax.spines['bottom'].set_linewidth(2.0) 
        ax.spines['bottom'].set_color('black') 
        
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')

        ticks = np.arange(-10, 11, 1)
        labels = [str(x) if x in [-10, -5, 5, 10] else '' for x in ticks]
        
        ax.set_xticks(ticks)
        ax.set_xticklabels(labels)
        ax.set_yticks(ticks)
        ax.set_yticklabels(labels)
        
        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)
        ax.set_aspect('equal')

        ax.text(10.2, 0, 'x', va='center', ha='left', fontsize=12, fontweight='bold')
        ax.text(0, 10.2, 'y', va='bottom', ha='center', fontsize=12, fontweight='bold')

        if st.session_state.submitted_ans:
            q_vis_type = st.session_state.get('q_type_vis', 'vis_none')
            
            if q_vis_type == 'vis_find_y':
                tx = st.session_state.trace_x
                ty = st.session_state.trace_y
                ax.plot([tx, tx], [0, ty], linestyle='--', color='red', linewidth=1.2, alpha=0.7)
                ax.plot([tx, 0], [ty, ty], linestyle='--', color='red', linewidth=1.2, alpha=0.7)
                ax.plot(tx, ty, 'ro', markersize=6)
                
            elif q_vis_type == 'vis_find_x':
                ty = st.session_state.trace_y
                ax_list = st.session_state.trace_alla_x
                if ax_list:
                    min_ax = min(ax_list + [0])
                    max_ax = max(ax_list + [0])
                    ax.plot([min_ax, max_ax], [ty, ty], linestyle='--', color='red', linewidth=1.2, alpha=0.7)
                    
                    for ax_v in ax_list:
                        ax.plot([ax_v, ax_v], [ty, 0], linestyle='--', color='red', linewidth=1.2, alpha=0.7)
                        ax.plot(ax_v, ty, 'ro', markersize=6)

        st.pyplot(fig)
        plt.close(fig) 

    with col_kontroller:
        st.subheader("Inställningar")
        aktuellt_index = 0 if st.session_state.niva == 1 else 1
        ny_niva = st.radio("Välj svårighetsgrad:", [1, 2], horizontal=True, index=aktuellt_index, key="graf_niva_val")
        
        if ny_niva != st.session_state.niva:
            st.session_state.niva = ny_niva
            ny_uppgift()
            st.rerun()
            
        st.divider() 
        st.subheader("Uppgift")
        st.markdown(f"<div style='font-size: 32px; font-weight: bold; color: #0056b3; margin-bottom: 20px;'>{st.session_state.fraga}</div>", unsafe_allow_html=True)
        
        antal_svar = len(st.session_state.ratt_svar)
        svar_lista = []
        
        for i in range(antal_svar):
            etikett = f"Svar {i+1}:" if antal_svar > 1 else "Skriv ditt svar här:"
            nyckel = f"input_{st.session_state.fraga_nr}_{i}"
            svar = st.text_input(etikett, key=nyckel)
            svar_lista.append(svar)
            
        st.write("") 
        
        knapp_col1, knapp_col2 = st.columns(2)
        with knapp_col1:
            rattat = st.button("Rätta svar", type="primary", use_container_width=True)
        with knapp_col2:
            ny_graf = st.button("Ny graf", use_container_width=True)
            
        if ny_graf:
            ny_uppgift()
            st.rerun()
            
        if rattat:
            st.session_state.submitted_ans = True
            if all(s.strip() != "" for s in svar_lista):
                try:
                    anv_svar_float = [round(float(s.strip().replace(',', '.')), 4) for s in svar_lista]
                    if sorted(anv_svar_float) == st.session_state.ratt_svar:
                        st.session_state.svar_status = 'ratt'
                    else:
                        st.session_state.svar_status = 'fel'
                except ValueError:
                    st.session_state.svar_status = 'varning_format'
            else:
                st.session_state.svar_status = 'varning_tom'
            st.rerun()

        if st.session_state.submitted_ans:
            if st.session_state.svar_status == 'ratt':
                st.success("✅ Helt rätt! Snyggt jobbat.")
            elif st.session_state.svar_status == 'fel':
                svar_str = ' och '.join([f"{a:g}".replace('.', ',') for a in st.session_state.ratt_svar])
                st.error(f"❌ Tyvärr fel. Rätt svar var: {svar_str}")
            elif st.session_state.svar_status == 'varning_format':
                st.warning("⚠️ Ange bara siffror (t.ex. 2, -3, eller 1,5).")
            elif st.session_state.svar_status == 'varning_tom':
                st.warning("Fyll i alla rutor innan du rättar.")

# ==========================================
# PLACEHOLDERS FÖR ÖVRIGA LÄGEN
# ==========================================
elif vald_kategori == "Funktioner: Algebraisk lösning":
    st.title("Algebraisk lösning av funktioner")
    
    # --- Funktion för att generera uppgifter ---
    def ny_algebra_uppgift():
        niva = st.session_state.get('alg_niva', 1)
        st.session_state.alg_rattat = False
        st.session_state.alg_status = None
        
        # Det smarta sättet att tömma rutan: Vi uppdaterar ett ID varje gång!
        st.session_state.alg_uppgift_nr = st.session_state.get('alg_uppgift_nr', 0) + 1
            
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
                    else: # exponential
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
                        
                else: # f(x) = C (Bara linjära, bråk okej)
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
                        
            else: # Niva 2: Sammansatta funktioner (bara linjära)
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

    # --- Initiera variabler ---
    if 'alg_niva' not in st.session_state:
        st.session_state.alg_niva = 1
    if 'alg_uppgift_nr' not in st.session_state:
        st.session_state.alg_uppgift_nr = 0
    if 'alg_fraga' not in st.session_state:
        ny_algebra_uppgift()

    # --- UI för modulen ---
    col_uppgift, col_installningar = st.columns([1.5, 1], gap="large")
    
    with col_installningar:
        st.subheader("Inställningar")
        aktuellt_index = 0 if st.session_state.alg_niva == 1 else 1
        ny_niva = st.radio("Välj svårighetsgrad:", [1, 2], horizontal=True, index=aktuellt_index, key="alg_niva_val")
        if ny_niva != st.session_state.alg_niva:
            st.session_state.alg_niva = ny_niva
            ny_algebra_uppgift()
            st.rerun()
            
    with col_uppgift:
        st.markdown("<div style='text-align: center; font-size: 20px; color: gray;'>Givet funktionen:</div>", unsafe_allow_html=True)
        
        st.latex(f"f(x) = {st.session_state.alg_funktion}")
        
        st.markdown(f"<div style='text-align: center; font-size: 32px; color: #0056b3; margin-bottom: 25px;'>{st.session_state.alg_fraga}</div>", unsafe_allow_html=True)
        
        # Här använder vi det nya unika ID:t så att rutan alltid börjar tom för en ny uppgift!
        unik_key = f"alg_input_{st.session_state.alg_uppgift_nr}"
        svar = st.text_input("Skriv in ditt svar (heltal):", key=unik_key)
        
        k1, k2 = st.columns(2)
        with k1:
            if st.button("Rätta svar", type="primary", use_container_width=True, key="alg_ratta"):
                st.session_state.alg_rattat = True
                if svar.strip() != "":
                    try:
                        anv_svar = int(svar.strip())
                        if anv_svar == st.session_state.alg_svar:
                            st.session_state.alg_status = 'ratt'
                        else:
                            st.session_state.alg_status = 'fel'
                    except ValueError:
                        st.session_state.alg_status = 'format'
                else:
                    st.session_state.alg_status = 'tom'
        with k2:
            if st.button("Ny uppgift", use_container_width=True, key="alg_ny"):
                ny_algebra_uppgift()
                st.rerun()

        if st.session_state.get('alg_rattat', False):
            if st.session_state.alg_status == 'ratt':
                st.success("✅ Helt rätt! Bra jobbat.")
            elif st.session_state.alg_status == 'fel':
                st.error(f"❌ Tyvärr fel. Rätt svar var: {st.session_state.alg_svar}")
            elif st.session_state.alg_status == 'format':
                st.warning("⚠️ Svaret ska vara ett heltal (t.ex. 5 eller -3).")
            elif st.session_state.alg_status == 'tom':
                st.warning("Skriv in ett svar först.")
                
elif vald_kategori == "Ekvationer":
    st.title("Lös ekvationerna")
    
    # --- Funktion för att generera ekvationer ---
    def ny_ekvation():
        niva = st.session_state.get('ekv_niva', 1)
        st.session_state.ekv_rattat = False
        st.session_state.ekv_status = None
        
        # Uppdaterar ID för att tömma svarsrutan säkert
        st.session_state.ekv_uppgift_nr = st.session_state.get('ekv_uppgift_nr', 0) + 1
        
        while True:
            # Vi bestämmer svaret (x) först, så det alltid blir ett heltal!
            x = random.randint(-10, 10)
            
            def formatera_sida(k, m):
                if k == 1: k_str = "x"
                elif k == -1: k_str = "-x"
                else: k_str = f"{k}x"
                
                if m > 0: return f"{k_str} + {m}"
                elif m < 0: return f"{k_str} - {-m}"
                else: return k_str

            if niva == 1:
                # Nivå 1: ax + b = cx + d
                a = random.choice([-5, -4, -3, -2, 2, 3, 4, 5])
                c = random.choice([-5, -4, -3, -2, 2, 3, 4, 5])
                if a == c: continue # x-termerna får inte ta ut varandra
                
                b = random.randint(-20, 20)
                # Räkna ut vad d måste vara för att vårt x ska stämma: a*x + b = c*x + d
                d = a*x + b - c*x
                
                VL = formatera_sida(a, b)
                HL = formatera_sida(c, d)
                st.session_state.ekv_str = f"{VL} = {HL}"
                st.session_state.ekv_svar = x
                break
                
            else:
                # Nivå 2: a(x + b) = cx + d
                a = random.choice([-4, -3, -2, 2, 3, 4])
                c = random.choice([-5, -4, -3, -2, 2, 3, 4, 5])
                if a == c: continue
                
                b = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
                # Räkna ut d för att x ska stämma: a*(x + b) = c*x + d
                d = a*(x + b) - c*x
                
                b_str = f"+ {b}" if b > 0 else f"- {-b}"
                VL = f"{a}(x {b_str})"
                HL = formatera_sida(c, d)
                
                st.session_state.ekv_str = f"{VL} = {HL}"
                st.session_state.ekv_svar = x
                break

    # --- Initiera variabler ---
    if 'ekv_niva' not in st.session_state:
        st.session_state.ekv_niva = 1
    if 'ekv_uppgift_nr' not in st.session_state:
        st.session_state.ekv_uppgift_nr = 0
    if 'ekv_str' not in st.session_state:
        ny_ekvation()

    # --- UI för modulen ---
    col_uppgift, col_installningar = st.columns([1.5, 1], gap="large")
    
    with col_installningar:
        st.subheader("Inställningar")
        aktuellt_index = 0 if st.session_state.ekv_niva == 1 else 1
        ny_niva = st.radio("Välj svårighetsgrad:", [1, 2], horizontal=True, index=aktuellt_index, key="ekv_niva_val")
        if ny_niva != st.session_state.ekv_niva:
            st.session_state.ekv_niva = ny_niva
            ny_ekvation()
            st.rerun()
            
    with col_uppgift:
        st.markdown("<div style='text-align: center; font-size: 20px; color: gray;'>Lös ekvationen:</div>", unsafe_allow_html=True)
        
        st.latex(st.session_state.ekv_str)
        
        st.write("") # Lite mellanrum
        unik_key = f"ekv_input_{st.session_state.ekv_uppgift_nr}"
        svar = st.text_input("Vad är x? (Svara med ett heltal):", key=unik_key)
        
        k1, k2 = st.columns(2)
        with k1:
            if st.button("Rätta svar", type="primary", use_container_width=True, key="ekv_ratta"):
                st.session_state.ekv_rattat = True
                if svar.strip() != "":
                    try:
                        anv_svar = int(svar.strip())
                        if anv_svar == st.session_state.ekv_svar:
                            st.session_state.ekv_status = 'ratt'
                        else:
                            st.session_state.ekv_status = 'fel'
                    except ValueError:
                        st.session_state.ekv_status = 'format'
                else:
                    st.session_state.ekv_status = 'tom'
        with k2:
            if st.button("Ny ekvation", use_container_width=True, key="ekv_ny"):
                ny_ekvation()
                st.rerun()

        if st.session_state.get('ekv_rattat', False):
            if st.session_state.ekv_status == 'ratt':
                st.success("✅ Helt rätt! Snyggt jobbat.")
            elif st.session_state.ekv_status == 'fel':
                st.error(f"❌ Tyvärr fel. Rätt svar var: {st.session_state.ekv_svar}")
            elif st.session_state.ekv_status == 'format':
                st.warning("⚠️ Svaret ska vara ett heltal (t.ex. 5 eller -3). Skriv inte 'x=' i rutan.")
            elif st.session_state.ekv_status == 'tom':
                st.warning("Skriv in ett svar först.")

elif vald_kategori == "Algebra":
    st.title("Förenkla algebraiska uttryck")
    
    # --- Funktion för att generera uppgifter ---
    def ny_algebra_uttryck():
        niva = st.session_state.get('alg_uttryck_niva', 1)
        st.session_state.alg_uttryck_rattat = False
        st.session_state.alg_uttryck_status = None
        st.session_state.alg_uttryck_uppgift_nr = st.session_state.get('alg_uttryck_uppgift_nr', 0) + 1
        
        # Hjälpfunktion för att formatera kx + m snyggt i flervalsalternativen
        def formatera_svar(k, m):
            if k == 0 and m == 0: return "0"
            if k == 0: return str(m)
            
            if k == 1: k_str = "x"
            elif k == -1: k_str = "-x"
            else: k_str = f"{k}x"
            
            if m == 0: return k_str
            if m > 0: return f"{k_str} + {m}"
            return f"{k_str} - {-m}"

        if niva == 1:
            # Nivå 1: Förenkla ax + b + cx + d
            a = random.randint(1, 6)
            b = random.randint(-10, 10)
            c = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            d = random.randint(-10, 10)
            
            # Bygg uppgiftssträngen (t.ex. 3x - 5 - 2x + 8)
            a_str = f"{a}x" if a != 1 else "x"
            b_str = f"+ {b}" if b >= 0 else f"- {-b}"
            c_str = f"+ {c}x" if c > 0 else (f"+ x" if c==1 else (f"- x" if c==-1 else f"- {-c}x"))
            d_str = f"+ {d}" if d >= 0 else f"- {-d}"
            
            st.session_state.alg_uttryck_str = f"{a_str} {b_str} {c_str} {d_str}"
            
            ratt_k = a + c
            ratt_m = b + d
            svar_ratt = formatera_svar(ratt_k, ratt_m)
            
            # Skapa felaktiga alternativ (distraktorer)
            d1 = formatera_svar(a - c, b + d)
            d2 = formatera_svar(a + c, b - d)
            d3 = formatera_svar(a + c + 1, b + d - 2)
            
        else:
            # Nivå 2: Multiplicera in och förenkla a(x + b) - c(x + d)
            a = random.randint(2, 5)
            b = random.choice([-5, -4, -3, -2, 2, 3, 4, 5])
            c = random.randint(2, 5)
            d = random.choice([-5, -4, -3, -2, 2, 3, 4, 5])
            
            b_str = f"+ {b}" if b > 0 else f"- {-b}"
            d_str = f"+ {d}" if d > 0 else f"- {-d}"
            
            st.session_state.alg_uttryck_str = f"{a}(x {b_str}) - {c}(x {d_str})"
            
            ratt_k = a - c
            ratt_m = a*b - c*d
            svar_ratt = formatera_svar(ratt_k, ratt_m)
            
            # Skapa felaktiga alternativ utifrån vanliga teckenfel
            d1 = formatera_svar(a - c, a*b - c)      # Glömde multiplicera in c i d
            d2 = formatera_svar(a - c, a*b + c*d)    # Glömde byta tecken (minus framför parentes)
            d3 = formatera_svar(a + c, a*b - c*d)    # Adderade x-termerna istället för subtraktion
            
        # Samla och blanda alternativen
        alternativ = list(set([svar_ratt, d1, d2, d3]))
        
        # Säkerställ att vi har exakt 4 unika alternativ (ifall slumpen råkade skapa två likadana)
        while len(alternativ) < 4:
            nytt_alt = formatera_svar(random.randint(-5, 5), random.randint(-15, 15))
            if nytt_alt not in alternativ:
                alternativ.append(nytt_alt)
                
        random.shuffle(alternativ)
        st.session_state.alg_uttryck_svar = svar_ratt
        st.session_state.alg_uttryck_alternativ = alternativ

    # --- Initiera variabler ---
    if 'alg_uttryck_niva' not in st.session_state:
        st.session_state.alg_uttryck_niva = 1
    if 'alg_uttryck_uppgift_nr' not in st.session_state:
        st.session_state.alg_uttryck_uppgift_nr = 0
    if 'alg_uttryck_str' not in st.session_state:
        ny_algebra_uttryck()

    # --- UI för modulen ---
    col_uppgift, col_installningar = st.columns([1.5, 1], gap="large")
    
    with col_installningar:
        st.subheader("Inställningar")
        aktuellt_index = 0 if st.session_state.alg_uttryck_niva == 1 else 1
        ny_niva = st.radio("Välj svårighetsgrad:", [1, 2], horizontal=True, index=aktuellt_index, key="alg_uttryck_niva_val")
        if ny_niva != st.session_state.alg_uttryck_niva:
            st.session_state.alg_uttryck_niva = ny_niva
            ny_algebra_uttryck()
            st.rerun()
            
    with col_uppgift:
        st.markdown("<div style='text-align: center; font-size: 20px; color: gray;'>Förenkla uttrycket:</div>", unsafe_allow_html=True)
        st.latex(st.session_state.alg_uttryck_str)
        st.write("")
        
        # Flervalsfråga! index=None gör att ingen knapp är förvald.
        unik_key = f"alg_uttryck_input_{st.session_state.alg_uttryck_uppgift_nr}"
        valt_svar = st.radio("Välj det korrekt förenklade uttrycket:", st.session_state.alg_uttryck_alternativ, index=None, key=unik_key)
        
        st.write("")
        k1, k2 = st.columns(2)
        with k1:
            if st.button("Rätta svar", type="primary", use_container_width=True, key="alg_uttryck_ratta"):
                st.session_state.alg_uttryck_rattat = True
                if valt_svar is not None:
                    if valt_svar == st.session_state.alg_uttryck_svar:
                        st.session_state.alg_uttryck_status = 'ratt'
                    else:
                        st.session_state.alg_uttryck_status = 'fel'
                else:
                    st.session_state.alg_uttryck_status = 'tom'
        with k2:
            if st.button("Nytt uttryck", use_container_width=True, key="alg_uttryck_ny"):
                ny_algebra_uttryck()
                st.rerun()

        if st.session_state.get('alg_uttryck_rattat', False):
            if st.session_state.alg_uttryck_status == 'ratt':
                st.success("✅ Helt rätt! Bra förenklat.")
            elif st.session_state.alg_uttryck_status == 'fel':
                st.error(f"❌ Tyvärr fel. Rätt svar var: {st.session_state.alg_uttryck_svar}")
            elif st.session_state.alg_uttryck_status == 'tom':
                st.warning("Välj ett alternativ innan du klickar på Rätta.")

elif vald_kategori == "Blandat (Slumpas)":
    st.title("Blandat!")
    st.info("Detta läge kommer att slumpa bland alla aktiverade delar ovan när de är färdiga.")
