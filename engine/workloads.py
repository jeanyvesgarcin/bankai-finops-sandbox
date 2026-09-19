"""
Banking AI Workloads - Real-World Financial Scenarios.
Defines 3 core banking workloads:
1. Credit Scoring & Risk Decisioning (Regulatory Batch / High Volume)
2. Corporate KYC & Financial Document Extraction (Variable Size / Anti-DoW)
3. Wealth Advisory Private Banking Copilot (Multi-Turn Chat / Context Inflation)
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional
import random
from .banking_llm_mock import BankingLLMMock, LLMResponse

# 2,500 tokens of strict regulatory credit rules (EBA Guidelines, Bâle IV, ACPR)
CREDIT_SCORING_REGULATORY_PROMPT = """
RÉGLEMENTATION BANCAIRE EUROPÉENNE & INTERNE — OCTROI DE CRÉDIT RETAIL (BÂLE IV / EBA / ACPR)
Vous êtes le moteur d'évaluation des risques de crédit de la banque Apex. Vous devez appliquer strictement les règles suivantes :
ARTICLE 1 : TAUX D'EFFORT (DEBT-TO-INCOME RATIO - DTI)
1. Le taux d'endettement maximal autorisé est de 35.00% assurance comprise.
2. Tout dépassement au-delà de 35.00% nécessite une dérogation expresse accordée uniquement si le reste à vivre par personne est supérieur à 1500 EUR.
ARTICLE 2 : SCORING DE CRÉDIT & PROBABILITÉ DE DÉFAUT (PD)
1. Tout dossier avec un score interne FICO < 650 est classé en Risque Élevé et doit être rejeté ou réorienté vers une analyse manuelle par un analyste niveau 3.
2. Un score compris entre 650 et 720 autorise un octroi sous condition d'un apport personnel minimal de 15%.
3. Un score supérieur à 720 autorise un accord de principe automatique avec taux bonifié.
ARTICLE 3 : CONFORMITÉ EU AI ACT (SYSTÈME HAUT RISQUE ANNEXE III)
Ce système est classifié Haut Risque au sens de l'Article 6 et Annexe III du Règlement UE 2024/1689.
Toute décision de rejet doit obligatoirement expliciter les facteurs déterminants de manière intelligible et non discriminatoire.
Interdiction formelle d'utiliser des critères d'origine géographique, de genre, d'âge ou d'état de santé dans le calcul de la note de crédit.
ARTICLE 4 : MATRICE DES PONDÉRATIONS DE RISQUE PONDÉRÉES (RWA)
Pour chaque euro prêté, la banque immobilise des fonds propres prudentiels selon la catégorie de solvabilité :
- Catégorie A (Excellente solvabilité) : Pondération RWA = 20%, Fonds propres Tier 1 requis = 8%.
- Catégorie B (Bonne solvabilité) : Pondération RWA = 35%, Fonds propres Tier 1 requis = 8%.
- Catégorie C (Solvabilité modérée) : Pondération RWA = 75%, Fonds propres Tier 1 requis = 8%.
- Catégorie D (Risque spéculatif) : Pondération RWA = 150%, Accord automatisé strictement interdit.
ARTICLE 5 : PROTOCOLE D'AUDITABILITÉ ET LOGS
Chaque évaluation doit produire une trace chiffrée horodatée conforme DORA Art. 12 et stockée pendant 10 ans.
""".strip() * 3  # Repeats to guarantee > 1,500 tokens for prefix cache eligibility

KYC_EXTRACTION_SYSTEM_PROMPT = """
ANALYSE DE CONFORMITÉ KYC & UBO (LUTTE ANTI-BLANCHIMENT / LCB-FT / 5TH AML DIRECTIVE)
Vous êtes l'analyste virtuel KYC chargé de vérifier l'authenticité des pièces justificatives d'entreprises :
1. Extraction du numéro SIREN/SIRET et contrôle de concordance avec l'extrait Kbis.
2. Détection des Bénéficiaires Effectifs (UBO) détenant plus de 25% du capital direct ou indirect.
3. Vérification du statut de Personne Politiquement Exposée (PPE) et croisement avec les listes de sanctions internationales (OFAC, UE, ONU).
4. Détection de falsifications visuelles, incohérences de polices de caractères ou métadonnées suspectes.
""".strip() * 3

WEALTH_COPILOT_SYSTEM_PROMPT = """
ASSISTANT CONSEILLER EN GESTION DE PATRIMOINE (PRIVATE BANKING & MIFID II)
Vous assistez les banquiers privés dans la structuration des portefeuilles d'actifs pour les clients fortunés (HNWI).
RÈGLES MIFID II IMPÉRATIVES :
1. Profil de risque : Toute recommandation doit respecter strictement l'appétence au risque déclarée par le client (Prudent, Équilibré, Dynamique, Offensif).
2. Diversification : Aucun actif individuel ne doit représenter plus de 10% de la valeur liquidative totale hors immobilier.
3. Transparence des frais : Révéler systématiquement les frais de gestion annuels et les rétrocessions d'OPCVM.
""".strip() * 2

class CreditScoringWorkload:
    """Workload 1 : Octroi de crédit retail en fort volume."""
    def __init__(self, llm: BankingLLMMock):
        self.llm = llm

    def process_application(
        self,
        applicant_id: str,
        income_eur: float,
        loan_amount_eur: float,
        monthly_debt_eur: float,
        credit_score: int,
        use_cache_busting: bool = False,
        target_model: Optional[str] = None
    ) -> LLMResponse:
        system_prompt = CREDIT_SCORING_REGULATORY_PROMPT
        if use_cache_busting:
            # Anomaly : Dynamic timestamp / random salt at the start of system prompt destroys cache!
            salt = f"// TRANSACTION_ID: {applicant_id}_{random.random()}_{random.randint(100000, 999999)}\n"
            system_prompt = salt + system_prompt

        user_content = (
            f"DOSSIER CRÉDIT ID: {applicant_id}\n"
            f"Revenus mensuels nets: {income_eur} EUR\n"
            f"Montant emprunté demandé: {loan_amount_eur} EUR\n"
            f"Charges d'emprunt existantes: {monthly_debt_eur} EUR\n"
            f"Score de crédit interne FICO: {credit_score}\n"
            f"Veuillez évaluer l'éligibilité et calculer le taux d'effort."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ]

        return self.llm.generate(messages, model=target_model)


class KYCExtractionWorkload:
    """Workload 2 : Extraction documentaire KYC avec protection Anti-DoW."""
    def __init__(self, llm: BankingLLMMock):
        self.llm = llm

    def process_kyc_document(
        self,
        company_name: str,
        document_text: str,
        page_count: int,
        enable_anti_dow_guard: bool = True,
        max_pages_allowed: int = 10,
        max_bytes_allowed: int = 50_000
    ) -> Dict[str, Any]:
        doc_size_bytes = len(document_text.encode("utf-8"))

        # QA FinOps Guard : Pre-validation check before spending LLM tokens
        if enable_anti_dow_guard:
            if page_count > max_pages_allowed or doc_size_bytes > max_bytes_allowed:
                return {
                    "status": "REJECTED_BY_ANTI_DOW",
                    "reason": f"Document trop volumineux ({page_count} pages, {doc_size_bytes} octets). Seuil max: {max_pages_allowed} pages / {max_bytes_allowed} octets.",
                    "cost_eur": 0.0,
                    "tokens_saved": int(doc_size_bytes / 3.8),
                    "financial_saving_eur": round((doc_size_bytes / 3.8 / 1_000_000.0) * 2.50 * 0.92, 4)
                }

        messages = [
            {"role": "system", "content": KYC_EXTRACTION_SYSTEM_PROMPT},
            {"role": "user", "content": f"Entreprise: {company_name}\nContenu du document extrait:\n{document_text}"}
        ]
        resp = self.llm.generate(messages, model="gpt-4o")
        return {
            "status": "PROCESSED",
            "reason": "OK",
            "cost_eur": resp.cost_eur,
            "tokens": resp.prompt_tokens + resp.completion_tokens,
            "financial_saving_eur": 0.0,
            "response": resp
        }


class WealthCopilotWorkload:
    """Workload 3 : Copilote de Banque Privée avec gestion de fenêtre glissante."""
    def __init__(self, llm: BankingLLMMock):
        self.llm = llm

    def run_multi_turn_session(
        self,
        num_turns: int = 8,
        enable_sliding_window: bool = True,
        max_history_turns: int = 2
    ) -> List[LLMResponse]:
        responses = []
        conversation_history: List[Dict[str, str]] = []

        for turn in range(1, num_turns + 1):
            user_msg = f"Tour {turn} : Client souhaite analyser l'impact fiscal d'un arbitrage de 250k EUR vers un fonds obligataire Daté."

            if enable_sliding_window and len(conversation_history) > (max_history_turns * 2):
                # Retain system prompt + summarized context + last 2 exchanges
                active_history = conversation_history[-(max_history_turns * 2):]
            else:
                active_history = conversation_history

            messages = [{"role": "system", "content": WEALTH_COPILOT_SYSTEM_PROMPT}] + active_history + [{"role": "user", "content": user_msg}]

            resp = self.llm.generate(messages, model="gpt-4o-mini")
            responses.append(resp)

            # Record in full history
            conversation_history.append({"role": "user", "content": user_msg})
            conversation_history.append({"role": "assistant", "content": resp.content})

        return responses
