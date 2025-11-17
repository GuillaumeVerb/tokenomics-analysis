"""
Module de calcul du Tokenomics Viability Index.

Le score final (0-100) est calculé selon 5 composantes :
1. Inflation (25%)
2. Distribution (20%)
3. Utilité (25%)
4. Gouvernance (15%)
5. Incitations (15%)
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
    
    # Pondérations
    weights = {
        'inflation': 0.25,
        'distribution': 0.20,
        'utility': 0.25,
        'governance': 0.15,
        'incentives': 0.15
    }
    
    # Calcul du score final
    final_score = (
        inflation_score * weights['inflation'] +
        distribution_score * weights['distribution'] +
        utility_score * weights['utility'] +
        governance_score * weights['governance'] +
        incentives_score * weights['incentives']
    )
    
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
    
    if score_data['final_score'] >= 80:
        recommendations.append("✅ **Tokenomics solide** : Le modèle économique semble viable à long terme")
    elif score_data['final_score'] >= 65:
        recommendations.append("✅ **Tokenomics correcte** : Quelques points d'amélioration mais globalement sain")
    elif score_data['final_score'] < 35:
        recommendations.append("🚨 **Tokenomics très risquée** : Nombreux red flags, prudence recommandée")
    
    return recommendations

