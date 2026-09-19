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
    print(" Framework de Recette Financière & Résilience IA pour AI Test Architect ")
    print("=" * 72)

def print_live_metrics_card(metrics: Dict[str, Any]):
    print("\n" + "-" * 72)
    print(" 📊 TABLEAU DE BORD TÉLÉMÉTRIQUE EN DIRECT (REAL-TIME METRICS) ")
    print("-" * 72)
    print(f"  • Requêtes traitées        : {metrics.get('total_requests', 0):,}")
    print(f"  • Volume de Tokens         : {metrics.get('total_tokens', 0):,} tokens")
    print(f"  • Tokens en Cache Préfixe  : {metrics.get('total_cached_tokens', 0):,} tokens")
    print(f"  • Taux d'utilisation Cache : {metrics.get('global_cache_hit_ratio', 0.0):.2f} %")
    print(f"  • Dépense Cumulée          : {metrics.get('total_cost_eur', 0.0):.4f} €")
    print(f"  • Coût Moyen par Requête   : {metrics.get('avg_cost_per_request_eur', 0.0):.6f} €")
    print(f"  • Coût pour 1,000 Requêtes : {metrics.get('cost_per_1k_requests_eur', 0.0):.4f} €")
    print("-" * 72)

def print_anomaly_table(results: List[AnomalyResult]):
    print("\n" + "=" * 72)
    print(" 🛡️  RÉSULTATS DES SCÉNARIOS DE CHAOS & D'ANOMALIES FINANCIÈRES ")
    print("=" * 72)
    print(f"{'Scénario de Chaos':<32} | {'Sans Garde':<10} | {'Avec Garde':<10} | {'Économie (€)':<12} | {'Gain %'}")
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
    print(f"{'TOTAL CONSOLIDÉ':<32} | {total_unprot:>8.4f} € | {total_prot:>8.4f} € | {total_savings:>10.4f} € | {total_pct:>5.1f} %")
    print("=" * 72)

    print("\n💡 SYNTHÈSE DE LA VALEUR APPORTÉE PAR L'AI TEST ARCHITECT :")
    for r in results:
        print(f"  [✓] {r.name} :")
        print(f"      Action QA : {r.remediation_action}")
        print(f"      Impact   : {r.savings_eur:.4f} € économisés immédiatement sur ce run.\n")

def print_portfolio_instructions():
    print("=" * 72)
    print(" 🚀 COMMENT VALORISER CE PROJET DANS VOTRE PORTFOLIO & CV ")
    print("=" * 72)
    print("""
1. GitHub Repository :
   Publiez ce dossier sous le nom `bankai-finops-sandbox`.
   Le fichier `PORTFOLIO_CASE_STUDY.md` généré est prêt à l'emploi.

2. Sur votre Profil LinkedIn & CV :
   Titre : AI Test Architect / AI FinOps Lead
   Projet phare : "Apex Bank AI FinOps Lab — Framework de contrôle de dérive
   budgétaire et résilience financière des systèmes LLM bancaires régulés."

3. En Entretien d'Embauche :
   Présentez les 4 anomalies de chaos et comment vos tests automatisés ont évité
   une dérive de 70% à 95% des coûts par rapport à une implémentation naïve.
""")
    print("=" * 72)
