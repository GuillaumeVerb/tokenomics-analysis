"""
Script de test pour vérifier que tous les modules fonctionnent correctement.
"""

import sys
from tokenomics.scenarios import get_all_scenarios, get_scenario_params, get_inflation_projection
from tokenomics.scoring import calculate_viability_index
from tokenomics.visualizations import (
    create_supply_distribution_chart,
    create_dilution_projection,
    create_gauge_chart
)


def test_scenarios():
    """Test du module scenarios."""
    print("🧪 Test du module scenarios...")
    
    scenarios = get_all_scenarios()
    assert len(scenarios) == 18, f"Expected 18 scenarios, got {len(scenarios)}"
    print(f"  ✅ {len(scenarios)} scénarios chargés")
    
    # Test d'un scénario
    params = get_scenario_params("Projet early-stage")
    assert params['circulating_supply'] == 100_000_000
    print("  ✅ Paramètres d'un scénario chargés correctement")
    
    # Test de projection d'inflation
    projection = get_inflation_projection("Inflation stable 5% / an", years=5)
    assert len(projection) == 5
    assert all(rate == 5.0 for rate in projection)
    print("  ✅ Projection d'inflation calculée correctement")


def test_scoring():
    """Test du module scoring."""
    print("\n🧪 Test du module scoring...")
    
    params = {
        'circulating_supply': 500_000_000,
        'total_supply': 1_000_000_000,
        'max_supply': 1_000_000_000,
        'inflation_rate': 5.0,
        'emission_years_left': 5,
        'team_allocation': 15.0,
        'vesting_years': 3,
        'top_10_concentration': 30.0,
        'utility_gas': True,
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
    
    result = calculate_viability_index(params)
    
    assert 'final_score' in result
    assert 0 <= result['final_score'] <= 100
    print(f"  ✅ Score calculé : {result['final_score']:.1f}/100")
    
    assert 'verdict' in result
    print(f"  ✅ Verdict : {result['verdict']}")


def test_visualizations():
    """Test du module visualizations."""
    print("\n🧪 Test du module visualizations...")
    
    try:
        # Test camembert
        fig = create_supply_distribution_chart(500_000_000, 750_000_000, 1_000_000_000)
        assert fig is not None
        print("  ✅ Camembert de supply créé")
        
        # Test projection
        fig = create_dilution_projection(500_000_000, inflation_rate=5.0, years=5)
        assert fig is not None
        print("  ✅ Projection de dilution créée")
        
        # Test jauge
        fig = create_gauge_chart(75.5)
        assert fig is not None
        print("  ✅ Jauge de score créée")
        
    except Exception as e:
        print(f"  ❌ Erreur lors de la création des graphiques : {e}")
        return False
    
    return True


def test_all_scenarios():
    """Test de tous les scénarios."""
    print("\n🧪 Test de tous les scénarios...")
    
    scenarios = get_all_scenarios()
    errors = []
    
    for scenario in scenarios:
        try:
            params = get_scenario_params(scenario)
            result = calculate_viability_index(params)
            assert 0 <= result['final_score'] <= 100
        except Exception as e:
            errors.append(f"  ❌ Erreur avec '{scenario}': {e}")
    
    if errors:
        for error in errors:
            print(error)
        return False
    else:
        print(f"  ✅ Tous les {len(scenarios)} scénarios testés avec succès")
        return True


def main():
    """Exécute tous les tests."""
    print("=" * 60)
    print("🧪 TESTS DE TOKENOMICS ANALYZER")
    print("=" * 60)
    
    try:
        test_scenarios()
        test_scoring()
        test_visualizations()
        test_all_scenarios()
        
        print("\n" + "=" * 60)
        print("✅ TOUS LES TESTS SONT PASSÉS")
        print("=" * 60)
        print("\n🚀 Vous pouvez maintenant lancer l'application avec :")
        print("   streamlit run app.py")
        print("   ou")
        print("   ./run.sh\n")
        
        return 0
        
    except AssertionError as e:
        print(f"\n❌ TEST ÉCHOUÉ : {e}")
        return 1
    except Exception as e:
        print(f"\n❌ ERREUR INATTENDUE : {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

