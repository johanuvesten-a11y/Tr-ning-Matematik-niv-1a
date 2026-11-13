import random
import plotly.graph_objects as go
import numpy as np
from models import Uppgift

def rita_funktion_graf(f, title="Funktionsgraf", visa_facit=False, extrempunkt=None, nollstallen=None):
    fig = go.Figure()
    x_plot = np.linspace(-10, 10, 400)
    y_plot = f(x_plot)
    fig.add_trace(go.Scatter(x=x_plot, y=y_plot, mode='lines', line=dict(color='blue', width=2), hoverinfo='skip'))
    
    if visa_facit:
        if extrempunkt:
            tx, ty = extrempunkt
            fig.add_trace(go.Scatter(x=[tx, tx, 0], y=[0, ty, ty], mode='lines+markers', line=dict(color='red', dash='dash', width=2), marker=dict(size=8, color='red'), showlegend=False, hoverinfo='skip'))
        if nollstallen:
            for nx in nollstallen:
                fig.add_trace(go.Scatter(x=[nx, nx], y=[0, 0], mode='markers', marker=dict(size=10, color='green'), showlegend=False, hoverinfo='skip'))

    tick_vals = [-10, -5, 5, 10]
    fig.add_trace(go.Scatter(x=tick_vals, y=[-0.6]*4, mode='text', text=[str(v) for v in tick_vals], textposition='bottom center', showlegend=False, hoverinfo='skip', textfont=dict(color='black', size=14)))
    fig.add_trace(go.Scatter(x=[-0.6]*4, y=tick_vals, mode='text', text=[str(v) for v in tick_vals], textposition='middle left', showlegend=False, hoverinfo='skip', textfont=dict(color='black', size=14)))
    fig.add_trace(go.Scatter(x=[-0.4], y=[-0.6], mode='text', text=['0'], textposition='bottom left', showlegend=False, hoverinfo='skip', textfont=dict(color='black', size=14)))
    
    axis_layout = dict(range=[-10.8, 10.8], zeroline=True, zerolinewidth=3, zerolinecolor='black', showgrid=True, gridwidth=2, gridcolor='#cccccc', minor=dict(dtick=1, gridwidth=2, gridcolor='#e0e0e0'), showticklabels=False, fixedrange=True)
    pil_inst = dict(showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2, arrowcolor='black')
    
    fig.update_layout(xaxis=axis_layout, yaxis=axis_layout, showlegend=False, margin=dict(l=20, r=20, t=40, b=20), height=550, plot_bgcolor='white', hovermode=False, dragmode=False,
        annotations=[
            dict(x=10.8, y=0, ax=9.8, ay=0, xref='x', yref='y', axref='x', ayref='y', **pil_inst),
            dict(x=10.8, y=-0.5, text="x", showarrow=False, xref='x', yref='y', font=dict(size=16, color='black')),
            dict(x=0, y=10.8, ax=0, ay=9.8, xref='x', yref='y', axref='x', ayref='y', **pil_inst),
            dict(x=-0.5, y=10.8, text="y", showarrow=False, xref='x', yref='y', font=dict(size=16, color='black'))
        ], title=title)
    return fig

def skapa_funktions_uppgift(niva=1):
    typ = random.choice(['nollstallen', 'symmetrilinje', 'vertex', 'exponential', 'potens'])
    
    if typ in ['nollstallen', 'symmetrilinje', 'vertex']:
        # Skapa en andragradsfunktion y = a(x-x1)(x-x2)
        x1 = random.randint(-5, -1)
        x2 = random.randint(1, 5)
        a = random.choice([-1, 1]) * random.choice([0.5, 1, 2])
        sym_x = (x1 + x2) / 2
        sym_y = a * (sym_x - x1) * (sym_x - x2)
        
        # Expanderad form y = ax^2 + bx + c
        b = -a * (x1 + x2)
        c = a * x1 * x2
        
        def func(x): return a * x**2 + b * x + c
        
        if typ == 'nollstallen':
            fraga = "Vilka är funktionens nollställen? (Ange x-värdena separerade med mellanslag)"
            svar = sorted([x1, x2])
            u = Uppgift(fraga=fraga, ratt_svar=svar, input_typ='flera_text', svarstyp='array_float', 
                        info_text=f"En funktion är given av f(x) = {a}x^2 + {b}x + {c}",
                        undertext="Sätt f(x) = 0 och lös ekvationen.",
                        plotly_fig=rita_funktion_graf(func, nollstallen=svar))
            return u
            
        elif typ == 'symmetrilinje':
            fraga = "Vilken x-koordinat har funktionens symmetrilinje?"
            u = Uppgift(fraga=fraga, ratt_svar=sym_x, input_typ='text', svarstyp='float',
                        info_text=f"En funktion är given av f(x) = {a}x^2 + {b}x + {c}",
                        undertext="Symmetrilinjen ligger mitt emellan nollställena.",
                        plotly_fig=rita_funktion_graf(func, extrempunkt=(sym_x, sym_y)))
            return u
            
        elif typ == 'vertex':
            extrem_typ = "maximipunkt" if a < 0 else "minimipunkt"
            fraga = f"Vilken y-koordinat har funktionens {extrem_typ} (vertex)?"
            u = Uppgift(fraga=fraga, ratt_svar=sym_y, input_typ='text', svarstyp='float',
                        info_text=f"En funktion är given av f(x) = {a}x^2 + {b}x + {c}",
                        undertext="Beräkna först symmetrilinjen och sätt in i funktionen.",
                        plotly_fig=rita_funktion_graf(func, extrempunkt=(sym_x, sym_y)))
            return u

    elif typ == 'exponential':
        C = random.choice([100, 500, 1000, 2000])
        a = random.choice([1.05, 1.10, 1.20, 0.8, 0.9])
        x_val = random.randint(2, 5)
        y_val = round(C * a**x_val, 2)
        
        fraga = f"Ett startvärde är {C} och förändringsfaktorn är {a}. Vad är värdet efter {x_val} tidsenheter?"
        u = Uppgift(fraga=fraga, ratt_svar=y_val, input_typ='text', svarstyp='float',
                    info_box_text=f"Använd exponentialfunktionen y = C * a^x", info_box_style='blue',
                    undertext="Beräkna y med värdena givna i uppgiften.")
        return u

    elif typ == 'potens':
        y_val = random.choice([25, 36, 49, 64, 81, 100])
        a = random.choice([2, 3])
        x_val = round(y_val ** (1/a), 2)
        
        fraga = f"Lös ekvationen x^{a} = {y_val}. Vad är det positiva värdet på x? (Avrunda till två decimaler)"
        u = Uppgift(fraga=fraga, ratt_svar=x_val, input_typ='text', svarstyp='float',
                    info_box_text="Lös potensekvationen.", info_box_style='pink',
                    undertext="Använd n:te roten ur eller upphöjt till 1/a.")
        return u
