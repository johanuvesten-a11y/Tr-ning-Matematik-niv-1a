import random
from models import Uppgift
from utils import formatera_kr


def _bygg_kalkylblad_html(kolumner, rader, markera_cell=None):
    """Bygger en HTML-tabell som efterliknar ett kalkylblad med kolumnbokstäver (A, B, C...) och radnummer (1, 2, 3...)."""
    html = (
        "<table style='width: 100%; border-collapse: collapse; font-family: Arial, sans-serif; "
        "font-size: 16px; text-align: center; box-shadow: 0 2px 6px rgba(0,0,0,0.08);'>"
    )
    # Rubrikrad med kolumnbokstäver
    html += "<thead><tr style='background-color: #e9ecef; color: #333; font-weight: bold;'>"
    html += "<th style='border: 1px solid #adb5bd; padding: 8px; width: 42px;'></th>"
    for kol in kolumner:
        html += f"<th style='border: 1px solid #adb5bd; padding: 8px;'>{kol}</th>"
    html += "</tr></thead><tbody>"

    # Datarader (rad 1, 2, 3...)
    for rad_idx, rad in enumerate(rader, start=1):
        bg_row = "#f8f9fa" if rad_idx == 1 else "#ffffff"
        font_weight = "bold" if rad_idx == 1 else "normal"
        html += f"<tr style='background-color: {bg_row}; font-weight: {font_weight};'>"
        html += (
            f"<td style='border: 1px solid #adb5bd; padding: 8px; background-color: #e9ecef; "
            f"font-weight: bold; color: #333;'>{rad_idx}</td>"
        )
        for kol_idx, varde in enumerate(rad):
            cell_namn = f"{kolumner[kol_idx]}{rad_idx}"
            if markera_cell and cell_namn == markera_cell:
                html += (
                    f"<td style='border: 2px solid #0056b3; background-color: #fff3cd; "
                    f"color: #0056b3; font-weight: bold; padding: 8px;'>{varde}</td>"
                )
            else:
                html += f"<td style='border: 1px solid #ced4da; padding: 8px;'>{varde}</td>"
        html += "</tr>"

    html += "</tbody></table>"
    return html


def skapa_kalkylblad_uppgift(niva):
    omrade = random.choice(["lan", "faktura", "lon"])

    # ==========================================
    # OMRÅDE 1: LÅN OCH AMORTERING
    # ==========================================
    if omrade == "lan":
        if niva == 1:
            typ = random.choice(["att_betala", "ny_skuld", "rak_amortering"])
            skuld = random.choice([60000, 120000, 180000, 240000, 300000])
            manader = random.choice([12, 24, 36, 48, 60])
            amortering = skuld // manader
            ranta_kr = random.choice([250, 400, 550, 750, 900])

            if typ == "att_betala":
                tabell = _bygg_kalkylblad_html(
                    ["A", "B", "C", "D", "E"],
                    [
                        ["Månad", "Skuld vid start (kr)", "Ränta (kr)", "Amortering (kr)", "Att betala (kr)"],
                        ["1", formatera_kr(skuld), formatera_kr(ranta_kr), formatera_kr(amortering), "?"],
                    ],
                    markera_cell="E2",
                )
                return Uppgift(
                    html_table=tabell,
                    fraga="Vilken formel ska stå i cell E2 för att beräkna det totala beloppet att betala?",
                    ratt_svar="=C2+D2",
                    ratt_svar_visning="=C2+D2",
                    ratt_svar_lista=["=C2+D2", "=D2+C2", "=SUMMA(C2:D2)"],
                    input_typ="text",
                    svarstyp="kalkyl_formel",
                    undertext="Använd cellreferenser (t.ex. =A1+B1). Inga mellanslag behövs.",
                    losningsforslag="Månadsbetalningen består av ränta (C2) plus amortering (D2): =C2+D2.",
                )

            elif typ == "ny_skuld":
                tabell = _bygg_kalkylblad_html(
                    ["A", "B", "C", "D", "E"],
                    [
                        ["Månad", "Skuld vid start (kr)", "Ränta (kr)", "Amortering (kr)", "Ny skuld (kr)"],
                        ["1", formatera_kr(skuld), formatera_kr(ranta_kr), formatera_kr(amortering), "?"],
                    ],
                    markera_cell="E2",
                )
                return Uppgift(
                    html_table=tabell,
                    fraga="Vilken formel ska stå i cell E2 för att beräkna den nya skulden efter betalningen?",
                    ratt_svar="=B2-D2",
                    ratt_svar_visning="=B2-D2",
                    ratt_svar_lista=["=B2-D2"],
                    input_typ="text",
                    svarstyp="kalkyl_formel",
                    undertext="Använd cellreferenser (t.ex. =A1-B1).",
                    losningsforslag="Det är bara amorteringen (D2) som minskar skulden (B2) – räntan är en kostnad för lånet. Därför blir formeln =B2-D2.",
                )

            else:  # rak_amortering
                tabell = _bygg_kalkylblad_html(
                    ["A", "B", "C", "D"],
                    [
                        ["Lån", "Lånebelopp (kr)", "Återbetalningstid (mån)", "Amortering/mån (kr)"],
                        ["Billån", formatera_kr(skuld), str(manader), "?"],
                    ],
                    markera_cell="D2",
                )
                return Uppgift(
                    html_table=tabell,
                    fraga="Lånet har rak amortering. Vilken formel ska stå i cell D2 för att beräkna amorteringen per månad?",
                    ratt_svar="=B2/C2",
                    ratt_svar_visning="=B2/C2",
                    ratt_svar_lista=["=B2/C2"],
                    input_typ="text",
                    svarstyp="kalkyl_formel",
                    undertext="Använd snedstreck (/) för division.",
                    losningsforslag="Vid rak amortering delas hela lånebeloppet (B2) lika på antalet månader (C2): =B2/C2.",
                )

        else:  # Nivå 2 (Lån)
            typ = random.choice(["manadsranta", "manadskostnad", "skuld_rad3"])
            skuld = random.choice([120000, 180000, 240000, 360000])
            arsranta = random.choice(["4,8%", "6%", "3,6%", "5,4%"])
            amortering = random.choice([2000, 2500, 3000, 4000])

            if typ == "manadsranta":
                tabell = _bygg_kalkylblad_html(
                    ["A", "B", "C", "D"],
                    [
                        ["Månad", "Skuld vid start (kr)", "Årsränta", "Månadsränta (kr)"],
                        ["1", formatera_kr(skuld), arsranta, "?"],
                    ],
                    markera_cell="D2",
                )
                return Uppgift(
                    html_table=tabell,
                    fraga="Vilken formel ska stå i cell D2 för att beräkna månadens räntekostnad?",
                    ratt_svar="=B2*C2/12",
                    ratt_svar_visning="=B2*C2/12",
                    ratt_svar_lista=["=B2*C2/12", "=C2*B2/12", "=(B2*C2)/12", "=(C2*B2)/12", "=B2*(C2/12)"],
                    input_typ="text",
                    svarstyp="kalkyl_formel",
                    undertext="Tänk på att cell C2 anger årsräntan.",
                    losningsforslag="Multiplicera skulden (B2) med årsräntan (C2) och dela med 12 månader: =B2*C2/12.",
                )

            elif typ == "manadskostnad":
                tabell = _bygg_kalkylblad_html(
                    ["A", "B", "C", "D", "E"],
                    [
                        ["Månad", "Skuld vid start (kr)", "Årsränta", "Amortering (kr)", "Att betala (kr)"],
                        ["1", formatera_kr(skuld), arsranta, formatera_kr(amortering), "?"],
                    ],
                    markera_cell="E2",
                )
                return Uppgift(
                    html_table=tabell,
                    fraga="Vilken formel ska stå i cell E2 för att beräkna hela månadsbetalningen (ränta + amortering)?",
                    ratt_svar="=B2*C2/12+D2",
                    ratt_svar_visning="=B2*C2/12+D2",
                    ratt_svar_lista=[
                        "=B2*C2/12+D2",
                        "=C2*B2/12+D2",
                        "=(B2*C2)/12+D2",
                        "=(C2*B2)/12+D2",
                        "=D2+B2*C2/12",
                        "=D2+C2*B2/12",
                        "=D2+(B2*C2)/12",
                        "=D2+(C2*B2)/12",
                    ],
                    input_typ="text",
                    svarstyp="kalkyl_formel",
                    undertext="Använd cellreferenser i kalkylbladet.",
                    losningsforslag="Månadsräntan är B2*C2/12 och sedan adderas amorteringen i D2: =B2*C2/12+D2.",
                )

            else:  # skuld_rad3
                ny_skuld_1 = skuld - amortering
                tabell = _bygg_kalkylblad_html(
                    ["A", "B", "C", "D"],
                    [
                        ["Månad", "Skuld vid start (kr)", "Amortering (kr)", "Ny skuld (kr)"],
                        ["1", formatera_kr(skuld), formatera_kr(amortering), formatera_kr(ny_skuld_1)],
                        ["2", formatera_kr(ny_skuld_1), formatera_kr(amortering), "?"],
                    ],
                    markera_cell="D3",
                )
                return Uppgift(
                    html_table=tabell,
                    fraga="Vilken formel ska stå i cell D3 för att beräkna den nya skulden efter månad 2?",
                    ratt_svar="=B3-C3",
                    ratt_svar_visning="=B3-C3",
                    ratt_svar_lista=["=B3-C3", "=D2-C3", "=B2-C2-C3"],
                    input_typ="text",
                    svarstyp="kalkyl_formel",
                    undertext="Använd cellreferenser.",
                    losningsforslag="Ta skulden vid start av månad 2 (B3) minus amorteringen för månad 2 (C3): =B3-C3.",
                )

    # ==========================================
    # OMRÅDE 2: FAKTUROR OCH MOMS
    # ==========================================
    elif omrade == "faktura":
        if niva == 1:
            typ = random.choice(["radsumma", "totalsumma", "moms_kr"])
            antal_1, pris_1 = random.randint(2, 8), random.choice([150, 240, 350, 480])
            antal_2, pris_2 = random.randint(2, 6), random.choice([120, 200, 300, 450])
            antal_3, pris_3 = random.randint(1, 5), random.choice([190, 280, 400, 520])
            rad_1, rad_2, rad_3 = antal_1 * pris_1, antal_2 * pris_2, antal_3 * pris_3
            tot_exkl = rad_1 + rad_2 + rad_3

            if typ == "radsumma":
                tabell = _bygg_kalkylblad_html(
                    ["A", "B", "C", "D"],
                    [
                        ["Artikel", "Antal", "À-pris (kr)", "Summa (kr)"],
                        ["Skruvpaket", str(antal_1), formatera_kr(pris_1), "?"],
                        ["Färgburk 3L", str(antal_2), formatera_kr(pris_2), formatera_kr(rad_2)],
                    ],
                    markera_cell="D2",
                )
                return Uppgift(
                    html_table=tabell,
                    fraga="Vilken formel ska stå i cell D2 för att beräkna kostnaden för artikeln?",
                    ratt_svar="=B2*C2",
                    ratt_svar_visning="=B2*C2",
                    ratt_svar_lista=["=B2*C2", "=C2*B2"],
                    input_typ="text",
                    svarstyp="kalkyl_formel",
                    undertext="Använd asterisk (*) för multiplikation.",
                    losningsforslag="Multiplicera antalet (B2) med styckpriset (C2): =B2*C2.",
                )

            elif typ == "totalsumma":
                tabell = _bygg_kalkylblad_html(
                    ["A", "B", "C", "D"],
                    [
                        ["Artikel", "Antal", "À-pris (kr)", "Summa (kr)"],
                        ["Skruvpaket", str(antal_1), formatera_kr(pris_1), formatera_kr(rad_1)],
                        ["Färgburk 3L", str(antal_2), formatera_kr(pris_2), formatera_kr(rad_2)],
                        ["Penselset", str(antal_3), formatera_kr(pris_3), formatera_kr(rad_3)],
                        ["", "", "Summa exkl. moms:", "?"],
                    ],
                    markera_cell="D5",
                )
                return Uppgift(
                    html_table=tabell,
                    fraga="Vilken formel ska stå i cell D5 för att beräkna totalsumman exklusive moms?",
                    ratt_svar="=SUMMA(D2:D4)",
                    ratt_svar_visning="=SUMMA(D2:D4)",
                    ratt_svar_lista=["=SUMMA(D2:D4)", "=D2+D3+D4", "=D2+D4+D3", "=D3+D2+D4", "=D3+D4+D2", "=D4+D2+D3", "=D4+D3+D2"],
                    input_typ="text",
                    svarstyp="kalkyl_formel",
                    undertext="Använd gärna funktionen SUMMA.",
                    losningsforslag="Addera radsummorna D2 till D4 med =SUMMA(D2:D4) (eller =D2+D3+D4).",
                )

            else:  # moms_kr
                tabell = _bygg_kalkylblad_html(
                    ["A", "B", "C", "D"],
                    [
                        ["Artikel", "Antal", "À-pris (kr)", "Summa (kr)"],
                        ["Arbetstid (tim)", str(antal_1), formatera_kr(pris_1), formatera_kr(rad_1)],
                        ["Material", str(antal_2), formatera_kr(pris_2), formatera_kr(rad_2)],
                        ["", "", "Summa exkl. moms:", formatera_kr(rad_1 + rad_2)],
                        ["", "Momssats:", "25%", "?"],
                    ],
                    markera_cell="D5",
                )
                return Uppgift(
                    html_table=tabell,
                    fraga="Vilken formel ska stå i cell D5 för att beräkna momsen i kronor?",
                    ratt_svar="=D4*C5",
                    ratt_svar_visning="=D4*C5",
                    ratt_svar_lista=["=D4*C5", "=C5*D4", "=D4*0,25", "=0,25*D4", "=D4*0.25", "=0.25*D4", "=D4*25%", "=25%*D4"],
                    input_typ="text",
                    svarstyp="kalkyl_formel",
                    undertext="Använd cellreferenser i kalkylbladet.",
                    losningsforslag="Multiplicera summan exklusive moms (D4) med momssatsen i C5: =D4*C5.",
                )

        else:  # Nivå 2 (Fakturor)
            typ = random.choice(["inkl_moms", "rabatt", "frakt_och_moms"])

            if typ == "inkl_moms":
                summa_exkl = random.choice([2400, 3600, 4800, 6000])
                tabell = _bygg_kalkylblad_html(
                    ["A", "B", "C", "D"],
                    [
                        ["Beskrivning", "Antal", "À-pris (kr)", "Belopp (kr)"],
                        ["Service & underhåll", "1", formatera_kr(summa_exkl), formatera_kr(summa_exkl)],
                        ["", "", "Summa exkl. moms:", formatera_kr(summa_exkl)],
                        ["", "Momssats:", "25%", ""],
                        ["", "", "Totalt inkl. moms:", "?"],
                    ],
                    markera_cell="D5",
                )
                return Uppgift(
                    html_table=tabell,
                    fraga="Vilken formel ska stå i cell D5 för att beräkna totalbeloppet inklusive moms?",
                    ratt_svar="=D3*(1+C4)",
                    ratt_svar_visning="=D3*(1+C4)",
                    ratt_svar_lista=[
                        "=D3*(1+C4)",
                        "=(1+C4)*D3",
                        "=D3+D3*C4",
                        "=D3+C4*D3",
                        "=D3*1,25",
                        "=1,25*D3",
                        "=D3*1.25",
                        "=1.25*D3",
                        "=D3+D3*0,25",
                        "=D3+D3*0.25",
                        "=D3*(1+0,25)",
                        "=D3*(1+0.25)",
                    ],
                    input_typ="text",
                    svarstyp="kalkyl_formel",
                    undertext="Använd cellreferenser (D3 och C4).",
                    losningsforslag="Multiplicera summan exklusive moms (D3) med förändringsfaktorn (1 + C4), dvs. =D3*(1+C4) eller =D3+D3*C4.",
                )

            elif typ == "rabatt":
                ord_pris = random.choice([800, 1200, 1500, 2000])
                rabatt_pct = random.choice([15, 20, 25, 30])
                kvar_k = f"{1 - rabatt_pct / 100:g}".replace(".", ",")
                kvar_p = f"{1 - rabatt_pct / 100:g}"
                rab_k = f"{rabatt_pct / 100:g}".replace(".", ",")
                rab_p = f"{rabatt_pct / 100:g}"

                tabell = _bygg_kalkylblad_html(
                    ["A", "B", "C", "D"],
                    [
                        ["Produkt", "Ordinarie pris (kr)", "Rabatt", "Pris efter rabatt (kr)"],
                        ["Verktygsväska", formatera_kr(ord_pris), f"{rabatt_pct}%", "?"],
                    ],
                    markera_cell="D2",
                )
                return Uppgift(
                    html_table=tabell,
                    fraga="Vilken formel ska stå i cell D2 för att beräkna priset efter rabatt?",
                    ratt_svar="=B2*(1-C2)",
                    ratt_svar_visning="=B2*(1-C2)",
                    ratt_svar_lista=[
                        "=B2*(1-C2)",
                        "=(1-C2)*B2",
                        "=B2-B2*C2",
                        "=B2-C2*B2",
                        f"=B2*{kvar_k}",
                        f"={kvar_k}*B2",
                        f"=B2*{kvar_p}",
                        f"={kvar_p}*B2",
                        f"=B2*(1-{rab_k})",
                        f"=B2*(1-{rab_p})",
                        f"=B2-B2*{rab_k}",
                        f"=B2-B2*{rab_p}",
                    ],
                    input_typ="text",
                    svarstyp="kalkyl_formel",
                    undertext="Använd cellreferenser i kalkylbladet.",
                    losningsforslag="Dra bort rabatten från 1 för att få förändringsfaktorn: =B2*(1-C2) (eller =B2-B2*C2).",
                )

            else:  # frakt_och_moms
                varor = random.choice([1600, 2200, 3000])
                frakt = random.choice([120, 160, 200])
                tabell = _bygg_kalkylblad_html(
                    ["A", "B"],
                    [
                        ["Post", "Belopp (kr)"],
                        ["Varor exkl. moms", formatera_kr(varor)],
                        ["Frakt exkl. moms", formatera_kr(frakt)],
                        ["Totalt inkl. 25 % moms", "?"],
                    ],
                    markera_cell="B4",
                )
                return Uppgift(
                    html_table=tabell,
                    fraga="Vilken formel ska stå i cell B4 för att beräkna totalbeloppet inklusive 25 % moms?",
                    ratt_svar="=(B2+B3)*1,25",
                    ratt_svar_visning="=(B2+B3)*1,25",
                    ratt_svar_lista=[
                        "=(B2+B3)*1,25",
                        "=1,25*(B2+B3)",
                        "=(B2+B3)*1.25",
                        "=1.25*(B2+B3)",
                        "=SUMMA(B2:B3)*1,25",
                        "=1,25*SUMMA(B2:B3)",
                        "=SUMMA(B2:B3)*1.25",
                        "=1.25*SUMMA(B2:B3)",
                        "=B2*1,25+B3*1,25",
                        "=B2*1.25+B3*1.25",
                    ],
                    input_typ="text",
                    svarstyp="kalkyl_formel",
                    undertext="Kom ihåg parenteser om du adderar först!",
                    losningsforslag="Addera varor (B2) och frakt (B3) inom parentes och multiplicera med förändringsfaktorn 1,25: =(B2+B3)*1,25.",
                )

    # ==========================================
    # OMRÅDE 3: LÖN OCH SKATT
    # ==========================================
    else:
        if niva == 1:
            typ = random.choice(["bruttolon", "nettolon_enkel", "skatt_kr"])
            timmar = random.choice([18, 24, 32, 40])
            timlon = random.choice([145, 160, 175, 190])
            brutto = timmar * timlon
            skatt_kr = int(round(brutto * 0.30))

            if typ == "bruttolon":
                tabell = _bygg_kalkylblad_html(
                    ["A", "B", "C", "D"],
                    [
                        ["Anställd", "Arbetade timmar", "Timlön (kr)", "Bruttolön (kr)"],
                        ["Alex", str(timmar), formatera_kr(timlon), "?"],
                    ],
                    markera_cell="D2",
                )
                return Uppgift(
                    html_table=tabell,
                    fraga="Vilken formel ska stå i cell D2 för att beräkna bruttolönen?",
                    ratt_svar="=B2*C2",
                    ratt_svar_visning="=B2*C2",
                    ratt_svar_lista=["=B2*C2", "=C2*B2"],
                    input_typ="text",
                    svarstyp="kalkyl_formel",
                    undertext="Använd asterisk (*) för multiplikation.",
                    losningsforslag="Multiplicera arbetade timmar (B2) med timlönen (C2): =B2*C2.",
                )

            elif typ == "nettolon_enkel":
                tabell = _bygg_kalkylblad_html(
                    ["A", "B", "C", "D"],
                    [
                        ["Anställd", "Bruttolön (kr)", "Skatt (kr)", "Nettolön (kr)"],
                        ["Sam", formatera_kr(brutto), formatera_kr(skatt_kr), "?"],
                    ],
                    markera_cell="D2",
                )
                return Uppgift(
                    html_table=tabell,
                    fraga="Vilken formel ska stå i cell D2 för att beräkna nettolönen (lön efter skatt)?",
                    ratt_svar="=B2-C2",
                    ratt_svar_visning="=B2-C2",
                    ratt_svar_lista=["=B2-C2"],
                    input_typ="text",
                    svarstyp="kalkyl_formel",
                    undertext="Använd cellreferenser i kalkylbladet.",
                    losningsforslag="Nettolön är bruttolönen (B2) minus skatten (C2): =B2-C2.",
                )

            else:  # skatt_kr
                tabell = _bygg_kalkylblad_html(
                    ["A", "B", "C", "D"],
                    [
                        ["Anställd", "Bruttolön (kr)", "Skattesats", "Skatteavdrag (kr)"],
                        ["Kim", formatera_kr(brutto), "30%", "?"],
                    ],
                    markera_cell="D2",
                )
                return Uppgift(
                    html_table=tabell,
                    fraga="Vilken formel ska stå i cell D2 för att beräkna skatteavdraget i kronor?",
                    ratt_svar="=B2*C2",
                    ratt_svar_visning="=B2*C2",
                    ratt_svar_lista=["=B2*C2", "=C2*B2", "=B2*0,3", "=B2*0,30", "=B2*0.3", "=B2*0.30", "=B2*30%", "=30%*B2"],
                    input_typ="text",
                    svarstyp="kalkyl_formel",
                    undertext="Använd cellreferenser (B2 och C2).",
                    losningsforslag="Multiplicera bruttolönen (B2) med skattesatsen (C2): =B2*C2.",
                )

        else:  # Nivå 2 (Lön och skatt)
            typ = random.choice(["nettolon_procent", "semesterersattning", "overtid"])

            if typ == "nettolon_procent":
                brutto = random.choice([24000, 28000, 32000, 35000])
                skatt_pct = random.choice([28, 30, 32])
                kvar_k = f"{1 - skatt_pct / 100:g}".replace(".", ",")
                kvar_p = f"{1 - skatt_pct / 100:g}"
                sk_k = f"{skatt_pct / 100:g}".replace(".", ",")
                sk_p = f"{skatt_pct / 100:g}"

                tabell = _bygg_kalkylblad_html(
                    ["A", "B", "C", "D"],
                    [
                        ["Anställd", "Bruttolön (kr)", "Skattesats", "Nettolön (kr)"],
                        ["Robin", formatera_kr(brutto), f"{skatt_pct}%", "?"],
                    ],
                    markera_cell="D2",
                )
                return Uppgift(
                    html_table=tabell,
                    fraga="Vilken formel ska stå i cell D2 för att beräkna nettolönen direkt?",
                    ratt_svar="=B2*(1-C2)",
                    ratt_svar_visning="=B2*(1-C2)",
                    ratt_svar_lista=[
                        "=B2*(1-C2)",
                        "=(1-C2)*B2",
                        "=B2-B2*C2",
                        "=B2-C2*B2",
                        f"=B2*{kvar_k}",
                        f"={kvar_k}*B2",
                        f"=B2*{kvar_p}",
                        f"={kvar_p}*B2",
                        f"=B2*(1-{sk_k})",
                        f"=B2*(1-{sk_p})",
                        f"=B2-B2*{sk_k}",
                        f"=B2-B2*{sk_p}",
                    ],
                    input_typ="text",
                    svarstyp="kalkyl_formel",
                    undertext="Använd cellreferenser i kalkylbladet.",
                    losningsforslag="Multiplicera bruttolönen (B2) med andelen du får behålla efter skatt (1 - C2): =B2*(1-C2).",
                )

            elif typ == "semesterersattning":
                grundlon = random.choice([14000, 18000, 22000])
                tabell = _bygg_kalkylblad_html(
                    ["A", "B", "C", "D"],
                    [
                        ["Anställd", "Grundlön (kr)", "Semesterersättning", "Total bruttolön (kr)"],
                        ["Charlie", formatera_kr(grundlon), "12%", "?"],
                    ],
                    markera_cell="D2",
                )
                return Uppgift(
                    html_table=tabell,
                    fraga="Vilken formel ska stå i cell D2 för att beräkna total bruttolön inklusive semesterersättning?",
                    ratt_svar="=B2*(1+C2)",
                    ratt_svar_visning="=B2*(1+C2)",
                    ratt_svar_lista=[
                        "=B2*(1+C2)",
                        "=(1+C2)*B2",
                        "=B2+B2*C2",
                        "=B2+C2*B2",
                        "=B2*1,12",
                        "=1,12*B2",
                        "=B2*1.12",
                        "=1.12*B2",
                        "=B2+B2*0,12",
                        "=B2+B2*0.12",
                    ],
                    input_typ="text",
                    svarstyp="kalkyl_formel",
                    undertext="Använd cellreferenser i kalkylbladet.",
                    losningsforslag="Öka grundlönen (B2) med semesterersättningen (C2): =B2*(1+C2) (eller =B2+B2*C2).",
                )

            else:  # overtid
                timlon = random.choice([160, 180, 200])
                ord_tim = random.choice([30, 35, 40])
                over_tim = random.choice([4, 6, 8])
                tabell = _bygg_kalkylblad_html(
                    ["A", "B", "C", "D", "E"],
                    [
                        ["Anställd", "Timlön (kr)", "Ordinarie tim", "Övertid (+50 %)", "Bruttolön (kr)"],
                        ["Noah", formatera_kr(timlon), str(ord_tim), str(over_tim), "?"],
                    ],
                    markera_cell="E2",
                )
                return Uppgift(
                    html_table=tabell,
                    fraga="Övertid ger 50 % högre timlön. Vilken formel ska stå i cell E2 för total bruttolön?",
                    ratt_svar="=B2*C2+B2*D2*1,5",
                    ratt_svar_visning="=B2*C2+B2*D2*1,5",
                    ratt_svar_lista=[
                        "=B2*C2+B2*D2*1,5",
                        "=B2*C2+B2*D2*1.5",
                        "=B2*C2+1,5*B2*D2",
                        "=B2*C2+1.5*B2*D2",
                        "=B2*(C2+D2*1,5)",
                        "=B2*(C2+D2*1.5)",
                        "=B2*(C2+1,5*D2)",
                        "=B2*(C2+1.5*D2)",
                    ],
                    input_typ="text",
                    svarstyp="kalkyl_formel",
                    undertext="50 % påslag motsvarar förändringsfaktorn 1,5.",
                    losningsforslag="Ordinarie lön är B2*C2 och övertidslönen är B2*D2*1,5. Tillsammans: =B2*C2+B2*D2*1,5.",
                )


# Alias så att både ursprungliga namn och kortare importnamn fungerar
skapa_kalkylblad = skapa_kalkylblad_uppgift
