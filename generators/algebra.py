import random
from models import Uppgift
from utils import formatera_polynom

def skapa_pq_uppgift(niva: int) -> Uppgift:
    """Skapar en andragradsekvation som kan lösas med pq-formeln."""
    for _ in range(100):
        # Slumpa två heltalsrötter
        x1 = random.randint(-8, 8)
        x2 = random.randint(-8, 8)
        
        if x1 == x2:
            continue
            
        # Konstruera ekvationen x^2 + px + q = 0 utifrån rötterna
        p = -(x1 + x2)
        q = x1 * x2
        
        # Formatera till en snygg sträng
        ekvation = formatera_polynom([(1, "x^2"), (p, "x"), (q, "")]) + " = 0"
        
        return Uppgift(
            fraga="Lös andragradsekvationen:",
            latex_text=ekvation,
            ratt_svar=[float(x1), float(x2)],
            input_typ="text",
            svarstyp="array_float",
            undertext="Ange båda lösningarna separerade med kommatecken eller 'och'."
        )
        
    # Fallback om loopen mot förmodan misslyckas 100 gånger
    return Uppgift(
        fraga="Lös andragradsekvationen:",
        latex_text="x^2 - 4 = 0",
        ratt_svar=[2.0, -2.0],
        input_typ="text",
        svarstyp="array_float"
    )

def skapa_ekvationssystem_uppgift(niva: int) -> Uppgift:
    """Skapar ett linjärt ekvationssystem."""
    for _ in range(100):
        x = random.randint(-5, 5)
        y = random.randint(-5, 5)
        
        # Ekvation 1: a1*x + b1*y = c1
        a1 = random.choice([1, 2, 3])
        b1 = random.choice([-2, -1, 1, 2])
        c1 = a1 * x + b1 * y
        
        # Ekvation 2: a2*x + b2*y = c2
        a2 = random.choice([-3, -2, -1, 1])
        b2 = random.choice([-3, 1, 2, 3])
        c2 = a2 * x + b2 * y
        
        # Se till att de inte är parallella (determinanten skild från 0)
        if a1 * b2 - a2 * b1 == 0:
            continue
            
        eq1 = formatera_polynom([(a1, "x"), (b1, "y")]) + f" = {c1}"
        eq2 = formatera_polynom([(a2, "x"), (b2, "y")]) + f" = {c2}"
        
        system_latex = f"\\begin{{cases}} {eq1} \\\\ {eq2} \\end{{cases}}"
        
        return Uppgift(
            fraga="Lös ekvationssystemet:",
            latex_text=system_latex,
            ratt_svar=[float(x), float(y)],
            input_typ="text",
            svarstyp="ekvationssystem",
            undertext="Ange svaret som x, y (t.ex. '2, -1')."
        )
        
    return Uppgift(
        fraga="Lös ekvationssystemet:",
        latex_text="\\begin{cases} x + y = 3 \\\\ x - y = 1 \\end{cases}",
        ratt_svar=[2.0, 1.0],
        input_typ="text",
        svarstyp="ekvationssystem"
    )

def skapa_konjugat_uppgift(niva: int) -> Uppgift:
    """Skapar en uppgift om konjugatregeln."""
    for _ in range(100):
        a = random.randint(2, 6)
        b = random.randint(1, 9)
        
        uttryck = f"({a}x + {b})({a}x - {b})"
        # Svaret blir (a^2)x^2 - b^2
        ratt = f"{a**2}x^2 - {b**2}"
        
        return Uppgift(
            fraga="Utveckla uttrycket med hjälp av konjugatregeln:",
            latex_text=uttryck,
            ratt_svar=ratt,
            input_typ="text",
            svarstyp="string_math",
            krav_inga_parenteser=True,
            undertext="Svara på formen ax^2 - c"
        )
        
    return Uppgift(
        fraga="Utveckla uttrycket:",
        latex_text="(x + 2)(x - 2)",
        ratt_svar="x^2 - 4",
        input_typ="text",
        svarstyp="string_math"
    )
