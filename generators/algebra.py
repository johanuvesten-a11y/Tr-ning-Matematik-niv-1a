import random
from models import Uppgift
from utils import formatera_polynom

def skapa_ekv_uppgift(niva):
    def formatera_sida(k, m):
        return formatera_polynom([(k, 'x'), (m, '')])
        
    while True:
        x = random.randint(-10, 10)
        if niva == 1:
            typ = random.choice(['tvosteg', 'division', 'bada_sidor', 'enkel_parentes'])
            if typ == 'tvosteg':
                a = random.choice([-5, -4, -3, -2, -1, 2, 3, 4, 5])
                b = random.randint(-15, 15)
                ekv = f"{formatera_sida(a, b)} = {a * x + b}"
            elif typ == 'division':
                a = random.choice([2, 3, 4, 5])
                x = random.randint(-6, 6) * a 
                b = random.randint(-10, 10)
                b_str = f" + {b}" if b > 0 else (f" - {-b}" if b < 0 else "")
                ekv = f"\\frac{{x}}{{{a}}}{b_str} = {int(round(x / a)) + b}"
            elif typ == 'bada_sidor':
                a = random.choice([-5, -4, -3, -2, 2, 3, 4, 5])
                c_coeff = random.choice([-5, -4, -3, -2, 2, 3, 4, 5])
                if a == c_coeff: continue 
                b = random.randint(-20, 20)
                ekv = f"{formatera_sida(a, b)} = {formatera_sida(c_coeff, a * x + b - c_coeff * x)}"
            elif typ == 'enkel_parentes':
                a = random.choice([-5, -4, -3, -2, 2, 3, 4, 5])
                b = random.choice([-5, -4, -3, -2, 1, 2, 3, 4, 5])
                b_str = f"+ {b}" if b > 0 else f"- {-b}"
                ekv = f"{a}(x {b_str}) = {a * (x + b)}"
        else:
            typ = random.choice(['nuvarande', 'parenteser_bada', 'gemensam_namnare', 'x_i_namnare', 'gomda_forstagrads'])
            if typ == 'nuvarande':
                A = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
                C = random.choice([2, 3, 4, 5])
                val_VL = random.randint(-10, 10)
                B = C * val_VL - A * x
                if abs(A) % C == 0 and abs(B) % C == 0: continue
                E = random.choice([1, 2, 3, 4, 5])
                F = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
                op = random.choice(['+', '-'])
                D = val_VL - E * (x + F) if op == '+' else val_VL + E * (x + F)
                A_str = "x" if A == 1 else ("-x" if A == -1 else f"{A}x")
                B_str = f" + {B}" if B > 0 else (f" - {-B}" if B < 0 else "")
                E_str = "" if E == 1 else str(E)
                F_str = f"+ {F}" if F > 0 else f"- {-F}"
                ekv = f"\\frac{{{A_str}{B_str}}}{{{C}}} = {D} {op} {E_str}(x {F_str})"
            elif typ == 'parenteser_bada':
                A = random.choice([2, 3, 4, 5])
                D = random.choice([2, 3, 4, 5])
                if A == D: continue
                B = random.choice([-5, -4, -3, -2, 1, 2, 3, 4, 5])
                E = random.choice([-5, -4, -3, -2, 1, 2, 3, 4, 5])
                C = D*x + D*E - A*x - A*B
                B_str = f"+ {B}" if B > 0 else f"- {-B}"
                E_str = f"+ {E}" if E > 0 else f"- {-E}"
                C_str = f" + {C}" if C > 0 else (f" - {-C}" if C < 0 else "")
                ekv = f"{A}(x {B_str}){C_str} = {D}(x {E_str})"
            elif typ == 'gemensam_namnare':
                B = random.choice([2, 3, 4])
                D = random.choice([2, 3, 4])
                if B == D: continue
                A = random.randint(-5, 5)
                x = random.randint(-3, 3) * B - A
                C = random.randint(-5, 5)
                E = (x + A) / B + (x + C) / D
                if not E.is_integer(): continue 
                A_str = f"+ {A}" if A > 0 else (f"- {-A}" if A < 0 else "")
                C_str = f"+ {C}" if C > 0 else (f"- {-C}" if C < 0 else "")
                ekv = f"\\frac{{x {A_str}}}{{{B}}} + \\frac{{x {C_str}}}{{{D}}} = {int(round(E))}"
            elif typ == 'x_i_namnare':
                B = random.choice([-5, -4, -3, -2, 1, 2, 3, 4, 5])
                x = random.randint(-10, 10)
                if x + B == 0: continue 
                C = random.choice([-4, -3, -2, -1, 2, 3, 4])
                B_str = f"+ {B}" if B > 0 else f"- {-B}"
                ekv = f"\\frac{{{C * (x + B)}}}{{x {B_str}}} = {C}"
            elif typ == 'gomda_forstagrads':
                A = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
                B = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
                C = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
                if A + B == C: continue 
                D = (A + B - C) * x + A * B
                A_str = f"+ {A}" if A > 0 else f"- {-A}"
                B_str = f"+ {B}" if B > 0 else f"- {-B}"
                C_str = "+ x" if C == 1 else ("- x" if C == -1 else (f"+ {C}x" if C > 0 else f"- {-C}x"))
                D_str = f"+ {D}" if D > 0 else (f"- {-D}" if D < 0 else "")
                ekv = f"(x {A_str})(x {B_str}) = x^2 {C_str} {D_str}".strip()
                
        return Uppgift(
            extra_data={"info_text": "Lös ekvationen:", "latex_text": ekv, "undertext": "Lös gärna på papper och skriv in ditt svar."},
            fraga="Vad är x? (Svara med ett heltal):", 
            ratt_svar=x,
            input_typ="text", 
            svarstyp="int"
        )

def skapa_alg_uttryck(niva):
    # KLISTRA IN DIN KOD FÖR skapa_alg_uttryck HÄR
    # Returnera ett Uppgift-objekt precis som i originalkoden
    pass
