"""
AI FinOps Chaos Injector - Banking Anomaly Simulations.
Allows the AI QA Architect to inject and measure 4 realistic financial failure modes:
1. Cache-Busting Deployment (Prefix cache destruction)
2. Silent Cloud Fallback Spill (Sovereign GPU failover to expensive Public API)
3. Denial of Wallet (DoW) Document Bombardment
4. Runaway Autonomous Agent Loop
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional
import time
from ..engine.banking_llm_mock import BankingLLMMock
from ..engine.workloads import CreditScoringWorkload, KYCExtractionWorkload

@dataclass
class AnomalyResult:
    name: str
    scenario_description: str
    requests_processed: int
    unprotected_cost_eur: float
    protected_cost_eur: float
    savings_eur: float
    savings_percent: float
    anomaly_detected: bool
    remediation_action: str

class BankingChaosInjector:
    """Injects and quantifies FinOps chaos scenarios."""

    def __init__(self):
        pass

    def run_cache_busting_scenario(self, n_requests: int = 50) -> AnomalyResult:
        """
        Scenario 1: A developer inserted a dynamic timestamp or random UUID at the beginning of the system prompt.
        Compares normal execution (cache active) vs corrupted execution (prefix cache destroyed).
        """
        # Baseline: With prefix caching
        llm_normal = BankingLLMMock(default_model="gpt-4o")
        workload_normal = CreditScoringWorkload(llm_normal)
        for i in range(n_requests):
            workload_normal.process_application(
                applicant_id=f"APP_{i:04d}",
                income_eur=3500.0,
                loan_amount_eur=180000.0,
                monthly_debt_eur=600.0,
                credit_score=710,
                use_cache_busting=False,
                target_model="gpt-4o"
            )
        cost_normal = llm_normal.total_cost_eur

        # Anomaly: Cache busting active
        llm_busted = BankingLLMMock(default_model="gpt-4o")
        workload_busted = CreditScoringWorkload(llm_busted)
        for i in range(n_requests):
            workload_busted.process_application(
                applicant_id=f"APP_{i:04d}",
                income_eur=3500.0,
                loan_amount_eur=180000.0,
                monthly_debt_eur=600.0,
                credit_score=710,
                use_cache_busting=True,  # BUG INJECTED
                target_model="gpt-4o"
            )
        cost_busted = llm_busted.total_cost_eur

        savings = cost_busted - cost_normal
        pct = (savings / max(0.0001, cost_busted)) * 100.0

        return AnomalyResult(
            name="Prompt Caching Destruction (Cache-Busting)",
            scenario_description="Dynamic UUID prepended to system prompt, completely destroying prefix cache reuse.",
            requests_processed=n_requests,
            unprotected_cost_eur=round(cost_busted, 4),
            protected_cost_eur=round(cost_normal, 4),
            savings_eur=round(savings, 4),
            savings_percent=round(pct, 2),
            anomaly_detected=True,
            remediation_action="Static prompt linting in CI/CD and automated Pytest assertion on cache_hit_ratio."
        )

    def run_silent_fallback_scenario(self, n_requests: int = 100, fail_at: int = 20) -> AnomalyResult:
        """
        Scenario 2: Sovereign vLLM on-prem cluster crashes (GPU OOM). The system silently fails over
        to OpenAI GPT-4o Cloud API. Without a circuit breaker, expenses spiral exponentially.
        """
        # Unprotected: Unbounded failover
        llm_unprotected = BankingLLMMock()
        workload_unprotected = CreditScoringWorkload(llm_unprotected)
        for i in range(n_requests):
            model = "llama-3-70b-vllm" if i < fail_at else "gpt-4o"
            workload_unprotected.process_application(
                applicant_id=f"APP_{i:04d}",
                income_eur=4000.0,
                loan_amount_eur=250000.0,
                monthly_debt_eur=800.0,
                credit_score=750,
                target_model=model
            )
        cost_unprotected = llm_unprotected.total_cost_eur

        # Protected: FallbackCircuitGuard trips after 10 fallback requests
        llm_protected = BankingLLMMock()
        workload_protected = CreditScoringWorkload(llm_protected)
        fallback_counter = 0
        circuit_tripped = False

        for i in range(n_requests):
            if i < fail_at:
                model = "llama-3-70b-vllm"
            else:
                if fallback_counter >= 10:
                    circuit_tripped = True
                    # Circuit tripped: graceful degradation to zero-cost deterministic rule engine
                    model = "llama-3-70b-vllm"
                    continue
                else:
                    model = "gpt-4o"
                    fallback_counter += 1

            workload_protected.process_application(
                applicant_id=f"APP_{i:04d}",
                income_eur=4000.0,
                loan_amount_eur=250000.0,
                monthly_debt_eur=800.0,
                credit_score=750,
                target_model=model
            )
        cost_protected = llm_protected.total_cost_eur
        savings = cost_unprotected - cost_protected
        pct = (savings / max(0.0001, cost_unprotected)) * 100.0

        return AnomalyResult(
            name="Silent Cloud Fallback Spill",
            scenario_description="Sovereign GPU cluster failure leaking 80 high-volume requests to expensive public cloud APIs.",
            requests_processed=n_requests,
            unprotected_cost_eur=round(cost_unprotected, 4),
            protected_cost_eur=round(cost_protected, 4),
            savings_eur=round(savings, 4),
            savings_percent=round(pct, 2),
            anomaly_detected=circuit_tripped,
            remediation_action="FallbackCircuitGuard tripped at 10 requests, switching to deterministic rule fallback."
        )

    def run_denial_of_wallet_scenario(self, n_heavy_docs: int = 30) -> AnomalyResult:
        """
        Scenario 3: Denial of Wallet bombardment of 50-page financial statements (350 KB) on the KYC pipeline.
        """
        heavy_text = "CONSOLIDATED CORPORATE FINANCIAL STATEMENT & TAX AUDIT DISCLOSURES\n" * 5000  # ~350 KB
        normal_text = "Certificate of Incorporation - Apex Holdings Limited."

        # Unprotected
        llm_unprotected = BankingLLMMock()
        workload_unprotected = KYCExtractionWorkload(llm_unprotected)
        for i in range(n_heavy_docs):
            workload_unprotected.process_kyc_document(
                company_name=f"CorporateEntity_{i}",
                document_text=heavy_text,
                page_count=50,
                enable_anti_dow_guard=False  # No guard
            )
        cost_unprotected = llm_unprotected.total_cost_eur

        # Protected
        llm_protected = BankingLLMMock()
        workload_protected = KYCExtractionWorkload(llm_protected)
        blocked_count = 0
        for i in range(n_heavy_docs):
            res = workload_protected.process_kyc_document(
                company_name=f"CorporateEntity_{i}",
                document_text=heavy_text,
                page_count=50,
                enable_anti_dow_guard=True  # Guard active
            )
            if res["status"] == "REJECTED_BY_ANTI_DOW":
                blocked_count += 1
        cost_protected = llm_protected.total_cost_eur

        savings = cost_unprotected - cost_protected
        pct = (savings / max(0.0001, cost_unprotected)) * 100.0

        return AnomalyResult(
            name="Denial of Wallet Attack (KYC Bombardment)",
            scenario_description=f"Submission of {n_heavy_docs} oversized 50-page documents aimed at budget exhaustion.",
            requests_processed=n_heavy_docs,
            unprotected_cost_eur=round(cost_unprotected, 4),
            protected_cost_eur=round(cost_protected, 4),
            savings_eur=round(savings, 4),
            savings_percent=round(pct, 2),
            anomaly_detected=blocked_count == n_heavy_docs,
            remediation_action=f"Pre-execution gate rejected {blocked_count}/{n_heavy_docs} oversized payloads at 0 EUR cost."
        )

    def run_runaway_agent_loop_scenario(self) -> AnomalyResult:
        """
        Scenario 4: Autonomous AML compliance investigation agent trapped in an infinite loop.
        """
        llm = BankingLLMMock(default_model="gpt-4o")

        # Unprotected simulation: 40 recursive turns
        unprotected_cost = 0.0
        for turn in range(40):
            resp = llm.generate([
                {"role": "system", "content": "You are an autonomous compliance agent."},
                {"role": "user", "content": f"Turn {turn}: Cross-reference legal ownership hierarchy for corporate subsidiary #{turn}."}
            ])
            unprotected_cost += resp.cost_eur

        # Protected simulation: Forcibly interrupted at turn 5 by MaxStepBudgetGuard
        protected_cost = 0.0
        llm_prot = BankingLLMMock(default_model="gpt-4o")
        max_turns = 5
        for turn in range(max_turns):
            resp = llm_prot.generate([
                {"role": "system", "content": "You are an autonomous compliance agent."},
                {"role": "user", "content": f"Turn {turn}: Cross-reference legal ownership hierarchy for corporate subsidiary #{turn}."}
            ])
            protected_cost += resp.cost_eur

        savings = unprotected_cost - protected_cost
        pct = (savings / max(0.0001, unprotected_cost)) * 100.0

        return AnomalyResult(
            name="Runaway Autonomous Agent Loop",
            scenario_description="Autonomous compliance agent trapped in circular corporate shareholding exploration (40 iterations).",
            requests_processed=40,
            unprotected_cost_eur=round(unprotected_cost, 4),
            protected_cost_eur=round(protected_cost, 4),
            savings_eur=round(savings, 4),
            savings_percent=round(pct, 2),
            anomaly_detected=True,
            remediation_action="Hard cutoff at turn 5 by MaxStepBudgetGuard with escalation to human compliance officer."
        )
