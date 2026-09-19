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

# 2,500 tokens of strict regulatory credit rules (EBA Guidelines, Basel IV, ACPR)
CREDIT_SCORING_REGULATORY_PROMPT = """
EUROPEAN & INTERNAL BANKING REGULATION — RETAIL CREDIT DECISIONING (BASEL IV / EBA / ACPR)
You are the credit risk underwriting engine of Apex Bank. You must strictly enforce the following rules:
ARTICLE 1: DEBT-TO-INCOME RATIO (DTI) LIMITS
1. The maximum allowable debt-to-income ratio is 35.00% including loan insurance.
2. Any exception beyond 35.00% requires express executive sign-off and is granted only if disposable residual income per person exceeds 1,500 EUR/month.
ARTICLE 2: CREDIT SCORING & PROBABILITY OF DEFAULT (PD)
1. Any applicant file with an internal FICO/credit score < 650 is classified as High Risk and must be automatically rejected or routed to manual Tier-3 credit analysis.
2. A score between 650 and 720 allows conditional approval subject to a minimum personal cash down payment of 15%.
3. A score above 720 qualifies for automatic pre-approval with preferential interest rates.
ARTICLE 3: EU ARTIFICIAL INTELLIGENCE ACT COMPLIANCE (ANNEX III HIGH-RISK SYSTEM)
This credit decisioning system is classified as High Risk pursuant to Article 6 and Annex III of Regulation (EU) 2024/1689.
Any adverse or rejection decision must explicitly state the determining factors in an intelligible and non-discriminatory manner.
It is strictly prohibited to utilize geographical origin, gender, age, or health data in calculating creditworthiness scores.
ARTICLE 4: RISK-WEIGHTED ASSETS (RWA) CAPITAL BUFFER MATRIX
For every euro lent, the bank provisions regulatory Tier-1 prudential capital according to solvency categories:
- Solvency Category A (Prime): Risk weight = 20%, Minimum Tier-1 capital requirement = 8.0%.
- Solvency Category B (Upper Medium): Risk weight = 35%, Minimum Tier-1 capital requirement = 8.0%.
- Solvency Category C (Lower Medium): Risk weight = 75%, Minimum Tier-1 capital requirement = 8.0%.
- Solvency Category D (Subprime): Risk weight = 150%, Automated approval strictly prohibited.
ARTICLE 5: AUDIT TRAIL AND LOG INTEGRITY PROTOCOL
Every automated underwriting assessment must produce an immutable, timestamped audit record compliant with DORA Art. 12 and retained for 10 years.
""".strip() * 3  # Repeats to guarantee > 1,500 tokens for prefix cache eligibility

KYC_EXTRACTION_SYSTEM_PROMPT = """
CORPORATE KYC & UBO COMPLIANCE ENGINE (5TH EU AML DIRECTIVE / FATF STANDARDS)
You are the automated compliance analyst verifying legal corporate entity documentation:
1. Legal Entity Identifier (LEI/SIREN) verification and concordance cross-check with Certificate of Incorporation.
2. Identification of Ultimate Beneficial Owners (UBO) holding directly or indirectly over 25.0% of share capital or voting rights.
3. Screening against Politically Exposed Persons (PEP) registries and international sanctions lists (OFAC, EU, UN).
4. Anomaly detection for forged documents, font inconsistencies, and suspicious digital metadata manipulation.
""".strip() * 3

WEALTH_COPILOT_SYSTEM_PROMPT = """
PRIVATE BANKING WEALTH ADVISORY COPILOT (MIFID II COMPLIANT)
You assist private wealth managers in structuring asset portfolios for High Net Worth Individuals (HNWI).
MANDATORY MIFID II CONDUCT OF BUSINESS RULES:
1. Suitability & Risk Profile: All asset allocation recommendations must strictly adhere to the client's declared risk profile (Conservative, Balanced, Dynamic, Aggressive).
2. Diversification Limits: No single non-sovereign asset or issuer may represent more than 10.0% of total portfolio net asset value (NAV).
3. Fee Transparency: Systematically disclose ongoing fund expense ratios, performance fees, and distribution retrocessions.
""".strip() * 2

class CreditScoringWorkload:
    """Workload 1 : High-volume retail credit underwriting."""
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
            # Anomaly: Dynamic timestamp or random UUID prepended to system prompt destroys prefix cache!
            salt = f"// TRANSACTION_ID: {applicant_id}_{random.random()}_{random.randint(100000, 999999)}\n"
            system_prompt = salt + system_prompt

        user_content = (
            f"CREDIT APPLICATION ID: {applicant_id}\n"
            f"Net Monthly Income: {income_eur} EUR\n"
            f"Requested Loan Principal: {loan_amount_eur} EUR\n"
            f"Existing Monthly Debt Obligations: {monthly_debt_eur} EUR\n"
            f"Internal FICO Credit Score: {credit_score}\n"
            f"Please assess applicant eligibility and compute debt-to-income ratio."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ]

        return self.llm.generate(messages, model=target_model)


class KYCExtractionWorkload:
    """Workload 2 : Corporate KYC document extraction with Anti-DoW pre-validation guard."""
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

        # QA FinOps Guard : Pre-validation check before spending expensive LLM tokens
        if enable_anti_dow_guard:
            if page_count > max_pages_allowed or doc_size_bytes > max_bytes_allowed:
                return {
                    "status": "REJECTED_BY_ANTI_DOW",
                    "reason": f"Document too large ({page_count} pages, {doc_size_bytes} bytes). Allowed threshold: {max_pages_allowed} pages / {max_bytes_allowed} bytes.",
                    "cost_eur": 0.0,
                    "tokens_saved": int(doc_size_bytes / 3.8),
                    "financial_saving_eur": round((doc_size_bytes / 3.8 / 1_000_000.0) * 2.50 * 0.92, 4)
                }

        messages = [
            {"role": "system", "content": KYC_EXTRACTION_SYSTEM_PROMPT},
            {"role": "user", "content": f"Entity: {company_name}\nExtracted Document Content:\n{document_text}"}
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
    """Workload 3 : Private Banking Wealth Copilot with sliding context window."""
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
            user_msg = f"Turn {turn}: Client requests portfolio rebalancing analysis of 250k EUR into Target-Maturity Bond Funds."

            if enable_sliding_window and len(conversation_history) > (max_history_turns * 2):
                # Retain system prompt + summarized context + last 2 turns
                active_history = conversation_history[-(max_history_turns * 2):]
            else:
                active_history = conversation_history

            messages = [{"role": "system", "content": WEALTH_COPILOT_SYSTEM_PROMPT}] + active_history + [{"role": "user", "content": user_msg}]

            resp = self.llm.generate(messages, model="gpt-4o-mini")
            responses.append(resp)

            # Record in conversation log
            conversation_history.append({"role": "user", "content": user_msg})
            conversation_history.append({"role": "assistant", "content": resp.content})

        return responses
