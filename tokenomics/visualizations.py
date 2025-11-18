"""
Module de visualisations pour l'analyse de tokenomics.
Utilise Plotly pour des graphiques interactifs.
"""

import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any, List
from tokenomics.scenarios import get_inflation_projection


def create_supply_distribution_chart(
    circulating_supply: float,
    total_supply: float,
    max_supply: float
) -> go.Figure:
    """
    Crée un camembert de distribution de la supply.
    
    Args:
        circulating_supply: Supply en circulation
        total_supply: Supply totale actuelle
        max_supply: Supply maximale
        
    Returns:
        Figure Plotly
    """
    # Calcul des différentes parts
    if max_supply > 0:
        locked_supply = total_supply - circulating_supply
        future_supply = max_supply - total_supply
        
        labels = ['En circulation', 'Locked/Vested', 'Non émise']
        values = [circulating_supply, locked_supply, future_supply]
        colors = ['#10b981', '#f59e0b', '#ef4444']
    else:
        # Pas de max supply définie
        locked_supply = total_supply - circulating_supply
        
        labels = ['En circulation', 'Locked/Vested']
        values = [circulating_supply, locked_supply]
        colors = ['#10b981', '#f59e0b']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors),
        hole=0.3,
        textinfo='label+percent',
        textposition='outside',
        hovertemplate='<b>%{label}</b><br>%{value:,.0f}<br>%{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title={
            'text': "Distribution de la Supply",
            'x': 0.5,
            'xanchor': 'center'
        },
        showlegend=True,
        height=400,
        margin=dict(t=80, b=20, l=20, r=20)
    )
    
    return fig


def create_dilution_projection(
    circulating_supply: float,
    scenario_name: str = None,
    inflation_rate: float = 5.0,
    years: int = 5
) -> go.Figure:
    """
    Crée une projection de dilution sur X années.
    
    Args:
        circulating_supply: Supply actuelle en circulation
        scenario_name: Nom du scénario (pour projection spécifique)
        inflation_rate: Taux d'inflation annuel par défaut (%)
        years: Nombre d'années à projeter
        
    Returns:
        Figure Plotly
    """
    # Obtenir les taux d'inflation par année
    if scenario_name:
        inflation_rates = get_inflation_projection(scenario_name, years)
    else:
        inflation_rates = [inflation_rate] * years
    
    # Calculer la supply cumulée
    year_labels = ['Année 0'] + [f'Année {i+1}' for i in range(years)]
    supply_values = [circulating_supply]
    
    current_supply = circulating_supply
    for rate in inflation_rates:
        current_supply = current_supply * (1 + rate / 100)
        supply_values.append(current_supply)
    
    # Calculer le % de dilution depuis le début
    dilution_pct = [(s / circulating_supply - 1) * 100 for s in supply_values]
    
    # Créer le graphique avec deux axes Y
    fig = go.Figure()
    
    # Ligne de supply (axe Y gauche)
    fig.add_trace(go.Scatter(
        x=year_labels,
        y=supply_values,
        name='Supply totale',
        mode='lines+markers',
        line=dict(color='#6366f1', width=3),
        marker=dict(size=8),
        hovertemplate='<b>%{x}</b><br>Supply: %{y:,.0f}<extra></extra>'
    ))
    
    # Barres de dilution (axe Y droit)
    fig.add_trace(go.Bar(
        x=year_labels,
        y=dilution_pct,
        name='Dilution cumulée',
        marker=dict(
            color=dilution_pct,
            colorscale='Reds',
            showscale=False
        ),
        yaxis='y2',
        hovertemplate='<b>%{x}</b><br>Dilution: %{y:.1f}%<extra></extra>',
        opacity=0.6
    ))
    
    fig.update_layout(
        title={
            'text': "Projection de Dilution",
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis=dict(title='Période'),
        yaxis=dict(
            title='Supply',
            titlefont=dict(color='#6366f1'),
            tickfont=dict(color='#6366f1')
        ),
        yaxis2=dict(
            title='Dilution cumulée (%)',
            titlefont=dict(color='#ef4444'),
            tickfont=dict(color='#ef4444'),
            overlaying='y',
            side='right'
        ),
        hovermode='x unified',
        height=450,
        showlegend=True,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        ),
        margin=dict(t=100, b=60, l=60, r=60)
    )
    
    return fig


def create_score_breakdown_chart(score_data: Dict[str, Any]) -> go.Figure:
    """
    Crée un graphique en barres des scores par catégorie.
    
    Args:
        score_data: Résultats de calculate_viability_index()
        
    Returns:
        Figure Plotly
    """
    categories = ['Inflation', 'Distribution', 'Utilité', 'Gouvernance', 'Incitations']
    scores = [
        score_data['inflation_score'],
        score_data['distribution_score'],
        score_data['utility_score'],
        score_data['governance_score'],
        score_data['incentives_score']
    ]
    weights = [
        score_data['weights']['inflation'] * 100,
        score_data['weights']['distribution'] * 100,
        score_data['weights']['utility'] * 100,
        score_data['weights']['governance'] * 100,
        score_data['weights']['incentives'] * 100
    ]
    
    # Couleurs selon le score
    colors = []
    for score in scores:
        if score >= 80:
            colors.append('#10b981')  # Vert
        elif score >= 65:
            colors.append('#84cc16')  # Vert clair
        elif score >= 50:
            colors.append('#f59e0b')  # Orange
        else:
            colors.append('#ef4444')  # Rouge
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=categories,
        y=scores,
        marker=dict(color=colors),
        text=[f"{s:.1f}<br>({w:.0f}%)" for s, w in zip(scores, weights)],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Score: %{y:.1f}/100<extra></extra>'
    ))
    
    # Ligne de référence à 50
    fig.add_hline(
        y=50,
        line_dash="dash",
        line_color="gray",
        annotation_text="Seuil minimal",
        annotation_position="right"
    )
    
    fig.update_layout(
        title={
            'text': "Scores par Composante (pondération entre parenthèses)",
            'x': 0.5,
            'xanchor': 'center'
        },
        yaxis=dict(
            title='Score / 100',
            range=[0, 105]
        ),
        xaxis=dict(title=''),
        height=400,
        showlegend=False,
        margin=dict(t=80, b=60, l=60, r=40)
    )
    
    return fig


def create_gauge_chart(score: float, title: str = "Tokenomics Viability Index") -> go.Figure:
    """
    Crée une jauge circulaire pour le score final.
    
    Args:
        score: Score final (0-100)
        title: Titre du graphique
        
    Returns:
        Figure Plotly
    """
    # Déterminer la couleur selon le score
    if score >= 80:
        color = '#10b981'  # Vert
    elif score >= 65:
        color = '#84cc16'  # Vert clair
    elif score >= 50:
        color = '#f59e0b'  # Orange
    elif score >= 35:
        color = '#fb923c'  # Orange foncé
    else:
        color = '#ef4444'  # Rouge
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 24}},
        number={'suffix': "/100", 'font': {'size': 48}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkgray"},
            'bar': {'color': color, 'thickness': 0.75},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 35], 'color': '#fee2e2'},
                {'range': [35, 50], 'color': '#fed7aa'},
                {'range': [50, 65], 'color': '#fef3c7'},
                {'range': [65, 80], 'color': '#d9f99d'},
                {'range': [80, 100], 'color': '#d1fae5'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 50
            }
        }
    ))
    
    fig.update_layout(
        height=350,
        margin=dict(t=80, b=20, l=40, r=40)
    )
    
    return fig


def create_inflation_comparison(scenarios: List[str], years: int = 5) -> go.Figure:
    """
    Compare les projections d'inflation de plusieurs scénarios.
    
    Args:
        scenarios: Liste des noms de scénarios à comparer
        years: Nombre d'années
        
    Returns:
        Figure Plotly
    """
    fig = go.Figure()
    
    for scenario in scenarios:
        inflation_rates = get_inflation_projection(scenario, years)
        year_labels = [f'An {i+1}' for i in range(years)]
        
        fig.add_trace(go.Scatter(
            x=year_labels,
            y=inflation_rates,
            name=scenario,
            mode='lines+markers',
            line=dict(width=2),
            marker=dict(size=8)
        ))
    
    fig.update_layout(
        title={
            'text': "Comparaison des Taux d'Inflation Annuels",
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis=dict(title='Année'),
        yaxis=dict(title='Taux d\'inflation (%)'),
        hovermode='x unified',
        height=450,
        showlegend=True,
        legend=dict(
            orientation='v',
            yanchor='top',
            y=0.99,
            xanchor='left',
            x=0.01
        ),
        margin=dict(t=80, b=60, l=60, r=40)
    )
    
    return fig

