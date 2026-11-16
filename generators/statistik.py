import random
from fractions import Fraction
import numpy as np

from models import Uppgift
from graphics import rita_traddiagram, rita_stat_graf


def skapa_slump_uppgift(niva):
    if niva == 1:
        typ = random.choice([
            'flerval_uppstallning',
            'berakna_enkla',
            'enkel_dragning',
            'tarning_mynt',
            'trad_berakna',
            'trad_saknas',
        ])
        if typ == 'trad_berakna':
            A, B = random.randint(3, 6), random.randint(3, 6)
            tot = A + B
            p1, p2 = Fraction(A, tot), Fraction(B, tot)
            p3, p4 = Fraction(A - 1, tot - 1), Fraction(B, tot - 1)
            p5, p6 = Fraction(A, tot - 1), Fraction(B - 1, tot - 1)
            gren_texter = [f"{p.numerator}/{p.denominator}" for p in [p1, p2, p3, p4, p5, p6]]
            fraga_val = random.choice(['två röda', 'två blå', 'exakt en av varje färg'])
            if fraga_val == 'två röda':
                ratt_svar = p1 * p3
                forklaring = f"Följ grenen Röd → Röd och multiplicera sannolikheterna: ({A}/{tot}) · ({A-1}/{tot-1})."
            elif fraga_val == 'två blå':
                ratt_svar = p2 * p6
                forklaring = f"Följ grenen Blå → Blå och multiplicera sannolikheterna: ({B}/{tot}) · ({B-1}/{tot-1})."
            else:
                ratt_svar = (p1 * p4) + (p2 * p5)
                forklaring = "Två grenar ger en av varje färg (Röd → Blå samt Blå → Röd). Multiplicera längs varje gren och addera sedan resultaten."
            return Uppgift(
                info_box_text=f"I en påse finns {A} röda och {B} blå kulor. Träddiagrammet visar vad som kan hända om du drar två kulor utan återläggning.",
                info_box_style="pink",
                plotly_fig=rita_traddiagram(gren_texter, "Röd", "Blå"),
                fraga=f"Vad är sannolikheten att du drar {fraga_val}? (Svara i bråkform)",
                ratt_svar=ratt_svar,
                input_typ="text",
                svarstyp="fraction",
                undertext="Svara i bråkform med ett snedstreck (t.ex. 3/8). Bråket behöver inte vara förkortat maximalt.",
                losningsforslag=forklaring,
            )

        elif typ == 'trad_saknas':
            A, B = random.randint(3, 7), random.randint(3, 7)
            tot = A + B
            fractions = [
                Fraction(A, tot),
                Fraction(B, tot),
                Fraction(A - 1, tot - 1),
                Fraction(B, tot - 1),
                Fraction(A, tot - 1),
                Fraction(B - 1, tot - 1),
            ]
            gren_texter = [f"{p.numerator}/{p.denominator}" for p in fractions]
            saknad_idx = random.randint(0, 5)
            ratt_svar = fractions[saknad_idx]
            gren_texter[saknad_idx] = "x"
            return Uppgift(
                info_box_text=f"I en påse finns {A} röda och {B} blå kulor. Du drar två kulor utan återläggning.",
                info_box_style="pink",
                plotly_fig=rita_traddiagram(gren_texter, "Röd", "Blå"),
                fraga="Ett värde i träddiagrammet har bytts ut mot 'x'. Vilket bråktal ska stå istället för x i diagrammet?",
                ratt_svar=ratt_svar,
                input_typ="text",
                svarstyp="fraction",
                undertext="Svara i bråkform med ett snedstreck (t.ex. 3/8). Bråket behöver inte vara förkortat maximalt.",
                losningsforslag="Summan av sannolikheterna från en och samma förgrening är alltid 1, och vid dragning utan återläggning minskar totala antalet kulor med 1 i andra dragningen.",
            )

        elif typ == 'flerval_uppstallning':
            A, B = random.randint(3, 7), random.randint(3, 7)
            tot = A + B
            ratt = f"\\frac{{{A}}}{{{tot}}} \\cdot \\frac{{{A-1}}}{{{tot-1}}}"
            alt = [
                ratt,
                f"\\frac{{{A}}}{{{tot}}} \\cdot \\frac{{{A}}}{{{tot}}}",
                f"\\frac{{{A}}}{{{tot}}} + \\frac{{{A-1}}}{{{tot-1}}}",
                f"\\frac{{{A}}}{{{tot}}} \\cdot \\frac{{{A-1}}}{{{tot}}}",
            ]
            random.shuffle(alt)
            return Uppgift(
                info_box_text=f"I en påse finns {A} röda och {B} gröna godisbitar. Du drar två godisbitar slumpmässigt utan att titta.",
                info_box_style="pink",
                fraga="Vilken beräkning ger sannolikheten att du får två röda godisbitar?",
                ratt_svar=f"${ratt}$",
                alternativ=[f"${a}$" for a in alt],
                input_typ="radio",
                svarstyp="string",
                undertext="Välj det alternativ som visar rätt uträkning.",
            )

        elif typ == 'berakna_enkla':
            tot = random.randint(4, 12)
            vinst, nit = 1, tot - 1
            return Uppgift(
                info_box_text=f"Ett lyckohjul har {tot}\xa0lika stora fält. Endast {vinst} av fälten ger vinst och {nit} ger nit. Du snurrar hjulet två gånger.",
                info_box_style="pink",
                fraga="Vad är sannolikheten att du vinner på båda snurren?",
                ratt_svar=Fraction(vinst, tot) * Fraction(vinst, tot),
                input_typ="text",
                svarstyp="fraction",
                undertext="Svara i bråkform med ett snedstreck (t.ex. 3/8). Bråket behöver inte vara förkortat maximalt.",
            )

        elif typ == 'enkel_dragning':
            farg1_plur, farg1_sing = random.choice([('röda', 'röd'), ('gröna', 'grön'), ('blåa', 'blå')])
            farg2_plur, farg2_sing = random.choice([('gula', 'gul'), ('svarta', 'svart'), ('vita', 'vit')])
            A, B = random.randint(3, 8), random.randint(3, 8)
            return Uppgift(
                info_box_text=f"I en påse finns {A} {farg1_plur} och {B} {farg2_plur} kulor. Du drar en kula utan att titta.",
                info_box_style="pink",
                fraga=f"Vad är sannolikheten att du drar en {farg1_sing} kula?",
                ratt_svar=Fraction(A, A + B),
                input_typ="text",
                svarstyp="fraction",
                undertext="Svara i bråkform med ett snedstreck (t.ex. 3/8). Bråket behöver inte vara förkortat maximalt.",
            )

        elif typ == 'tarning_mynt':
            tarning_events = [
                ("ett jämnt tal", Fraction(3, 6)),
                ("ett udda tal", Fraction(3, 6)),
                ("mer än 4", Fraction(2, 6)),
                ("mindre än 3", Fraction(2, 6)),
                ("mer än 2", Fraction(4, 6)),
                ("mindre än 5", Fraction(4, 6)),
            ] + [(f"en {i}:a", Fraction(1, 6)) for i in range(1, 7)]
            valt_tarning_event, tarning_prob = random.choice(tarning_events)
            target_mynt = random.choice(['krona', 'klave'])
            return Uppgift(
                info_box_text="Du kastar en vanlig sexsidig tärning och singlar ett mynt.",
                info_box_style="pink",
                fraga=f"Vad är sannolikheten att du får {valt_tarning_event} och {target_mynt}?",
                ratt_svar=tarning_prob * Fraction(1, 2),
                input_typ="text",
                svarstyp="fraction",
                undertext="Svara i bråkform med ett snedstreck (t.ex. 3/8). Bråket behöver inte vara förkortat maximalt.",
            )

    else:  # Nivå 2
        typ = random.choice(['komplement_oberoende', 'komplement_beroende', 'flera_vagar', 'tarning_summa'])
        if typ == 'komplement_oberoende':
            kast = random.choice([3, 4])
            return Uppgift(
                info_box_text=f"Du kastar en vanlig sexsidig tärning {kast}\xa0gånger i rad.",
                info_box_style="pink",
                fraga="Vad är sannolikheten att du slår minst en sexa?",
                ratt_svar=Fraction(1, 1) - (Fraction(5, 6) ** kast),
                input_typ="text",
                svarstyp="fraction",
                undertext="Svara i bråkform med ett snedstreck (t.ex. 3/8). Bråket behöver inte vara förkortat maximalt.",
                losningsforslag=f"Använd komplementhändelsen (ingen sexa alls): P(minst en sexa) = 1 - (5/6)^{kast}.",
            )

        elif typ == 'komplement_beroende':
            vinst, nit = random.randint(2, 4), random.randint(8, 15)
            tot = vinst + nit
            return Uppgift(
                info_box_text=f"I en skål ligger {tot}\xa0lotter. {vinst} är vinstlotter och {nit} är nitlotter. Du drar två lotter utan att titta.",
                info_box_style="pink",
                fraga="Vad är sannolikheten att du får minst en vinstlott?",
                ratt_svar=Fraction(1, 1) - (Fraction(nit, tot) * Fraction(nit - 1, tot - 1)),
                input_typ="text",
                svarstyp="fraction",
                undertext="Svara i bråkform med ett snedstreck (t.ex. 3/8). Bråket behöver inte vara förkortat maximalt.",
                losningsforslag=f"Beräkna komplementhändelsen (två nitlotter): 1 - ({nit}/{tot}) · ({nit-1}/{tot-1}).",
            )

        elif typ == 'flera_vagar':
            A, B = random.randint(3, 6), random.randint(3, 6)
            return Uppgift(
                info_box_text=f"I en ask finns {A} röda och {B} blå bollar. Du drar två bollar slumpmässigt utan återläggning.",
                info_box_style="pink",
                fraga="Vad är sannolikheten att du får exakt en av varje färg?",
                ratt_svar=Fraction(2 * A * B, (A + B) * (A + B - 1)),
                input_typ="text",
                svarstyp="fraction",
                undertext="Svara i bråkform med ett snedstreck (t.ex. 3/8). Bråket behöver inte vara förkortat maximalt.",
                losningsforslag="Du kan antingen dra röd sedan blå, eller blå sedan röd. Båda vägarna har samma sannolikhet, så addera dem (multiplicera med 2).",
            )

        elif typ == 'tarning_summa':
            summan = random.randint(4, 10)
            gynsamma = sum(1 for i in range(1, 7) for j in range(1, 7) if i + j == summan)
            return Uppgift(
                info_box_text="Du kastar två vanliga sexsidiga tärningar.",
                info_box_style="pink",
                fraga=f"Vad är sannolikheten att tärningarnas summa blir exakt {summan}?",
                ratt_svar=Fraction(gynsamma, 36),
                input_typ="text",
                svarstyp="fraction",
                undertext="Svara i bråkform med ett snedstreck (t.ex. 3/8). Bråket behöver inte vara förkortat maximalt.",
                losningsforslag=f"Det finns 6 · 6 = 36 möjliga utfall totalt och {gynsamma} kombinationer som ger summan {summan}.",
            )


def skapa_stat_uppgift(niva=1):
    typ = random.choice(['spridning', 'konf_overlapp', 'konf_baklanges', 'konf_urval', 'konf_falskt', 'kausalitet'])

    if typ == 'spridning':
        num_points = random.randint(40, 60)
        x = np.random.uniform(10, 90, num_points)
        korr = random.choice(['Stark positiv', 'Svag positiv', 'Stark negativ', 'Svag negativ', 'Ingen korrelation'])
        if korr == 'Stark positiv':
            y = 1.5 * x + np.random.normal(0, 6, num_points)
        elif korr == 'Svag positiv':
            y = 1.5 * x + np.random.normal(0, 25, num_points)
        elif korr == 'Stark negativ':
            y = -1.5 * x + 150 + np.random.normal(0, 6, num_points)
        elif korr == 'Svag negativ':
            y = -1.5 * x + 150 + np.random.normal(0, 25, num_points)
        else:
            y = np.random.uniform(10, 90, num_points)
        return Uppgift(
            info_text_italic="Kika på spridningsdiagrammet ovan.",
            plotly_fig=rita_stat_graf(x, y),
            fraga="Vilken typ av korrelation visar diagrammet?",
            ratt_svar=korr,
            alternativ=['Välj svar...', 'Stark positiv', 'Svag positiv', 'Stark negativ', 'Svag negativ', 'Ingen korrelation'],
            input_typ="selectbox",
            svarstyp="string",
        )

    elif typ == 'konf_overlapp':
        A = random.randint(14, 25)
        B, fm = A - random.randint(1, 3), random.randint(2, 4)
        overlapp = (A - fm) <= (B + fm)
        ratt = (
            "Vi kan inte vara helt säkra på vilket parti som är störst, eftersom felmarginalerna överlappar."
            if overlapp
            else "Parti A är med största sannolikhet större än Parti B, eftersom felmarginalerna inte överlappar."
        )
        alts = [
            ratt,
            "Parti A är garanterat större än Parti B." if overlapp else "Vi kan inte vara helt säkra på vilket parti som är störst, eftersom felmarginalerna överlappar.",
            "Parti A har ökat mer än Parti B sedan förra valet.",
            f"Parti A kommer att få exakt {A}\xa0% av rösterna i valet.",
        ]
        random.shuffle(alts)
        return Uppgift(
            info_box_text=f"En väljarbarometer visar att Parti A får {A}\xa0% och Parti B får {B}\xa0% av väljarstödet. Felmarginalen är ±{fm}\xa0procentenheter för båda partierna vid 95\xa0% konfidensgrad.",
            info_box_style="purple",
            fraga="Vilken slutsats kan dras med 95\xa0% säkerhet?",
            ratt_svar=ratt,
            alternativ=alts,
            input_typ="radio",
            svarstyp="string",
            losningsforslag=f"Parti A:s intervall är {A-fm}–{A+fm} % och Parti B:s intervall är {B-fm}–{B+fm} %. När intervallen överlappar går det inte att säkert avgöra vilket parti som är störst.",
        )

    elif typ == 'konf_baklanges':
        resultat = round(random.uniform(4.0, 12.0), 1)
        fm = round(random.uniform(1.5, 3.5), 1)
        ratt = f"Resultatet var {f'{resultat:g}'.replace('.', ',')}\xa0% med en felmarginal på ±{f'{fm:g}'.replace('.', ',')}\xa0procentenheter."
        alts = [
            ratt,
            f"Resultatet var {f'{round(resultat+fm, 1):g}'.replace('.', ',')}\xa0% med en felmarginal på ±{f'{round(fm*2, 1):g}'.replace('.', ',')}\xa0procentenheter.",
            f"Resultatet var {f'{round(resultat-fm, 1):g}'.replace('.', ',')}\xa0% med en felmarginal på ±{f'{round(resultat+fm, 1):g}'.replace('.', ',')}\xa0procentenheter.",
            f"Resultatet var {f'{resultat:g}'.replace('.', ',')}\xa0% med en felmarginal på ±{f'{round(fm/2, 1):g}'.replace('.', ',')}\xa0procentenheter.",
        ]
        random.shuffle(alts)
        return Uppgift(
            info_box_text=f"Ett 95\xa0% konfidensintervall för andelen defekta produkter i en fabrik anges till {f'{round(resultat-fm, 1):g}'.replace('.', ',')}-{f'{round(resultat+fm, 1):g}'.replace('.', ',')}\xa0%.",
            info_box_style="purple",
            fraga="Vad var resultatet i själva stickprovet, och vad var felmarginalen?",
            ratt_svar=ratt,
            alternativ=alts,
            input_typ="radio",
            svarstyp="string",
            losningsforslag="Stickprovsresultatet ligger alltid mitt i konfidensintervallet (medelvärdet av nedre och övre gräns), och felmarginalen är halva intervallets bredd.",
        )

    elif typ == 'konf_urval':
        scenario = random.choice(['minska_fm', 'öka_n_effekt', 'minska_n_effekt', 'jamfora_tva_n'])
        fm = round(random.uniform(3.0, 5.0), 1)
        if scenario == 'minska_fm':
            ratt = "Fråga betydligt fler personer i nästa undersökning."
            alts = [
                ratt,
                "Fråga färre personer så att risken för felräkning minskar.",
                "Bara fråga personer som de vet är insatta i ämnet.",
                "Ställa frågan på ett annat sätt så att fler svarar ja.",
            ]
            info = f"En tidning publicerar en opinionsundersökning men tycker att felmarginalen på ±{f'{fm:g}'.replace('.', ',')}\xa0procentenheter gör resultatet för osäkert. De vill ha ett snävare (mindre) konfidensintervall nästa månad."
            fraga = "Vad är det bästa sättet för dem att minska felmarginalen rent statistiskt?"
        elif scenario == 'öka_n_effekt':
            ratt = "Felmarginalen minskar och intervallet blir snävare."
            alts = [
                ratt,
                "Felmarginalen ökar och intervallet blir bredare.",
                "Felmarginalen påverkas inte alls av antalet tillfrågade.",
                "Resultatet i själva stickprovet ändras.",
            ]
            info = "Ett undersökningsföretag brukar fråga 1\xa0000 personer i sina mätningar. Till nästa mätning bestämmer de sig för att ställa samma fråga till 3\xa0000 personer istället. Båda beräknas med 95\xa0% konfidensgrad."
            fraga = "Vad händer med felmarginalen när de ökar antalet tillfrågade på detta sätt?"
        elif scenario == 'minska_n_effekt':
            ratt = "Felmarginalen ökar (intervallet blir bredare)."
            alts = [
                ratt,
                "Felmarginalen minskar (intervallet blir snävare).",
                "Felmarginalen påverkas inte, så länge det är exakt samma fråga.",
                "Undersökningen blir helt ogiltig och kan inte användas alls.",
            ]
            info = "En forskare skickar ut en enkät till 2\xa0000 personer, men får en väldigt låg svarsfrekvens och bara 400\xa0personer svarar. Hon beräknar ett 95\xa0% konfidensintervall baserat på de 400 svaren."
            fraga = "Hur blir felmarginalen nu, jämfört med om alla 2\xa0000 hade svarat?"
        else:
            ratt = "Undersökning A har en större felmarginal än Undersökning B."
            alts = [
                ratt,
                "Undersökning B har en större felmarginal än Undersökning A.",
                "De har exakt samma felmarginal eftersom båda har 95\xa0% konfidensgrad.",
                "Det går inte att säga vilken felmarginal som är störst utan att veta vad folk svarade.",
            ]
            info = "Två olika tidningar gör varsin undersökning om samma sak. Båda använder 95\xa0% konfidensgrad. Undersökning A frågar 500\xa0slumpmässigt valda personer. Undersökning B frågar 2\xa0500\xa0slumpmässigt valda personer."
            fraga = "Vilket påstående om undersökningarnas felmarginal är sant?"
        random.shuffle(alts)
        return Uppgift(
            info_box_text=info,
            info_box_style="purple",
            fraga=fraga,
            ratt_svar=ratt,
            alternativ=alts,
            input_typ="radio",
            svarstyp="string",
        )

    elif typ == 'konf_falskt':
        resultat, fm = random.randint(55, 75), random.randint(2, 4)
        ratt = f"Mellan {resultat - fm}\xa0% och {resultat + fm}\xa0% av eleverna *som tillfrågades* vill ha längre raster."
        alts = [
            ratt,
            f"Det sanna värdet för hela skolan ligger med 95\xa0% säkerhet mellan {resultat - fm}\xa0% och {resultat + fm}\xa0%.",
            f"I det faktiska stickprovet svarade exakt {resultat}\xa0% att de vill ha längre raster.",
            "Även om intervallet är brett, finns det en risk att det sanna värdet ligger utanför intervallet.",
        ]
        random.shuffle(alts)
        return Uppgift(
            info_box_text=f"En undersökning visar att {resultat}\xa0% av eleverna på en stor skola vill ha längre raster. Undersökningen har en felmarginal på ±{fm}\xa0procentenheter vid 95\xa0% konfidensgrad.",
            info_box_style="purple",
            fraga="Vilket av följande påståenden är FALSKT (felaktigt)?",
            ratt_svar=ratt,
            alternativ=alts,
            input_typ="radio",
            svarstyp="string",
            losningsforslag="I själva stickprovet vet vi exakt hur många som svarade ja (precis 55–75 %). Felmarginalen handlar om osäkerheten när vi drar slutsatser om hela populationen.",
        )

    else:  # kausalitet
        scenario = random.choice(['glass', 'skor', 'pulsklocka'])
        if scenario == 'glass':
            info = (
                "En kommunal utredare har samlat in data över ett helt år. Hen upptäcker ett starkt samband (en positiv korrelation) mellan hur mycket glass som säljs och hur många personer som drunknar. Ju mer glass som säljs, desto fler drunkningsolyckor inträffar.<br><br>"
                "Utredaren drar slutsatsen att glassätande gör människor trötta, vilket orsakar drunkningsolyckorna. Kommunen överväger därför att förbjuda glassförsäljning vid stränderna."
            )
            fraga = "Vad är det mest sannolika felet med utredarens slutsats?"
            ratt = "Utredaren blandar ihop korrelation med kausalitet. Varmt sommarväder är en bakomliggande faktor som orsakar BÅDE mer glassätande och fler badande."
            alts = [
                ratt,
                "Utredaren borde ha kollat på data över tio år, ett år är för kort tid för att bevisa att glass orsakar drunkning.",
                "Felmarginalen i undersökningen är troligtvis för stor.",
                "Drunkningsolyckor orsakar stress och sorg, vilket leder till att människor tröstäter glass i högre utsträckning.",
            ]
        elif scenario == 'skor':
            info = "En stor undersökning genomförs på en grundskola, från förskoleklass till årskurs 9. Forskarna mäter elevernas skostorlek och testar sedan deras förmåga att lösa svåra matematikuppgifter. Resultatet visar en mycket stark positiv korrelation: Ju större fötter en elev har, desto bättre är eleven på matematik."
            fraga = "Vilken är den mest rimliga förklaringen till det starka sambandet?"
            ratt = "Det finns en bakomliggande orsak (ålder) som förklarar båda sakerna. Äldre barn har hunnit få både större fötter och lära sig mer matematik."
            alts = [
                ratt,
                "Att ha stora fötter ger bättre balans, vilket frigör hjärnkapacitet till att räkna matematik.",
                "Det är ett slumpmässigt fel (statistiskt brus), och sambandet skulle försvinna om man frågade fler elever.",
                "Att tänka intensivt på svår matematik ökar blodcirkulationen, vilket på sikt får fötterna att växa snabbare.",
            ]
        else:  # pulsklocka
            info = (
                "Ett företag säljer dyra pulsklockor. I sin reklamkampanj hänvisar de till en ny undersökning som visar att personer som äger företagets pulsklocka i genomsnitt har lägre blodtryck och bättre kondition än de som inte äger en pulsklocka.<br><br>"
                "Företaget hävdar därför i reklamen: <i>'Köp vår pulsklocka – den förbättrar din hälsa!'</i>"
            )
            fraga = "Varför kan man kritisera företagets påstående med hjälp av begreppet kausalitet?"
            ratt = "Bara för att det finns ett samband betyder det inte att klockan ORSAKAR hälsan. Personer som redan tränar mycket är mer benägna att köpa pulsklockor."
            alts = [
                ratt,
                "Företaget har inte angett någon konfidensgrad, så man vet inte om resultatet är säkerställt.",
                "Personer med dålig hälsa kanske inte har råd att köpa dyra pulsklockor.",
                "Klockorna mäter ofta fel, så den uppmätta konditionen stämmer förmodligen inte överens med verkligheten.",
            ]

        random.shuffle(alts)
        return Uppgift(
            info_box_text=info,
            info_box_style="purple",
            fraga=fraga,
            ratt_svar=ratt,
            alternativ=alts,
            input_typ="radio",
            svarstyp="string",
        )


# Alias så att både ursprungliga namn och kortare importnamn i __init__.py fungerar
skapa_slump = skapa_slump_uppgift
