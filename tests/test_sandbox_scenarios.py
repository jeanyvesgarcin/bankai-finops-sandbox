"""
Automated Pytest Suite for BankAI FinOps Sandbox.
Validates the financial invariants, guardrails, and chaos mitigations.
"""

import sys
from pathlib import Path
import pytest

# Ensure bankai_finops_sandbox and root are on sys.path
TEST_DIR = Path(__file__).resolve().parent
SANDBOX_DIR = TEST_DIR.parent
ROOT_DIR = SANDBOX_DIR.parent

for p in [str(ROOT_DIR), str(SANDBOX_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from bankai_finops_sandbox.engine.banking_llm_mock import BankingLLMMock
    from bankai_finops_sandbox.engine.workloads import CreditScoringWorkload, KYCExtractionWorkload, WealthCopilotWorkload
    from bankai_finops_sandbox.chaos.chaos_injector import BankingChaosInjector
except ImportError:
    from engine.banking_llm_mock import BankingLLMMock
    from engine.workloads import CreditScoringWorkload, KYCExtractionWorkload, WealthCopilotWorkload
    from chaos.chaos_injector import BankingChaosInjector

@pytest.fixture
def chaos_injector():
    return BankingChaosInjector()

def test_credit_scoring_nominal_budget():
    """Vérifie que le coût par dossier de crédit reste inférieur au seuil NFR de 0.0005 EUR."""
    llm = BankingLLMMock(default_model="gpt-4o-mini")
    workload = CreditScoringWorkload(llm)

    # 1st call warms up cache
    workload.process_application("APP_0001", 3000.0, 150000.0, 500.0, 720)

    # 2nd call uses cache
    resp = workload.process_application("APP_0002", 3200.0, 160000.0, 550.0, 740)

    assert resp.cost_eur < 0.0005, f"Le coût unitaire ({resp.cost_eur:.6f} EUR) dépasse le plafond NFR."
    assert resp.cached_tokens > 0, "Le Prompt Caching préfixe aurait dû être activé."

def test_cache_busting_anomaly_mitigation(chaos_injector):
    """Vérifie que l'anomalie de cache busting entraîne bien un surcoût détecté et quantifié."""
    res = chaos_injector.run_cache_busting_scenario(n_requests=20)
    assert res.anomaly_detected is True
    assert res.unprotected_cost_eur > res.protected_cost_eur
    assert res.savings_percent > 30.0, "La protection de cache doit générer au moins 30% d'économies."

def test_silent_fallback_circuit_breaker(chaos_injector):
    """Vérifie que le disjoncteur coupe la bascule silencieuse vers l'API Cloud coûteuse."""
    res = chaos_injector.run_silent_fallback_scenario(n_requests=50, fail_at=10)
    assert res.anomaly_detected is True
    assert res.protected_cost_eur < res.unprotected_cost_eur
    assert res.savings_eur > 0.0

def test_denial_of_wallet_guard_blocks_heavy_docs(chaos_injector):
    """Vérifie que l'attaque DoW est bloquée à 100% sans consommer de tokens LLM."""
    res = chaos_injector.run_denial_of_wallet_scenario(n_heavy_docs=10)
    assert res.anomaly_detected is True
    assert res.protected_cost_eur == 0.0, "Les documents lourds doivent être rejetés à coût 0€."
    assert res.savings_percent == 100.0

def test_wealth_copilot_sliding_window_inflation():
    """Vérifie que la fenêtre glissante empêche l'inflation quadratique des coûts de chat."""
    llm_unprot = BankingLLMMock(default_model="gpt-4o-mini")
    workload_unprot = WealthCopilotWorkload(llm_unprot)
    resps_unprot = workload_unprot.run_multi_turn_session(num_turns=6, enable_sliding_window=False)
    cost_unprot = llm_unprot.total_cost_eur

    llm_prot = BankingLLMMock(default_model="gpt-4o-mini")
    workload_prot = WealthCopilotWorkload(llm_prot)
    resps_prot = workload_prot.run_multi_turn_session(num_turns=6, enable_sliding_window=True, max_history_turns=2)
    cost_prot = llm_prot.total_cost_eur

    assert cost_prot < cost_unprot, "La fenêtre glissante doit réduire le coût sur les sessions longues."
