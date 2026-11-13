import random
import plotly.graph_objects as go
from fractions import Fraction

from models import Uppgift
from graphics import rita_stat_graf, rita_traddiagram

def skapa_stat_uppgift(niva):
    if niva == 1:
        # Läs av ett stolpdiagram
        kategorier = ["Måndag", "Tisdag", "Onsdag", "Torsdag", "Fredag"]
        varden = [random.randint(2, 10) for _ in range(5)]
        
        # Vi sparar parametrar för att rita grafen i appen
        graf_params = {"x": kategorier, "y": varden, "titel": "Antal träningspass per dag"}
        
        fraga_typ = random.choice(["totalt", "skillnad", "specifik"])
        if fraga_typ == "totalt":
            svar = sum(varden)
            fraga = "Hur många träningspass genomfördes totalt under veckan?"
        elif fraga_typ == "skillnad":
            svar = abs(varden[0] - varden[4])
            fraga = "Vad är skillnaden i antal träningspass mellan måndag och fredag?"
        else:
            svar = varden[2]
            fraga = "Hur många träningspass genomfördes på onsdagen?"
            
        return Uppgift(
            fraga=fraga,
            ratt_svar=svar,
            input_typ="text",
            svarstyp="int",
            extra_data={"stat_graf": graf_params}
        )
    else:
        # Beräkna andel/procent baserat på text (använder ditt avklippta tema)
        varde1 = random.randint(10, 30) # Tränar aldrig
        varde2 = random.randint(30, 50) # Tränar ibland
        varde3 = random.randint(20, 40) # Personer som redan tränar
        totalt = varde1 + varde2 + varde3
        
        info = (f"I en undersökning om hälsa deltog {totalt} personer. "
                f"{varde1} personer angav att de aldrig tränar, "
                f"{varde2} personer att de tränar ibland, "
                f"och resten är personer som redan tränar regelbundet.")
        
        fraga = "Hur många procent av de tillfrågade tränar regelbundet? (Avrunda till närmaste heltal)"
        svar = round((varde3 / totalt) * 100)
        
        return Uppgift(
            fraga=fraga,
            ratt_svar=svar,
            input_typ="text",
            svarstyp="int",
            extra_data={"info_text": info}
        )

def skapa_slump(niva):
    if niva == 1:
        # Enkel sannolikhet med en dragning
        roda = random.randint(2, 6)
        bla = random.randint(2, 6)
        totalt = roda + bla
        fraga = f"I en påse finns {roda} röda kulor och {bla} blå kulor. Du drar en kula slumpmässigt. Vad är sannolikheten att du drar en röd kula? (Svara i bråkform, t.ex. 1/2)"
        svar = f"{roda}/{totalt}"
        
        return Uppgift(
            fraga=fraga,
            ratt_svar=svar,
            input_typ="text",
            svarstyp="fraction"
        )
    else:
        # Sannolikhet med två dragningar utan återläggning (träddiagram-scenario)
        roda = random.randint(3, 5)
        bla = random.randint(3, 5)
        totalt = roda + bla
        fraga = f"I en påse finns {roda} röda och {bla} blå kulor. Du drar två kulor utan återläggning. Vad är sannolikheten att du drar två röda kulor? (Svara i bråkform)"
        
        täljare = roda * (roda - 1)
        nämnare = totalt * (totalt - 1)
        svar = f"{täljare}/{nämnare}"
        
        # Flagga för appen att den ska rendera ett träddiagram om vi vill visa det som ledtråd
        return Uppgift(
            fraga=fraga,
            ratt_svar=svar,
            input_typ="text",
            svarstyp="fraction",
            extra_data={"visa_traddiagram": True, "farg1": "red", "farg2": "blue"}
        )
