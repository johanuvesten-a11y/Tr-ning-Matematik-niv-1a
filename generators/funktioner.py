import random
import numpy as np
from models import Uppgift
from utils import formatera_polynom

def generera_deterministisk_funktion():
    typ = random.choice(['linjar', 'kvadratisk', 'kubisk', 'exponential', 'sinus'])
    if typ == 'linjar':
        k = random.choice([-2, -1.5, -1, -0.5, 0.5, 1, 1.5, 2])
        x_target = random.randint(-5, 5)
        y_target = random.randint(-5, 5)
        m = y_target - k * x_target
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

def skapa_graf_uppgift(niva):
    while True: 
        f = generera_deterministisk_funktion()
        giltiga_punkter = []
        for x_val in [i / 2 for i in range(-16, 17)]:
            y_val = f(x_val)
            if abs(y_val) <= 10 and round(y_val * 2, 4).is_integer():
                giltiga_punkter.append((round(x_val, 4), round(y_val, 4)))
                
        if not giltiga_punkter: continue 
        
        if niva == 1:
            target_x, target_y = random.choice(giltiga_punkter)
            fraga_typ = random.choice(['hitta_y', 'hitta_x'])
            
            if fraga_typ == 'hitta_y':
                fraga = f"Bestäm f({target_x:g})"
                return Uppgift(
                    graf_funktion=f, 
                    extra_data={'q_type_vis': 'vis_find_y', 'trace_x': target_x, 'trace_y': target_y},
                    fraga=fraga.replace('.', ','), 
                    ratt_svar=[round(target_y, 4) + 0.0],
                    input_typ="flera_text", 
                    svarstyp="array_float"
                )
            else:
                alla_x = list(set([p[0] for p in giltiga_punkter if p[1] == target_y]))
                if len(alla_x) > 3: continue 
                fraga = f"Bestäm ett värde på x så att f(x) = {target_y + 0.0:g}"
                return Uppgift(
                    graf_funktion=f, 
                    extra_data={'q_type_vis': 'vis_find_x', 'trace_y': target_y, 'trace_alla_x': alla_x},
                    fraga=fraga.replace('.', ','), 
                    ratt_svar=[round(ans, 4) + 0.0 for ans in sorted(alla_x)],
                    input_typ="flera_text", 
                    svarstyp="array_float"
                )
        else:
            fraga_typ = random.choice(['f_x_plus_c', 'f_f_c', 'f_a_op_f_b', 'f_kx'])
            if fraga_typ == 'f_x_plus_c':
                hel_punkter = [p for p in giltiga_punkter if round(p[1], 4).is_integer()]
                if not hel_punkter: continue
                target_x, target_y = random.choice(hel_punkter)
                c = random.choice([-3, -2, -1, 1, 2, 3])
                c_str = f"+ {c}" if c > 0 else f"- {abs(c)}"
                alla_mål_x = [p[0] for p in giltiga_punkter if p[1] == target_y]
                if len(alla_mål_x) > 3: continue 
                fraga = f"Bestäm x om f(x {c_str}) = {target_y + 0.0:g}"
                ratt_svar = sorted([tx - c for tx in alla_mål_x])
                return Uppgift(
                    graf_funktion=f, 
                    extra_data={'q_type_vis': 'vis_find_x', 'trace_y': target_y, 'trace_alla_x': alla_mål_x}, 
                    fraga=fraga.replace('.', ','), 
                    ratt_svar=[round(ans, 4) + 0.0 for ans in ratt_svar], 
                    input_typ="flera_text", 
                    svarstyp="array_float"
                )
                
            elif fraga_typ == 'f_f_c':
                valid_c = []
                for x_val in range(-8, 9):
                    y1 = f(x_val)
                    if round(y1, 4).is_integer() and -8 <= y1 <= 8:
                        y2 = f(y1)
                        if abs(y2) <= 10 and round(y2 * 2, 4).is_integer(): valid_c.append(x_val)
                if not valid_c: continue 
                c = random.choice(valid_c)
                ratt_svar = [round(f(round(f(c), 4)), 4)]
                fraga = f"Bestäm f(f({c}))"
                return Uppgift(
                    graf_funktion=f, 
                    fraga=fraga.replace('.', ','), 
                    ratt_svar=[round(ans, 4) + 0.0 for ans in ratt_svar], 
                    input_typ="flera_text", 
                    svarstyp="array_float"
                )
                
            elif fraga_typ == 'f_a_op_f_b':
                hel_punkter = [p for p in giltiga_punkter if round(p[1], 4).is_integer() and round(p[0], 4).is_integer()]
                if len(hel_punkter) < 2: continue
                p1, p2 = random.sample(hel_punkter, 2)
                op = random.choice(['+', '-'])
                svar = p1[1] + p2[1] if op == '+' else p1[1] - p2[1]
                fraga = f"Bestäm f({p1[0]:g}) {op} f({p2[0]:g})"
                return Uppgift(
                    graf_funktion=f, 
                    fraga=fraga.replace('.', ','), 
                    ratt_svar=[round(svar, 4) + 0.0], 
                    input_typ="flera_text", 
                    svarstyp="array_float"
                )
                
            elif fraga_typ == 'f_kx':
                mål_y = random.choice([p[1] for p in giltiga_punkter])
                alla_mål_x = [p[0] for p in giltiga_punkter if p[1] == mål_y]
                if len(alla_mål_x) > 3: continue 
                k_val = random.choice([2, -2])
                mojliga_svar = [x / k_val for x in alla_mål_x]
                if all(round(s * 2, 4).is_integer() and abs(s) <= 20 for s in mojliga_svar):
                    fraga = f"Bestäm x om f({k_val:g}x) = {mål_y + 0.0:g}"
                    return Uppgift(
                        graf_funktion=f, 
                        extra_data={'q_type_vis': 'vis_find_x', 'trace_y': mål_y, 'trace_alla_x': alla_mål_x}, 
                        fraga=fraga.replace('.', ','), 
                        ratt_svar=[round(ans, 4) + 0.0 for ans in sorted(mojliga_svar)], 
                        input_typ="flera_text", 
                        svarstyp="array_float"
                    )

def skapa_alg_func_uppgift(niva):
    while True:
        if niva == 1:
            typ = random.choice(['f_a', 'f_x_C', 'f_x_C_kvadrat'])
            if typ == 'f_a':
                func_type = random.choice(['linjar', 'kvadratisk', 'exponential'])
                a = random.randint(-10, 10)
                if func_type == 'linjar':
                    k = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
                    m = random.randint(-10, 10)
                    svar = k*a + m
                    f_str = formatera_polynom([(k, 'x'), (m, '')])
                elif func_type == 'kvadratisk':
                    k = random.choice([-3, -2, -1, 1, 2, 3])
                    m = random.randint(-10, 10)
                    svar = k*(a**2) + m
                    f_str = formatera_polynom([(k, 'x^2'), (m, '')])
                else:
                    bas = random.choice([2, 3])
                    a = random.randint(0, 4) 
                    k = random.choice([-3, -2, -1, 1, 2, 3])
                    svar = k * (bas**a)
                    if k == 1: f_str = f"{bas}^x"
                    elif k == -1: f_str = f"-{bas}^x"
                    else: f_str = f"{k} \\cdot {bas}^x"
                
                if abs(svar) <= 100:
                    return Uppgift(
                        extra_data={"info_text": "Givet funktionen:", "latex_text": f"f(x) = {f_str}", "undertext": "Lös gärna på papper och skriv in ditt svar."}, 
                        fraga=f"Bestäm f({a})", 
                        ratt_svar=svar, 
                        input_typ="text", 
                        svarstyp="int"
                    )
                    
            elif typ == 'f_x_C_kvadrat':
                x = random.randint(1, 10) 
                k = random.choice([-3, -2, -1, 1, 2, 3])
                m = random.randint(-15, 15)
                C = k*(x**2) + m
                f_str = formatera_polynom([(k, 'x^2'), (m, '')])
                
                if abs(C) <= 300:
                    return Uppgift(
                        extra_data={"info_text": "Givet funktionen:", "latex_text": f"f(x) = {f_str}", "undertext": "Lös gärna på papper och skriv in ditt svar."}, 
                        fraga=f"Bestäm det positiva värdet på x om f(x) = {C}", 
                        ratt_svar=x, 
                        input_typ="text", 
                        svarstyp="int"
                    )
                    
            else: # Linjär
                b = random.choice([1, 1, 2, 3, 4]) 
                a_coeff = random.choice([-4, -3, -2, -1, 1, 2, 3, 4])
                if b > 1 and abs(a_coeff) % b == 0: continue
                m = random.randint(-15, 15)
                x = random.randint(-20, 20) * b 
                if b == 1:
                    C = a_coeff*x + m
                    f_str = formatera_polynom([(a_coeff, 'x'), (m, '')])
                else:
                    term_x = f"\\frac{{x}}{{{b}}}" if a_coeff == 1 else (f"-\\frac{{x}}{{{b}}}" if a_coeff == -1 else f"\\frac{{{a_coeff}x}}{{{b}}}")
                    C = int(round((a_coeff*x)/b + m))
                    m_str = f" + {m}" if m > 0 else (f" - {-m}" if m < 0 else "")
                    f_str = f"{term_x}{m_str}"
                
                if abs(x) <= 100 and abs(C) <= 100:
                    return Uppgift(
                        extra_data={"info_text": "Givet funktionen:", "latex_text": f"f(x) = {f_str}", "undertext": "Lös gärna på papper och skriv in ditt svar."}, 
                        fraga=f"Bestäm x om f(x) = {C}", 
                        ratt_svar=x, 
                        input_typ="text", 
                        svarstyp="int"
                    )
                    
        else: # Niva 2 
            def formatera_linjar(k, m):
                return formatera_polynom([(k, 'x'), (m, '')])
            typ = random.choice(['f_f_a', 'f_f_x_C', 'f_g_a', 'f_likamed_g'])
            
            if typ in ['f_f_a', 'f_f_x_C']:
                k = random.choice([-3, -2, -1, 2, 3])
                m = random.randint(-10, 10)
                if typ == 'f_f_a':
                    a = random.randint(-8, 8)
                    svar = k*(k*a + m) + m
                    if abs(svar) <= 150:
                        return Uppgift(
                            extra_data={"info_text": "Givet funktionen:", "latex_text": f"f(x) = {formatera_linjar(k, m)}", "undertext": "Lös gärna på papper och skriv in ditt svar."}, 
                            fraga=f"Bestäm f(f({a}))", 
                            ratt_svar=svar, 
                            input_typ="text", 
                            svarstyp="int"
                        )
                else:
                    x = random.randint(-12, 12)
                    C = k*(k*x + m) + m
                    if abs(x) <= 100 and abs(C) <= 150:
                        return Uppgift(
                            extra_data={"info_text": "Givet funktionen:", "latex_text": f"f(x) = {formatera_linjar(k, m)}", "undertext": "Lös gärna på papper och skriv in ditt svar."}, 
                            fraga=f"Bestäm x om f(f(x)) = {C}", 
                            ratt_svar=x, 
                            input_typ="text", 
                            svarstyp="int"
                        )
            elif typ == 'f_g_a':
                k1 = random.choice([-4, -3, -2, -1, 2, 3, 4])
                m1 = random.randint(-10, 10)
                k2 = random.choice([-4, -3, -2, -1, 2, 3, 4])
                m2 = random.randint(-10, 10)
                a = random.randint(-5, 5)
                svar = k1*(k2*a + m2) + m1
                return Uppgift(
                    extra_data={"info_text": "Givet funktionen:", "latex_text": f"f(x) = {formatera_linjar(k1, m1)} \\quad \\text{{och}} \\quad g(x) = {formatera_linjar(k2, m2)}", "undertext": "Lös gärna på papper och skriv in ditt svar."}, 
                    fraga=f"Bestäm f(g({a}))", 
                    ratt_svar=svar, 
                    input_typ="text", 
                    svarstyp="int"
                )
            elif typ == 'f_likamed_g':
                x = random.randint(-10, 10)
                k1 = random.choice([-5, -4, -3, -2, 2, 3, 4, 5])
                k2 = random.choice([-5, -4, -3, -2, 2, 3, 4, 5])
                if k1 == k2: continue 
                m1 = random.randint(-15, 15)
                m2 = (k1 - k2)*x + m1 
                return Uppgift(
                    extra_data={"info_text": "Givet funktionen:", "latex_text": f"f(x) = {formatera_linjar(k1, m1)} \\quad \\text{{och}} \\quad g(x) = {formatera_linjar(k2, m2)}", "undertext": "Lös gärna på papper och skriv in ditt svar."}, 
                    fraga="Bestäm x om f(x) = g(x)", 
                    ratt_svar=x, 
                    input_typ="text", 
                    svarstyp="int"
                )
