"""
Module d'intégration avec l'API CoinGecko pour récupérer les données de tokenomics.
"""

import requests
from typing import Dict, Any, Optional


def fetch_coingecko_data(coin_id: str) -> Optional[Dict[str, Any]]:
    """
    Récupère les données d'un token depuis l'API CoinGecko.
    
    Args:
        coin_id: Identifiant CoinGecko du token (ex: "ethereum", "bitcoin")
        
    Returns:
        Dictionnaire avec les données ou None si erreur
    """
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
    # Base de données simplifiée de tokens connus
    known_tokens = {
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
        }
    }
    
    if coin_id in known_tokens:
        params.update(known_tokens[coin_id])
        params['description'] += f" | Données enrichies pour {coin_id}"
    
    return params

