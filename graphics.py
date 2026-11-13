import numpy as np
import plotly.graph_objects as go

def rita_plotly_graf(f, visa_facit=False, q_vis_type='vis_none', trace_x=None, trace_y=None, trace_alla_x=None):
    """
    Ritar en matematisk funktion med Plotly.
    Stöder utritning av specifika punkter (trace_x, trace_y) och anpassning av axlar.
    """
    x = np.linspace(-10, 10, 400)
    y = f(x)
    
    fig = go.Figure()
    
    # Huvudfunktionen
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='f(x)', line=dict(color='blue', width=2.5)))
    
    # Om specifika punkter ska markeras
    if trace_x is not None and trace_y is not None:
        fig.add_trace(go.Scatter(x=trace_x, y=trace_y, mode='markers', name='Punkter', 
                                 marker=dict(color='red', size=10, line=dict(color='black', width=1))))
        
    fig.update_layout(
        xaxis=dict(
            zeroline=True, zerolinewidth=2, zerolinecolor='black', 
            gridcolor='lightgray', range=[-10, 10], dtick=1
        ),
        yaxis=dict(
            zeroline=True, zerolinewidth=2, zerolinecolor='black', 
            gridcolor='lightgray', range=[-10, 10], dtick=1
        ),
        plot_bgcolor='white',
        margin=dict(l=20, r=20, t=20, b=20),
        showlegend=False,
        height=400
    )
    return fig

def rita_traddiagram(grenar, farg1='#1f77b4', farg2='#ff7f0e'):
    """
    Genererar ett probabilistiskt träddiagram.
    'grenar' kan struktureras för att skicka in sannolikheter och etiketter.
    """
    fig = go.Figure()
    
    # Basstruktur för ett 2-stegs träd
    x_nodes = [0, 1, 1, 2, 2, 2, 2]
    y_nodes = [0, 1, -1, 1.5, 0.5, -0.5, -1.5]
    
    # Rita kanter (edges)
    edges = [(0,1), (0,2), (1,3), (1,4), (2,5), (2,6)]
    for edge in edges:
        fig.add_trace(go.Scatter(
            x=[x_nodes[edge[0]], x_nodes[edge[1]]],
            y=[y_nodes[edge[0]], y_nodes[edge[1]]],
            mode='lines',
            line=dict(color='gray', width=2),
            hoverinfo='skip'
        ))
        
    # Rita noder
    fig.add_trace(go.Scatter(
        x=x_nodes, 
        y=y_nodes, 
        mode='markers+text', 
        marker=dict(size=25, color=[farg1, farg1, farg2, farg1, farg2, farg1, farg2], line=dict(color='black', width=1)),
        text=["Start", "A", "B", "A1", "B1", "A2", "B2"],
        textposition="top center"
    ))
        
    fig.update_layout(
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor='white',
        showlegend=False,
        margin=dict(l=20, r=20, t=40, b=20),
        height=300
    )
    return fig

def rita_stat_graf(x, y, titel=""):
    """Ritar ett stapeldiagram för statistikuppgifter."""
    fig = go.Figure(data=[go.Bar(x=x, y=y, marker_color='#4CAF50')])
    fig.update_layout(
        title=titel,
        plot_bgcolor='white',
        xaxis=dict(gridcolor='lightgray', tickmode='linear'),
        yaxis=dict(gridcolor='lightgray'),
        margin=dict(l=20, r=20, t=40, b=20),
        height=350
    )
    return fig
