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
    
    # Paramètres par défaut (non disponibles via API CoinGecko)
    params = {
        'circulating_supply': circulating_supply,
        'total_supply': total_supply,
        'max_supply': max_supply,
        'inflation_rate': round(inflation_rate, 2),
        'emission_years_left': emission_years_left,
        
        # Paramètres non disponibles via API (valeurs par défaut)
        'team_allocation': 15.0,
        'vesting_years': 3,
        'top_10_concentration': 30.0,
        
        'utility_gas': False,
        'utility_staking': False,
        'utility_governance': False,
        'utility_collateral': False,
        'utility_discount': False,
        
        'gov_timelock': True,
        'gov_multisig': True,
        'gov_dao_active': True,
        
        'incentive_lock': False,
        'incentive_staking': False,
        'incentive_burn': False,
        'lock_duration_months': 0,
        'burn_rate': 0.0,
        
        # Métadonnées
        'name': data.get('name', ''),
        'symbol': data.get('symbol', '').upper(),
        'price_usd': market_data.get('current_price', {}).get('usd', 0),
        'market_cap_usd': market_data.get('market_cap', {}).get('usd', 0),
        'description': "Données importées depuis CoinGecko. Les paramètres qualitatifs (utilité, gouvernance) sont des valeurs par défaut à ajuster manuellement."
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
    }
    
    if coin_id in known_tokens:
        params.update(known_tokens[coin_id])
        params['description'] += f" | Données enrichies pour {coin_id}"
    
    return params

