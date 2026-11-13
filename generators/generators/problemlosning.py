import random
from fractions import Fraction
import plotly.graph_objects as go

from models import Uppgift
from utils import formatera_kr


def rita_mönster_kuber(max_fig=4, typ=1):
    """Ritar isometriska kuber som ett plotlymönster baserat på vald typ."""
    fig = go.Figure()
    offset_u = 0

    for n in range(1, max_fig + 1):
        kuber = []
        if typ == 1:  # Trappan
            for x in range(n):
                for y in range(n):
                    kuber.append((x, y, 0, 'vit'))
                    if x + y <= n - 2:
                        kuber.append((x, y, 1, 'grå'))
        elif typ == 2:  # Pyramiden
            for x in range(n + 1):
                for y in range(n + 1):
                    kuber.append((x, y, 0, 'vit'))
            for x in range(n):
                for y in range(n):
                    kuber.append((x + 0.5, y + 0.5, 1, 'grå'))
        elif typ == 3:  # Delad kvadrat
            for x in range(n):
                for y in range(n):
                    if x >= y:
                        kuber.append((x, y, 0, 'vit'))
                    else:
                        kuber.append((x, y, 0, 'grå'))

        # Painter's algorithm: sort back-to-front
        kuber.sort(key=lambda k: (k[0], k[1], k[2]))

        for x, y, z, farg in kuber:
            u_c = (x - y) + offset_u
            v_c = z - 0.5 * (x + y)

            if farg == 'vit':
                c_top, c_left, c_right = '#ffffff', '#e0e0e0', '#cccccc'
            else:
                c_top, c_left, c_right = '#888888', '#666666', '#444444'

            fig.add_trace(go.Scatter(
                x=[u_c, u_c + 1, u_c, u_c - 1, u_c],
                y=[v_c + 0.5, v_c, v_c - 0.5, v_c, v_c + 0.5],
                fill='toself', fillcolor=c_top, mode='lines',
                line=dict(color='#333', width=1), hoverinfo='skip'
            ))
            fig.add_trace(go.Scatter(
                x=[u_c, u_c + 1, u_c + 1, u_c, u_c],
                y=[v_c - 0.5, v_c, v_c - 1, v_c - 1.5, v_c - 0.5],
                fill='toself', fillcolor=c_right, mode='lines',
                line=dict(color='#333', width=1), hoverinfo='skip'
            ))
            fig.add_trace(go.Scatter(
                x=[u_c, u_c - 1, u_c - 1, u_c, u_c],
                y=[v_c - 0.5, v_c, v_c - 1, v_c - 1.5, v_c - 0.5],
                fill='toself', fillcolor=c_left, mode='lines',
                line=dict(color='#333', width=1), hoverinfo='skip'
            ))

        bredd = (n + 1) if typ == 2 else n
        fig.add_trace(go.Scatter(
            x=[offset_u], y=[-bredd - 1.0], mode='text',
            text=[f"<b>Figur {n}</b>"],
            textfont=dict(size=16, color='black'), hoverinfo='skip'
        ))

        offset_u += (2 * bredd) + 2

    fig.update_layout(
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, visible=False, scaleanchor="x", scaleratio=1),
        showlegend=False, margin=dict(l=10, r=10, t=10, b=10),
        plot_bgcolor='white', height=350, dragmode=False
    )
    return fig


def skapa_lan_uppgift(niva):
    if niva == 1:
        typ = random.choice(['arsranta', 'manadsranta', 'rak_amortering', 'kalkylblad_varde', 'kalkylblad_formel'])
        if typ == 'arsranta':
            kapital = random.choice([15000, 20000, 35000, 50000, 80000, 150000])
            ranta = random.choice([3, 4, 5, 6, 7, 8])
            return Uppgift(
                info_box_text=f"Du lånar {formatera_kr(kapital)}\xa0kr av banken med en årsränta på {ranta}\xa0%.",
                info_box_style="blue",
                fraga="Hur mycket får du betala i ränta under det första året? (Svara i kr)",
                ratt_svar=int(round(kapital * (ranta / 100))),
                input_typ="text", svarstyp="int", suffix="kr"
            )
        elif typ == 'manadsranta':
            kapital = random.choice([12000, 24000, 36000, 60000, 120000])
            ranta = random.choice([3, 4, 5, 6, 7, 8])
            return Uppgift(
                info_box_text=f"Du tar ett lån på {formatera_kr(kapital)}\xa0kr. Årsräntan är {ranta}\xa0%.",
                info_box_style="blue",
                fraga="Hur stor blir räntekostnaden för den allra första månaden? (Svara i kr)",
                ratt_svar=int(round((kapital * (ranta / 100)) / 12)),
                input_typ="text", svarstyp="int", suffix="kr"
            )
        elif typ == 'rak_amortering':
            ar = random.choice([2, 3, 4, 5, 10])
            amort = random.choice([500, 1000, 1500, 2000, 2500])
            return Uppgift(
                info_box_text=f"Du lånar {formatera_kr(amort * ar * 12)}\xa0kr som ska betalas tillbaka med rak amortering under {ar}\xa0år.",
                info_box_style="blue",
                fraga="Hur mycket ska du amortera varje månad? (Svara i kr)",
                ratt_svar=amort,
                input_typ="text", svarstyp="int", suffix="kr"
            )
        elif typ in ['kalkylblad_varde', 'kalkylblad_formel']:
            p_komb = random.choice([(60000, 5), (120000, 5), (120000, 10), (240000, 10), (240000, 20)])
            kapital, ar = p_komb
            ranta = random.choice([3, 4, 5, 6])
            amort = int(kapital / (ar * 12))
            manadsranta_kr = int(round(kapital * (ranta / 100) / 12))

            subtyper = ['C2_ranta', 'E2_tot', 'D2_amort', 'tid_manader', 'F2_tid_ar']
            if typ == 'kalkylblad_varde':
                subtyper.remove('F2_tid_ar')
            subtyp = random.choice(subtyper)

            C2_val, D2_val, E2_val, F2_val = "[tom]", "[tom]", "[tom]", str(ar)

            if subtyp == 'C2_ranta':
                D2_val = formatera_kr(amort)
            elif subtyp == 'E2_tot':
                C2_val = formatera_kr(manadsranta_kr)
                D2_val = formatera_kr(amort)
            elif subtyp == 'D2_amort':
                pass
            elif subtyp in ['tid_manader', 'F2_tid_ar']:
                D2_val = formatera_kr(amort)
                F2_val = "[tom]"

            tabell_html = f"""
            <div style="overflow-x: auto; margin-top: 10px; margin-bottom: 20px;">
                <table style="width: 100%; border-collapse: collapse; font-family: sans-serif; font-size: 14px; background-color: white; color: black; border: 1px solid #ccc;">
                    <thead>
                        <tr style="background-color: #f1f3f4; border-bottom: 2px solid #ccc;">
                            <th style="padding: 8px; border: 1px solid #ccc; width: 40px; color: black;"></th>
                            <th style="padding: 8px; border: 1px solid #ccc; text-align: center; color: black;">A</th>
                            <th style="padding: 8px; border: 1px solid #ccc; text-align: center; color: black;">B</th>
                            <th style="padding: 8px; border: 1px solid #ccc; text-align: center; color: black;">C</th>
                            <th style="padding: 8px; border: 1px solid #ccc; text-align: center; color: black;">D</th>
                            <th style="padding: 8px; border: 1px solid #ccc; text-align: center; color: black;">E</th>
                            <th style="padding: 8px; border: 1px solid #ccc; text-align: center; color: black;">F</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <th style="background-color: #f1f3f4; padding: 8px; border: 1px solid #ccc; text-align: center; color: black;">1</th>
                            <td style="padding: 8px; border: 1px solid #ccc; font-weight: bold; text-align: center; color: black;">Lånebelopp</td>
                            <td style="padding: 8px; border: 1px solid #ccc; font-weight: bold; text-align: center; color: black;">Räntesats</td>
                            <td style="padding: 8px; border: 1px solid #ccc; font-weight: bold; text-align: center; color: black;">Räntekostnad<br>/mån</td>
                            <td style="padding: 8px; border: 1px solid #ccc; font-weight: bold; text-align: center; color: black;">Amortering<br>/mån</td>
                            <td style="padding: 8px; border: 1px solid #ccc; font-weight: bold; text-align: center; color: black;">Månads-<br>kostnad</td>
                            <td style="padding: 8px; border: 1px solid #ccc; font-weight: bold; text-align: center; color: black;">Återbet.tid<br>(år)</td>
                        </tr>
                        <tr>
                            <th style="background-color: #f1f3f4; padding: 8px; border: 1px solid #ccc; text-align: center; color: black;">2</th>
                            <td style="padding: 8px; border: 1px solid #ccc; text-align: center; color: black;">{formatera_kr(kapital)}</td>
                            <td style="padding: 8px; border: 1px solid #ccc; text-align: center; color: black;">{ranta}\xa0%</td>
                            <td style="padding: 8px; border: 1px solid #ccc; text-align: center; color: {'black' if C2_val != '[tom]' else 'gray'}; font-style: {'normal' if C2_val != '[tom]' else 'italic'};">{C2_val}</td>
                            <td style="padding: 8px; border: 1px solid #ccc; text-align: center; color: {'black' if D2_val != '[tom]' else 'gray'}; font-style: {'normal' if D2_val != '[tom]' else 'italic'};">{D2_val}</td>
                            <td style="padding: 8px; border: 1px solid #ccc; text-align: center; color: {'black' if E2_val != '[tom]' else 'gray'}; font-style: {'normal' if E2_val != '[tom]' else 'italic'};">{E2_val}</td>
                            <td style="padding: 8px; border: 1px solid #ccc; text-align: center; color: {'black' if F2_val != '[tom]' else 'gray'}; font-style: {'normal' if F2_val != '[tom]' else 'italic'};">{F2_val}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            """

            if typ == 'kalkylblad_varde':
                if subtyp == 'C2_ranta':
                    return Uppgift(
                        info_box_text="Titta på kalkylarket nedan:", info_box_style="blue",
                        html_table=tabell_html,
                        fraga="I cell C2 skriver du in formeln: `=A2*B2/12`. Vilket värde kommer att visas i cell C2 när du trycker på Enter? (Svara i kr)",
                        ratt_svar=manadsranta_kr, input_typ="text", svarstyp="int", suffix="kr"
                    )
                elif subtyp == 'E2_tot':
                    return Uppgift(
                        info_box_text=f"Titta på kalkylarket nedan. Tänk dig att du redan har räknat ut att räntekostnaden i cell C2 blev {formatera_kr(manadsranta_kr)}\xa0kr.",
                        info_box_style="blue", html_table=tabell_html,
                        fraga="I cell E2 skriver du in formeln: `=C2+D2`. Vilket värde kommer att visas i cell E2? (Svara i kr)",
                        ratt_svar=manadsranta_kr + amort, input_typ="text", svarstyp="int", suffix="kr"
                    )
                elif subtyp == 'D2_amort':
                    return Uppgift(
                        info_box_text="Titta på kalkylarket nedan:", info_box_style="blue",
                        html_table=tabell_html,
                        fraga="Lånet ska betalas tillbaka med samma summa varje månad under den tid som står i cell F2. Hur stor blir amorteringen per månad? (Svara i kr)",
                        ratt_svar=amort, input_typ="text", svarstyp="int", suffix="kr"
                    )
                elif subtyp == 'tid_manader':
                    return Uppgift(
                        info_box_text="Titta på kalkylarket nedan:", info_box_style="blue",
                        html_table=tabell_html,
                        fraga="Om du amorterar det belopp som står i cell D2 varje månad, hur många MÅNADER kommer det ta innan hela lånet är noll?",
                        ratt_svar=ar * 12, input_typ="text", svarstyp="int", suffix="månader"
                    )

            elif typ == 'kalkylblad_formel':
                if subtyp == 'C2_ranta':
                    return Uppgift(
                        info_box_text="Titta på kalkylarket nedan:", info_box_style="blue",
                        html_table=tabell_html,
                        fraga="Vilken formel ska du skriva in i cell C2 för att kalkylarket ska räkna ut räntekostnaden för en månad?",
                        ratt_svar_lista=[
                            '=a2*b2/12', '=b2*a2/12', '=a2*(b2/100)/12', '=(a2*b2)/12',
                            '=a2/12*b2', '=b2/12*a2', '=a2*b2/100/12', '=(a2*b2/100)/12',
                            '=b2*a2/100/12', '=a2*(b2/12)', '=(a2/12)*b2', '=(b2/12)*a2'
                        ],
                        ratt_svar_visning="=A2*B2/12", ratt_svar="=A2*B2/12",
                        input_typ="text", svarstyp="kalkyl_formel"
                    )
                elif subtyp == 'E2_tot':
                    return Uppgift(
                        info_box_text="Titta på kalkylarket nedan:", info_box_style="blue",
                        html_table=tabell_html,
                        fraga="Vilken formel ska du skriva in i cell E2 för att kalkylarket ska räkna ut den totala månadskostnaden?",
                        ratt_svar_lista=['=c2+d2', '=d2+c2'],
                        ratt_svar_visning="=C2+D2", ratt_svar="=C2+D2",
                        input_typ="text", svarstyp="kalkyl_formel"
                    )
                elif subtyp == 'D2_amort':
                    return Uppgift(
                        info_box_text="Titta på kalkylarket nedan:", info_box_style="blue",
                        html_table=tabell_html,
                        fraga="Vilken formel ska du skriva in i cell D2 för att räkna ut amorteringen per månad? Tänk på att löptiden i F2 anges i år.",
                        ratt_svar_lista=[
                            '=a2/(f2*12)', '=a2/(12*f2)', '=(a2/f2)/12',
                            '=(a2/12)/f2', '=a2/f2/12', '=a2/12/f2'
                        ],
                        ratt_svar_visning="=A2/(F2*12)", ratt_svar="=A2/(F2*12)",
                        input_typ="text", svarstyp="kalkyl_formel"
                    )
                elif subtyp == 'tid_manader':
                    return Uppgift(
                        info_box_text="Titta på kalkylarket nedan:", info_box_style="blue",
                        html_table=tabell_html,
                        fraga="Du vill räkna ut hur många MÅNADER det tar att betala av hela lånet om du amorterar det belopp som står i cell D2. Vilken formel använder du?",
                        ratt_svar_lista=['=a2/d2'],
                        ratt_svar_visning="=A2/D2", ratt_svar="=A2/D2",
                        input_typ="text", svarstyp="kalkyl_formel"
                    )
                elif subtyp == 'F2_tid_ar':
                    return Uppgift(
                        info_box_text="Titta på kalkylarket nedan:", info_box_style="blue",
                        html_table=tabell_html,
                        fraga="Vilken formel kan du skriva i cell F2 för att räkna ut hur många ÅR lånet ska betalas tillbaka på, om du amorterar det belopp som står i D2 varje månad?",
                        ratt_svar_lista=[
                            '=(a2/d2)/12', '=a2/(d2*12)', '=(a2/12)/d2',
                            '=a2/d2/12', '=a2/12/d2', '=a2/(12*d2)'
                        ],
                        ratt_svar_visning="=(A2/D2)/12", ratt_svar="=(A2/D2)/12",
                        input_typ="text", svarstyp="kalkyl_formel"
                    )
    else:
        typ = random.choice(['manadskostnad_1', 'manadskostnad_2', 'snabblan'])
        if typ in ['manadskostnad_1', 'manadskostnad_2']:
            p = random.choice([
                {"K": 60000, "ar": 5, "amort": 1000, "rantor": [3, 6, 9]},
                {"K": 120000, "ar": 5, "amort": 2000, "rantor": [3, 6, 9]},
                {"K": 72000, "ar": 3, "amort": 2000, "rantor": [3, 4, 5, 6]}
            ])
            ranta = random.choice(p["rantor"])
            avgift = random.choice([25, 35, 45])
            if typ == 'manadskostnad_1':
                svar = int(round(p["amort"] + (p["K"] * (ranta / 100)) / 12 + avgift))
                return Uppgift(
                    info_box_text=f"Du köper en bil för {formatera_kr(p['K'])}\xa0kr på avbetalning. Lånet har rak amortering över {p['ar']}\xa0år och en årsränta på {ranta}\xa0%. Banken tar också ut en aviseringsavgift på {avgift}\xa0kr/månad.",
                    info_box_style="blue",
                    fraga="Vad blir din TOTALA månadskostnad den första månaden? (Svara i kr)",
                    ratt_svar=svar, input_typ="text", svarstyp="int", suffix="kr"
                )
            else:
                svar = int(round(p["amort"] + ((p["K"] - p["amort"]) * (ranta / 100)) / 12 + avgift))
                return Uppgift(
                    info_box_text=f"Du tar ett lån på {formatera_kr(p['K'])}\xa0kr med rak amortering över {p['ar']}\xa0år och en årsränta på {ranta}\xa0%. Aviseringsavgiften är {avgift}\xa0kr/månad.",
                    info_box_style="blue",
                    fraga="När du ska betala din ANDRA faktura har lånet minskat. Vad blir din TOTALA månadskostnad den andra månaden? (Svara i kr)",
                    ratt_svar=svar, input_typ="text", svarstyp="int", suffix="kr"
                )
        elif typ == 'snabblan':
            kapital = random.choice([3000, 4000, 5000, 8000])
            manadsranta = random.choice([2, 3, 4, 5])
            upplagg = random.choice([295, 395, 495])
            avi = random.choice([35, 45, 55])
            return Uppgift(
                info_box_text=f"Du tar ett snabblån på {formatera_kr(kapital)}\xa0kr som ska betalas tillbaka i sin helhet efter exakt en månad. Uppläggningsavgiften är {upplagg}\xa0kr, aviseringsavgiften {avi}\xa0kr och månadsräntan är {manadsranta}\xa0%.",
                info_box_style="blue",
                fraga="Hur mycket måste du totalt betala tillbaka när månaden är slut? (Svara i kr)",
                ratt_svar=int(round(kapital + kapital * (manadsranta / 100) + upplagg + avi)),
                input_typ="text", svarstyp="int", suffix="kr"
            )


def skapa_ff_uppgift(niva):
    if niva == 1:
        typ = random.choice(['berakna_ff', 'nytt_pris', 'hitta_procent'])

        if typ == 'berakna_ff':
            riktning = random.choice(['ökar', 'minskar'])
            procent = round(random.uniform(1.5, 80.5), 1) if random.choice([True, False]) else random.randint(5, 80)
            return Uppgift(
                info_box_text=f"Ett pris {riktning} med {f'{procent:g}'.replace('.', ',')}\xa0%.",
                info_box_style="green",
                fraga="Vad blir förändringsfaktorn? (Svara med decimaltal)",
                ratt_svar=round(1 + (procent / 100) if riktning == 'ökar' else 1 - (procent / 100), 4),
                input_typ="text", svarstyp="float"
            )

        elif typ == 'hitta_procent':
            riktning = random.choice(['ökar', 'minskar'])
            procent = round(random.uniform(1.5, 95.5), 1) if random.choice([True, False]) else random.randint(5, 95)
            ff = 1 + (procent / 100) if riktning == 'ökar' else 1 - (procent / 100)
            return Uppgift(
                info_box_text=f"En förändringsfaktor är {f'{round(ff, 4):g}'.replace('.', ',')}.",
                info_box_style="green",
                fraga="Vilken procentuell förändring motsvarar detta? (En sänkning svaras med minus, t.ex. -12,5)",
                ratt_svar=procent if riktning == 'ökar' else -procent,
                input_typ="text", svarstyp="procent"
            )

        elif typ == 'nytt_pris':
            startpris = random.choice([100, 200, 250, 400, 500, 800, 1000, 1500])
            riktning = random.choice(['höjs', 'sänks'])
            procent = random.choice([10, 15, 20, 25, 30, 40, 50, 12.5])
            nytt = int(round(startpris * (1 + procent / 100))) if riktning == 'höjs' else int(round(startpris * (1 - procent / 100)))
            return Uppgift(
                info_box_text=f"En vara kostar {startpris}\xa0kr. Priset {riktning} med {f'{procent:g}'.replace('.', ',')}\xa0%.",
                info_box_style="green",
                fraga="Vad blir det nya priset? (Svara i hela kronor)",
                ratt_svar=nytt,
                input_typ="text", svarstyp="int", suffix="kr"
            )

    else:
        typ = random.choice(['hitta_gammalt', 'upprepad_procent'])

        if typ == 'hitta_gammalt':
            gammalt_pris = random.choice([400, 500, 800, 1000, 1200, 1500, 2000])
            procent = random.choice([10, 20, 25, 30, 40, 50])
            riktning = random.choice(['höjs', 'sänks'])
            nytt_pris = int(round(gammalt_pris * (1 + procent / 100))) if riktning == 'höjs' else int(round(gammalt_pris * (1 - procent / 100)))
            return Uppgift(
                info_box_text=f"Efter att priset på en vara {riktning} med {procent}\xa0% kostar den nu {nytt_pris}\xa0kr.",
                info_box_style="green",
                fraga="Vad kostade varan från början? (Svara i hela kronor)",
                ratt_svar=gammalt_pris,
                input_typ="text", svarstyp="int", suffix="kr"
            )

        elif typ == 'upprepad_procent':
            p1 = random.choice([10, 20, 25, 30])
            p2 = random.choice([10, 20, 25, 30])
            r1 = random.choice(['ökar', 'minskar'])
            r2 = random.choice(['ökar', 'minskar'])
            f1 = (1 + p1 / 100) if r1 == 'ökar' else (1 - p1 / 100)
            f2 = (1 + p2 / 100) if r2 == 'ökar' else (1 - p2 / 100)
            return Uppgift(
                info_box_text=f"Priset på en produkt {r1} först med {p1}\xa0% och {r2} därefter med {p2}\xa0%.",
                info_box_style="green",
                fraga="Vad är den totala förändringsfaktorn för båda ändringarna tillsammans? (Svara med decimaltal)",
                ratt_svar=round(f1 * f2, 4),
                input_typ="text", svarstyp="float"
            )


def skapa_index_uppgift(niva):
    if niva == 1:
        typ = random.choice(['index_berakna', 'index_nytt_varde', 'index_procentuell_forandring'])

        if typ == 'index_berakna':
            P0 = random.choice([50, 100, 200, 250, 400, 500])
            idx_val = random.choice([110, 120, 125, 130, 140, 150])
            P1 = int(P0 * idx_val / 100)
            return Uppgift(
                info_box_text=f"Ett basår kostade en specifik vara {P0}\xa0kr. Några år senare kostar samma vara {P1}\xa0kr.",
                info_box_style="green",
                fraga="Vilket index har varan det senare året? (Svara med ett heltal)",
                ratt_svar=idx_val, input_typ="text", svarstyp="int"
            )

        elif typ == 'index_nytt_varde':
            P0 = random.choice([100, 200, 500, 1000, 2000, 5000])
            idx_val = random.choice([112, 115, 120, 130, 140, 150])
            P1 = int(P0 * idx_val / 100)
            return Uppgift(
                info_box_text=f"En vara kostade {P0}\xa0kr under basåret (då index alltid är 100). Ett senare år är index för varan {idx_val}.",
                info_box_style="green",
                fraga="Vad kostar varan det senare året? (Svara i kr)",
                ratt_svar=P1, input_typ="text", svarstyp="int", suffix="kr"
            )

        elif typ == 'index_procentuell_forandring':
            ans = random.choice(range(5, 155, 5))
            i1 = random.randint(5, 15) * 20
            i2 = int(round(i1 * (1 + ans / 100.0)))
            return Uppgift(
                info_box_text=f"Index för en viss vara var {i1} år 1 och {i2} år 2.",
                info_box_style="green",
                fraga="Med hur många procent ökade priset från år 1 till år 2?",
                ratt_svar=ans, input_typ="text", svarstyp="procent"
            )

    else:  # Nivå 2
        typ = random.choice(['index_byta_basar', 'index_reallon'])

        if typ == 'index_byta_basar':
            komb = [(120, 144, 120), (120, 150, 125), (125, 150, 120), (140, 168, 120), (150, 180, 120), (150, 195, 130)]
            old_i2, old_i3, new_i3 = random.choice(komb)
            return Uppgift(
                info_box_text=f"I en indextabell är index 100 för år 1, {old_i2} för år 2, och {old_i3} för år 3. Man bestämmer sig sedan för att byta basår till år 2.",
                info_box_style="green",
                fraga="Vilket index får år 3 i den nya tabellen?",
                ratt_svar=new_i3, input_typ="text", svarstyp="int"
            )

        elif typ == 'index_reallon':
            kpi = random.choice([110, 120, 125, 140, 150])
            lon_faktor = random.choice([1.05, 1.1, 1.15, 1.2])
            base_lon = random.choice([20000, 25000, 30000, 35000])
            new_lon = int(base_lon * (kpi / 100) * lon_faktor)
            reallon = int(new_lon / (kpi / 100))
            return Uppgift(
                info_box_text=f"År 1 är KPI 100 och din månadslön är {formatera_kr(base_lon)}\xa0kr. År 2 är KPI {kpi} och din lön har ökat till {formatera_kr(new_lon)}\xa0kr.",
                info_box_style="green",
                fraga="Vad är din lön år 2 omräknad till penningvärdet för år 1 (så kallad reallön)?",
                ratt_svar=reallon, input_typ="text", svarstyp="int", suffix="kr"
            )


def skapa_procent_vs_enheter_uppgift(niva=1):
    if niva == 1:
        typ = random.choice(['rantehojning', 'valbarometern', 'batteriladdning', 'skattesankning'])

        if typ == 'rantehojning':
            start = random.choice([1.5, 2.0, 2.5, 3.0])
            hojning_enheter = random.choice([0.5, 1.0, 1.5])
            ny_ranta = round(start + hojning_enheter, 1)
            relativ = int(round((hojning_enheter / start) * 100))

            fraga_typ = random.choice(['enheter', 'procent'])
            info = f"Banken höjer räntan på ditt bolån från {str(start).replace('.', ',')}\xa0% till {str(ny_ranta).replace('.', ',')}\xa0%."

            if fraga_typ == 'enheter':
                return Uppgift(
                    info_box_text=info, info_box_style="blue",
                    fraga="Med hur många procentenheter har räntan höjts?",
                    ratt_svar=hojning_enheter, input_typ="text", svarstyp="float", suffix="procentenheter"
                )
            else:
                return Uppgift(
                    info_box_text=info, info_box_style="blue",
                    fraga="Med hur många procent har din räntekostnad ökat?",
                    ratt_svar=relativ, input_typ="text", svarstyp="int", suffix="%"
                )

        elif typ == 'valbarometern':
            start = random.choice([4.0, 5.0, 8.0])
            nytt = start + random.choice([1.0, 2.0])
            relativ = int(round(((nytt - start) / start) * 100))

            info = (
                f"Ett politiskt parti ökar sitt väljarstöd från {str(start).replace('.', ',')}\xa0% till {str(nytt).replace('.', ',')}\xa0% i en ny mätning.<br><br>"
                f"Partiledaren jublar i en intervju och säger: <i>'Fantastiskt! Vårt stöd har ökat med {relativ}\xa0%!'</i><br><br>"
                f"En politisk motståndare twittrar: <i>'Vilken överdrift, ni har ju bara ökat med {str(nytt - start).replace('.', ',')}\xa0%.'</i>"
            )
            ratt = "Bara partiledaren (motståndaren blandar ihop % och procentenheter)"
            alts = [ratt, "Bara den politiska motståndaren", "Båda har rätt", "Båda har fel"]
            random.shuffle(alts)
            return Uppgift(
                info_box_text=info, info_box_style="blue",
                fraga="Vem uttrycker sig matematiskt korrekt?",
                ratt_svar=ratt, alternativ=alts, input_typ="radio", svarstyp="string"
            )

        elif typ == 'batteriladdning':
            start = random.choice([10, 20, 25, 40])
            okning = random.choice([20, 30, 40, 50])
            nytt = start + okning
            relativ = int(round((okning / start) * 100))

            info = f"Du sätter din mobil på laddning. Batterinivån går från {start}\xa0% till {nytt}\xa0%."
            return Uppgift(
                info_box_text=info, info_box_style="blue",
                fraga="Hur stor är den procentuella (relativa) ökningen av din batterinivå?",
                ratt_svar=relativ, input_typ="text", svarstyp="int", suffix="%"
            )

        elif typ == 'skattesankning':
            ny = random.choice([30.0, 31.5, 32.0, 33.5])
            sankning = random.choice([0.5, 1.0, 1.5])
            gammal = round(ny + sankning, 1)

            info = f"Din kommun beslutar sig för att sänka kommunalskatten med {str(sankning).replace('.', ',')}\xa0procentenheter. Efter sänkningen är skatten {str(ny).replace('.', ',')}\xa0%."
            return Uppgift(
                info_box_text=info, info_box_style="blue",
                fraga="Vad var kommunalskatten innan sänkningen?",
                ratt_svar=gammal, input_typ="text", svarstyp="float", suffix="%"
            )

    else:  # Nivå 2
        typ = random.choice(['baklanges', 'flersteg', 'jamforelse', 'indexfalla'])
        if typ == 'baklanges':
            start = random.choice([4.0, 5.0, 6.0, 8.0])
            okning_enheter = random.choice([1.0, 1.5, 2.0])
            relativ_proc = int(round((okning_enheter / start) * 100))

            info = (
                f"Ett politiskt parti ökar sitt väljarstöd med {str(okning_enheter).replace('.', ',')}\xa0procentenheter i den senaste mätningen.<br><br>"
                f"Partiledaren är väldigt nöjd, eftersom detta motsvarar en relativ ökning av deras väljarstöd med exakt {relativ_proc}\xa0%."
            )
            return Uppgift(
                info_box_text=info, info_box_style="blue",
                fraga="Vad var partiets väljarstöd (i procent) INNAN ökningen?",
                ratt_svar=start, input_typ="text", svarstyp="float", suffix="%"
            )

        elif typ == 'flersteg':
            start = random.choice([3.0, 4.0, 5.0])
            relativ_okning = random.choice([20, 25, 50])
            ny_ranta_1 = start * (1 + relativ_okning / 100.0)
            sankning_enheter = random.choice([0.5, 1.0])
            slut_ranta = round(ny_ranta_1 - sankning_enheter, 2)

            info = f"En bank har en bolåneränta på {str(start).replace('.', ',')}\xa0%. Först höjer de räntan med {relativ_okning}\xa0% (en relativ höjning). Ett halvår senare sänker de den nya räntan med {str(sankning_enheter).replace('.', ',')}\xa0procentenheter."
            return Uppgift(
                info_box_text=info, info_box_style="blue",
                fraga="Vad är den nya räntan efter båda ändringarna?",
                ratt_svar=slut_ranta, input_typ="text", svarstyp="float", suffix="%"
            )

        elif typ == 'jamforelse':
            start_A = random.choice([20, 25])
            start_B = random.choice([30, 40])
            relativ_okning_A = random.choice([40, 50, 60])
            okning_enheter_B = random.choice([4, 5, 6])

            ny_A = start_A * (1 + relativ_okning_A / 100.0)
            ny_B = start_B + okning_enheter_B
            diff = int(abs(ny_A - ny_B))

            info = (
                f"På en skola cyklar {start_A}\xa0% av tjejerna och {start_B}\xa0% av killarna till skolan.<br><br>"
                f"Efter en kampanj för bättre hälsa ökar andelen tjejer som cyklar med {relativ_okning_A}\xa0% (relativ ökning). Samtidigt ökar andelen killar som cyklar med {okning_enheter_B}\xa0procentenheter."
            )
            return Uppgift(
                info_box_text=info, info_box_style="blue",
                fraga="Vad är skillnaden i procentenheter mellan tjejernas och killarnas nya andelar?",
                ratt_svar=diff, input_typ="text", svarstyp="int", suffix="procentenheter"
            )

        elif typ == 'indexfalla':
            start_index = random.choice([150, 200, 250])
            okning_enheter = random.choice([6, 8, 10, 15])
            nytt_index = start_index + okning_enheter
            faktisk_proc = int(round((okning_enheter / start_index) * 100))

            info = f"Prisindex för en kaffemaskin har gått från {start_index} till {nytt_index}. En butiksägare påstår att maskinens pris har ökat med {okning_enheter}\xa0% eftersom {nytt_index} - {start_index} = {okning_enheter}."
            return Uppgift(
                info_box_text=info, info_box_style="blue",
                fraga="Butiksägaren räknar fel. Vad är den faktiska procentuella prishöjningen?",
                ratt_svar=faktisk_proc, input_typ="text", svarstyp="int", suffix="%"
            )


def skapa_problemlosning_uppgift(niva):
    namn_lista = ["Charlie", "Kim", "Ali", "Maja", "Sami", "Robin", "Nilo", "Alex", "Noa", "Elsa", "Viktor"]

    if niva == 1:
        typ = random.choice([
            'hyra_fordon', 'vardeminskning', 'pannkakor_proportion', 'valuta_omvandling',
            'jamfora_abonnemang', 'vattenlackage', 'upprepad_procent_rea',
            'enhetsomvandling_regn', 'formel_kokpunkt', 'enkel_tidszon_resa', 'jamforpris',
            'monster_kuber_1', 'lon_och_ob', 'steg_genomsnitt', 'linjar_vs_exponentiell'
        ])
        if typ == 'steg_genomsnitt':
            namn = random.choice(namn_lista)
            mal_snitt = random.randint(80, 120) * 100
            diff = random.choice([-800, -600, -500, -400, -200, -100, 100, 200])
            snitt_6_dagar = mal_snitt + diff
            svar = (mal_snitt * 7) - (snitt_6_dagar * 6)

            info = f"{namn} har som mål att under en vecka (7 dagar) gå i genomsnitt {formatera_kr(mal_snitt)}\xa0steg per dag.<br><br>Under de sex första dagarna har hen gått i genomsnitt {formatera_kr(snitt_6_dagar)}\xa0steg per dag."
            return Uppgift(
                info_box_text=info, info_box_style="blue",
                fraga="Hur många steg behöver hen minst gå den sjunde dagen för att nå sitt mål?",
                ratt_svar=svar, input_typ="text", svarstyp="int", suffix="steg",
                undertext="Lös uppgiften med huvudräkning (utan miniräknare)."
            )

        elif typ == 'linjar_vs_exponentiell':
            linjara = [
                "En bilhyra kostar 300 kr i grundavgift och 20 kr per mil.",
                "En snickare tar 450 kr i framkörningsavgift och sedan 600 kr i timmen.",
                "Du sparar 500 kr varje månad på ett räntefritt konto.",
                "En vattentank töms med exakt 15 liter vatten i minuten.",
                "En solros växer i genomsnitt 2 cm per dygn.",
                "Priset på en biobiljett höjs med 5 kr varje år."
            ]
            exponentiella = [
                "Värdet på en moped minskar med 15 % varje år.",
                "Antalet bakterier i en odling fördubblas varje timme.",
                "Ett radioaktivt ämne halveras i massa var sjätte månad.",
                "Du sätter in pengar på en fond som växer med 6 % i genomsnitt per år.",
                "En kaninpopulation blir tre gånger så stor varje år.",
                "Ett isberg förlorar en tiondel av sin volym varje vecka."
            ]

            typ_A = random.choice(['linjar', 'exponentiell'])
            text_A = random.choice(linjara) if typ_A == 'linjar' else random.choice(exponentiella)

            typ_B = random.choice(['linjar', 'exponentiell'])
            while True:
                text_B = random.choice(linjara) if typ_B == 'linjar' else random.choice(exponentiella)
                if text_A != text_B:
                    break

            info = f"<b>Händelse A:</b> {text_A}<br><br><b>Händelse B:</b> {text_B}"

            if typ_A == 'exponentiell' and typ_B == 'linjar':
                ratt = "Bara händelse A"
            elif typ_A == 'linjar' and typ_B == 'exponentiell':
                ratt = "Bara händelse B"
            elif typ_A == 'exponentiell' and typ_B == 'exponentiell':
                ratt = "Båda händelserna"
            else:
                ratt = "Ingen av händelserna"

            alts = ["Bara händelse A", "Bara händelse B", "Båda händelserna", "Ingen av händelserna"]

            return Uppgift(
                info_box_text=info,
                info_box_style="blue",
                fraga="Vilken eller vilka av händelserna beskriver en exponentiell förändring?",
                ratt_svar=ratt,
                alternativ=alts,
                input_typ="radio",
                svarstyp="string",
                undertext="Tänk på att en exponentiell förändring innebär en relativ förändring (samma faktor/procent varje gång), medan en linjär är en absolut förändring (samma belopp/antal varje gång)."
            )

        elif typ == 'lon_och_ob':
            namn = random.choice(namn_lista)
            grundlon = random.randint(100, 150)
            vardag_tim = random.randint(10, 20)
            helg_tim = random.randint(5, 12)
            skatt_procent = random.choice([25, 30, 32, 35])

            brutto_vardag = grundlon * vardag_tim
            brutto_helg = (grundlon * 1.5) * helg_tim
            brutto_total = brutto_vardag + brutto_helg
            netto = brutto_total * (1 - skatt_procent / 100)

            info = f"{namn} jobbar extra på helgerna. Hen har en grundlön på {grundlon}\xa0kr/h. På söndagar får hen dessutom 50\xa0% i OB-tillägg.<br><br>Förra månaden jobbade {namn} {vardag_tim}\xa0timmar på vanliga vardagar och {helg_tim}\xa0timmar på söndagar. Kommunalskatten dras med {skatt_procent}\xa0%."
            return Uppgift(
                info_box_text=info, info_box_style="blue",
                fraga=f"Hur mycket pengar fick {namn} totalt behålla efter att skatten dragits?",
                ratt_svar=int(round(netto)), input_typ="text", svarstyp="int", suffix="kr",
                undertext="Lös uppgiften i flera steg på papper."
            )

        elif typ == 'monster_kuber_1':
            monster_typ = random.choice([1, 2, 3])
            fig_graf = rita_mönster_kuber(4, monster_typ)
            info = "Bilden visar ett mönster byggt av vita och grå kuber. Kika noga på hur mönstret växer från Figur 1 till Figur 4."
            target_fig = random.choice([5, 6, 7])
            fraga_fokus = random.choice(['vita', 'grå', 'totala'])

            if monster_typ == 1:
                vita = target_fig**2
                gra = int(target_fig * (target_fig - 1) / 2)
                tot = vita + gra
            elif monster_typ == 2:
                vita = (target_fig + 1)**2
                gra = target_fig**2
                tot = vita + gra
            else:  # typ 3
                tot = target_fig**2
                vita = int(target_fig * (target_fig + 1) / 2)
                gra = int(target_fig * (target_fig - 1) / 2)

            if fraga_fokus == 'vita':
                svar = vita
                fraga = f"Hur många VITA kuber kommer det att finnas i Figur {target_fig}?"
            elif fraga_fokus == 'grå':
                svar = gra
                fraga = f"Hur många GRÅ kuber kommer det att finnas i Figur {target_fig}?"
            else:
                svar = tot
                fraga = f"Hur många kuber kommer det att finnas TOTALT i Figur {target_fig}?"

            return Uppgift(
                info_box_text=info, info_box_style="blue", plotly_fig=fig_graf,
                fraga=fraga, ratt_svar=svar, input_typ="text", svarstyp="int",
                undertext="Lös uppgiften på papper (utan miniräknare). Ett tips är att skriva upp en tabell."
            )

        elif typ == 'hyra_fordon':
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
            info = f"{namn} ska hyra en {fordon}. Startavgiften är {formatera_kr(start)}\xa0kr. Dessutom kostar det {mil_kost}\xa0kr för varje mil hen kör."
            return Uppgift(
                info_box_text=info, info_box_style="blue",
                fraga="Vilken formel beskriver den totala kostnaden y kr för x mil som körs?",
                ratt_svar=f"${ratt}$", alternativ=alts, input_typ="radio", svarstyp="string",
                undertext="Lös uppgiften med huvudräkning (utan miniräknare)."
            )

        elif typ == 'vardeminskning':
            fordon = random.choice(["bil", "båt", "husvagn", "traktor", "motorcykel"])
            pris = random.randint(15, 60) * 10000
            procent = random.randint(10, 25)
            ff = round((100 - procent) / 100.0, 2)
            info = f"En {fordon} kostar {formatera_kr(pris)}\xa0kr i inköpspris. Värdet minskar med {procent}\xa0% per år."
            return Uppgift(
                info_box_text=info, info_box_style="blue",
                fraga="Skriv ett uttryck som beskriver värdet i kronor x år efter inköp.",
                ratt_svar=f"{pris}*{ff}**x", input_typ="text", svarstyp="string_math",
                undertext="Ange uttrycket med x som variabel och ^ för upphöjt till (t.ex. 500*0,8^x).\nLös uppgiften med huvudräkning (utan miniräknare)."
            )

        elif typ == 'pannkakor_proportion':
            kombinationer = [
                (4, 200, 6), (6, 300, 4), (8, 400, 6), (6, 400, 9),
                (10, 500, 15), (4, 200, 10), (6, 150, 10)
            ]
            personer_start, mjol, personer_mal = random.choice(kombinationer)
            svar = int((mjol / personer_start) * personer_mal)
            info = f"Ett recept för {personer_start}\xa0portioner kräver {mjol}\xa0gram mjöl."
            return Uppgift(
                info_box_text=info, info_box_style="blue",
                fraga=f"Hur mycket mjöl krävs om man ska laga {personer_mal}\xa0portioner?",
                ratt_svar=svar, input_typ="text", svarstyp="int", suffix="gram",
                undertext="Lös uppgiften med huvudräkning (utan miniräknare)."
            )

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
            info = f"{namn1} växlar {sek_A}\xa0kr till {valuta_namn} ({valuta_kod}) och får {formatera_kr(val_A)}\xa0{valuta_kod}.<br><br>{namn2} växlar {sek_B}\xa0kr till samma kurs."
            return Uppgift(
                info_box_text=info, info_box_style="blue",
                fraga=f"Hur mycket får {namn2}?",
                ratt_svar=val_B, input_typ="text", svarstyp="int", suffix=valuta_kod,
                undertext="Lös uppgiften med huvudräkning (utan miniräknare)."
            )

        elif typ == 'jamforpris':
            vara = random.choice(['lösgodis', 'kaffebönor', 'naturgodis', 'teblad', 'brända mandlar'])
            combos = [
                (150, 24, 160), (300, 42, 140), (120, 18, 150),
                (250, 35, 140), (400, 36, 90), (200, 17, 85), (150, 21, 140)
            ]
            vikt, pris, kilopris = random.choice(combos)
            info = f"En påse med {vara} som väger {vikt}\xa0gram kostar {pris}\xa0kr."
            return Uppgift(
                info_box_text=info, info_box_style="blue",
                fraga="Vad är priset per kilogram (kg)?",
                ratt_svar=kilopris, input_typ="text", svarstyp="int", suffix="kr/kg",
                undertext="Lös uppgiften med huvudräkning (utan miniräknare)."
            )

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
            ankomst_lokal_tid = (ankomst_svensk_tid + (destination["tidsskillnad"] * 60)) % (24 * 60)
            ankomst_h = ankomst_lokal_tid // 60
            ankomst_m = ankomst_lokal_tid % 60
            avresa_str = f"{avresa_h:02d}:{avresa_m:02d}"
            restid_str = f"{restid_h}h {restid_m_rest}min"
            diff_str = f"+{destination['tidsskillnad']}h" if destination['tidsskillnad'] > 0 else f"{destination['tidsskillnad']}h"
            info = f"Du reser från Stockholm kl. {avresa_str} och resan till {destination['stad']} tar {restid_str}."
            fraga = f"Vad är klockan lokalt i {destination['stad']} när du landar om tidsskillnaden är {diff_str}? (Svara i formatet HH:MM)"
            svar = f"{ankomst_h:02d}:{ankomst_m:02d}"
            return Uppgift(
                info_box_text=info, info_box_style="blue", fraga=fraga,
                ratt_svar=svar, input_typ="text", svarstyp="string",
                undertext="Svara med klockslag i formatet HH:MM (till exempel 08:30 eller 15:00)."
            )

        elif typ == 'jamfora_abonnemang':
            R_B = random.choice([30, 40, 50])
            R_A = R_B + random.choice([20, 30, 40])
            visits = random.choice([4, 5, 6, 8, 10])
            F_A = random.choice([100, 150, 200, 250])
            F_B = F_A + visits * (R_A - R_B)
            info = f"Du funderar på att skaffa gymkort.<br><br>&bull; <b>Gym A</b> tar {F_A}\xa0kr i fast månadsavgift och sedan {R_A}\xa0kr per träningspass.<br>&bull; <b>Gym B</b> tar {F_B}\xa0kr i fast månadsavgift och sedan {R_B}\xa0kr per träningspass."
            return Uppgift(
                info_box_text=info, info_box_style="blue",
                fraga="Vid exakt hur många träningspass under en månad kostar de båda gymmen lika mycket?",
                ratt_svar=visits, input_typ="text", svarstyp="int", suffix="pass",
                undertext="Lös uppgiften på papper (utan miniräknare)."
            )

        elif typ == 'vattenlackage':
            start_vol = random.randint(10, 50) * 10
            leak = random.randint(2, 8)
            info = f"En vattentunna innehåller från början {start_vol}\xa0liter vatten. Det har gått hål i botten och tunnan läcker därefter {leak}\xa0liter per minut."
            return Uppgift(
                info_box_text=info, info_box_style="blue",
                fraga="Skriv ett algebraiskt uttryck för volymen vatten (i liter) som finns kvar i tunnan efter t minuter.",
                ratt_svar=f"{start_vol} - {leak}*t", input_typ="text", svarstyp="string_math",
                undertext="Använd t som variabel. Lös uppgiften med huvudräkning (utan miniräknare)."
            )

        elif typ == 'upprepad_procent_rea':
            rea1 = random.choice([20, 30, 40])
            rea2 = random.choice([10, 20, 25])
            rabatt_total = 100 - 100 * (1 - rea1 / 100.0) * (1 - rea2 / 100.0)
            info = f"En klädbutik har en stor utförsäljning med {rea1}\xa0% rabatt på alla varor i butiken. Eftersom du är VIP-medlem får du dessutom ytterligare {rea2}\xa0% rabatt i kassan på det redan sänkta priset."
            return Uppgift(
                info_box_text=info, info_box_style="blue",
                fraga="Hur stor blir den TOTALA rabatten i procent från varans ursprungspris?",
                ratt_svar=int(round(rabatt_total)), input_typ="text", svarstyp="procent", suffix="%",
                undertext="Lös uppgiften med huvudräkning (utan miniräknare)."
            )

        elif typ == 'enhetsomvandling_regn':
            area = random.choice([50, 100, 150, 200, 500])
            regn = random.choice([2, 5, 8, 10, 12, 15])
            svar = area * regn
            info = f"Ett kraftigt regnoväder drar in och det faller {regn}\xa0mm regn över ett platt tak som har arean {area}\xa0m²."
            return Uppgift(
                info_box_text=info, info_box_style="blue",
                fraga="Hur många liter vatten har det fallit på taket?",
                ratt_svar=svar, input_typ="text", svarstyp="int", suffix="liter",
                undertext="Tips: 1 liter är detsamma som 1 kubikdecimeter (dm³). Lös uppgiften med huvudräkning."
            )

        elif typ == 'formel_kokpunkt':
            fraga_typ = random.choice(['hitta_t', 'hitta_h'])
            if fraga_typ == 'hitta_t':
                h = random.choice([1500, 3000, 4500, 6000])
                t = int(100 - h / 300)
                info = f"Vattnets kokpunkt <i>t</i> (i °C) beror på höjden över havet <i>h</i> (i meter) enligt formeln:<br><br><b>t = 100 - h/300</b><br><br>Du befinner dig på ett berg på {formatera_kr(h)}\xa0meters höjd."
                return Uppgift(
                    info_box_text=info, info_box_style="blue",
                    fraga="Vid vilken temperatur kokar vattnet där du är?",
                    ratt_svar=t, input_typ="text", svarstyp="int", suffix="°C"
                )
            else:
                t = random.choice([80, 85, 90, 95])
                h = (100 - t) * 300
                info = f"Vattnets kokpunkt <i>t</i> (i °C) beror på höjden över havet <i>h</i> (i meter) enligt formeln:<br><br><b>t = 100 - h/300</b><br><br>Du kokar vatten uppe på ett berg och märker att det börjar koka redan vid {t}\xa0°C."
                return Uppgift(
                    info_box_text=info, info_box_style="blue",
                    fraga="På ungefär vilken höjd över havet befinner du dig?",
                    ratt_svar=h, input_typ="text", svarstyp="int", suffix="meter"
                )

    else:  # Nivå 2
        typ = random.choice([
            'pizza_brak', 'algebraisk_forstaelse', 'monster_stickor', 'monster_kuber_2', 'tolka_uttryck_rabatt',
            'tidsvinst_hastighet', 'area_uttryck', 'medelfart', 'relativ_procent', 'valgorenhet',
            'omvanda_proportioner', 'pizza_area', 'kakla_rum', 'handskakningar', 'blanda_saft', 'bil_vs_elbil'
        ])

        if typ == 'bil_vs_elbil':
            namn = random.choice(namn_lista)
            bensin_forbrukning = round(random.uniform(0.5, 0.8), 1)
            bensin_pris = random.choice([18, 19, 20, 21])
            el_forbrukning = round(random.uniform(1.5, 2.5), 1)
            el_pris = round(random.uniform(2.0, 4.0), 1)

            kostnad_bensin_per_mil = bensin_forbrukning * bensin_pris
            kostnad_el_per_mil = el_forbrukning * el_pris

            skillnad_per_mil = kostnad_bensin_per_mil - kostnad_el_per_mil
            if skillnad_per_mil <= 0:
                return skapa_problemlosning_uppgift(niva)

            fasta_kostnader_el_extra = random.randint(300, 800) * 10
            mil_for_breakeven = int(round(fasta_kostnader_el_extra / skillnad_per_mil))

            info = (
                f"{namn} funderar på att byta sin bensinbil mot en elbil.<br><br>"
                f"&bull; Bensinbilen drar {bensin_forbrukning}\xa0liter/mil och bensinen kostar {bensin_pris}\xa0kr/liter.<br>"
                f"&bull; Elbilen drar {el_forbrukning}\xa0kWh/mil och elen kostar i snitt {el_pris:.2f}\xa0kr/kWh.<br><br>"
                f"Elbilen är dock dyrare i inköp och försäkring, vilket ger en extra fast kostnad på {formatera_kr(fasta_kostnader_el_extra)}\xa0kr om året jämfört med bensinbilen."
            )
            return Uppgift(
                info_box_text=info.replace('.', ','), info_box_style="blue",
                fraga="Vid exakt hur många körda mil per år blir de båda bilarna lika dyra totalt sett?",
                ratt_svar=mil_for_breakeven, input_typ="text", svarstyp="int", suffix="mil",
                undertext="Ställ upp en ekvation. Avrunda ditt svar till närmaste heltal om det behövs."
            )

        elif typ == 'blanda_saft':
            vol1 = random.choice([1, 2, 3])
            halt1 = random.choice([10, 15, 20])
            vol2 = random.choice([2, 3, 4, 5])
            while vol1 == vol2:
                vol2 = random.randint(2, 5)
            halt2 = random.choice([25, 30, 40])

            socker_total = (vol1 * halt1) + (vol2 * halt2)
            vol_total = vol1 + vol2
            ny_halt = socker_total / vol_total

            while not ny_halt.is_integer():
                vol1 = random.choice([1, 2, 3])
                halt1 = random.choice([10, 15, 20])
                vol2 = random.choice([2, 3, 4, 5])
                halt2 = random.choice([25, 30, 40])
                socker_total = (vol1 * halt1) + (vol2 * halt2)
                vol_total = vol1 + vol2
                ny_halt = socker_total / vol_total

            info = f"Du har {vol1}\xa0liter saft som har en sockerhalt på {halt1}\xa0%. Du häller därefter i {vol2}\xa0liter av en annan saft som har sockerhalten {halt2}\xa0%."
            return Uppgift(
                info_box_text=info, info_box_style="blue",
                fraga="Vilken sockerhalt (i procent) får den nya, färdiga blandningen?",
                ratt_svar=int(ny_halt), input_typ="text", svarstyp="int", suffix="%",
                undertext="Tips: Räkna ut hur mycket 'ren socker' som finns totalt först."
            )

        elif typ == 'handskakningar':
            n = random.randint(6, 12)
            svar = int(n * (n - 1) / 2)
            scenario_typ = random.choice(['sport', 'fest'])
            if scenario_typ == 'sport':
                sport = random.choice(['innebandyserie', 'fotbollsturnering', 'schackturnering'])
                info = f"I en {sport} med {n}\xa0lag (eller spelare) ska alla möta varandra exakt en gång."
                fraga = "Hur många matcher spelas det totalt i turneringen?"
            else:
                info = f"På ett affärsmöte deltar {n}\xa0personer. Innan mötet börjar hälsar alla på varandra genom att skaka hand med alla andra exakt en gång."
                fraga = "Hur många handskakningar blir det totalt?"
            return Uppgift(
                info_box_text=info, info_box_style="blue", fraga=fraga,
                ratt_svar=svar, input_typ="text", svarstyp="int",
                undertext="Börja gärna med att rita upp hur det fungerar för 3 eller 4 personer."
            )

        elif typ == 'kakla_rum':
            langd = random.choice([2.4, 3.0, 3.6, 4.2])
            bredd = random.choice([2.0, 2.5, 3.0])
            sida_cm = random.choice([10, 20, 30])

            area_m2 = langd * bredd
            sida_m = sida_cm / 100
            area_platta_m2 = sida_m * sida_m
            antal_plattor = int(round(area_m2 / area_platta_m2))

            info = f"Ett badrumsgolv är rektangulärt och har måtten {str(langd).replace('.', ',')}\xa0meter gånger {str(bredd).replace('.', ',')}\xa0meter.<br><br>Golvet ska täckas med kvadratiska kakelplattor som är {sida_cm}\xa0cm x {sida_cm}\xa0cm."
            return Uppgift(
                info_box_text=info, info_box_style="blue",
                fraga="Hur många kakelplattor går det åt (om vi bortser från fogar och spill)?",
                ratt_svar=antal_plattor, input_typ="text", svarstyp="int", suffix="st",
                undertext="Håll tungan rätt i mun när du omvandlar mellan längdenheter och areaenheter!"
            )

        elif typ == 'pizza_area':
            d_liten = random.choice([20, 25])
            d_stor = d_liten * 2

            info = f"Pizzeria Napoli säljer små pizzor med diametern {d_liten}\xa0cm och stora familjepizzor med diametern {d_stor}\xa0cm. Tjockleken är densamma."
            ratt = "Familjepizzan är exakt lika stor som FYRA små pizzor tillsammans."
            alts = [
                ratt,
                "Familjepizzan är exakt lika stor som TVÅ små pizzor tillsammans.",
                "Familjepizzan är exakt lika stor som TRE små pizzor tillsammans.",
                "Det går inte att jämföra arean utan att veta pizzans radie."
            ]
            random.shuffle(alts)
            return Uppgift(
                info_box_text=info, info_box_style="blue",
                fraga="Vilket av följande påståenden om pizzornas storlek (area) är matematiskt korrekt?",
                ratt_svar=ratt, alternativ=alts, input_typ="radio", svarstyp="string"
            )

        elif typ == 'omvanda_proportioner':
            n_start = random.choice([4, 6])
            dagar_start = random.choice([6, 8, 12])
            arbetstimmar = n_start * dagar_start
            n_ny = n_start - random.choice([1, 2])

            while arbetstimmar % n_ny != 0:
                n_ny -= 1
                if n_ny == 1:
                    break

            dagar_ny = int(arbetstimmar / n_ny)
            yrke = random.choice(['målare', 'snickare', 'programmerare'])
            jobb = random.choice(['måla om en skola', 'bygga ett hus', 'skriva en app'])

            info = f"{n_start} stycken {yrke} behöver arbeta i {dagar_start}\xa0dagar för att {jobb}.<br><br>Inför ett exakt likadant jobb nästa månad blir några sjuka, så de är bara {n_ny} stycken {yrke} som kan arbeta. De jobbar i samma tempo som tidigare."
            return Uppgift(
                info_box_text=info, info_box_style="blue",
                fraga="Hur många dagar tar det för den mindre gruppen att göra klart jobbet?",
                ratt_svar=dagar_ny, input_typ="text", svarstyp="int", suffix="dagar",
                undertext="Lös uppgiften på papper. Tänk på vad som händer med tiden när antalet personer minskar."
            )

        elif typ == 'monster_kuber_2':
            monster_typ = random.choice([1, 2, 3])
            fig_graf = rita_mönster_kuber(4, monster_typ)
            info = "Bilden visar ett mönster byggt av vita och grå kuber. Kika noga på hur mönstret växer från Figur 1 till Figur 4."
            fraga_fokus = random.choice(['vita', 'grå', 'totala'])

            if monster_typ == 1:
                formel_vita = "n**2"
                formel_gra = "\\frac{n(n-1)}{2}"
                formel_tot = "n^2 + \\frac{n(n-1)}{2}"
            elif monster_typ == 2:
                formel_vita = "(n+1)**2"
                formel_gra = "n**2"
                formel_tot = "(n+1)^2 + n^2"
            else:  # typ 3
                formel_tot = "n**2"
                formel_vita = "\\frac{n(n+1)}{2}"
                formel_gra = "\\frac{n(n-1)}{2}"

            if fraga_fokus == 'vita':
                if monster_typ == 1:
                    return Uppgift(
                        info_box_text=info, info_box_style="blue", plotly_fig=fig_graf,
                        fraga="Skriv ett algebraiskt uttryck för antalet VITA kuber i figur n.",
                        ratt_svar=formel_vita, input_typ="text", svarstyp="string_math",
                        undertext="Använd n som variabel."
                    )
                elif monster_typ == 2:
                    return Uppgift(
                        info_box_text=info, info_box_style="blue", plotly_fig=fig_graf,
                        fraga="Skriv ett algebraiskt uttryck för antalet VITA kuber i figur n.",
                        ratt_svar=formel_vita, input_typ="text", svarstyp="string_math",
                        undertext="Använd n som variabel. T.ex. (n+2)^2"
                    )
                else:
                    ratt = formel_vita
                    alts = [f"${ratt}$", r"$\frac{n(n-1)}{2}$", r"$\frac{n^2}{2}$", "$n^2+1$"]
                    random.shuffle(alts)
                    return Uppgift(
                        info_box_text=info, info_box_style="blue", plotly_fig=fig_graf,
                        fraga="Vilket uttryck beskriver antalet VITA kuber i figur n?",
                        ratt_svar=f"${ratt}$", alternativ=alts, input_typ="radio", svarstyp="string",
                        undertext="Börja gärna med att ställa upp tabellvärden på ett papper."
                    )
            elif fraga_fokus == 'grå':
                if monster_typ == 2:
                    return Uppgift(
                        info_box_text=info, info_box_style="blue", plotly_fig=fig_graf,
                        fraga="Skriv ett algebraiskt uttryck för antalet GRÅ kuber i figur n.",
                        ratt_svar=formel_gra, input_typ="text", svarstyp="string_math",
                        undertext="Använd n som variabel."
                    )
                else:
                    ratt = formel_gra
                    alts = [f"${ratt}$", r"$\frac{n(n+1)}{2}$", r"$\frac{n^2}{2}$", "$n^2-1$"]
                    random.shuffle(alts)
                    return Uppgift(
                        info_box_text=info, info_box_style="blue", plotly_fig=fig_graf,
                        fraga="Vilket uttryck beskriver antalet GRÅ kuber i figur n?",
                        ratt_svar=f"${ratt}$", alternativ=alts, input_typ="radio", svarstyp="string",
                        undertext="Börja gärna med att ställa upp tabellvärden på ett papper."
                    )
            else:  # totala
                if monster_typ == 3:
                    return Uppgift(
                        info_box_text=info, info_box_style="blue", plotly_fig=fig_graf,
                        fraga="Skriv ett algebraiskt uttryck för antalet kuber TOTALT i figur n.",
                        ratt_svar=formel_tot, input_typ="text", svarstyp="string_math",
                        undertext="Använd n som variabel."
                    )
                elif monster_typ == 1:
                    ratt = formel_tot
                    d1 = r"n^2 + \frac{n(n+1)}{2}"
                    d2 = "n^2 + n - 1"
                    d3 = "2n^2 - n"
                    alts = [f"${ratt}$", f"${d1}$", f"${d2}$", f"${d3}$"]
                    random.shuffle(alts)
                    return Uppgift(
                        info_box_text=info, info_box_style="blue", plotly_fig=fig_graf,
                        fraga="Vilket uttryck beskriver antalet kuber TOTALT i figur n?",
                        ratt_svar=f"${ratt}$", alternativ=alts, input_typ="radio", svarstyp="string",
                        undertext="Börja gärna med att ställa upp tabellvärden på ett papper."
                    )
                else:
                    ratt = formel_tot
                    d1 = "n^2 + (n-1)^2"
                    d2 = "2n^2 + 1"
                    d3 = "(n+1)^2 + n"
                    alts = [f"${ratt}$", f"${d1}$", f"${d2}$", f"${d3}$"]
                    random.shuffle(alts)
                    return Uppgift(
                        info_box_text=info, info_box_style="blue", plotly_fig=fig_graf,
                        fraga="Vilket uttryck beskriver antalet kuber TOTALT i figur n?",
                        ratt_svar=f"${ratt}$", alternativ=alts, input_typ="radio", svarstyp="string",
                        undertext="Börja gärna med att ställa upp tabellvärden på ett papper."
                    )

        elif typ == 'pizza_brak':
            namn1, namn2 = random.sample(namn_lista, 2)
            A_den = random.choice([3, 4, 5])
            B_den = random.choice([2, 3])
            kvar_1 = Fraction(1, 1) - Fraction(1, A_den)
            ata_2 = Fraction(1, B_den) * kvar_1
            kvar_total = kvar_1 - ata_2
            info = f"{namn1} och {namn2} köper en stor pizza tillsammans. {namn1} äter upp 1/{A_den} av hela pizzan. Senare äter {namn2} upp 1/{B_den} av det som är kvar."
            return Uppgift(
                info_box_text=info, info_box_style="blue",
                fraga="Hur stor andel av HELA pizzan finns sedan kvar?",
                ratt_svar=kvar_total, input_typ="text", svarstyp="fraction",
                undertext="Lös uppgiften med huvudräkning (utan miniräknare).\nSvara i bråkform med ett snedstreck (t.ex. 3/8)."
            )

        elif typ == 'algebraisk_forstaelse':
            namn1, namn2 = random.sample(namn_lista, 2)
            proc_okning = random.choice([15, 20, 25, 30, 40])
            dec_okning = round(proc_okning / 100.0, 2)
            info = f"{namn1} väger <i>a</i>\xa0kg och {namn2} väger <i>b</i>\xa0kg. Du vet att följande samband gäller:<br><br><b>a + {str(dec_okning).replace('.', ',')}a = b</b>"
            ratt1 = f"{namn2} väger {proc_okning}\xa0% mer än {namn1}"
            ratt2 = f"{namn2}s vikt är {str(round(1 + dec_okning, 2)).replace('.', ',')} gånger {namn1}s vikt"
            fel1 = f"{namn1} väger {proc_okning}\xa0% mer än {namn2}"
            fel2 = f"{namn1} väger {str(dec_okning).replace('.', ',')}\xa0kg mer än {namn2}"
            fel3 = f"{namn2} väger {str(dec_okning).replace('.', ',')}\xa0kg mer än {namn1}"
            fel4 = f"{namn1}s vikt är {str(round(1 + dec_okning, 2)).replace('.', ',')} gånger {namn2}s vikt"
            valt_ratt = random.choice([ratt1, ratt2])
            alts_visning = random.sample([valt_ratt, fel1, random.choice([fel2, fel3]), fel4], 4)
            return Uppgift(
                info_box_text=info, info_box_style="blue",
                fraga="Vilket av följande alternativ stämmer alltid?",
                ratt_svar=valt_ratt, alternativ=alts_visning, input_typ="radio", svarstyp="string",
                undertext="Lös uppgiften med huvudräkning (utan miniräknare)."
            )

        elif typ == 'monster_stickor':
            k = random.randint(2, 5)
            m = random.randint(1, 4)
            f1, f2, f3 = k * 1 + m, k * 2 + m, k * 3 + m
            info = f"Ett mönster byggs med tändstickor.<br><br>&bull; Figur 1 består av {f1}\xa0stickor.<br>&bull; Figur 2 består av {f2}\xa0stickor.<br>&bull; Figur 3 består av {f3}\xa0stickor."
            return Uppgift(
                info_box_text=info, info_box_style="blue",
                fraga="Skriv ett generellt algebraiskt uttryck för antalet stickor i figur n.",
                ratt_svar=f"{k}*n + {m}", input_typ="text", svarstyp="string_math",
                undertext="Lös uppgiften med huvudräkning (utan miniräknare).\nAnvänd n som variabel. Svara med ett uttryck, till exempel 6n + 2."
            )

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
            info = f"I simhallen kostar en engångsentré {engangs}\xa0kr. Man kan också köpa ett rabattkort för 10 gånger som kostar {klipp}\xa0kr.<br><br>En person beräknar följande:<br><b>{valt_uttryck}</b>"
            alts = [v[1] for v in varianter]
            random.shuffle(alts)
            return Uppgift(
                info_box_text=info, info_box_style="blue",
                fraga="Förklara vad personen har beräknat genom att välja rätt svarsalternativ.",
                ratt_svar=ratt_svar_text, alternativ=alts, input_typ="radio", svarstyp="string",
                undertext="Läs uttrycket noggrant och fundera på vad uträkningen faktiskt ger för svar.<br>Lös uppgiften med huvudräkning (utan miniräknare)."
            )

        elif typ == 'tidsvinst_hastighet':
            combos = [(30, 60, 90, 10), (40, 80, 120, 10), (60, 90, 120, 10), (20, 60, 80, 5), (10, 40, 60, 5)]
            s, v1, v2, t = random.choice(combos)
            info = f"I en tidningsartikel presenteras en formel för att beräkna tidsskillnaden <i>t</i> (i minuter) om man kör en viss sträcka <i>s</i> (i km) med två olika hastigheter:<br><br><b>t = (1/v<sub>1</sub> - 1/v<sub>2</sub>) &middot; s &middot; 60</b><br><br>Du brukar köra till jobbet med hastigheten {v1}\xa0km/h, men funderar på hur mycket tid du tjänar på att istället köra {v2}\xa0km/h. Sträckan till jobbet är {s}\xa0km."
            return Uppgift(
                info_box_text=info, info_box_style="blue",
                fraga="Hur många minuter tjänar du på att köra i den snabbare hastigheten?",
                ratt_svar=t, input_typ="text", svarstyp="int", suffix="min",
                undertext="Sätt in siffrorna i formeln och räkna. Lös uppgiften med papper och penna."
            )

        elif typ == 'area_uttryck':
            L = random.randint(2, 6) * 10
            info = f"En bonde ska bygga en rektangulär hage till sina djur. Hagen ska byggas mot en lång, rak ladugårdsvägg, så bonden behöver bara bygga staket på tre av sidorna. Bonden har totalt {L}\xa0meter staket att använda.<br><br>Sidorna som är vinkelräta (går rakt ut) från väggen kallas för <i>x</i>."
            ratt = f"x({L} - 2x)"
            alts = [f"${ratt}$", f"$x({L}-x)$", f"$x(2x-{L})$", f"$x(\\frac{{{L}}}{{2}} - x)$"]
            random.shuffle(alts)
            return Uppgift(
                info_box_text=info, info_box_style="blue",
                fraga="Vilket av följande uttryck beskriver hagens area (i kvadratmeter) beroende på x?",
                ratt_svar=f"${ratt}$", alternativ=alts, input_typ="radio", svarstyp="string",
                undertext="Börja gärna med att rita en figur på papper."
            )

        elif typ == 'medelfart':
            combos = [(30, 15, 10), (60, 30, 20), (24, 24, 12), (60, 20, 12)]
            s, v1, v2 = random.choice(combos)
            tot_s = 2 * s
            tot_t = (s / v1) + (s / v2)
            medelfart = int(tot_s / tot_t)
            namn = random.choice(namn_lista)
            fordon = random.choice(['cyklar', 'kör moped', 'kör elsparkcykel'])
            info = f"{namn} {fordon} till en ort som ligger {s}\xa0km bort. På ditvägen är medelhastigheten {v1}\xa0km/h. På hemvägen är det motvind och medelhastigheten blir bara {v2}\xa0km/h."
            return Uppgift(
                info_box_text=info, info_box_style="blue",
                fraga="Vad är medelhastigheten för HELA resan (dit och hem)?",
                ratt_svar=medelfart, input_typ="text", svarstyp="int", suffix="km/h",
                undertext="Tänk på att du måste räkna ut den totala tiden först. Lös gärna med huvudräkning."
            )

        elif typ == 'relativ_procent':
            namn1, namn2, namn3 = random.sample(namn_lista, 3)
            combos = [(40, 20, 75), (50, 25, 100), (20, 40, 100), (80, 10, 100), (10, 45, 100)]
            p_mer, p_mindre, p_svar = random.choice(combos)
            sak = random.choice(['vinner pengar i ett lotteri', 'får lön för ett sommarjobb', 'säljer jultidningar'])
            info = f"Tre vänner {sak}.<br><br>&bull; {namn1} får {p_mer}\xa0% <b>mer</b> än {namn2}.<br>&bull; {namn3} får {p_mindre}\xa0% <b>mindre</b> än {namn2}."
            return Uppgift(
                info_box_text=info, info_box_style="blue",
                fraga=f"Hur många procent MER får {namn1} jämfört med {namn3}?",
                ratt_svar=p_svar, input_typ="text", svarstyp="int", suffix="%",
                undertext="Lös med huvudräkning."
            )

        elif typ == 'valgorenhet':
            pop_milj = random.choice([5, 10, 20])
            items = random.choice([50000, 100000, 200000])
            pris = random.choice([200, 400, 500])
            effektivitet = random.choice([80, 50])
            total_items_cost = items * pris
            total_needed = total_items_cost / (effektivitet / 100.0)
            per_person = int(total_needed / (pop_milj * 1000000))
            sak = random.choice(['nödpaket', 'vaccindoser', 'varma filtar'])
            info = f"I ett land med {pop_milj}\xa0miljoner invånare startas en insamling för att köpa {formatera_kr(items)} {sak}. De kostar {pris}\xa0kr styck.<br><br>På grund av administrativa kostnader går dock bara {effektivitet}\xa0% av de insamlade pengarna till själva inköpen."
            return Uppgift(
                info_box_text=info, info_box_style="blue",
                fraga="Hur mycket måste varje invånare i landet i genomsnitt skänka för att målet ska nås?",
                ratt_svar=per_person, input_typ="text", svarstyp="int", suffix="kr",
                undertext="Håll koll på nollorna! Lös gärna med papper och penna."
            )


# Alias så att både ursprungliga namn och kortare importnamn i __init__.py fungerar
skapa_problemlosning = skapa_problemlosning_uppgift
skapa_lan = skapa_lan_uppgift
skapa_index = skapa_index_uppgift
skapa_procent = skapa_procent_vs_enheter_uppgift
skapa_ff = skapa_ff_uppgift
