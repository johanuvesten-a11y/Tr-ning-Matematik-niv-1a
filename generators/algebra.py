import math
import random
from models import Uppgift
from utils import formatera_polynom, formatera_kr


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
                if a == c_coeff:
                    continue
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
                if abs(A) % C == 0 and abs(B) % C == 0:
                    continue
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
                if A == D:
                    continue
                B = random.choice([-5, -4, -3, -2, 1, 2, 3, 4, 5])
                E = random.choice([-5, -4, -3, -2, 1, 2, 3, 4, 5])
                C = D * x + D * E - A * x - A * B
                B_str = f"+ {B}" if B > 0 else f"- {-B}"
                E_str = f"+ {E}" if E > 0 else f"- {-E}"
                C_str = f" + {C}" if C > 0 else (f" - {-C}" if C < 0 else "")
                ekv = f"{A}(x {B_str}){C_str} = {D}(x {E_str})"
            elif typ == 'gemensam_namnare':
                B = random.choice([2, 3, 4])
                D = random.choice([2, 3, 4])
                if B == D:
                    continue
                A = random.randint(-5, 5)
                x = random.randint(-3, 3) * B - A
                C = random.randint(-5, 5)
                E = (x + A) / B + (x + C) / D
                if not E.is_integer():
                    continue
                A_str = f"+ {A}" if A > 0 else (f"- {-A}" if A < 0 else "")
                C_str = f"+ {C}" if C > 0 else (f"- {-C}" if C < 0 else "")
                ekv = f"\\frac{{x {A_str}}}{{{B}}} + \\frac{{x {C_str}}}{{{D}}} = {int(round(E))}"
            elif typ == 'x_i_namnare':
                B = random.choice([-5, -4, -3, -2, 1, 2, 3, 4, 5])
                x = random.randint(-10, 10)
                if x + B == 0:
                    continue
                C = random.choice([-4, -3, -2, -1, 2, 3, 4])
                B_str = f"+ {B}" if B > 0 else f"- {-B}"
                ekv = f"\\frac{{{C * (x + B)}}}{{x {B_str}}} = {C}"
            elif typ == 'gomda_forstagrads':
                A = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
                B = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
                C = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
                if A + B == C:
                    continue
                D = (A + B - C) * x + A * B
                A_str = f"+ {A}" if A > 0 else f"- {-A}"
                B_str = f"+ {B}" if B > 0 else f"- {-B}"
                C_str = "+ x" if C == 1 else ("- x" if C == -1 else (f"+ {C}x" if C > 0 else f"- {-C}x"))
                D_str = f"+ {D}" if D > 0 else (f"- {-D}" if D < 0 else "")
                ekv = f"(x {A_str})(x {B_str}) = x^2 {C_str} {D_str}".strip()

        return Uppgift(
            info_text="Lös ekvationen:",
            latex_text=ekv,
            fraga="Vad är x? (Svara med ett heltal):",
            ratt_svar=x,
            input_typ="text",
            svarstyp="int",
            undertext="Lös gärna på papper och skriv in ditt svar.",
        )


def skapa_alg_uttryck_uppgift(niva):
    def formatera_svar(k2, k, m):
        return formatera_polynom([(k2, 'x^2'), (k, 'x'), (m, '')])

    while True:
        if niva == 1:
            typ = random.choice([
                'minus_parentes',
                'mult_parentes',
                'konstant_parentes',
                'faktorisera',
                'forhallande_blanda',
                'forhallande_forenkla',
            ])

            if typ == 'forhallande_blanda':
                A, B = random.randint(1, 3), random.randint(2, 5)
                if A == B:
                    B += 1
                k = random.randint(2, 6)
                saft, vatten = A * k, B * k
                total = saft + vatten
                fraga_vatten = random.choice([True, False])
                info = f"Du ska blanda saft och vatten i förhållandet {A}:{B}. Du häller i {saft}\xa0dl koncentrerad saft."
                if fraga_vatten:
                    fraga = "Hur många deciliter (dl) vatten ska du blanda med?"
                    svar = vatten
                else:
                    fraga = "Hur många deciliter (dl) färdigblandad saft får du totalt?"
                    svar = total
                return Uppgift(
                    info_box_text=info,
                    info_box_style="blue",
                    fraga=fraga,
                    ratt_svar=svar,
                    input_typ="text",
                    svarstyp="int",
                    suffix="dl",
                    undertext="Svara med ett heltal.",
                )

            elif typ == 'forhallande_forenkla':
                A, B = random.randint(2, 6), random.randint(2, 6)
                while math.gcd(A, B) != 1 or A == B:
                    A, B = random.randint(2, 6), random.randint(2, 6)
                k = random.randint(3, 8)
                killar, tjejer = A * k, B * k
                if random.choice([True, False]):
                    info = f"I en klass finns det {killar} killar och {tjejer} tjejer."
                    fraga = "Vilket är förhållandet mellan antalet killar och tjejer?"
                else:
                    info = f"I en fruktskål ligger {killar} äpplen och {tjejer} päron."
                    fraga = "Vilket är förhållandet mellan antalet äpplen och päron?"
                return Uppgift(
                    info_box_text=info,
                    info_box_style="blue",
                    fraga=fraga,
                    ratt_svar=f"{A}:{B}",
                    input_typ="text",
                    svarstyp="ratio",
                    undertext="Svara på enklaste form med ett kolon (t.ex. 2:3).",
                )

            elif typ == 'minus_parentes':
                c = random.choice([2, 3, 4])
                B = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
                alg_uttryck_str = f"x - ({c}x {f'+ {B}' if B > 0 else f'- {-B}'})"
                svar_ratt = formatera_svar(0, 1 - c, -B)
                d1 = formatera_svar(0, 1 - c, B)
                d2 = formatera_svar(0, 1 + c, -B)
                d3 = formatera_svar(0, -c, -B)

            elif typ == 'konstant_parentes':
                a, c = random.randint(2, 5), random.randint(2, 5)
                A, B = random.choice([-4, -3, -2, 2, 3, 4]), random.choice([-4, -3, -2, 2, 3, 4])
                alg_uttryck_str = f"{a}(x {f'+ {A}' if A > 0 else f'- {-A}'}) - {c}(x {f'+ {B}' if B > 0 else f'- {-B}'})"
                svar_ratt = formatera_svar(0, a - c, a * A - c * B)
                d1 = formatera_svar(0, a - c, a * A + c * B)
                d2 = formatera_svar(0, a + c, a * A - c * B)
                d3 = formatera_svar(0, a - c, a * A - B)

            elif typ == 'mult_parentes':
                A = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
                B = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
                alg_uttryck_str = f"(x {f'+ {A}' if A > 0 else f'- {-A}'})(x {f'+ {B}' if B > 0 else f'- {-B}'})"
                svar_ratt = formatera_svar(1, A + B, A * B)
                d1 = formatera_svar(1, 0, A * B)
                d2 = formatera_svar(1, A + B, A + B)
                d3 = formatera_svar(1, A * B, A * B)

            elif typ == 'faktorisera':
                k = random.choice([2, 3, 4, 5, 6, 7])
                a = random.choice([2, 3, 4, 5, 6])
                b = random.choice([1, 2, 3, 4, 5, 6])
                while math.gcd(a, b) != 1:
                    b = random.randint(1, 6)
                op = random.choice(['+', '-'])
                alg_uttryck_str = f"{k * a}x {op} {k * b}"
                svar_ratt = f"{k}({a}x {op} {b})"
                d1 = f"{a}({k}x {op} {b})"
                d2 = f"{k}({a}x {op} {k * b})"
                d3 = f"{k}x({a} {op} {b})" if op == '+' else f"{k}x({a} - {b})"

        else:  # Nivå 2
            typ = random.choice([
                'faktorisera_avancerat',
                'mult_parentes_koeff',
                'flersteg',
                'rationell',
                'likhet_parentes',
                'forhallande_dela_total',
                'forhallande_tre_parter',
            ])

            if typ == 'forhallande_dela_total':
                A, B = random.randint(2, 7), random.randint(2, 7)
                while math.gcd(A, B) != 1 or A == B:
                    A, B = random.randint(2, 7), random.randint(2, 7)
                k = random.choice([50, 100, 200, 500])
                total = (A + B) * k
                info = f"Två personer ska dela på {formatera_kr(total)}\xa0kr i förhållandet {A}:{B} (den första får {A} delar, den andra får {B} delar)."
                if random.choice([True, False]):
                    fraga = "Hur många kronor får den som får den STÖRSTA andelen?"
                    svar = max(A, B) * k
                else:
                    fraga = "Hur många kronor får den som får den MINSTA andelen?"
                    svar = min(A, B) * k
                return Uppgift(
                    info_box_text=info,
                    info_box_style="blue",
                    fraga=fraga,
                    ratt_svar=svar,
                    input_typ="text",
                    svarstyp="int",
                    suffix="kr",
                    undertext="Svara med ett heltal.",
                )

            elif typ == 'forhallande_tre_parter':
                A, B, C = random.randint(1, 4), random.randint(1, 4), random.randint(1, 4)
                while A == B and B == C:
                    C = random.randint(1, 4)
                k = random.randint(3, 8)

                recept_typ = random.choice(['marinad', 'betong'])
                if recept_typ == 'marinad':
                    info = f"Ett recept på marinad anger förhållandet mellan olja, soja och vinäger till {A}:{B}:{C}. Du gör en stor sats och använder {A * k}\xa0msk olja."
                    delar = [('soja', B * k), ('vinäger', C * k)]
                    vald_del = random.choice(delar)
                    fraga = f"Hur många matskedar {vald_del[0]} ska du använda?"
                    suffix = "msk"
                else:
                    info = f"För att blanda en viss sorts betong är förhållandet mellan cement, grus och sand {A}:{B}:{C}. Du använder {A * k}\xa0kg cement."
                    delar = [('grus', B * k), ('sand', C * k)]
                    vald_del = random.choice(delar)
                    fraga = f"Hur många kg {vald_del[0]} ska du använda?"
                    suffix = "kg"
                return Uppgift(
                    info_box_text=info,
                    info_box_style="blue",
                    fraga=fraga,
                    ratt_svar=vald_del[1],
                    input_typ="text",
                    svarstyp="int",
                    suffix=suffix,
                    undertext="Svara med ett heltal.",
                )

            elif typ == 'likhet_parentes':
                while True:
                    A = random.choice([2, 3, 4, 5])
                    D = random.choice([2, 3, 4, 5])
                    if A == D:
                        continue
                    E = random.choice([-5, -4, -3, -2, 2, 3, 4, 5])
                    F = random.choice([-10, -9, -8, -7, -6, -5, -4, -3, -2, 2, 3, 4, 5, 6, 7, 8, 9, 10])
                    if (D * E) % A == 0 and (D * F) % A == 0:
                        B = (D * E) // A
                        C = (D * F) // A
                        break

                VL = f"{A}({formatera_polynom([(B, 'x'), (C, '')])})"
                HL = f"{D}( \\dots )"
                alg_uttryck_str = f"{VL} = {HL}"
                svar_ratt = formatera_polynom([(E, 'x'), (F, '')])
                return Uppgift(
                    info_text="Skriv ett uttryck i parentesen så att likheten gäller:",
                    latex_text=alg_uttryck_str,
                    undertext="Svara på formen ax + b (t.ex. 6x - 15).",
                    fraga="Vad ska stå i parentesen?",
                    ratt_svar=svar_ratt,
                    input_typ="text",
                    svarstyp="string_math",
                )

            elif typ == 'faktorisera_avancerat':
                c, a = random.choice([2, 3, 4, 5]), random.choice([2, 3, 4, 5])
                b = random.choice([1, 2, 3, 4, 5])
                while math.gcd(a, b) != 1:
                    b = random.randint(1, 5)
                var_typ, op = random.choice(['xy', 'x2']), random.choice(['+', '-'])
                if var_typ == 'xy':
                    alg_uttryck_str = f"{c * a}xy {op} {c * b}x"
                    svar_ratt = f"{c}x({a}y {op} {b})"
                    d1, d2, d3 = f"{a}x({c}y {op} {b})", f"{c}({a}xy {op} {b}x)", f"{c}xy({a} {op} {b})"
                else:
                    alg_uttryck_str = f"{c * a}x^2 {op} {c * b}x"
                    svar_ratt = f"{c}x({a}x {op} {b})"
                    d1, d2, d3 = f"{a}x({c}x {op} {b})", f"{c}({a}x^2 {op} {b}x)", f"{c}x^2({a} {op} {b})"

            elif typ == 'mult_parentes_koeff':
                a, c = random.choice([2, 3, 4]), random.choice([2, 3, 4])
                b, d = random.choice([-4, -3, -2, -1, 1, 2, 3, 4]), random.choice([-4, -3, -2, -1, 1, 2, 3, 4])
                alg_uttryck_str = f"({a}x {f'+ {b}' if b > 0 else f'- {-b}'})({c}x {f'+ {d}' if d > 0 else f'- {-d}'})"
                svar_ratt = formatera_svar(a * c, a * d + b * c, b * d)
                d1 = formatera_svar(a * c, 0, b * d)
                d2 = formatera_svar(a * c, a * d + b * c, b + d)
                d3 = formatera_svar(a + c, a * d + b * c, b * d)

            elif typ == 'flersteg':
                a = random.choice([2, 3])
                b, c, d = (
                    random.choice([-4, -3, 2, 3, 4]),
                    random.choice([-3, -2, -1, 1, 2, 3]),
                    random.choice([-3, -2, -1, 1, 2, 3]),
                )
                alg_uttryck_str = f"x({a}x {f'+ {b}' if b > 0 else f'- {-b}'}) - (x {f'+ {c}' if c > 0 else f'- {-c}'})(x {f'+ {d}' if d > 0 else f'- {-d}'})"
                svar_ratt = formatera_svar(a - 1, b - (c + d), -(c * d))
                d1 = formatera_svar(a - 1, b - (c + d), c * d)
                d2 = formatera_svar(a + 1, b - (c + d), -(c * d))
                d3 = formatera_svar(a - 1, b + c + d, -(c * d))

            elif typ == 'rationell':
                C = random.choice([2, 3, 4, 5])
                a, b = random.choice([-4, -3, -2, 2, 3, 4]), random.choice([-5, -4, -3, -2, 2, 3, 4, 5])
                B_str = f"+ {b * C}" if b * C > 0 else f"- {-b * C}"
                alg_uttryck_str = f"\\frac{{{a * C}x^2 {B_str}x}}{{{C}x}}"
                b_svar = f"+ {b}" if b > 0 else f"- {-b}"
                svar_ratt = f"{a}x {b_svar}"
                B_fel = f"+ {b * C}" if b * C > 0 else f"- {-b * C}"
                d1 = f"{a}x^2 {b_svar}"
                d2 = f"{a * C}x {b_svar}"
                d3 = f"{a}x {B_fel}"

        svar_ratt_latex = f"${svar_ratt}$"
        alternativ = [svar_ratt_latex, f"${d1}$", f"${d2}$", f"${d3}$"]

        if len(set(alternativ)) == 4:
            break

    random.shuffle(alternativ)
    return Uppgift(
        info_text="Förenkla uttrycket:" if typ not in ('faktorisera', 'faktorisera_avancerat') else "Faktorisera uttrycket så långt som möjligt:",
        latex_text=alg_uttryck_str,
        undertext="Lös gärna på papper och välj ditt svar.",
        fraga="Välj rätt alternativ:",
        ratt_svar=svar_ratt_latex,
        alternativ=alternativ,
        input_typ="radio",
        svarstyp="string",
    )


# Alias så att både ursprungliga namn och kortare importnamn i __init__.py fungerar
skapa_alg_uttryck = skapa_alg_uttryck_uppgift
