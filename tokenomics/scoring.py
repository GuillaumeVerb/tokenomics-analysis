"""
Module de calcul du Tokenomics Viability Index.

Le score final (0-100) est calculé selon 8 composantes :
1. Inflation (20%)
2. Distribution (15%)
3. Utilité (20%)
4. Gouvernance (10%)
5. Incitations (10%)
6. Liquidité (15%)
7. Adoption (10%)
8. Sécurité (5% bonus)
"""

from typing import Dict, Any, Tuple


def calculate_inflation_score(
    circulating_supply: float,
    total_supply: float,
    max_supply: float,
    inflation_rate: float,
    emission_years_left: int
) -> Tuple[float, str]:
    """
    Calcule le score d'inflation (0-100).
    
    Args:
        circulating_supply: Supply en circulation
        total_supply: Supply totale actuelle
        max_supply: Supply maximale (0 = illimité)
        inflation_rate: Taux d'inflation annuel (%)
        emission_years_left: Années d'émission restantes
        
    Returns:
        (score, commentaire)
    """
    score = 100.0
    comments = []
    
    # 1. Dilution potentielle (jusqu'à -40 points)
    if max_supply > 0 and circulating_supply > 0:
        dilution_potential = ((max_supply - circulating_supply) / circulating_supply) * 100
        if dilution_potential > 300:
            score -= 40
            comments.append(f"⚠️ Dilution potentielle massive : {dilution_potential:.1f}%")
        elif dilution_potential > 150:
            score -= 30
            comments.append(f"⚠️ Dilution potentielle élevée : {dilution_potential:.1f}%")
        elif dilution_potential > 50:
            score -= 15
            comments.append(f"⚠️ Dilution potentielle modérée : {dilution_potential:.1f}%")
        elif dilution_potential > 20:
            score -= 5
            comments.append(f"Dilution potentielle faible : {dilution_potential:.1f}%")
        else:
            comments.append(f"✅ Supply presque entièrement émise ({dilution_potential:.1f}% restant)")
    
    # 2. Taux d'inflation annuel (jusqu'à -35 points)
    if inflation_rate < 0:
        score += 10
        comments.append(f"✅ Inflation négative (burn) : {inflation_rate:.1f}%")
    elif inflation_rate <= 2:
        comments.append(f"✅ Inflation très faible : {inflation_rate:.1f}%")
    elif inflation_rate <= 5:
        score -= 5
        comments.append(f"Inflation modérée : {inflation_rate:.1f}%")
    elif inflation_rate <= 10:
        score -= 15
        comments.append(f"⚠️ Inflation élevée : {inflation_rate:.1f}%")
    elif inflation_rate <= 20:
        score -= 25
        comments.append(f"⚠️ Inflation très élevée : {inflation_rate:.1f}%")
    else:
        score -= 35
        comments.append(f"🚨 Inflation excessive : {inflation_rate:.1f}%")
    
    # 3. Durée d'émission (jusqu'à -15 points)
    if emission_years_left > 10:
        score -= 15
        comments.append(f"⚠️ Émissions longues ({emission_years_left} ans)")
    elif emission_years_left > 5:
        score -= 8
        comments.append(f"Émissions moyennes ({emission_years_left} ans)")
    elif emission_years_left > 0:
        score -= 3
        comments.append(f"Émissions courtes ({emission_years_left} ans)")
    else:
        comments.append("✅ Plus d'émissions prévues")
    
    # 4. Supply actuelle vs totale (jusqu'à -10 points)
    if total_supply > 0 and circulating_supply > 0:
        supply_ratio = (circulating_supply / total_supply) * 100
        if supply_ratio < 20:
            score -= 10
            comments.append(f"⚠️ Très peu de supply en circulation : {supply_ratio:.1f}%")
        elif supply_ratio < 40:
            score -= 5
            comments.append(f"Peu de supply en circulation : {supply_ratio:.1f}%")
        elif supply_ratio > 90:
            comments.append(f"✅ Supply majoritairement en circulation : {supply_ratio:.1f}%")
    
    score = max(0, min(100, score))
    comment = " | ".join(comments)
    
    return score, comment


def calculate_distribution_score(
    team_allocation: float,
    vesting_years: int,
    top_10_concentration: float
) -> Tuple[float, str]:
    """
    Calcule le score de distribution (0-100).
    
    Args:
        team_allocation: Allocation team/insiders (%)
        vesting_years: Durée du vesting (années)
        top_10_concentration: Concentration top 10 holders (%)
        
    Returns:
        (score, commentaire)
    """
    score = 100.0
    comments = []
    
    # 1. Allocation team (jusqu'à -30 points)
    if team_allocation > 30:
        score -= 30
        comments.append(f"🚨 Allocation team excessive : {team_allocation:.1f}%")
    elif team_allocation > 20:
        score -= 20
        comments.append(f"⚠️ Allocation team élevée : {team_allocation:.1f}%")
    elif team_allocation > 15:
        score -= 10
        comments.append(f"Allocation team modérée : {team_allocation:.1f}%")
    elif team_allocation > 10:
        score -= 5
        comments.append(f"Allocation team acceptable : {team_allocation:.1f}%")
    else:
        comments.append(f"✅ Allocation team faible : {team_allocation:.1f}%")
    
    # 2. Vesting (jusqu'à -25 points)
    if team_allocation > 10:  # Vesting pertinent seulement si allocation significative
        if vesting_years < 2:
            score -= 25
            comments.append(f"🚨 Vesting trop court : {vesting_years} ans")
        elif vesting_years < 3:
            score -= 15
            comments.append(f"⚠️ Vesting court : {vesting_years} ans")
        elif vesting_years < 4:
            score -= 5
            comments.append(f"Vesting acceptable : {vesting_years} ans")
        else:
            comments.append(f"✅ Vesting solide : {vesting_years} ans")
    
    # 3. Concentration (jusqu'à -45 points)
    if top_10_concentration > 60:
        score -= 45
        comments.append(f"🚨 Concentration extrême : {top_10_concentration:.1f}%")
    elif top_10_concentration > 50:
        score -= 35
        comments.append(f"🚨 Concentration très élevée : {top_10_concentration:.1f}%")
    elif top_10_concentration > 40:
        score -= 25
        comments.append(f"⚠️ Concentration élevée : {top_10_concentration:.1f}%")
    elif top_10_concentration > 30:
        score -= 15
        comments.append(f"⚠️ Concentration modérée : {top_10_concentration:.1f}%")
    elif top_10_concentration > 20:
        score -= 5
        comments.append(f"Concentration acceptable : {top_10_concentration:.1f}%")
    else:
        comments.append(f"✅ Bonne décentralisation : {top_10_concentration:.1f}%")
    
    score = max(0, min(100, score))
    comment = " | ".join(comments)
    
    return score, comment


def calculate_utility_score(
    utility_gas: bool,
    utility_staking: bool,
    utility_governance: bool,
    utility_collateral: bool,
    utility_discount: bool
) -> Tuple[float, str]:
    """
    Calcule le score d'utilité (0-100).
    
    Args:
        utility_gas: Utilisé comme gas fees
        utility_staking: Utilisé pour le staking
        utility_governance: Utilisé pour la gouvernance
        utility_collateral: Utilisé comme collatéral
        utility_discount: Utilisé pour des discounts/rewards
        
    Returns:
        (score, commentaire)
    """
    score = 0.0
    utilities = []
    
    # Gas fees = utilité la plus forte (40 points)
    if utility_gas:
        score += 40
        utilities.append("Gas fees")
    
    # Staking (20 points)
    if utility_staking:
        score += 20
        utilities.append("Staking")
    
    # Gouvernance (15 points)
    if utility_governance:
        score += 15
        utilities.append("Gouvernance")
    
    # Collatéral (20 points)
    if utility_collateral:
        score += 20
        utilities.append("Collatéral")
    
    # Discount (5 points)
    if utility_discount:
        score += 5
        utilities.append("Discount/Rewards")
    
    if len(utilities) == 0:
        comment = "🚨 Aucune utilité claire"
    elif len(utilities) == 1:
        comment = f"⚠️ Utilité limitée : {utilities[0]}"
    elif len(utilities) == 2:
        comment = f"Utilités : {', '.join(utilities)}"
    else:
        comment = f"✅ Utilités multiples : {', '.join(utilities)}"
    
    score = max(0, min(100, score))
    
    return score, comment


def calculate_governance_score(
    gov_timelock: bool,
    gov_multisig: bool,
    gov_dao_active: bool,
    top_10_concentration: float
) -> Tuple[float, str]:
    """
    Calcule le score de gouvernance (0-100).
    
    Args:
        gov_timelock: Présence d'un timelock
        gov_multisig: Présence d'un multisig
        gov_dao_active: DAO active et fonctionnelle
        top_10_concentration: Concentration (influence le contrôle)
        
    Returns:
        (score, commentaire)
    """
    score = 100.0
    comments = []
    
    # 1. Timelock (crucial pour sécurité)
    if not gov_timelock:
        score -= 30
        comments.append("🚨 Pas de timelock")
    else:
        comments.append("✅ Timelock présent")
    
    # 2. Multisig
    if not gov_multisig:
        score -= 20
        comments.append("⚠️ Pas de multisig")
    else:
        comments.append("✅ Multisig présent")
    
    # 3. DAO active
    if not gov_dao_active:
        score -= 25
        comments.append("⚠️ DAO non active")
    else:
        comments.append("✅ DAO active")
    
    # 4. Impact de la concentration
    if top_10_concentration > 50:
        score -= 25
        comments.append("🚨 Risque de capture (concentration élevée)")
    elif top_10_concentration > 35:
        score -= 15
        comments.append("⚠️ Risque de capture (concentration modérée)")
    
    score = max(0, min(100, score))
    comment = " | ".join(comments)
    
    return score, comment


def calculate_incentives_score(
    incentive_lock: bool,
    incentive_staking: bool,
    incentive_burn: bool,
    lock_duration_months: int,
    burn_rate: float,
    inflation_rate: float
) -> Tuple[float, str]:
    """
    Calcule le score d'incitations (0-100).
    
    Args:
        incentive_lock: Mécanisme de lock/ve-token
        incentive_staking: Staking disponible
        incentive_burn: Mécanisme de burn
        lock_duration_months: Durée du lock (mois)
        burn_rate: Taux de burn (%)
        inflation_rate: Taux d'inflation (pour contexte)
        
    Returns:
        (score, commentaire)
    """
    score = 40.0  # Base
    comments = []
    
    # 1. Lock mechanism (jusqu'à +30 points)
    if incentive_lock:
        if lock_duration_months >= 24:
            score += 30
            comments.append(f"✅ Lock long terme : {lock_duration_months} mois")
        elif lock_duration_months >= 12:
            score += 20
            comments.append(f"✅ Lock moyen terme : {lock_duration_months} mois")
        elif lock_duration_months >= 6:
            score += 10
            comments.append(f"Lock court terme : {lock_duration_months} mois")
        else:
            score += 5
            comments.append(f"⚠️ Lock très court : {lock_duration_months} mois")
    else:
        comments.append("Pas de mécanisme de lock")
    
    # 2. Staking (jusqu'à +20 points)
    if incentive_staking:
        score += 20
        comments.append("✅ Staking disponible")
    else:
        comments.append("⚠️ Pas de staking")
    
    # 3. Burn mechanism (jusqu'à +25 points)
    if incentive_burn:
        if burn_rate > inflation_rate and inflation_rate > 0:
            score += 25
            comments.append(f"✅ Burn > inflation : {burn_rate:.1f}% burn vs {inflation_rate:.1f}% inflation")
        elif burn_rate >= 1.0:
            score += 20
            comments.append(f"✅ Burn significatif : {burn_rate:.1f}%")
        elif burn_rate >= 0.5:
            score += 15
            comments.append(f"✅ Burn modéré : {burn_rate:.1f}%")
        elif burn_rate > 0:
            score += 10
            comments.append(f"Burn faible : {burn_rate:.1f}%")
    else:
        comments.append("Pas de mécanisme de burn")
    
    # 4. Synergie (bonus si plusieurs mécanismes)
    active_mechanisms = sum([incentive_lock, incentive_staking, incentive_burn])
    if active_mechanisms == 3:
        score += 10
        comments.append("✅ Synergie complète (lock + staking + burn)")
    elif active_mechanisms == 0:
        score -= 20
        comments.append("🚨 Aucun mécanisme d'incitation")
    
    score = max(0, min(100, score))
    comment = " | ".join(comments)
    
    return score, comment


def calculate_viability_index(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calcule le Tokenomics Viability Index global.
    
    Args:
        params: Dictionnaire contenant tous les paramètres
        
    Returns:
        Dictionnaire avec scores détaillés et index final
    """
    # Calcul des scores par catégorie
    inflation_score, inflation_comment = calculate_inflation_score(
        params['circulating_supply'],
        params['total_supply'],
        params['max_supply'],
        params['inflation_rate'],
        params['emission_years_left']
    )
    
    distribution_score, distribution_comment = calculate_distribution_score(
        params['team_allocation'],
        params['vesting_years'],
        params['top_10_concentration']
    )
    
    utility_score, utility_comment = calculate_utility_score(
        params['utility_gas'],
        params['utility_staking'],
        params['utility_governance'],
        params['utility_collateral'],
        params['utility_discount']
    )
    
    governance_score, governance_comment = calculate_governance_score(
        params['gov_timelock'],
        params['gov_multisig'],
        params['gov_dao_active'],
        params['top_10_concentration']
    )
    
    incentives_score, incentives_comment = calculate_incentives_score(
        params['incentive_lock'],
        params['incentive_staking'],
        params['incentive_burn'],
        params['lock_duration_months'],
        params['burn_rate'],
        params['inflation_rate']
    )
    
    # Nouveaux critères
    liquidity_score, liquidity_comment = calculate_liquidity_score(
        params.get('volume_24h', 0),
        params.get('market_cap_usd', 0),
        params.get('volume_to_market_cap', 0),
        params.get('market_cap_rank', 999)
    )
    
    adoption_score, adoption_comment = calculate_adoption_score(
        params.get('market_cap_usd', 0),
        params.get('market_cap_rank', 999),
        params.get('price_change_30d', 0)
    )
    
    security_score, security_comment = calculate_security_score(
        params.get('name', '').lower().replace(' ', '-'),
        params.get('market_cap_rank', 999)
    )
    
    # Pondérations (total = 105% avec bonus sécurité)
    weights = {
        'inflation': 0.20,
        'distribution': 0.15,
        'utility': 0.20,
        'governance': 0.10,
        'incentives': 0.10,
        'liquidity': 0.15,
        'adoption': 0.10,
        'security': 0.05  # Bonus
    }
    
    # Calcul du score final (peut dépasser 100 avec bonus sécurité)
    final_score = (
        inflation_score * weights['inflation'] +
        distribution_score * weights['distribution'] +
        utility_score * weights['utility'] +
        governance_score * weights['governance'] +
        incentives_score * weights['incentives'] +
        liquidity_score * weights['liquidity'] +
        adoption_score * weights['adoption'] +
        security_score * weights['security']
    )
    
    # Cap à 100
    final_score = min(final_score, 100)
    
    # Détermination du verdict
    if final_score >= 80:
        verdict = "✅ Excellent"
        verdict_color = "green"
    elif final_score >= 65:
        verdict = "✅ Bon"
        verdict_color = "green"
    elif final_score >= 50:
        verdict = "⚠️ Acceptable"
        verdict_color = "orange"
    elif final_score >= 35:
        verdict = "⚠️ Risqué"
        verdict_color = "orange"
    else:
        verdict = "🚨 Très risqué"
        verdict_color = "red"
    
    return {
        'final_score': round(final_score, 1),
        'verdict': verdict,
        'verdict_color': verdict_color,
        'inflation_score': round(inflation_score, 1),
        'inflation_comment': inflation_comment,
        'distribution_score': round(distribution_score, 1),
        'distribution_comment': distribution_comment,
        'utility_score': round(utility_score, 1),
        'utility_comment': utility_comment,
        'governance_score': round(governance_score, 1),
        'governance_comment': governance_comment,
        'incentives_score': round(incentives_score, 1),
        'incentives_comment': incentives_comment,
        'liquidity_score': round(liquidity_score, 1),
        'liquidity_comment': liquidity_comment,
        'adoption_score': round(adoption_score, 1),
        'adoption_comment': adoption_comment,
        'security_score': round(security_score, 1),
        'security_comment': security_comment,
        'weights': weights
    }


def get_recommendations(score_data: Dict[str, Any]) -> list:
    """
    Génère des recommandations basées sur les scores.
    
    Args:
        score_data: Résultats de calculate_viability_index()
        
    Returns:
        Liste de recommandations
    """
    recommendations = []
    
    if score_data['inflation_score'] < 50:
        recommendations.append("⚠️ **Inflation élevée** : Vérifier les mécanismes de compensation (burn, lock, utilité forte)")
    
    if score_data['distribution_score'] < 50:
        recommendations.append("⚠️ **Distribution problématique** : Concentration élevée ou vesting insuffisant")
    
    if score_data['utility_score'] < 40:
        recommendations.append("🚨 **Utilité faible** : Le token manque de cas d'usage réels et de demande intrinsèque")
    
    if score_data['governance_score'] < 50:
        recommendations.append("⚠️ **Gouvernance à risque** : Timelock et décentralisation insuffisants")
    
    if score_data['incentives_score'] < 50:
        recommendations.append("⚠️ **Incitations faibles** : Peu de mécanismes pour retenir les holders long terme")
    
    # Nouveaux critères
    if score_data.get('liquidity_score', 100) < 50:
        recommendations.append("🚨 **Liquidité très faible** : Risque de slippage et manipulation de prix élevé")
    
    if score_data.get('adoption_score', 100) < 50:
        recommendations.append("⚠️ **Adoption limitée** : Faible traction utilisateurs ou market cap")
    
    if score_data.get('security_score', 50) < 40:
        recommendations.append("🚨 **Sécurité non vérifiée** : Absence d'audits confirmés - risque smart contract")
    
    if score_data['final_score'] >= 80:
        recommendations.append("✅ **Tokenomics solide** : Le modèle économique semble viable à long terme")
    elif score_data['final_score'] >= 65:
        recommendations.append("✅ **Tokenomics correcte** : Quelques points d'amélioration mais globalement sain")
    elif score_data['final_score'] < 35:
        recommendations.append("🚨 **Tokenomics très risquée** : Nombreux red flags, prudence recommandée")
    
    return recommendations


def calculate_liquidity_score(
    volume_24h: float,
    market_cap: float,
    volume_to_mcap: float,
    market_cap_rank: int
) -> Tuple[float, str]:
    """
    Calcule le score de liquidité (0-100).
    
    Args:
        volume_24h: Volume 24h en USD
        market_cap: Market cap en USD
        volume_to_mcap: Ratio Volume/Market Cap en %
        market_cap_rank: Rang du token
        
    Returns:
        (score, commentaire)
    """
    score = 100.0
    comments = []
    
    # 1. Ratio Volume/Market Cap (jusqu'à -40 points)
    if volume_to_mcap >= 10:
        comments.append(f"✅ Liquidité excellente : {volume_to_mcap:.1f}% du market cap")
    elif volume_to_mcap >= 5:
        score -= 10
        comments.append(f"✅ Bonne liquidité : {volume_to_mcap:.1f}% du market cap")
    elif volume_to_mcap >= 2:
        score -= 20
        comments.append(f"⚠️ Liquidité modérée : {volume_to_mcap:.1f}% du market cap")
    elif volume_to_mcap >= 1:
        score -= 30
        comments.append(f"⚠️ Liquidité faible : {volume_to_mcap:.1f}% du market cap")
    else:
        score -= 40
        comments.append(f"🚨 Liquidité très faible : {volume_to_mcap:.1f}% du market cap - risque de slippage")
    
    # 2. Volume absolu (jusqu'à -30 points)
    if volume_24h >= 100_000_000:  # >$100M
        comments.append("✅ Volume 24h très élevé (>$100M)")
    elif volume_24h >= 10_000_000:  # >$10M
        score -= 5
        comments.append("✅ Volume 24h élevé (>$10M)")
    elif volume_24h >= 1_000_000:  # >$1M
        score -= 15
        comments.append("⚠️ Volume 24h modéré (>$1M)")
    elif volume_24h >= 100_000:  # >$100K
        score -= 25
        comments.append("⚠️ Volume 24h faible (>$100K)")
    else:
        score -= 30
        comments.append("🚨 Volume 24h très faible (<$100K) - risque de manipulation")
    
    # 3. Bonus pour les top tokens
    if market_cap_rank <= 50:
        score += 10
        comments.append(f"✅ Top 50 market cap (Rank #{market_cap_rank})")
    elif market_cap_rank <= 100:
        score += 5
        comments.append(f"✅ Top 100 market cap (Rank #{market_cap_rank})")
    
    score = max(0, min(100, score))
    comment = " | ".join(comments)
    
    return score, comment


def calculate_adoption_score(
    market_cap: float,
    market_cap_rank: int,
    price_change_30d: float
) -> Tuple[float, str]:
    """
    Calcule le score d'adoption (0-100).
    Note: Version simplifiée sans TVL (nécessiterait DeFiLlama API)
    
    Args:
        market_cap: Market cap en USD
        market_cap_rank: Rang du token
        price_change_30d: Variation prix 30j en %
        
    Returns:
        (score, commentaire)
    """
    score = 100.0
    comments = []
    
    # 1. Market cap comme proxy d'adoption (jusqu'à -40 points)
    if market_cap >= 10_000_000_000:  # >$10B
        comments.append("✅ Adoption massive : Market cap >$10B")
    elif market_cap >= 1_000_000_000:  # >$1B
        score -= 10
        comments.append("✅ Forte adoption : Market cap >$1B")
    elif market_cap >= 100_000_000:  # >$100M
        score -= 20
        comments.append("⚠️ Adoption moyenne : Market cap >$100M")
    elif market_cap >= 10_000_000:  # >$10M
        score -= 30
        comments.append("⚠️ Adoption limitée : Market cap >$10M")
    else:
        score -= 40
        comments.append("🚨 Adoption très faible : Market cap <$10M")
    
    # 2. Rank comme indicateur de popularité (jusqu'à -30 points)
    if market_cap_rank <= 20:
        score += 10
        comments.append(f"✅ Top 20 crypto (Rank #{market_cap_rank})")
    elif market_cap_rank <= 100:
        score += 5
        comments.append(f"✅ Top 100 crypto (Rank #{market_cap_rank})")
    elif market_cap_rank <= 500:
        score -= 10
        comments.append(f"⚠️ Rank #{market_cap_rank}")
    else:
        score -= 20
        comments.append(f"⚠️ Rank très bas #{market_cap_rank}")
    
    # 3. Momentum (prix 30j) (jusqu'à -20 points)
    if price_change_30d >= 50:
        score += 10
        comments.append(f"📈 Forte croissance : +{price_change_30d:.1f}% (30j)")
    elif price_change_30d >= 20:
        score += 5
        comments.append(f"📈 Bonne croissance : +{price_change_30d:.1f}% (30j)")
    elif price_change_30d >= -10:
        comments.append(f"📊 Stable : {price_change_30d:+.1f}% (30j)")
    elif price_change_30d >= -30:
        score -= 10
        comments.append(f"📉 Baisse modérée : {price_change_30d:.1f}% (30j)")
    else:
        score -= 20
        comments.append(f"📉 Forte baisse : {price_change_30d:.1f}% (30j)")
    
    score = max(0, min(100, score))
    comment = " | ".join(comments)
    
    return score, comment


def calculate_security_score(
    coin_id: str,
    market_cap_rank: int
) -> Tuple[float, str]:
    """
    Calcule le score de sécurité (0-100).
    Base de données manuelle des audits pour les tokens enrichis.
    
    Args:
        coin_id: ID CoinGecko du token
        market_cap_rank: Rang du token
        
    Returns:
        (score, commentaire)
    """
    # Base de données des audits (à enrichir)
    security_db = {
        'ethereum': {'audits': 5, 'bug_bounty': True, 'bounty_amount': 10_000_000},
        'bitcoin': {'audits': 10, 'bug_bounty': False, 'bounty_amount': 0},
        'uniswap': {'audits': 4, 'bug_bounty': True, 'bounty_amount': 2_000_000},
        'aave': {'audits': 6, 'bug_bounty': True, 'bounty_amount': 1_000_000},
        'curve-dao-token': {'audits': 5, 'bug_bounty': True, 'bounty_amount': 500_000},
        'maker': {'audits': 7, 'bug_bounty': True, 'bounty_amount': 10_000_000},
        'chainlink': {'audits': 4, 'bug_bounty': True, 'bounty_amount': 1_000_000},
        'lido-dao': {'audits': 4, 'bug_bounty': True, 'bounty_amount': 2_000_000},
        'arbitrum': {'audits': 3, 'bug_bounty': True, 'bounty_amount': 2_000_000},
        'optimism': {'audits': 3, 'bug_bounty': True, 'bounty_amount': 2_000_000},
        'pendle': {'audits': 3, 'bug_bounty': True, 'bounty_amount': 500_000},
        'gmx': {'audits': 3, 'bug_bounty': True, 'bounty_amount': 500_000},
    }
    
    score = 50.0  # Score de base (neutre)
    comments = []
    
    if coin_id in security_db:
        data = security_db[coin_id]
        
        # Audits (jusqu'à +30 points)
        audits = data['audits']
        if audits >= 5:
            score += 30
            comments.append(f"✅ Très bien audité : {audits} audits")
        elif audits >= 3:
            score += 20
            comments.append(f"✅ Bien audité : {audits} audits")
        elif audits >= 1:
            score += 10
            comments.append(f"⚠️ Partiellement audité : {audits} audits")
        
        # Bug bounty (jusqu'à +20 points)
        if data['bug_bounty']:
            bounty = data['bounty_amount']
            if bounty >= 1_000_000:
                score += 20
                comments.append(f"✅ Bug bounty important : ${bounty:,.0f}")
            elif bounty >= 100_000:
                score += 10
                comments.append(f"✅ Bug bounty actif : ${bounty:,.0f}")
            else:
                score += 5
                comments.append("✅ Bug bounty actif")
    else:
        # Pas de données : estimation par heuristique
        if market_cap_rank <= 50:
            score = 60
            comments.append(f"⚠️ Top 50 : généralement audité (Rank #{market_cap_rank})")
        elif market_cap_rank <= 200:
            score = 50
            comments.append(f"⚠️ Audits probables mais non vérifiés (Rank #{market_cap_rank})")
        else:
            score = 30
            comments.append(f"⚠️ Audits non vérifiés - risque smart contract élevé (Rank #{market_cap_rank})")
        comments.append("ℹ️ Données d'audit à enrichir manuellement")
    
    score = max(0, min(100, score))
    comment = " | ".join(comments)
    
    return score, comment

