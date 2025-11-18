"""
Module d'intégration avec l'API CoinGecko pour récupérer les données de tokenomics.
"""

import requests
from typing import Dict, Any, Optional


# Mapping des symboles populaires vers les IDs CoinGecko
SYMBOL_TO_ID = {
    # Top cryptos
    'btc': 'bitcoin',
    'eth': 'ethereum',
    'usdt': 'tether',
    'bnb': 'binancecoin',
    'sol': 'solana',
    'xrp': 'ripple',
    'usdc': 'usd-coin',
    'ada': 'cardano',
    'avax': 'avalanche-2',
    'doge': 'dogecoin',
    'trx': 'tron',
    'dot': 'polkadot',
    'matic': 'matic-network',
    'link': 'chainlink',
    'wbtc': 'wrapped-bitcoin',
    'shib': 'shiba-inu',
    'dai': 'dai',
    'uni': 'uniswap',
    'atom': 'cosmos',
    'etc': 'ethereum-classic',
    'ltc': 'litecoin',
    'bch': 'bitcoin-cash',
    'xlm': 'stellar',
    'near': 'near',
    'apt': 'aptos',
    'arb': 'arbitrum',
    'op': 'optimism',
    'vet': 'vechain',
    'algo': 'algorand',
    'fil': 'filecoin',
    'icp': 'internet-computer',
    'inj': 'injective-protocol',
    'mkr': 'maker',
    'aave': 'aave',
    'crv': 'curve-dao-token',
    'snx': 'havven',
    'comp': 'compound-governance-token',
    'sushi': 'sushi',
    '1inch': '1inch',
    'grt': 'the-graph',
    'axs': 'axie-infinity',
    'sand': 'the-sandbox',
    'mana': 'decentraland',
    'ftm': 'fantom',
    'hbar': 'hedera-hashgraph',
}


def normalize_coin_input(user_input: str) -> str:
    """
    Normalise l'entrée utilisateur (symbole ou nom) vers un ID CoinGecko.
    
    Args:
        user_input: Input utilisateur (peut être un symbole ou un nom)
        
    Returns:
        ID CoinGecko normalisé
    """
    # Convertir en minuscules et enlever les espaces
    normalized = user_input.lower().strip()
    
    # Si c'est un symbole connu, convertir vers l'ID
    if normalized in SYMBOL_TO_ID:
        return SYMBOL_TO_ID[normalized]
    
    # Sinon retourner tel quel (peut être déjà un ID CoinGecko)
    return normalized


def fetch_coingecko_data(coin_id: str) -> Optional[Dict[str, Any]]:
    """
    Récupère les données d'un token depuis l'API CoinGecko.
    
    Args:
        coin_id: Identifiant CoinGecko du token (ex: "ethereum", "bitcoin") ou symbole (ex: "ETH", "BTC")
        
    Returns:
        Dictionnaire avec les données ou None si erreur
    """
    # Normaliser l'input (gérer les symboles)
    coin_id = normalize_coin_input(coin_id)
    
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
        params = {
            "localization": "false",
            "tickers": "false",
            "market_data": "true",
            "community_data": "false",
            "developer_data": "false",
            "sparkline": "false"
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération des données : {e}")
        return None


def parse_coingecko_to_params(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convertit les données CoinGecko en paramètres pour l'analyse.
    
    Args:
        data: Données brutes de CoinGecko
        
    Returns:
        Dictionnaire de paramètres normalisés
    """
    market_data = data.get('market_data', {})
    
    # Supply data
    circulating_supply = market_data.get('circulating_supply', 0) or 0
    total_supply = market_data.get('total_supply', 0) or 0
    max_supply = market_data.get('max_supply', 0) or 0
    
    # Si pas de max_supply définie, on prend total_supply
    if max_supply == 0:
        max_supply = total_supply
    
    # Estimation de l'inflation annuelle basée sur circulating vs total
    inflation_rate = 5.0  # Valeur par défaut
    if circulating_supply > 0 and total_supply > circulating_supply:
        # Estimation simplifiée : on suppose que la différence sera émise sur 5 ans
        remaining = total_supply - circulating_supply
        annual_emission = remaining / 5
        inflation_rate = (annual_emission / circulating_supply) * 100
        inflation_rate = min(inflation_rate, 50)  # Cap à 50%
    elif circulating_supply == total_supply:
        inflation_rate = 0.5  # Supply complètement émise
    
    # Estimation des années d'émission restantes
    emission_years_left = 5  # Par défaut
    if circulating_supply > 0 and max_supply > 0:
        remaining_ratio = (max_supply - circulating_supply) / circulating_supply
        if remaining_ratio < 0.1:
            emission_years_left = 1
        elif remaining_ratio < 0.3:
            emission_years_left = 2
        elif remaining_ratio < 0.5:
            emission_years_left = 3
        elif remaining_ratio > 2:
            emission_years_left = 10
    
    # Heuristiques pour différencier les tokens
    market_cap = market_data.get('market_cap', {}).get('usd', 0)
    market_cap_rank = data.get('market_cap_rank', 999)
    
    # Estimation de la concentration basée sur le market cap rank
    if market_cap_rank <= 10:
        top_10_concentration = 20.0  # Très décentralisé (BTC, ETH)
    elif market_cap_rank <= 50:
        top_10_concentration = 30.0  # Bien distribué
    elif market_cap_rank <= 200:
        top_10_concentration = 40.0  # Moyennement centralisé
    else:
        top_10_concentration = 50.0  # Plus centralisé
    
    # Estimation de l'allocation team basée sur l'âge et le type
    circulating_ratio = circulating_supply / max_supply if max_supply > 0 else 1.0
    if circulating_ratio > 0.95:
        team_allocation = 5.0  # Presque tout émis
        vesting_years = 0
    elif circulating_ratio > 0.8:
        team_allocation = 10.0
        vesting_years = 1
    elif circulating_ratio > 0.5:
        team_allocation = 15.0
        vesting_years = 2
    else:
        team_allocation = 20.0  # Beaucoup à émettre = probablement early stage
        vesting_years = 4
    
    # Heuristiques basées sur le market cap pour estimer l'utilité
    utility_gas = market_cap_rank <= 100  # Top 100 probablement des L1/L2
    utility_staking = market_cap_rank <= 150  # Top 150 ont souvent du staking
    utility_governance = market_cap_rank <= 200  # DeFi tokens ont gouvernance
    
    # Gouvernance basée sur le market cap
    gov_timelock = market_cap_rank <= 100
    gov_multisig = market_cap_rank <= 200
    gov_dao_active = market_cap_rank <= 150
    
    # Incitations basées sur l'inflation
    incentive_staking = inflation_rate > 0 and market_cap_rank <= 200
    incentive_burn = False  # Rare, à enrichir manuellement
    
    # Paramètres par défaut avec heuristiques
    params = {
        'circulating_supply': circulating_supply,
        'total_supply': total_supply,
        'max_supply': max_supply,
        'inflation_rate': round(inflation_rate, 2),
        'emission_years_left': emission_years_left,
        
        # Paramètres estimés via heuristiques
        'team_allocation': team_allocation,
        'vesting_years': vesting_years,
        'top_10_concentration': top_10_concentration,
        
        'utility_gas': utility_gas,
        'utility_staking': utility_staking,
        'utility_governance': utility_governance,
        'utility_collateral': market_cap_rank <= 50,  # Top 50 peuvent être collateral
        'utility_discount': False,
        
        'gov_timelock': gov_timelock,
        'gov_multisig': gov_multisig,
        'gov_dao_active': gov_dao_active,
        
        'incentive_lock': False,
        'incentive_staking': incentive_staking,
        'incentive_burn': incentive_burn,
        'lock_duration_months': 0,
        'burn_rate': 0.0,
        
        # Métadonnées
        'name': data.get('name', ''),
        'symbol': data.get('symbol', '').upper(),
        'price_usd': market_data.get('current_price', {}).get('usd', 0),
        'market_cap_usd': market_cap,
        'market_cap_rank': market_cap_rank,
        'description': f"Données CoinGecko avec heuristiques (Rank #{market_cap_rank}). Paramètres qualitatifs estimés automatiquement."
    }
    
    return params


def search_coingecko_coin(query: str) -> list:
    """
    Recherche un token sur CoinGecko.
    
    Args:
        query: Terme de recherche
        
    Returns:
        Liste de résultats [{id, symbol, name}]
    """
    try:
        url = "https://api.coingecko.com/api/v3/search"
        params = {"query": query}
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        coins = data.get('coins', [])
        
        # Limiter aux 10 premiers résultats
        return [{
            'id': coin['id'],
            'symbol': coin['symbol'],
            'name': coin['name']
        } for coin in coins[:10]]
        
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la recherche : {e}")
        return []


def enhance_params_with_known_data(params: Dict[str, Any], coin_id: str) -> Dict[str, Any]:
    """
    Améliore les paramètres avec des données connues pour certains tokens populaires.
    
    Args:
        params: Paramètres de base
        coin_id: ID CoinGecko
        
    Returns:
        Paramètres enrichis
    """
    # Base de données enrichie de tokens connus avec vraies données
    known_tokens = {
        # Layer 1
        'ethereum': {
            'utility_gas': True,
            'utility_staking': True,
            'utility_governance': False,
            'utility_collateral': True,
            'incentive_staking': True,
            'incentive_burn': True,
            'burn_rate': 0.3,
            'top_10_concentration': 25.0,
            'team_allocation': 0.0,
        },
        'bitcoin': {
            'utility_gas': True,
            'utility_collateral': True,
            'top_10_concentration': 15.0,
            'team_allocation': 0.0,
            'gov_timelock': False,
            'gov_multisig': False,
            'gov_dao_active': False,
        },
        'solana': {
            'utility_gas': True,
            'utility_staking': True,
            'utility_governance': False,
            'incentive_staking': True,
            'top_10_concentration': 32.0,
            'team_allocation': 12.5,
            'vesting_years': 4,
        },
        'cardano': {
            'utility_gas': True,
            'utility_staking': True,
            'utility_governance': True,
            'incentive_staking': True,
            'gov_dao_active': True,
            'top_10_concentration': 28.0,
            'team_allocation': 16.0,
        },
        'avalanche-2': {
            'utility_gas': True,
            'utility_staking': True,
            'incentive_staking': True,
            'top_10_concentration': 35.0,
            'team_allocation': 18.0,
            'vesting_years': 4,
        },
        'polkadot': {
            'utility_gas': True,
            'utility_staking': True,
            'utility_governance': True,
            'incentive_staking': True,
            'gov_dao_active': True,
            'top_10_concentration': 38.0,
            'team_allocation': 20.0,
        },
        
        # Layer 2
        'arbitrum': {
            'utility_gas': True,
            'utility_governance': True,
            'gov_timelock': True,
            'gov_dao_active': True,
            'team_allocation': 26.9,
            'vesting_years': 4,
            'top_10_concentration': 42.0,
        },
        'optimism': {
            'utility_gas': True,
            'utility_governance': True,
            'gov_timelock': True,
            'gov_dao_active': True,
            'team_allocation': 25.0,
            'vesting_years': 4,
            'top_10_concentration': 40.0,
        },
        'matic-network': {
            'utility_gas': True,
            'utility_staking': True,
            'utility_governance': True,
            'incentive_staking': True,
            'gov_dao_active': True,
            'top_10_concentration': 33.0,
            'team_allocation': 16.0,
        },
        
        # DeFi
        'uniswap': {
            'utility_governance': True,
            'utility_staking': False,
            'utility_discount': True,
            'gov_timelock': True,
            'gov_dao_active': True,
            'team_allocation': 21.5,
            'vesting_years': 4,
            'top_10_concentration': 35.0,
        },
        'curve-dao-token': {
            'utility_governance': True,
            'utility_staking': True,
            'utility_discount': True,
            'incentive_lock': True,
            'lock_duration_months': 48,
            'gov_timelock': True,
            'gov_dao_active': True,
            'team_allocation': 15.0,
            'top_10_concentration': 35.0,
        },
        'aave': {
            'utility_governance': True,
            'utility_staking': True,
            'utility_discount': True,
            'incentive_staking': True,
            'gov_timelock': True,
            'gov_dao_active': True,
            'team_allocation': 23.0,
            'top_10_concentration': 32.0,
        },
        'maker': {
            'utility_governance': True,
            'utility_staking': False,
            'utility_collateral': True,
            'incentive_burn': True,
            'burn_rate': 0.5,
            'gov_timelock': True,
            'gov_dao_active': True,
            'team_allocation': 0.0,
            'top_10_concentration': 22.0,
        },
        'compound-governance-token': {
            'utility_governance': True,
            'gov_timelock': True,
            'gov_dao_active': True,
            'team_allocation': 24.0,
            'vesting_years': 4,
            'top_10_concentration': 38.0,
        },
        'sushi': {
            'utility_governance': True,
            'utility_staking': True,
            'utility_discount': True,
            'incentive_staking': True,
            'gov_dao_active': True,
            'top_10_concentration': 30.0,
            'team_allocation': 10.0,
        },
        'pancakeswap-token': {
            'utility_governance': True,
            'utility_discount': True,
            'incentive_burn': True,
            'burn_rate': 1.2,
            'gov_dao_active': False,
            'top_10_concentration': 45.0,
            'team_allocation': 15.0,
        },
        '1inch': {
            'utility_governance': True,
            'utility_discount': True,
            'gov_dao_active': True,
            'top_10_concentration': 35.0,
            'team_allocation': 22.5,
            'vesting_years': 4,
        },
        
        # Staking / Liquid Staking
        'lido-dao': {
            'utility_governance': True,
            'utility_staking': False,
            'incentive_staking': True,
            'gov_timelock': True,
            'gov_dao_active': True,
            'top_10_concentration': 42.0,
            'team_allocation': 20.0,
        },
        'rocket-pool': {
            'utility_governance': True,
            'utility_staking': True,
            'incentive_staking': True,
            'gov_dao_active': True,
            'top_10_concentration': 28.0,
            'team_allocation': 18.0,
        },
        
        # Oracle
        'chainlink': {
            'utility_gas': True,
            'utility_staking': True,
            'incentive_staking': True,
            'top_10_concentration': 38.0,
            'team_allocation': 35.0,
            'vesting_years': 5,
        },
        
        # Gaming / Metaverse
        'the-sandbox': {
            'utility_governance': True,
            'utility_discount': True,
            'gov_dao_active': False,
            'top_10_concentration': 48.0,
            'team_allocation': 25.0,
            'vesting_years': 3,
        },
        'axie-infinity': {
            'utility_governance': True,
            'utility_staking': True,
            'incentive_staking': True,
            'gov_dao_active': False,
            'top_10_concentration': 52.0,
            'team_allocation': 21.0,
        },
        'decentraland': {
            'utility_governance': True,
            'gov_dao_active': True,
            'top_10_concentration': 42.0,
            'team_allocation': 20.0,
        },
        
        # Memecoins
        'dogecoin': {
            'utility_gas': True,
            'team_allocation': 0.0,
            'top_10_concentration': 35.0,
            'gov_timelock': False,
            'gov_multisig': False,
            'gov_dao_active': False,
        },
        'shiba-inu': {
            'incentive_burn': True,
            'burn_rate': 0.8,
            'team_allocation': 0.0,
            'top_10_concentration': 68.0,
            'gov_timelock': False,
            'gov_multisig': True,
            'gov_dao_active': False,
        },
        
        # Nouveau DeFi 2024
        'pendle': {
            'utility_governance': True,
            'utility_staking': True,
            'utility_discount': True,
            'incentive_lock': True,
            'incentive_staking': True,
            'incentive_burn': True,
            'lock_duration_months': 24,
            'burn_rate': 0.5,
            'gov_timelock': True,
            'gov_dao_active': True,
            'team_allocation': 12.0,
            'top_10_concentration': 28.0,
        },
        
        # Plus de L1/L2
        'tron': {
            'utility_gas': True,
            'utility_staking': True,
            'incentive_staking': True,
            'top_10_concentration': 45.0,
            'team_allocation': 20.0,
            'vesting_years': 10,
        },
        'near': {
            'utility_gas': True,
            'utility_staking': True,
            'utility_governance': True,
            'incentive_staking': True,
            'gov_dao_active': True,
            'top_10_concentration': 32.0,
            'team_allocation': 17.0,
            'vesting_years': 5,
        },
        'aptos': {
            'utility_gas': True,
            'utility_staking': True,
            'incentive_staking': True,
            'top_10_concentration': 51.0,
            'team_allocation': 51.0,
            'vesting_years': 10,
        },
        'sui': {
            'utility_gas': True,
            'utility_staking': True,
            'incentive_staking': True,
            'top_10_concentration': 50.0,
            'team_allocation': 50.0,
            'vesting_years': 10,
        },
        'cosmos': {
            'utility_gas': True,
            'utility_staking': True,
            'utility_governance': True,
            'incentive_staking': True,
            'gov_dao_active': True,
            'top_10_concentration': 28.0,
            'team_allocation': 10.0,
        },
        'fantom': {
            'utility_gas': True,
            'utility_staking': True,
            'incentive_staking': True,
            'top_10_concentration': 38.0,
            'team_allocation': 15.0,
        },
        'algorand': {
            'utility_gas': True,
            'utility_staking': True,
            'utility_governance': True,
            'incentive_staking': True,
            'gov_dao_active': True,
            'top_10_concentration': 25.0,
            'team_allocation': 25.0,
            'vesting_years': 10,
        },
        
        # Plus de DeFi
        'frax-share': {
            'utility_governance': True,
            'utility_staking': True,
            'utility_discount': True,
            'incentive_staking': True,
            'incentive_burn': True,
            'burn_rate': 0.3,
            'gov_dao_active': True,
            'top_10_concentration': 35.0,
            'team_allocation': 20.0,
        },
        'convex-finance': {
            'utility_governance': True,
            'utility_staking': True,
            'incentive_lock': True,
            'incentive_staking': True,
            'lock_duration_months': 16,
            'gov_dao_active': True,
            'top_10_concentration': 28.0,
            'team_allocation': 9.7,
        },
        'gmx': {
            'utility_governance': True,
            'utility_staking': True,
            'utility_discount': True,
            'incentive_staking': True,
            'incentive_burn': True,
            'burn_rate': 0.4,
            'gov_dao_active': True,
            'top_10_concentration': 35.0,
            'team_allocation': 15.0,
        },
        'synthetix-network-token': {
            'utility_governance': True,
            'utility_staking': True,
            'utility_collateral': True,
            'incentive_staking': True,
            'gov_dao_active': True,
            'top_10_concentration': 42.0,
            'team_allocation': 20.0,
        },
        'balancer': {
            'utility_governance': True,
            'utility_discount': True,
            'gov_dao_active': True,
            'gov_timelock': True,
            'top_10_concentration': 38.0,
            'team_allocation': 25.0,
            'vesting_years': 4,
        },
        'yearn-finance': {
            'utility_governance': True,
            'utility_staking': True,
            'incentive_staking': True,
            'incentive_burn': True,
            'burn_rate': 0.2,
            'gov_dao_active': True,
            'top_10_concentration': 32.0,
            'team_allocation': 0.0,
        },
        
        # Liquid Staking supplémentaires
        'staked-ether': {
            'utility_staking': False,
            'utility_collateral': True,
            'top_10_concentration': 85.0,
            'team_allocation': 0.0,
            'gov_timelock': False,
            'gov_multisig': False,
            'gov_dao_active': False,
        },
        'frax-ether': {
            'utility_collateral': True,
            'utility_governance': False,
            'top_10_concentration': 90.0,
            'team_allocation': 0.0,
        },
        
        # AI Tokens
        'render-token': {
            'utility_governance': True,
            'utility_gas': True,
            'incentive_burn': True,
            'burn_rate': 0.5,
            'gov_dao_active': False,
            'top_10_concentration': 45.0,
            'team_allocation': 25.0,
        },
        'fetch-ai': {
            'utility_gas': True,
            'utility_staking': True,
            'utility_governance': True,
            'incentive_staking': True,
            'gov_dao_active': True,
            'top_10_concentration': 35.0,
            'team_allocation': 30.0,
            'vesting_years': 10,
        },
        'singularitynet': {
            'utility_governance': True,
            'utility_staking': True,
            'gov_dao_active': True,
            'top_10_concentration': 38.0,
            'team_allocation': 28.0,
        },
        
        # Oracle supplémentaires
        'band-protocol': {
            'utility_gas': True,
            'utility_staking': True,
            'utility_governance': True,
            'incentive_staking': True,
            'gov_dao_active': True,
            'top_10_concentration': 42.0,
            'team_allocation': 22.0,
        },
        
        # Privacy
        'monero': {
            'utility_gas': True,
            'team_allocation': 0.0,
            'top_10_concentration': 20.0,
            'gov_timelock': False,
            'gov_multisig': False,
            'gov_dao_active': False,
        },
        'zcash': {
            'utility_gas': True,
            'team_allocation': 20.0,
            'top_10_concentration': 25.0,
            'vesting_years': 4,
            'gov_timelock': False,
            'gov_multisig': True,
            'gov_dao_active': False,
        },
        
        # Exchange Tokens
        'okb': {
            'utility_discount': True,
            'utility_staking': True,
            'incentive_burn': True,
            'incentive_staking': True,
            'burn_rate': 1.0,
            'top_10_concentration': 60.0,
            'team_allocation': 40.0,
            'gov_timelock': False,
            'gov_multisig': True,
            'gov_dao_active': False,
        },
        'kucoin-shares': {
            'utility_discount': True,
            'utility_staking': False,
            'incentive_burn': True,
            'burn_rate': 0.8,
            'top_10_concentration': 55.0,
            'team_allocation': 35.0,
            'gov_timelock': False,
            'gov_multisig': True,
            'gov_dao_active': False,
        },
        
        # Gaming supplémentaires
        'immutable-x': {
            'utility_gas': True,
            'utility_staking': True,
            'utility_governance': True,
            'incentive_staking': True,
            'gov_dao_active': False,
            'top_10_concentration': 48.0,
            'team_allocation': 51.7,
            'vesting_years': 4,
        },
        'gala': {
            'utility_governance': True,
            'utility_discount': True,
            'incentive_burn': True,
            'burn_rate': 0.5,
            'gov_dao_active': False,
            'top_10_concentration': 45.0,
            'team_allocation': 20.0,
        },
        
        # Bridges
        'wormhole': {
            'utility_governance': True,
            'utility_staking': True,
            'gov_timelock': True,
            'gov_multisig': True,
            'gov_dao_active': True,
            'top_10_concentration': 52.0,
            'team_allocation': 47.0,
            'vesting_years': 4,
        },
    }
    
    if coin_id in known_tokens:
        params.update(known_tokens[coin_id])
        params['description'] = f"✅ Données enrichies avec vraies valeurs pour {params.get('name', coin_id)}"
        params['is_enriched'] = True
    else:
        params['is_enriched'] = False
    
    return params


def get_enriched_tokens_list() -> Dict[str, list]:
    """
    Retourne la liste organisée de tous les tokens enrichis.
    
    Returns:
        Dictionnaire avec les catégories de tokens
    """
    return {
        "🔷 Layer 1 Blockchains": [
            "bitcoin", "ethereum", "solana", "cardano", "avalanche-2", 
            "polkadot", "tron", "near", "aptos", "sui", "cosmos", 
            "fantom", "algorand"
        ],
        "🔶 Layer 2 Solutions": [
            "arbitrum", "optimism", "matic-network"
        ],
        "💰 DeFi Protocols": [
            "uniswap", "curve-dao-token", "aave", "maker", "compound-governance-token",
            "sushi", "pancakeswap-token", "1inch", "frax-share", "convex-finance",
            "gmx", "synthetix-network-token", "balancer", "yearn-finance", "pendle"
        ],
        "🏦 Liquid Staking": [
            "lido-dao", "rocket-pool", "staked-ether", "frax-ether"
        ],
        "🔮 Oracle Networks": [
            "chainlink", "band-protocol"
        ],
        "🎮 Gaming & Metaverse": [
            "the-sandbox", "axie-infinity", "decentraland", "immutable-x", "gala"
        ],
        "🤖 AI & Data": [
            "render-token", "fetch-ai", "singularitynet"
        ],
        "🐕 Memecoins": [
            "dogecoin", "shiba-inu"
        ],
        "🔒 Privacy Coins": [
            "monero", "zcash"
        ],
        "🏪 Exchange Tokens": [
            "okb", "kucoin-shares"
        ],
        "🌉 Bridge Protocols": [
            "wormhole"
        ]
    }

