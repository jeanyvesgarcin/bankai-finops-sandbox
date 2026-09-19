"""
Main CLI Orchestrator for BankAI FinOps Sandbox.
Entry point for running simulated banking workloads, injecting chaos scenarios,
compiling interactive HTML dashboards, and generating portfolio case studies.
"""

import argparse
import sys
from pathlib import Path

# Configure UTF-8 for Windows console
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Ensure root directory is in sys.path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR.parent) not in sys.path:
    sys.path.insert(0, str(BASE_DIR.parent))

from bankai_finops_sandbox.engine.banking_llm_mock import BankingLLMMock
from bankai_finops_sandbox.engine.workloads import CreditScoringWorkload, KYCExtractionWorkload, WealthCopilotWorkload
from bankai_finops_sandbox.chaos.chaos_injector import BankingChaosInjector
from bankai_finops_sandbox.dashboard.interactive_console import (
    print_banner,
    print_live_metrics_card,
    print_anomaly_table,
    print_portfolio_instructions
)
from bankai_finops_sandbox.dashboard.export_html_dashboard import generate_html_dashboard
from bankai_finops_sandbox.reports.portfolio_generator import generate_portfolio_case_study

def run_nominal_simulation(n_credit: int = 40, n_kyc: int = 15, n_wealth_turns: int = 6) -> BankingLLMMock:
    print(f"\n[*] Exécution de la charge nominale bancaire ({n_credit} crédits, {n_kyc} KYC, {n_wealth_turns} tours conseiller)...")
    llm = BankingLLMMock(default_model="gpt-4o-mini")

    # 1. Credit scoring
    credit_wl = CreditScoringWorkload(llm)
    for i in range(n_credit):
        credit_wl.process_application(
            applicant_id=f"APP_{i:04d}",
            income_eur=2800.0 + (i * 50),
            loan_amount_eur=120000.0 + (i * 2000),
            monthly_debt_eur=500.0,
            credit_score=680 + (i % 80)
        )

    # 2. KYC
    kyc_wl = KYCExtractionWorkload(llm)
    for i in range(n_kyc):
        kyc_wl.process_kyc_document(
            company_name=f"Holding Financière {i}",
            document_text=f"Rapport d'activité annuel société {i} : SIREN 123456789, Bénéficiaires réguliers.",
            page_count=3,
            enable_anti_dow_guard=True
        )

    # 3. Wealth Copilot
    wealth_wl = WealthCopilotWorkload(llm)
    wealth_wl.run_multi_turn_session(num_turns=n_wealth_turns, enable_sliding_window=True)

    return llm

def main():
    parser = argparse.ArgumentParser(description="BankAI FinOps Sandbox & Portfolio Lab")
    parser.add_argument("--mode", choices=["demo", "chaos", "benchmark", "all"], default="all", help="Mode d'exécution")
    parser.add_argument("--export-html", action="store_true", default=True, help="Générer le tableau de bord HTML interactif")
    parser.add_argument("--export-portfolio", action="store_true", default=True, help="Générer l'étude de cas Markdown PORTFOLIO_CASE_STUDY.md")
    args = parser.parse_args()

    print_banner()

    # 1. Nominal simulation
    llm = run_nominal_simulation()
    metrics = llm.get_summary()
    print_live_metrics_card(metrics)

    # 2. Chaos scenarios
    print("[*] Injection des 4 scénarios d'anomalies financières et de résilience...")
    chaos = BankingChaosInjector()
    results = [
        chaos.run_cache_busting_scenario(n_requests=30),
        chaos.run_silent_fallback_scenario(n_requests=60, fail_at=15),
        chaos.run_denial_of_wallet_scenario(n_heavy_docs=20),
        chaos.run_runaway_agent_loop_scenario()
    ]
    print_anomaly_table(results)

    # 3. Export HTML dashboard
    if args.export_html or args.mode in ["benchmark", "all"]:
        html_file = BASE_DIR / "bankai_finops_dashboard.html"
        path = generate_html_dashboard(metrics, results, output_path=str(html_file))
        print(f"\n[✓] Tableau de bord interactif HTML généré : {path}")

    # 4. Export Portfolio Markdown
    if args.export_portfolio or args.mode in ["benchmark", "all"]:
        portfolio_file = BASE_DIR / "PORTFOLIO_CASE_STUDY.md"
        path = generate_portfolio_case_study(metrics, results, output_path=str(portfolio_file))
        print(f"[✓] Étude de cas portfolio générée : {path}")

    print_portfolio_instructions()

if __name__ == "__main__":
    main()
