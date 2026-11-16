import time
from fractions import Fraction

from models import Uppgift
from utils import ratta_svar
from graphics import rita_plotly_graf
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

GENERATORER = {
    "Funktioner (Grafisk)": skapa_graf_uppgift,
    "Funktioner (Algebraisk)": skapa_alg_func_uppgift,
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


def simulera_elevsvar(u: Uppgift):
    """Omvandlar uppgiftens facit till ett realistiskt elevsvar med komma, ^ och ·."""
    if u.input_typ == "flera_text":
        return [f"{val:g}".replace(".", ",") for val in u.ratt_svar]

    if u.input_typ in ("radio", "selectbox"):
        return str(u.ratt_svar)

    if u.input_typ == "text":
        if u.svarstyp == "int":
            return str(u.ratt_svar)
        if u.svarstyp in ("float", "procent"):
            return f"{float(u.ratt_svar):g}".replace(".", ",")
        if u.svarstyp == "fraction":
            if isinstance(u.ratt_svar, Fraction):
                return f"{u.ratt_svar.numerator}/{u.ratt_svar.denominator}"
            return str(u.ratt_svar)
        if u.svarstyp == "kalkyl_formel":
            return str(u.ratt_svar_visning)
        if u.svarstyp == "string_math":
            return str(u.ratt_svar).replace("**", "^").replace("*", "·")
        return str(u.ratt_svar)

    return ""


def kor_stresstest(antal_per_niva=200):
    print(f"Startar stresstest ({antal_per_niva} körningar per generator och nivå)...\n")
    totalt_fel = 0

    for namn, gen_func in GENERATORER.items():
        nivaer = [1] if namn == "Statistik" else [1, 2]

        for niva in nivaer:
            start_tid = time.perf_counter()
            fel_lista = []

            for i in range(antal_per_niva):
                try:
                    u = gen_func(niva)

                    if not isinstance(u, Uppgift):
                        fel_lista.append(f"Körning {i}: Returnerade inte ett Uppgift-objekt.")
                        continue

                    if not u.fraga or not str(u.fraga).strip():
                        fel_lista.append(f"Körning {i}: Tom frågetext.")

                    # Kontrollera flervalsfrågor
                    if u.input_typ in ("radio", "selectbox"):
                        if not u.alternativ or len(u.alternativ) < 2:
                            fel_lista.append(f"Körning {i}: Saknar svarsalternativ.")
                        elif u.ratt_svar not in u.alternativ:
                            fel_lista.append(
                                f"Körning {i}: Facit '{u.ratt_svar}' finns inte bland alternativen {u.alternativ}."
                            )
                        elif len(set(u.alternativ)) != len(u.alternativ):
                            fel_lista.append(f"Körning {i}: Dubbletter i alternativen {u.alternativ}.")

                    # Testa att rättningsfunktionen godkänner facitsvaret
                    elevsvar = simulera_elevsvar(u)
                    status = ratta_svar(u, elevsvar)
                    if status != "ratt":
                        fel_lista.append(
                            f"Körning {i}: Rättning gav '{status}' för elevsvar '{elevsvar}' "
                            f"(facit: '{u.ratt_svar}', svarstyp: '{u.svarstyp}', fråga: '{u.fraga}')."
                        )

                    # Testa grafrendering (de 10 första körningarna för att spara tid)
                    if u.graf_f is not None and i < 10:
                        rita_plotly_graf(
                            f=u.graf_f,
                            visa_facit=True,
                            q_vis_type=u.q_type_vis,
                            trace_x=u.trace_x,
                            trace_y=u.trace_y,
                            trace_alla_x=u.trace_alla_x,
                        )

                except Exception as e:
                    fel_lista.append(f"Körning {i}: Kraschade med {type(e).__name__}: {e}")

            tid_ms = (time.perf_counter() - start_tid) * 1000
            if fel_lista:
                totalt_fel += len(fel_lista)
                print(f"❌ {namn} (Nivå {niva}) — {len(fel_lista)} fel ({tid_ms:.0f} ms)")
                for f in fel_lista[:3]:  # Visar de 3 första felen per kategori
                    print(f"   -> {f}")
            else:
                print(f"✅ {namn:<28} Nivå {niva}: {antal_per_niva}/{antal_per_niva} OK ({tid_ms:.0f} ms)")

    print("\n" + "=" * 55)
    if totalt_fel == 0:
        print("🎉 Alla tester gick igenom utan ett enda fel!")
    else:
        print(f"⚠️ Totalt {totalt_fel} fel hittades. Se detaljerna ovan.")


if __name__ == "__main__":
    kor_stresstest(antal_per_niva=200)
