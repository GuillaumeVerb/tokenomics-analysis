"""
Tokenomics Analyzer - Application Streamlit

Application pour analyser la viabilité de la tokenomics des projets crypto.
"""

import streamlit as st
from typing import Dict, Any

from tokenomics.scenarios import (
    get_scenario_categories,
    get_all_scenarios,
    get_scenario_params
)
from tokenomics.scoring import (
    calculate_viability_index,
    get_recommendations
)
from tokenomics.api import (
    fetch_coingecko_data,
    parse_coingecko_to_params,
    enhance_params_with_known_data,
    search_coingecko_coin,
    get_enriched_tokens_list
)
from tokenomics.visualizations import (
    create_supply_distribution_chart,
    create_dilution_projection,
    create_score_breakdown_chart,
    create_gauge_chart
)


# Configuration de la page
st.set_page_config(
    page_title="Tokenomics Analyzer",
    page_icon="🪙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialiser le thème
if 'theme' not in st.session_state:
    st.session_state['theme'] = 'dark'

# Appliquer le CSS selon le thème
if st.session_state['theme'] == 'light':
    st.markdown("""
    <style>
        .stApp {
            background-color: #ffffff;
            color: #000000;
        }
        .stSidebar {
            background-color: #f0f2f6;
        }
        h1, h2, h3 {
            color: #1f1f1f !important;
        }
        .stMetric {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 15px;
        }
        .stExpander {
            background-color: #ffffff;
            border: 1px solid #e0e0e0;
        }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
        .stApp {
            background-color: #0e1117;
            color: #fafafa;
        }
        .stSidebar {
            background-color: #1e1e1e;
        }
        .stMetric {
            background-color: #1e1e1e;
            border-radius: 10px;
            padding: 15px;
        }
    </style>
    """, unsafe_allow_html=True)


def init_session_state():
    """Initialise les variables de session."""
    if 'analysis_params' not in st.session_state:
        st.session_state.analysis_params = None
    if 'current_scenario' not in st.session_state:
        st.session_state.current_scenario = "Aucun (configuration manuelle)"


def load_scenario(scenario_name: str):
    """Charge un scénario préconfigé dans le state."""
    if scenario_name != "Aucun (configuration manuelle)":
        params = get_scenario_params(scenario_name)
        st.session_state.analysis_params = params
        st.session_state.current_scenario = scenario_name
    else:
        st.session_state.current_scenario = scenario_name


def render_header():
    """Affiche l'en-tête de l'application."""
    st.title("🪙 Tokenomics Analyzer")
    st.markdown("""
    **Analysez la viabilité économique d'un projet crypto en quelques clics.**
    
    L'analyse produit un **Tokenomics Viability Index** (0–100) basé sur 5 piliers :
    inflation, distribution, utilité, gouvernance et incitations.
    """)
    st.divider()


def render_quick_analysis():
    """Affiche le mode d'analyse rapide CoinGecko."""
    st.header("⚡ Mode Analyse Rapide")
    st.markdown("Importez automatiquement les données depuis CoinGecko.")
    
    # Boutons rapides pour tokens populaires
    st.markdown("**🔥 Tokens populaires :**")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    quick_tokens = [
        ("Bitcoin", "btc", col1),
        ("Ethereum", "eth", col2),
        ("Solana", "sol", col3),
        ("BNB", "bnb", col4),
        ("Cardano", "ada", col5),
        ("Avalanche", "avax", col6),
    ]
    
    selected_quick_token = None
    for name, symbol, column in quick_tokens:
        with column:
            if st.button(f"₿ {name}", key=f"quick_{symbol}", use_container_width=True):
                selected_quick_token = symbol
    
    st.divider()
    
    # Champ de recherche manuel
    col1, col2 = st.columns([3, 1])
    
    with col1:
        coin_input = st.text_input(
            "Ou entrez un nom/symbole",
            placeholder="BTC, ETH, SOL, uniswap, aave...",
            help="Accepte les symboles (BTC, ETH) ou noms complets (bitcoin, ethereum)",
            value=selected_quick_token if selected_quick_token else ""
        )
    
    with col2:
        analyze_button = st.button("🔍 Analyser", type="primary", use_container_width=True)
    
    # Si bouton rapide cliqué, analyser automatiquement
    if selected_quick_token:
        coin_input = selected_quick_token
        analyze_button = True
    
    if analyze_button and coin_input:
        with st.spinner(f"Récupération des données pour '{coin_input}'..."):
            # Tentative de récupération directe
            data = fetch_coingecko_data(coin_input.lower())
            
            if data:
                params = parse_coingecko_to_params(data)
                params = enhance_params_with_known_data(params, coin_input.lower())
                
                st.success(f"✅ Données récupérées pour **{params['name']}** ({params['symbol']})")
                
                # Afficher les infos de base
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Prix", f"${params['price_usd']:,.2f}")
                with col2:
                    st.metric("Market Cap", f"${params['market_cap_usd']:,.0f}")
                with col3:
                    st.metric("Circulating Supply", f"{params['circulating_supply']:,.0f}")
                with col4:
                    if params['max_supply'] > 0:
                        st.metric("Max Supply", f"{params['max_supply']:,.0f}")
                    else:
                        st.metric("Max Supply", "Illimité")
                
                # Badge de qualité des données
                if params.get('is_enriched', False):
                    st.success(f"✅ **{params['description']}**")
                    st.info(f"📊 Market Cap Rank: #{params.get('market_cap_rank', 'N/A')}")
                else:
                    st.info(f"ℹ️ {params['description']}")
                    st.warning("⚠️ **Scores basés sur des heuristiques** (market cap rank, supply ratio). Les 27 tokens enrichis ont des vraies données. Ajustez manuellement pour plus de précision.")
                
                # Stocker dans la session
                st.session_state.analysis_params = params
                
                # Afficher l'analyse
                render_analysis_results(params, coin_input.lower())
                
            else:
                st.error(f"❌ Token '{coin_input}' non trouvé sur CoinGecko.")
                
                # Suggestions intelligentes
                col1, col2 = st.columns(2)
                
                with col1:
                    st.info("""
                    **💡 Essayez avec :**
                    - Un **symbole** : BTC, ETH, SOL, UNI
                    - Un **nom complet** : bitcoin, ethereum, solana
                    - L'**ID CoinGecko** exact : curve-dao-token
                    """)
                
                with col2:
                    st.success("""
                    **✅ Tokens populaires qui fonctionnent :**
                    - Bitcoin (`btc` ou `bitcoin`)
                    - Ethereum (`eth` ou `ethereum`)
                    - Uniswap (`uni` ou `uniswap`)
                    - Aave (`aave`)
                    """)
                
                # Recherche de tokens similaires
                with st.spinner("Recherche de tokens similaires..."):
                    results = search_coingecko_coin(coin_input)
                    if results:
                        st.write("**🔍 Tokens similaires trouvés :**")
                        for result in results[:5]:
                            st.write(f"- **{result['name']}** ({result['symbol'].upper()}) → essayez `{result['id']}`")


def render_manual_analysis():
    """Affiche le mode d'analyse manuelle avancée."""
    st.header("🔧 Mode Analyse Manuelle")
    st.markdown("Configuration complète des paramètres ou chargement d'un scénario préconfigé.")
    
    # Sélection de scénario
    st.subheader("📋 Scénarios Préconfigurés")
    
    categories = get_scenario_categories()
    all_scenarios = ["Aucun (configuration manuelle)"] + get_all_scenarios()
    
    # Organiser par catégories
    selected_scenario = st.selectbox(
        "Charger un scénario type",
        options=all_scenarios,
        index=all_scenarios.index(st.session_state.current_scenario) if st.session_state.current_scenario in all_scenarios else 0,
        help="Sélectionnez un scénario pour pré-remplir les champs automatiquement"
    )
    
    if selected_scenario != st.session_state.current_scenario:
        load_scenario(selected_scenario)
        st.rerun()
    
    # Afficher la description du scénario si disponible
    if selected_scenario != "Aucun (configuration manuelle)":
        params = get_scenario_params(selected_scenario)
        st.info(f"📄 **Description** : {params.get('description', 'N/A')}")
    
    st.divider()
    
    # Récupérer les paramètres par défaut
    if st.session_state.analysis_params and selected_scenario != "Aucun (configuration manuelle)":
        default_params = st.session_state.analysis_params
    else:
        default_params = {
            'circulating_supply': 500_000_000,
            'total_supply': 1_000_000_000,
            'max_supply': 1_000_000_000,
            'inflation_rate': 5.0,
            'emission_years_left': 5,
            'team_allocation': 15.0,
            'vesting_years': 3,
            'top_10_concentration': 30.0,
            'utility_gas': False,
            'utility_staking': True,
            'utility_governance': True,
            'utility_collateral': False,
            'utility_discount': False,
            'gov_timelock': True,
            'gov_multisig': True,
            'gov_dao_active': True,
            'incentive_lock': False,
            'incentive_staking': True,
            'incentive_burn': False,
            'lock_duration_months': 0,
            'burn_rate': 0.0
        }
    
    # Formulaire de saisie
    with st.form("manual_analysis_form"):
        st.subheader("📊 Supply & Inflation")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            circulating_supply = st.number_input(
                "Circulating Supply",
                min_value=0.0,
                value=float(default_params['circulating_supply']),
                step=1_000_000.0,
                format="%.0f"
            )
        with col2:
            total_supply = st.number_input(
                "Total Supply",
                min_value=0.0,
                value=float(default_params['total_supply']),
                step=1_000_000.0,
                format="%.0f"
            )
        with col3:
            max_supply = st.number_input(
                "Max Supply (0 = illimité)",
                min_value=0.0,
                value=float(default_params['max_supply']),
                step=1_000_000.0,
                format="%.0f"
            )
        
        col1, col2 = st.columns(2)
        with col1:
            inflation_rate = st.number_input(
                "Taux d'inflation annuel (%)",
                min_value=-10.0,
                max_value=100.0,
                value=float(default_params['inflation_rate']),
                step=0.5,
                help="Négatif si burn > emissions"
            )
        with col2:
            emission_years_left = st.number_input(
                "Années d'émission restantes",
                min_value=0,
                max_value=999,
                value=int(default_params['emission_years_left']),
                step=1
            )
        
        st.divider()
        st.subheader("📈 Distribution")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            team_allocation = st.slider(
                "Allocation team/insiders (%)",
                min_value=0.0,
                max_value=50.0,
                value=float(default_params['team_allocation']),
                step=0.5
            )
        with col2:
            vesting_years = st.number_input(
                "Durée du vesting (années)",
                min_value=0,
                max_value=10,
                value=int(default_params['vesting_years']),
                step=1
            )
        with col3:
            top_10_concentration = st.slider(
                "Concentration top 10 (%)",
                min_value=0.0,
                max_value=100.0,
                value=float(default_params['top_10_concentration']),
                step=1.0
            )
        
        st.divider()
        st.subheader("🔧 Utilité")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            utility_gas = st.checkbox("Gas fees", value=default_params['utility_gas'])
        with col2:
            utility_staking = st.checkbox("Staking", value=default_params['utility_staking'])
        with col3:
            utility_governance = st.checkbox("Gouvernance", value=default_params['utility_governance'])
        with col4:
            utility_collateral = st.checkbox("Collatéral", value=default_params['utility_collateral'])
        with col5:
            utility_discount = st.checkbox("Discount", value=default_params['utility_discount'])
        
        st.divider()
        st.subheader("🏛️ Gouvernance")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            gov_timelock = st.checkbox("Timelock présent", value=default_params['gov_timelock'])
        with col2:
            gov_multisig = st.checkbox("Multisig présent", value=default_params['gov_multisig'])
        with col3:
            gov_dao_active = st.checkbox("DAO active", value=default_params['gov_dao_active'])
        
        st.divider()
        st.subheader("🎁 Incitations")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            incentive_lock = st.checkbox("Lock/ve-token", value=default_params['incentive_lock'])
            lock_duration_months = st.number_input(
                "Durée du lock (mois)",
                min_value=0,
                max_value=120,
                value=int(default_params['lock_duration_months']),
                step=6,
                disabled=not incentive_lock
            )
        with col2:
            incentive_staking = st.checkbox("Staking rewards", value=default_params['incentive_staking'])
        with col3:
            incentive_burn = st.checkbox("Burn mechanism", value=default_params['incentive_burn'])
            burn_rate = st.number_input(
                "Taux de burn (%)",
                min_value=0.0,
                max_value=100.0,
                value=float(default_params['burn_rate']),
                step=0.1,
                disabled=not incentive_burn
            )
        
        st.divider()
        submit_button = st.form_submit_button("📊 Analyser la Tokenomics", type="primary", use_container_width=True)
    
    # Traitement du formulaire
    if submit_button:
        params = {
            'circulating_supply': circulating_supply,
            'total_supply': total_supply,
            'max_supply': max_supply,
            'inflation_rate': inflation_rate,
            'emission_years_left': emission_years_left,
            'team_allocation': team_allocation,
            'vesting_years': vesting_years,
            'top_10_concentration': top_10_concentration,
            'utility_gas': utility_gas,
            'utility_staking': utility_staking,
            'utility_governance': utility_governance,
            'utility_collateral': utility_collateral,
            'utility_discount': utility_discount,
            'gov_timelock': gov_timelock,
            'gov_multisig': gov_multisig,
            'gov_dao_active': gov_dao_active,
            'incentive_lock': incentive_lock,
            'incentive_staking': incentive_staking,
            'incentive_burn': incentive_burn,
            'lock_duration_months': lock_duration_months,
            'burn_rate': burn_rate
        }
        
        st.session_state.analysis_params = params
        render_analysis_results(params, selected_scenario)


def generate_export_html(params: Dict[str, Any], score_data: Dict[str, Any], recommendations: list) -> str:
    """Génère un HTML pour export/impression PDF."""
    token_name = params.get('name', 'Token')
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Tokenomics Analysis - {token_name}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            h1 {{ color: #6366f1; }}
            h2 {{ color: #4338ca; margin-top: 30px; }}
            .score {{ font-size: 48px; font-weight: bold; color: #10b981; }}
            .metric {{ display: inline-block; margin: 10px 20px; }}
            .metric-label {{ font-weight: bold; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
            th {{ background-color: #6366f1; color: white; }}
            .recommendation {{ margin: 10px 0; padding: 10px; background: #f3f4f6; border-radius: 5px; }}
            @media print {{ body {{ margin: 20px; }} }}
        </style>
    </head>
    <body>
        <h1>🪙 Tokenomics Analysis Report</h1>
        <h2>{token_name} ({params.get('symbol', 'N/A')})</h2>
        <p><strong>Date:</strong> {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        
        <h2>📊 Score Final</h2>
        <div class="score">{score_data['final_score']}/100</div>
        <p><strong>Verdict:</strong> {score_data['verdict']}</p>
        
        <h2>📈 Métriques Principales</h2>
        <div class="metric">
            <div class="metric-label">Prix:</div>
            ${params.get('price_usd', 0):,.2f}
        </div>
        <div class="metric">
            <div class="metric-label">Market Cap:</div>
            ${params.get('market_cap_usd', 0):,.0f}
        </div>
        <div class="metric">
            <div class="metric-label">Circulating Supply:</div>
            {params['circulating_supply']:,.0f}
        </div>
        <div class="metric">
            <div class="metric-label">Max Supply:</div>
            {'Illimité' if params['max_supply'] == 0 else f"{params['max_supply']:,.0f}"}
        </div>
        
        <h2>🎯 Scores Détaillés</h2>
        <table>
            <tr>
                <th>Composante</th>
                <th>Score</th>
                <th>Pondération</th>
                <th>Commentaire</th>
            </tr>
            <tr>
                <td>Inflation</td>
                <td>{score_data['inflation_score']:.1f}/100</td>
                <td>{score_data['weights']['inflation']*100:.0f}%</td>
                <td>{score_data['inflation_comment']}</td>
            </tr>
            <tr>
                <td>Distribution</td>
                <td>{score_data['distribution_score']:.1f}/100</td>
                <td>{score_data['weights']['distribution']*100:.0f}%</td>
                <td>{score_data['distribution_comment']}</td>
            </tr>
            <tr>
                <td>Utilité</td>
                <td>{score_data['utility_score']:.1f}/100</td>
                <td>{score_data['weights']['utility']*100:.0f}%</td>
                <td>{score_data['utility_comment']}</td>
            </tr>
            <tr>
                <td>Gouvernance</td>
                <td>{score_data['governance_score']:.1f}/100</td>
                <td>{score_data['weights']['governance']*100:.0f}%</td>
                <td>{score_data['governance_comment']}</td>
            </tr>
            <tr>
                <td>Incitations</td>
                <td>{score_data['incentives_score']:.1f}/100</td>
                <td>{score_data['weights']['incentives']*100:.0f}%</td>
                <td>{score_data['incentives_comment']}</td>
            </tr>
        </table>
        
        <h2>💡 Recommandations</h2>
        {''.join([f'<div class="recommendation">{rec}</div>' for rec in recommendations])}
        
        <hr style="margin-top: 50px;">
        <p style="text-align: center; color: gray;">
            Généré par <strong>Tokenomics Analyzer</strong> | 
            <a href="https://github.com/GuillaumeVerb/tokenomics-analysis">GitHub</a>
        </p>
        <p style="text-align: center; color: gray; font-size: 12px;">
            ⚠️ Cet outil est fourni à titre éducatif. Pas de conseil en investissement. DYOR.
        </p>
    </body>
    </html>
    """
    return html


def render_analysis_results(params: Dict[str, Any], scenario_name: str = None):
    """Affiche les résultats de l'analyse."""
    st.divider()
    
    # Bouton d'export en haut
    col_header1, col_header2 = st.columns([3, 1])
    with col_header1:
        st.header("📊 Résultats de l'Analyse")
    
    # Calcul du score
    score_data = calculate_viability_index(params)
    recommendations = get_recommendations(score_data)
    
    # Ajouter à l'historique
    if 'history' not in st.session_state:
        st.session_state['history'] = []
    
    import datetime
    history_entry = {
        'name': params.get('name', 'Token'),
        'symbol': params.get('symbol', 'N/A'),
        'score': score_data['final_score'],
        'time': datetime.datetime.now().strftime('%H:%M'),
        'params': params
    }
    
    # Éviter les doublons (même token dans les 2 dernières entrées)
    if not st.session_state['history'] or st.session_state['history'][-1]['symbol'] != history_entry['symbol']:
        st.session_state['history'].append(history_entry)
    
    # Limiter à 20 entrées max
    if len(st.session_state['history']) > 20:
        st.session_state['history'] = st.session_state['history'][-20:]
    
    # Bouton d'export
    with col_header2:
        html_export = generate_export_html(params, score_data, recommendations)
        st.download_button(
            label="📥 Export PDF",
            data=html_export,
            file_name=f"tokenomics_{params.get('symbol', 'token')}_{__import__('datetime').datetime.now().strftime('%Y%m%d')}.html",
            mime="text/html",
            help="Téléchargez le rapport (ouvrez le fichier HTML et imprimez en PDF)",
            use_container_width=True
        )
    
    # Score final (grande jauge)
    st.subheader("🎯 Score Final")
    gauge_fig = create_gauge_chart(score_data['final_score'])
    st.plotly_chart(gauge_fig, use_container_width=True)
    
    # Verdict
    verdict_colors = {
        'green': '🟢',
        'orange': '🟠',
        'red': '🔴'
    }
    verdict_emoji = verdict_colors.get(score_data['verdict_color'], '⚪')
    st.markdown(f"### {verdict_emoji} {score_data['verdict']} — Score : **{score_data['final_score']}/100**")
    
    st.divider()
    
    # Scores détaillés
    st.subheader("📈 Scores par Composante")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        breakdown_fig = create_score_breakdown_chart(score_data)
        st.plotly_chart(breakdown_fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 📋 Détails")
        
        components = [
            ("Inflation", score_data['inflation_score'], score_data['inflation_comment']),
            ("Distribution", score_data['distribution_score'], score_data['distribution_comment']),
            ("Utilité", score_data['utility_score'], score_data['utility_comment']),
            ("Gouvernance", score_data['governance_score'], score_data['governance_comment']),
            ("Incitations", score_data['incentives_score'], score_data['incentives_comment']),
            ("💰 Liquidité", score_data.get('liquidity_score', 0), score_data.get('liquidity_comment', 'N/A')),
            ("🌍 Adoption", score_data.get('adoption_score', 0), score_data.get('adoption_comment', 'N/A')),
            ("🔐 Sécurité", score_data.get('security_score', 0), score_data.get('security_comment', 'N/A'))
        ]
        
        for name, score, comment in components:
            with st.expander(f"**{name}** : {score:.1f}/100"):
                st.write(comment)
    
    st.divider()
    
    # Visualisations
    st.subheader("📊 Visualisations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        supply_fig = create_supply_distribution_chart(
            params['circulating_supply'],
            params['total_supply'],
            params['max_supply']
        )
        st.plotly_chart(supply_fig, use_container_width=True)
    
    with col2:
        dilution_fig = create_dilution_projection(
            params['circulating_supply'],
            scenario_name=scenario_name if scenario_name and scenario_name != "Aucun (configuration manuelle)" else None,
            inflation_rate=params['inflation_rate'],
            years=5
        )
        st.plotly_chart(dilution_fig, use_container_width=True)
    
    st.divider()
    
    # Recommandations
    st.subheader("💡 Recommandations")
    
    if recommendations:
        for rec in recommendations:
            st.markdown(f"- {rec}")
    else:
        st.success("✅ Aucune recommandation spécifique. La tokenomics semble bien équilibrée.")


def render_comparison_mode():
    """Affiche le mode de comparaison de 2 tokens."""
    st.header("⚖️ Mode Comparaison")
    st.markdown("Comparez la tokenomics de 2 projets côte à côte.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🅰️ Token A")
        token_a = st.text_input("Token A", placeholder="bitcoin, eth, sol...", key="token_a")
        analyze_a = st.button("Analyser A", key="btn_a", type="primary", use_container_width=True)
    
    with col2:
        st.subheader("🅱️ Token B")
        token_b = st.text_input("Token B", placeholder="ethereum, btc, ada...", key="token_b")
        analyze_b = st.button("Analyser B", key="btn_b", type="primary", use_container_width=True)
    
    # Analyser Token A
    if analyze_a and token_a:
        with col1:
            with st.spinner(f"Analyse de {token_a}..."):
                data_a = fetch_coingecko_data(token_a)
                if data_a:
                    params_a = parse_coingecko_to_params(data_a)
                    params_a = enhance_params_with_known_data(params_a, token_a.lower())
                    st.session_state['comparison_a'] = params_a
                    st.success(f"✅ {params_a['name']} chargé")
                else:
                    st.error(f"❌ {token_a} non trouvé")
    
    # Analyser Token B
    if analyze_b and token_b:
        with col2:
            with st.spinner(f"Analyse de {token_b}..."):
                data_b = fetch_coingecko_data(token_b)
                if data_b:
                    params_b = parse_coingecko_to_params(data_b)
                    params_b = enhance_params_with_known_data(params_b, token_b.lower())
                    st.session_state['comparison_b'] = params_b
                    st.success(f"✅ {params_b['name']} chargé")
                else:
                    st.error(f"❌ {token_b} non trouvé")
    
    # Si les deux tokens sont chargés, afficher la comparaison
    if 'comparison_a' in st.session_state and 'comparison_b' in st.session_state:
        st.divider()
        st.header("📊 Comparaison des Scores")
        
        params_a = st.session_state['comparison_a']
        params_b = st.session_state['comparison_b']
        
        score_a = calculate_viability_index(params_a)
        score_b = calculate_viability_index(params_b)
        
        # Scores finaux
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                f"🅰️ {params_a['name']}",
                f"{score_a['final_score']:.1f}/100",
                delta=None
            )
        with col2:
            st.metric(
                f"🅱️ {params_b['name']}",
                f"{score_b['final_score']:.1f}/100",
                delta=f"{score_b['final_score'] - score_a['final_score']:+.1f}"
            )
        
        # Tableau comparatif
        st.subheader("Comparaison Détaillée")
        
        comparison_data = {
            "Composante": ["Inflation", "Distribution", "Utilité", "Gouvernance", "Incitations", "**TOTAL**"],
            f"🅰️ {params_a['name']}": [
                f"{score_a['inflation_score']:.1f}",
                f"{score_a['distribution_score']:.1f}",
                f"{score_a['utility_score']:.1f}",
                f"{score_a['governance_score']:.1f}",
                f"{score_a['incentives_score']:.1f}",
                f"**{score_a['final_score']:.1f}**"
            ],
            f"🅱️ {params_b['name']}": [
                f"{score_b['inflation_score']:.1f}",
                f"{score_b['distribution_score']:.1f}",
                f"{score_b['utility_score']:.1f}",
                f"{score_b['governance_score']:.1f}",
                f"{score_b['incentives_score']:.1f}",
                f"**{score_b['final_score']:.1f}**"
            ],
            "Différence": [
                f"{score_b['inflation_score'] - score_a['inflation_score']:+.1f}",
                f"{score_b['distribution_score'] - score_a['distribution_score']:+.1f}",
                f"{score_b['utility_score'] - score_a['utility_score']:+.1f}",
                f"{score_b['governance_score'] - score_a['governance_score']:+.1f}",
                f"{score_b['incentives_score'] - score_a['incentives_score']:+.1f}",
                f"**{score_b['final_score'] - score_a['final_score']:+.1f}**"
            ]
        }
        
        import pandas as pd
        df = pd.DataFrame(comparison_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Métriques supply
        st.subheader("📈 Supply & Inflation")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**🅰️**")
            st.metric("Circulating", f"{params_a['circulating_supply']:,.0f}")
            st.metric("Inflation", f"{params_a['inflation_rate']:.1f}%")
        
        with col2:
            st.markdown("**🅱️**")
            st.metric("Circulating", f"{params_b['circulating_supply']:,.0f}")
            st.metric("Inflation", f"{params_b['inflation_rate']:.1f}%")
        
        with col3:
            st.markdown("**Gagnant**")
            if score_a['inflation_score'] > score_b['inflation_score']:
                st.success(f"🅰️ {params_a['name']}")
            elif score_b['inflation_score'] > score_a['inflation_score']:
                st.success(f"🅱️ {params_b['name']}")
            else:
                st.info("Égalité")


def render_methodology():
    """Affiche la section méthodologie."""
    st.header("📚 Méthodologie & Limites")
    
    # Liste des tokens enrichis
    with st.expander("✅ **Liste des 60+ Tokens Enrichis** (données réelles)", expanded=False):
        st.markdown("""
        Ces tokens disposent de **vraies données** collectées manuellement (concentration réelle, allocations confirmées, utilités vérifiées).
        
        Les autres tokens utilisent des **heuristiques automatiques** basées sur le market cap rank et le supply ratio.
        """)
        
        enriched_tokens = get_enriched_tokens_list()
        
        for category, tokens in enriched_tokens.items():
            st.markdown(f"### {category}")
            cols = st.columns(3)
            for i, token in enumerate(tokens):
                with cols[i % 3]:
                    token_display = token.replace('-', ' ').title()
                    st.markdown(f"- `{token}`")
        
        st.info(f"**Total : {sum(len(tokens) for tokens in enriched_tokens.values())} tokens enrichis** 🎉")
    
    with st.expander("🔍 **Comment est calculé le Tokenomics Viability Index ?**"):
        st.markdown("""
        Le score final (0–100) est une moyenne pondérée de 5 composantes :
        
        1. **Inflation (25%)** : Évalue la pression de l'émission future sur le prix
           - Dilution potentielle (supply non émise)
           - Taux d'inflation annuel
           - Durée des émissions
        
        2. **Distribution (20%)** : Analyse l'équité et la décentralisation
           - Allocation team/insiders
           - Durée du vesting
           - Concentration des top holders
        
        3. **Utilité (25%)** : Mesure les cas d'usage réels
           - Gas fees (forte utilité)
           - Staking
           - Gouvernance
           - Collatéral
           - Discounts/rewards
        
        4. **Gouvernance (15%)** : Évalue la sécurité et décentralisation
           - Présence de timelock
           - Multisig
           - DAO active
           - Impact de la concentration
        
        5. **Incitations (15%)** : Analyse les mécanismes d'engagement
           - Lock/ve-token
           - Staking rewards
           - Burn mechanisms
           - Synergie entre mécanismes
        
        **Score final** : Σ (score_composante × pondération)
        """)
    
    with st.expander("⚠️ **Limites & Hypothèses**"):
        st.markdown("""
        Cette analyse présente plusieurs limites importantes :
        
        **Données CoinGecko :**
        - Supply data : fiable
        - Inflation : estimée (non toujours disponible)
        - Paramètres qualitatifs : valeurs par défaut à ajuster manuellement
        
        **Hypothèses simplificatrices :**
        - Inflation linéaire (sauf scénarios spécifiques)
        - Pas de prise en compte de la vélocité du token
        - Gouvernance évaluée de manière binaire (présent/absent)
        - Pas d'analyse de sentiment ou d'adoption réelle
        
        **Ce que l'outil NE fait PAS :**
        - ❌ Recommandation d'investissement
        - ❌ Analyse de l'équipe ou du produit
        - ❌ Audit de smart contracts
        - ❌ Analyse de marché ou de compétition
        
        **Ce que vous DEVEZ faire :**
        - ✅ DYOR (Do Your Own Research)
        - ✅ Vérifier les données sur les sources officielles
        - ✅ Lire la documentation du projet
        - ✅ Consulter des audits indépendants
        """)
    
    with st.expander("📖 **Sources & Références**"):
        st.markdown("""
        **APIs utilisées :**
        - [CoinGecko API](https://www.coingecko.com/en/api) : données de supply et prix
        
        **Références méthodologiques :**
        - Tokenomics frameworks : Outlier Ventures, Messari
        - DeFi protocols : Curve, Pendle, EigenLayer whitepapers
        - Burn mechanisms : EIP-1559 (Ethereum)
        
        **Code source :**
        - GitHub : [lien du repo]
        - Licence : MIT
        """)


def main():
    """Fonction principale de l'application."""
    init_session_state()
    render_header()
    
    # Sidebar pour navigation
    with st.sidebar:
        st.image("https://via.placeholder.com/150x150.png?text=Logo", width=150)
        
        # Toggle thème
        col1, col2 = st.columns([2, 1])
        with col1:
            st.title("Navigation")
        with col2:
            # Initialiser le thème
            if 'theme' not in st.session_state:
                st.session_state['theme'] = 'dark'
            
            # Bouton toggle
            if st.button("🌓", help="Changer le thème", key="theme_toggle"):
                st.session_state['theme'] = 'light' if st.session_state['theme'] == 'dark' else 'dark'
                st.rerun()
        
        mode = st.radio(
            "Mode d'analyse",
            ["⚡ Analyse Rapide (CoinGecko)", "🔧 Analyse Manuelle", "⚖️ Comparaison", "📚 Méthodologie"],
            index=0
        )
        
        st.divider()
        
        st.markdown("### 📖 À propos")
        st.markdown("""
        **Tokenomics Analyzer** vous aide à évaluer la viabilité économique des projets crypto.
        
        Développé par Guillaume Verbiguié.
        """)
        
        st.divider()
        
        # Historique des analyses
        if 'history' in st.session_state and st.session_state['history']:
            st.divider()
            st.markdown("### 📝 Historique")
            with st.expander("Dernières analyses", expanded=False):
                for i, entry in enumerate(reversed(st.session_state['history'][-5:])):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**{entry['name']}** ({entry['symbol']})")
                        st.caption(f"Score: {entry['score']:.1f}/100 • {entry['time']}")
                    with col2:
                        if st.button("🔄", key=f"reload_{i}", help="Recharger"):
                            st.session_state.analysis_params = entry['params']
                            st.rerun()
        
        st.divider()
        
        st.markdown("### 🔗 Liens")
        st.markdown("""
        - [GitHub](https://github.com/guillaumeverbiguie)
        - [Malt](https://www.malt.fr/profile/guillaumeverbiguie)
        - [LinkedIn](https://www.linkedin.com/in/guillaumeverbiguie)
        - [Portfolio](https://guillaumeverbiguie.com)
        """)
    
    # Affichage selon le mode
    if mode == "⚡ Analyse Rapide (CoinGecko)":
        render_quick_analysis()
    elif mode == "🔧 Analyse Manuelle":
        render_manual_analysis()
    elif mode == "⚖️ Comparaison":
        render_comparison_mode()
    else:
        render_methodology()
    
    # Footer
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: gray; padding: 20px;'>
        🪙 <b>Tokenomics Analyzer</b> v1.0 — Développé avec ❤️ par Guillaume Verbiguié<br>
        ⚠️ Cet outil est fourni à titre éducatif. Pas de conseil en investissement. DYOR.
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

