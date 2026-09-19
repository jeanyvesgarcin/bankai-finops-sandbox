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
        Scenario 1 : Un développeur a inséré un timestamp dynamique au début du prompt système.
        Compare l'exécution normale (cache actif) vs corrompue (cache détruit).
        """
        # Baseline : Avec cache
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

        # Anomaly : Cache busting actif
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
            name="Destruction du Prompt Caching (Cache-Busting)",
            scenario_description="Insertion d'un UUID dynamique au début du prompt système détruisant le cache préfixe.",
            requests_processed=n_requests,
            unprotected_cost_eur=round(cost_busted, 4),
            protected_cost_eur=round(cost_normal, 4),
            savings_eur=round(savings, 4),
            savings_percent=round(pct, 2),
            anomaly_detected=True,
            remediation_action="Règles de linting QA sur prompts statiques et tests de régression de cache hit ratio."
        )

    def run_silent_fallback_scenario(self, n_requests: int = 100, fail_at: int = 20) -> AnomalyResult:
        """
        Scenario 2 : Le cluster souverain vLLM On-Prem tombe. Le système bascule silencieusement
        vers GPT-4o Cloud. Sans disjoncteur, la facture explose.
        """
        # Unprotected : Bascule totale sans limite
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

        # Protected : FallbackCircuitGuard coupe après 10 requêtes sur le modèle de secours
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
                    # Disjoncteur déclenché : bascule vers moteur de règles dégradé (coût 0€)
                    model = "llama-3-70b-vllm"  # simule règle statique
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
            name="Bascule Silencieuse Non Contrôlée (Silent Fallback Spill)",
            scenario_description="Panne du GPU souverain local entraînant une fuite de 80 requêtes vers l'API externe payante.",
            requests_processed=n_requests,
            unprotected_cost_eur=round(cost_unprotected, 4),
            protected_cost_eur=round(cost_protected, 4),
            savings_eur=round(savings, 4),
            savings_percent=round(pct, 2),
            anomaly_detected=circuit_tripped,
            remediation_action="Déclenchement du FallbackCircuitGuard au bout de 10 requêtes et bascule en mode dégradé."
        )

    def run_denial_of_wallet_scenario(self, n_heavy_docs: int = 30) -> AnomalyResult:
        """
        Scenario 3 : Bombardement de documents de 50 pages (300 KB) sur le pipeline KYC.
        """
        heavy_text = "BILAN COMPTABLE BANCAIRE & ANNEXES FINANCIÈRES CONFIDENTIELLES\n" * 5000  # ~350 KB
        normal_text = "Extrait Kbis Société Générale SAS au capital de 100000 EUR."

        # Unprotected
        llm_unprotected = BankingLLMMock()
        workload_unprotected = KYCExtractionWorkload(llm_unprotected)
        for i in range(n_heavy_docs):
            workload_unprotected.process_kyc_document(
                company_name=f"Entreprise_{i}",
                document_text=heavy_text,
                page_count=50,
                enable_anti_dow_guard=False  # Pas de garde-fou
            )
        cost_unprotected = llm_unprotected.total_cost_eur

        # Protected
        llm_protected = BankingLLMMock()
        workload_protected = KYCExtractionWorkload(llm_protected)
        blocked_count = 0
        for i in range(n_heavy_docs):
            res = workload_protected.process_kyc_document(
                company_name=f"Entreprise_{i}",
                document_text=heavy_text,
                page_count=50,
                enable_anti_dow_guard=True  # Garde-fou actif
            )
            if res["status"] == "REJECTED_BY_ANTI_DOW":
                blocked_count += 1
        cost_protected = llm_protected.total_cost_eur

        savings = cost_unprotected - cost_protected
        pct = (savings / max(0.0001, cost_unprotected)) * 100.0

        return AnomalyResult(
            name="Attaque Denial of Wallet (Bombardement KYC)",
            scenario_description=f"Envoi de {n_heavy_docs} documents lourds de 50 pages dans l'analyseur IA.",
            requests_processed=n_heavy_docs,
            unprotected_cost_eur=round(cost_unprotected, 4),
            protected_cost_eur=round(cost_protected, 4),
            savings_eur=round(savings, 4),
            savings_percent=round(pct, 2),
            anomaly_detected=blocked_count == n_heavy_docs,
            remediation_action=f"Validation pré-modèle : {blocked_count}/{n_heavy_docs} documents rejetés avant l'appel LLM."
        )

    def run_runaway_agent_loop_scenario(self) -> AnomalyResult:
        """
        Scenario 4 : Agent autonome de conformité bouclant en rond sur un dossier complexe.
        """
        llm = BankingLLMMock(default_model="gpt-4o")

        # Unprotected simulation : 40 tours de boucle
        unprotected_cost = 0.0
        for turn in range(40):
            resp = llm.generate([
                {"role": "system", "content": "Vous êtes un agent d'audit."},
                {"role": "user", "content": f"Tour {turn}: Vérifier les statuts juridiques de la filiale numéro {turn}."}
            ])
            unprotected_cost += resp.cost_eur

        # Protected simulation : Coupé au bout de 5 tours par le MaxStepBudgetGuard
        protected_cost = 0.0
        llm_prot = BankingLLMMock(default_model="gpt-4o")
        max_turns = 5
        for turn in range(max_turns):
            resp = llm_prot.generate([
                {"role": "system", "content": "Vous êtes un agent d'audit."},
                {"role": "user", "content": f"Tour {turn}: Vérifier les statuts juridiques de la filiale numéro {turn}."}
            ])
            protected_cost += resp.cost_eur

        savings = unprotected_cost - protected_cost
        pct = (savings / max(0.0001, unprotected_cost)) * 100.0

        return AnomalyResult(
            name="Boucle Infinie d'Agent Autonome (Runaway Agent)",
            scenario_description="Agent autonome bloqué dans une recherche circulaire d'actionnaires (40 itérations).",
            requests_processed=40,
            unprotected_cost_eur=round(unprotected_cost, 4),
            protected_cost_eur=round(protected_cost, 4),
            savings_eur=round(savings, 4),
            savings_percent=round(pct, 2),
            anomaly_detected=True,
            remediation_action="Interruption matérielle au 5ème tour par le MaxStepBudgetGuard et escalade humaine."
        )
