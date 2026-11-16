import numpy as np
import plotly.graph_objects as go


def rita_plotly_graf(f, visa_facit=False, q_vis_type='vis_none', trace_x=None, trace_y=None, trace_alla_x=None):
    fig = go.Figure()
    x_plot = np.linspace(-10, 10, 400)
    y_plot = f(x_plot)
    fig.add_trace(go.Scatter(x=x_plot, y=y_plot, mode='lines', line=dict(color='blue', width=2), hoverinfo='skip'))

    tx = trace_x[0] if isinstance(trace_x, list) and trace_x else trace_x
    ty = trace_y[0] if isinstance(trace_y, list) and trace_y else trace_y

    if visa_facit:
        if q_vis_type == 'vis_find_y' and tx is not None and ty is not None:
            fig.add_trace(go.Scatter(
                x=[tx, tx, 0], y=[0, ty, ty],
                mode='lines+markers',
                line=dict(color='red', dash='dash', width=2),
                marker=dict(size=8, color='red'),
                showlegend=False, hoverinfo='skip'
            ))
        elif q_vis_type == 'vis_find_x' and ty is not None:
            ax_list = trace_alla_x
            if ax_list:
                min_ax, max_ax = min(ax_list + [0]), max(ax_list + [0])
                fig.add_trace(go.Scatter(
                    x=[min_ax, max_ax], y=[ty, ty],
                    mode='lines',
                    line=dict(color='red', dash='dash', width=2),
                    showlegend=False, hoverinfo='skip'
                ))
                for ax_v in ax_list:
                    fig.add_trace(go.Scatter(
                        x=[ax_v, ax_v], y=[ty, 0],
                        mode='lines+markers',
                        line=dict(color='red', dash='dash', width=2),
                        marker=dict(size=8, color='red'),
                        showlegend=False, hoverinfo='skip'
                    ))

    tick_vals = [-10, -5, 5, 10]
    fig.add_trace(go.Scatter(
        x=tick_vals, y=[-0.6] * 4, mode='text',
        text=[str(v) for v in tick_vals], textposition='bottom center',
        showlegend=False, hoverinfo='skip', textfont=dict(color='black', size=14)
    ))
    fig.add_trace(go.Scatter(
        x=[-0.6] * 4, y=tick_vals, mode='text',
        text=[str(v) for v in tick_vals], textposition='middle left',
        showlegend=False, hoverinfo='skip', textfont=dict(color='black', size=14)
    ))
    fig.add_trace(go.Scatter(
        x=[-0.4], y=[-0.6], mode='text',
        text=['0'], textposition='bottom left',
        showlegend=False, hoverinfo='skip', textfont=dict(color='black', size=14)
    ))

    axis_layout = dict(
        range=[-10.8, 10.8], zeroline=True, zerolinewidth=3, zerolinecolor='black',
        showgrid=True, gridwidth=2, gridcolor='#cccccc',
        minor=dict(dtick=1, gridwidth=2, gridcolor='#e0e0e0'),
        showticklabels=False, fixedrange=True
    )
    pil_inst = dict(showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2, arrowcolor='black')

    fig.update_layout(
        xaxis=axis_layout, yaxis=axis_layout, showlegend=False,
        margin=dict(l=20, r=20, t=20, b=20), height=550,
        plot_bgcolor='white', hovermode=False, dragmode=False,
        annotations=[
            dict(x=10.8, y=0, ax=9.8, ay=0, xref='x', yref='y', axref='x', ayref='y', **pil_inst),
            dict(x=10.8, y=-0.5, text="x", showarrow=False, xref='x', yref='y', font=dict(size=16, color='black')),
            dict(x=0, y=10.8, ax=0, ay=9.8, xref='x', yref='y', axref='x', ayref='y', **pil_inst),
            dict(x=-0.5, y=10.8, text="y", showarrow=False, xref='x', yref='y', font=dict(size=16, color='black'))
        ]
    )
    return fig


def rita_traddiagram(grenar, farg1, farg2):
    fig = go.Figure()
    nodes_x = [0.5, 0.25, 0.75, 0.125, 0.375, 0.625, 0.875]
    nodes_y = [1, 0.5, 0.5, 0, 0, 0, 0]
    edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)]

    for i, (start, end) in enumerate(edges):
        fig.add_trace(go.Scatter(
            x=[nodes_x[start], nodes_x[end]], y=[nodes_y[start], nodes_y[end]],
            mode='lines', line=dict(color='black', width=2), hoverinfo='skip'
        ))
        if i < len(grenar):
            forskjutning = 0.65
            fig.add_annotation(
                x=nodes_x[start] + forskjutning * (nodes_x[end] - nodes_x[start]),
                y=nodes_y[start] + forskjutning * (nodes_y[end] - nodes_y[start]),
                text=f"<b>{grenar[i]}</b>",
                showarrow=False,
                font=dict(size=18, color='red' if grenar[i] == 'x' else '#0056b3'),
                bgcolor="white", borderpad=2
            )

    fig.add_trace(go.Scatter(
        x=nodes_x, y=nodes_y, mode='markers+text',
        marker=dict(size=40, color='white', line=dict(color='black', width=2)),
        text=[f"<b>{lbl}</b>" for lbl in ["Start", farg1, farg2, farg1, farg2, farg1, farg2]],
        textposition="middle center", textfont=dict(color='black', size=14), hoverinfo='skip'
    ))

    fig.add_annotation(x=-0.05, y=0.5, text="<b>Dragning 1</b>", showarrow=False, font=dict(size=14, color="gray"), xanchor="right")
    fig.add_annotation(x=-0.05, y=0, text="<b>Dragning 2</b>", showarrow=False, font=dict(size=14, color="gray"), xanchor="right")
    fig.update_layout(
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.3, 1.05]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.2, 1.1]),
        margin=dict(l=10, r=10, t=10, b=10), height=400,
        plot_bgcolor='white', showlegend=False, hovermode=False, dragmode=False
    )
    return fig


def rita_stat_graf(x, y):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='markers', marker=dict(size=10, color='#8B008B', opacity=0.7), hoverinfo='skip'))
    fig.update_layout(
        xaxis=dict(range=[0, 100], showticklabels=False, showgrid=False, zeroline=False, showline=False),
        yaxis=dict(range=[0, 160], showticklabels=False, showgrid=False, zeroline=False, showline=False),
        margin=dict(l=20, r=20, t=20, b=20), height=450,
        plot_bgcolor='white', hovermode=False, dragmode=False
    )
    fig.add_annotation(x=100, y=0, xref='x', yref='y', ax=0, ay=0, axref='x', ayref='y', showarrow=True, arrowhead=2, arrowsize=1.5, arrowwidth=2, arrowcolor='black')
    fig.add_annotation(x=0, y=160, xref='x', yref='y', ax=0, ay=0, axref='x', ayref='y', showarrow=True, arrowhead=2, arrowsize=1.5, arrowwidth=2, arrowcolor='black')
    return fig
