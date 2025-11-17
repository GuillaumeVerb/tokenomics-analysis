"""
Scénarios préconfigurés pour l'analyse de tokenomics.

Deux catégories :
- Catégorie A : Scénarios structurels (7)
- Catégorie B : Scénarios inflationnistes paramétriques (8)
"""

from typing import Dict, Any, List, Tuple


def get_scenario_categories() -> Dict[str, List[str]]:
    """Retourne les catégories de scénarios."""
    return {
        "📊 Scénarios Structurels": [
            "Projet early-stage",
            "Token utilitaire fort (ETH-like)",
            "Modèle DeFi inflationniste (Curve-like)",
            "Modèle Pendle-like",
            "Restaking / Sécurité économique (EigenLayer-like)",
            "Gouvernance capturée",
            "Token mature (Bitcoin/Ethereum-like)"
        ],
        "📈 Scénarios Inflationnistes": [
            "Inflation stable 2% / an",
            "Inflation stable 5% / an",
            "Inflation stable 10% / an",
            "Inflation haute 20% / an",
            "Inflation décroissante",
            "Inflation avec halving",
            "Inflation seasonal farming",
            "Inflation négative / burn dynamique"
        ]
    }


def get_all_scenarios() -> List[str]:
    """Retourne la liste complète de tous les scénarios."""
    categories = get_scenario_categories()
    all_scenarios = []
    for scenarios in categories.values():
        all_scenarios.extend(scenarios)
    return all_scenarios


def get_inflation_projection(scenario_name: str, years: int = 5) -> List[float]:
    """
    Génère une projection d'inflation annuelle selon le scénario.
    
    Args:
        scenario_name: Nom du scénario
        years: Nombre d'années à projeter
        
    Returns:
        Liste des taux d'inflation annuels (en %)
    """
    if scenario_name == "Inflation stable 2% / an":
        return [2.0] * years
    
    elif scenario_name == "Inflation stable 5% / an":
        return [5.0] * years
    
    elif scenario_name == "Inflation stable 10% / an":
        return [10.0] * years
    
    elif scenario_name == "Inflation haute 20% / an":
        return [20.0] * years
    
    elif scenario_name == "Inflation décroissante":
        # 10% → 7% → 5% → 3% → 1%
        base_rates = [10.0, 7.0, 5.0, 3.0, 1.0]
        return base_rates[:years] + [1.0] * max(0, years - 5)
    
    elif scenario_name == "Inflation avec halving":
        # Halving tous les 2 ans : 20% → 10% → 5% → 2.5% → 1.25%
        rate = 20.0
        rates = []
        for i in range(years):
            if i > 0 and i % 2 == 0:
                rate = rate / 2
            rates.append(rate)
        return rates
    
    elif scenario_name == "Inflation seasonal farming":
        # Forte inflation années 1-3, puis réduction brutale
        rates = []
        for i in range(years):
            if i < 3:
                rates.append(25.0)
            else:
                rates.append(5.0)
        return rates
    
    elif scenario_name == "Inflation négative / burn dynamique":
        # Inflation négative (burn > emission)
        return [-2.0] * years
    
    # Par défaut pour les autres scénarios
    elif "early-stage" in scenario_name:
        return [15.0, 12.0, 10.0, 8.0, 6.0][:years]
    
    elif "ETH-like" in scenario_name or "mature" in scenario_name:
        return [0.5, 0.5, 0.5, 0.5, 0.5][:years]
    
    elif "Curve-like" in scenario_name:
        return [20.0, 18.0, 16.0, 14.0, 12.0][:years]
    
    elif "Pendle-like" in scenario_name:
        return [3.0, 2.5, 2.0, 1.5, 1.0][:years]
    
    elif "EigenLayer-like" in scenario_name:
        return [5.0, 4.0, 3.0, 2.0, 1.5][:years]
    
    elif "capturée" in scenario_name:
        return [8.0, 7.0, 6.0, 5.0, 4.0][:years]
    
    else:
        return [5.0] * years


def get_scenario_params(scenario_name: str) -> Dict[str, Any]:
    """
    Retourne les paramètres d'un scénario préconfigé.
    
    Returns:
        Dictionnaire contenant tous les paramètres du scénario
    """
    
    # ========== CATÉGORIE A : SCÉNARIOS STRUCTURELS ==========
    
    if scenario_name == "Projet early-stage":
        return {
            "circulating_supply": 100_000_000,
            "total_supply": 1_000_000_000,
            "max_supply": 1_000_000_000,
            "inflation_rate": 15.0,
            "emission_years_left": 5,
            "team_allocation": 20.0,
            "vesting_years": 3,
            "top_10_concentration": 45.0,
            "utility_gas": False,
            "utility_staking": True,
            "utility_governance": True,
            "utility_collateral": False,
            "utility_discount": False,
            "gov_timelock": False,
            "gov_multisig": True,
            "gov_dao_active": False,
            "incentive_lock": False,
            "incentive_staking": True,
            "incentive_burn": False,
            "lock_duration_months": 0,
            "burn_rate": 0.0,
            "description": "Projet en phase de lancement avec forte dilution à venir et gouvernance centralisée."
        }
    
    elif scenario_name == "Token utilitaire fort (ETH-like)":
        return {
            "circulating_supply": 120_000_000,
            "total_supply": 120_000_000,
            "max_supply": 0,  # Pas de max supply
            "inflation_rate": 0.5,
            "emission_years_left": 999,  # Infini
            "team_allocation": 0.0,
            "vesting_years": 0,
            "top_10_concentration": 25.0,
            "utility_gas": True,
            "utility_staking": True,
            "utility_governance": True,
            "utility_collateral": True,
            "utility_discount": False,
            "gov_timelock": True,
            "gov_multisig": True,
            "gov_dao_active": True,
            "incentive_lock": False,
            "incentive_staking": True,
            "incentive_burn": True,
            "lock_duration_months": 0,
            "burn_rate": 0.3,
            "description": "Token avec utilité fondamentale forte (gas fees) et mécanismes de burn. Modèle Ethereum post-EIP1559."
        }
    
    elif scenario_name == "Modèle DeFi inflationniste (Curve-like)":
        return {
            "circulating_supply": 400_000_000,
            "total_supply": 3_000_000_000,
            "max_supply": 3_000_000_000,
            "inflation_rate": 20.0,
            "emission_years_left": 8,
            "team_allocation": 15.0,
            "vesting_years": 4,
            "top_10_concentration": 35.0,
            "utility_gas": False,
            "utility_staking": True,
            "utility_governance": True,
            "utility_collateral": False,
            "utility_discount": True,
            "gov_timelock": True,
            "gov_multisig": True,
            "gov_dao_active": True,
            "incentive_lock": True,
            "incentive_staking": True,
            "incentive_burn": False,
            "lock_duration_months": 48,
            "burn_rate": 0.0,
            "description": "Forte inflation compensée par mécanismes de lock long terme. Rewards de farming élevées."
        }
    
    elif scenario_name == "Modèle Pendle-like":
        return {
            "circulating_supply": 150_000_000,
            "total_supply": 258_000_000,
            "max_supply": 258_000_000,
            "inflation_rate": 3.0,
            "emission_years_left": 3,
            "team_allocation": 12.0,
            "vesting_years": 2,
            "top_10_concentration": 28.0,
            "utility_gas": False,
            "utility_staking": True,
            "utility_governance": True,
            "utility_collateral": False,
            "utility_discount": True,
            "gov_timelock": True,
            "gov_multisig": True,
            "gov_dao_active": True,
            "incentive_lock": True,
            "incentive_staking": True,
            "incentive_burn": True,
            "lock_duration_months": 24,
            "burn_rate": 0.5,
            "description": "Inflation faible, fees > emissions, mécanismes de lock productifs. Tokenomics soutenable."
        }
    
    elif scenario_name == "Restaking / Sécurité économique (EigenLayer-like)":
        return {
            "circulating_supply": 200_000_000,
            "total_supply": 1_000_000_000,
            "max_supply": 1_000_000_000,
            "inflation_rate": 5.0,
            "emission_years_left": 4,
            "team_allocation": 18.0,
            "vesting_years": 4,
            "top_10_concentration": 30.0,
            "utility_gas": False,
            "utility_staking": True,
            "utility_governance": True,
            "utility_collateral": True,
            "utility_discount": False,
            "gov_timelock": True,
            "gov_multisig": True,
            "gov_dao_active": True,
            "incentive_lock": True,
            "incentive_staking": True,
            "incentive_burn": False,
            "lock_duration_months": 12,
            "burn_rate": 0.0,
            "description": "Token utilisé comme collatéral pour sécurité économique. Risque de slashing réel, inflation contrôlée."
        }
    
    elif scenario_name == "Gouvernance capturée":
        return {
            "circulating_supply": 300_000_000,
            "total_supply": 1_000_000_000,
            "max_supply": 1_000_000_000,
            "inflation_rate": 8.0,
            "emission_years_left": 6,
            "team_allocation": 35.0,
            "vesting_years": 2,
            "top_10_concentration": 65.0,
            "utility_gas": False,
            "utility_staking": False,
            "utility_governance": True,
            "utility_collateral": False,
            "utility_discount": False,
            "gov_timelock": False,
            "gov_multisig": True,
            "gov_dao_active": False,
            "incentive_lock": False,
            "incentive_staking": False,
            "incentive_burn": False,
            "lock_duration_months": 0,
            "burn_rate": 0.0,
            "description": "Concentration excessive, gouvernance centralisée, pas de timelock. Red flags multiples."
        }
    
    elif scenario_name == "Token mature (Bitcoin/Ethereum-like)":
        return {
            "circulating_supply": 19_000_000,
            "total_supply": 19_500_000,
            "max_supply": 21_000_000,
            "inflation_rate": 0.5,
            "emission_years_left": 100,
            "team_allocation": 0.0,
            "vesting_years": 0,
            "top_10_concentration": 15.0,
            "utility_gas": True,
            "utility_staking": False,
            "utility_governance": False,
            "utility_collateral": True,
            "utility_discount": False,
            "gov_timelock": False,
            "gov_multisig": False,
            "gov_dao_active": False,
            "incentive_lock": False,
            "incentive_staking": False,
            "incentive_burn": False,
            "lock_duration_months": 0,
            "burn_rate": 0.0,
            "description": "Token entièrement mature avec quasi-totalité de la supply émise et utilité claire. Gouvernance décentralisée via consensus."
        }
    
    # ========== CATÉGORIE B : SCÉNARIOS INFLATIONNISTES ==========
    
    elif scenario_name == "Inflation stable 2% / an":
        return {
            "circulating_supply": 500_000_000,
            "total_supply": 1_000_000_000,
            "max_supply": 0,  # Pas de max
            "inflation_rate": 2.0,
            "emission_years_left": 999,
            "team_allocation": 15.0,
            "vesting_years": 3,
            "top_10_concentration": 30.0,
            "utility_gas": True,
            "utility_staking": True,
            "utility_governance": True,
            "utility_collateral": False,
            "utility_discount": False,
            "gov_timelock": True,
            "gov_multisig": True,
            "gov_dao_active": True,
            "incentive_lock": False,
            "incentive_staking": True,
            "incentive_burn": False,
            "lock_duration_months": 0,
            "burn_rate": 0.0,
            "description": "Inflation stable et modérée (2%/an), proche des monnaies 'soft inflation'. Soutenable long terme."
        }
    
    elif scenario_name == "Inflation stable 5% / an":
        return {
            "circulating_supply": 500_000_000,
            "total_supply": 1_000_000_000,
            "max_supply": 0,
            "inflation_rate": 5.0,
            "emission_years_left": 999,
            "team_allocation": 15.0,
            "vesting_years": 3,
            "top_10_concentration": 30.0,
            "utility_gas": True,
            "utility_staking": True,
            "utility_governance": True,
            "utility_collateral": False,
            "utility_discount": False,
            "gov_timelock": True,
            "gov_multisig": True,
            "gov_dao_active": True,
            "incentive_lock": False,
            "incentive_staking": True,
            "incentive_burn": False,
            "lock_duration_months": 0,
            "burn_rate": 0.0,
            "description": "Inflation modérée (5%/an). Soutenable si utilité forte et demande en croissance."
        }
    
    elif scenario_name == "Inflation stable 10% / an":
        return {
            "circulating_supply": 500_000_000,
            "total_supply": 1_000_000_000,
            "max_supply": 0,
            "inflation_rate": 10.0,
            "emission_years_left": 999,
            "team_allocation": 15.0,
            "vesting_years": 3,
            "top_10_concentration": 30.0,
            "utility_gas": True,
            "utility_staking": True,
            "utility_governance": True,
            "utility_collateral": False,
            "utility_discount": True,
            "gov_timelock": True,
            "gov_multisig": True,
            "gov_dao_active": True,
            "incentive_lock": True,
            "incentive_staking": True,
            "incentive_burn": False,
            "lock_duration_months": 12,
            "burn_rate": 0.0,
            "description": "Inflation forte (10%/an) typique de DeFi. Nécessite des mécanismes forts pour absorber la pression."
        }
    
    elif scenario_name == "Inflation haute 20% / an":
        return {
            "circulating_supply": 500_000_000,
            "total_supply": 1_000_000_000,
            "max_supply": 0,
            "inflation_rate": 20.0,
            "emission_years_left": 999,
            "team_allocation": 15.0,
            "vesting_years": 3,
            "top_10_concentration": 30.0,
            "utility_gas": False,
            "utility_staking": True,
            "utility_governance": True,
            "utility_collateral": False,
            "utility_discount": True,
            "gov_timelock": True,
            "gov_multisig": True,
            "gov_dao_active": True,
            "incentive_lock": True,
            "incentive_staking": True,
            "incentive_burn": False,
            "lock_duration_months": 24,
            "burn_rate": 0.0,
            "description": "Inflation très haute (20%/an). Modèle 'farming' insoutenable long terme sans demande massive."
        }
    
    elif scenario_name == "Inflation décroissante":
        return {
            "circulating_supply": 500_000_000,
            "total_supply": 800_000_000,
            "max_supply": 1_000_000_000,
            "inflation_rate": 10.0,  # Taux initial
            "emission_years_left": 10,
            "team_allocation": 15.0,
            "vesting_years": 3,
            "top_10_concentration": 30.0,
            "utility_gas": True,
            "utility_staking": True,
            "utility_governance": True,
            "utility_collateral": False,
            "utility_discount": False,
            "gov_timelock": True,
            "gov_multisig": True,
            "gov_dao_active": True,
            "incentive_lock": False,
            "incentive_staking": True,
            "incentive_burn": True,
            "lock_duration_months": 0,
            "burn_rate": 0.2,
            "description": "Inflation décroissante (10% → 7% → 5% → 3% → 1%). Modèle Ethereum pré-EIP1559."
        }
    
    elif scenario_name == "Inflation avec halving":
        return {
            "circulating_supply": 500_000_000,
            "total_supply": 700_000_000,
            "max_supply": 1_000_000_000,
            "inflation_rate": 20.0,  # Taux initial
            "emission_years_left": 10,
            "team_allocation": 10.0,
            "vesting_years": 4,
            "top_10_concentration": 25.0,
            "utility_gas": False,
            "utility_staking": True,
            "utility_governance": True,
            "utility_collateral": True,
            "utility_discount": False,
            "gov_timelock": True,
            "gov_multisig": True,
            "gov_dao_active": True,
            "incentive_lock": False,
            "incentive_staking": True,
            "incentive_burn": False,
            "lock_duration_months": 0,
            "burn_rate": 0.0,
            "description": "Halving tous les 2 ans (20% → 10% → 5% → 2.5%). Modèle Bitcoin adapté."
        }
    
    elif scenario_name == "Inflation seasonal farming":
        return {
            "circulating_supply": 300_000_000,
            "total_supply": 500_000_000,
            "max_supply": 1_000_000_000,
            "inflation_rate": 25.0,  # Taux initial élevé
            "emission_years_left": 5,
            "team_allocation": 15.0,
            "vesting_years": 2,
            "top_10_concentration": 35.0,
            "utility_gas": False,
            "utility_staking": True,
            "utility_governance": True,
            "utility_collateral": False,
            "utility_discount": True,
            "gov_timelock": True,
            "gov_multisig": True,
            "gov_dao_active": True,
            "incentive_lock": True,
            "incentive_staking": True,
            "incentive_burn": False,
            "lock_duration_months": 24,
            "burn_rate": 0.0,
            "description": "Forte inflation pendant 3 ans (farming), puis réduction brutale. DeFi 2020 style."
        }
    
    elif scenario_name == "Inflation négative / burn dynamique":
        return {
            "circulating_supply": 500_000_000,
            "total_supply": 500_000_000,
            "max_supply": 500_000_000,
            "inflation_rate": -2.0,  # Négatif !
            "emission_years_left": 0,
            "team_allocation": 10.0,
            "vesting_years": 3,
            "top_10_concentration": 25.0,
            "utility_gas": True,
            "utility_staking": True,
            "utility_governance": True,
            "utility_collateral": False,
            "utility_discount": False,
            "gov_timelock": True,
            "gov_multisig": True,
            "gov_dao_active": True,
            "incentive_lock": False,
            "incentive_staking": True,
            "incentive_burn": True,
            "lock_duration_months": 0,
            "burn_rate": 2.5,
            "description": "Burn > emissions = inflation négative. Supply diminue avec l'activité. EIP-1559 like."
        }
    
    else:
        # Scénario par défaut
        return {
            "circulating_supply": 500_000_000,
            "total_supply": 1_000_000_000,
            "max_supply": 1_000_000_000,
            "inflation_rate": 5.0,
            "emission_years_left": 5,
            "team_allocation": 15.0,
            "vesting_years": 3,
            "top_10_concentration": 30.0,
            "utility_gas": False,
            "utility_staking": True,
            "utility_governance": True,
            "utility_collateral": False,
            "utility_discount": False,
            "gov_timelock": True,
            "gov_multisig": True,
            "gov_dao_active": True,
            "incentive_lock": False,
            "incentive_staking": True,
            "incentive_burn": False,
            "lock_duration_months": 0,
            "burn_rate": 0.0,
            "description": "Scénario par défaut"
        }

