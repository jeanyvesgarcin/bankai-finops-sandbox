"""
Interactive Console Dashboard for AI FinOps Sandbox.
Provides terminal visualization with metrics tables, financial health badges,
and ROI calculations of QA FinOps interventions.
"""

import sys
import time
from typing import List, Dict, Any
from ..chaos.chaos_injector import AnomalyResult

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

def print_banner():
    print("=" * 72)
    print(" 🏛️  APEX BANK — AI FINOPS OPERATIONAL SANDBOX & LAB ")
    print(" Continuous Financial Testing & Resilience Framework for AI QA Architects ")
    print("=" * 72)

def print_live_metrics_card(metrics: Dict[str, Any]):
    print("\n" + "-" * 72)
    print(" 📊 REAL-TIME TELEMETRY DASHBOARD ")
    print("-" * 72)
    print(f"  • Requests Processed      : {metrics.get('total_requests', 0):,}")
    print(f"  • Total Token Volume      : {metrics.get('total_tokens', 0):,} tokens")
    print(f"  • Prefix Cached Tokens    : {metrics.get('total_cached_tokens', 0):,} tokens")
    print(f"  • Cache Utilization Ratio : {metrics.get('global_cache_hit_ratio', 0.0):.2f} %")
    print(f"  • Cumulative Expenditure  : {metrics.get('total_cost_eur', 0.0):.4f} €")
    print(f"  • Average Cost per Req    : {metrics.get('avg_cost_per_request_eur', 0.0):.6f} €")
    print(f"  • Cost per 1,000 Requests : {metrics.get('cost_per_1k_requests_eur', 0.0):.4f} €")
    print("-" * 72)

def print_anomaly_table(results: List[AnomalyResult]):
    print("\n" + "=" * 72)
    print(" 🛡️  FINANCIAL CHAOS SCENARIOS & ANOMALY INJECTION RESULTS ")
    print("=" * 72)
    print(f"{'Chaos Scenario':<32} | {'Baseline':<10} | {'QA Guard':<10} | {'Savings (€)':<12} | {'Gain %'}")
    print("-" * 72)

    total_unprot = 0.0
    total_prot = 0.0

    for r in results:
        total_unprot += r.unprotected_cost_eur
        total_prot += r.protected_cost_eur
        print(f"{r.name[:32]:<32} | {r.unprotected_cost_eur:>8.4f} € | {r.protected_cost_eur:>8.4f} € | {r.savings_eur:>10.4f} € | {r.savings_percent:>5.1f} %")

    total_savings = total_unprot - total_prot
    total_pct = (total_savings / max(0.0001, total_unprot)) * 100.0

    print("-" * 72)
    print(f"{'CONSOLIDATED TOTAL':<32} | {total_unprot:>8.4f} € | {total_prot:>8.4f} € | {total_savings:>10.4f} € | {total_pct:>5.1f} %")
    print("=" * 72)

    print("\n💡 AI TEST ARCHITECT VALUE SUMMARY :")
    for r in results:
        print(f"  [✓] {r.name} :")
        print(f"      QA Remediation : {r.remediation_action}")
        print(f"      Financial ROI  : {r.savings_eur:.4f} € saved immediately on this run.\n")

def print_portfolio_instructions():
    print("=" * 72)
    print(" 🚀 HOW TO SHOWCASE THIS LAB IN YOUR PORTFOLIO & INTERVIEWS ")
    print("=" * 72)
    print("""
1. GitHub Repository:
   Published at: https://github.com/jeanyvesgarcin/bankai-finops-sandbox
   The generated `PORTFOLIO_CASE_STUDY.md` is ready to be showcased.

2. On your LinkedIn & Resume:
   Title: AI Test Architect / AI FinOps Lead
   Featured Project: "Apex Bank AI FinOps Lab — Continuous Financial Testing
   Framework & Resilience Guardrails for Regulated Banking LLMs."

3. In Technical Job Interviews:
   Present the 4 chaos scenarios and demonstrate how your automated tests
   prevented a 70% to 95% budget overrun compared to a naive deployment.
""")
    print("=" * 72)
