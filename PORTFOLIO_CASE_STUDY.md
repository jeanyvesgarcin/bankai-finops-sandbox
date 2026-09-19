# 🏛️ Portfolio Showcase: Apex Bank AI FinOps & Resilience Framework
> **Author**: Jean-Yves GARCIN  
> **Role**: AI Test Architect & AI FinOps Lead  
> **Domain**: Tier-1 Banking, Regulated High-Risk AI Systems (**EU AI Act Annex III**, **DORA Art. 28**, **Basel IV**)  
> **Tech Stack**: Python 3.12, Pytest, Visual Studio Code, PromQL, vLLM (Llama-3-70B), OpenAI/Anthropic APIs, GitHub Actions  
> **Audit Score**: **100/100 (Grade A - Change Advisory Board Approved)**  
> **Repository**: [https://github.com/jeanyvesgarcin/bankai-finops-sandbox](https://github.com/jeanyvesgarcin/bankai-finops-sandbox)

---

## 📌 Executive Summary

As enterprise banks accelerate the deployment of Generative AI and Large Language Models (LLMs) across retail underwriting, corporate onboarding, and wealth management, delivery squads face critical financial and operational hazards: **uncontrolled token cost drift**, **Denial of Wallet (DoW) attacks**, and **unmonitored silent failovers to public cloud providers**.

As an **AI Test Architect**, I designed and implemented this comprehensive **Continuous AI FinOps Testing Framework** and **Day-0-to-Day-2 Governance Sandbox**, delivering:
1. **Hard caps on unit cost per transaction (CPIT)** to **< 0.0005 €** across retail credit decisioning.
2. **Over 75% inference budget savings** through automated prompt caching regression gates.
3. **100% mitigation of Denial of Wallet attacks** prior to expensive model invocation.
4. **Guaranteed regulatory compliance** with **DORA Art. 28** (ICT third-party concentration risk) and the **EU AI Act** (Annex III High-Risk Systems).

---

## 🎯 Technical Architecture & Control Gates

```
[Banking Workloads: Retail Credit, Corporate KYC, Wealth Copilot]
                               │
                               ▼
                 ┌───────────────────────────┐
                 │   QA Pre-Execution Gate   │  ◄── [Anti-DoW: Rejects oversized files at 0€ cost]
                 └─────────────┬─────────────┘
                               ▼
                 ┌───────────────────────────┐
                 │    Prefix Cache Engine    │  ◄── [Prompt Caching: > 80% tokens served at discount]
                 └─────────────┬─────────────┘
                               ▼
                 ┌───────────────────────────┐
                 │    Hybrid Model Router    │  ◄── [Sovereign on-prem vLLM vs Public Cloud API]
                 └─────────────┬─────────────┘
                               ▼
                 ┌───────────────────────────┐
                 │   FallbackCircuitGuard    │  ◄── [Sliding window breaker tripping on cost leakage]
                 └─────────────┬─────────────┘
                               ▼
                  [Production Banking Delivery]
```

---

## 🛡️ The 4 Financial Chaos & Anomaly Scenarios Resolved

| Production Risk Scenario | Unprotected Business Hazard | QA Guardrail Implemented | Benchmark Net Savings |
| :--- | :--- | :--- | :---: |
| **1. Prompt Cache Destruction (Cache-Busting)** | A developer prepended a dynamic timestamp/UUID to the system prompt, resetting prefix caching to 0% and tripling API bills. | Automated Pytest assertion on `cache_hit_ratio` and static prompt linting isolating dynamic inputs at the payload tail. | **+0.0584 € (34.5%)** |
| **2. Silent Cloud Fallback Spill** | On-prem sovereign vLLM GPU cluster crashed (OOM); traffic silently routed to OpenAI GPT-4o with no alerts or budget caps. | Sliding window `FallbackCircuitGuard` tripping after 10 requests and failing over to zero-cost deterministic rule engines. | **+0.1270 € (73.4%)** |
| **3. Denial of Wallet (DoW) Attack** | Hostile submission of 50-page financial statements (350 KB) aimed at exhausting monthly enterprise token quotas. | Pre-execution validation filter inspecting byte sizes and page counts, rejecting malicious payloads at zero token cost. | **+4.4488 € (100.0%)** |
| **4. Runaway Autonomous Agent Loop** | Multi-agent compliance investigation trapped in circular corporate hierarchy queries (40 iterations). | `MaxStepBudgetGuard` enforcing a hard cutoff at step 5 with automatic escalation to human compliance officers. | **+0.0429 € (87.5%)** |

**Consolidated Benchmark Metrics:**
* **Unprotected Baseline Cost:** `4.8402 €`
* **QA Protected Framework Cost:** `0.1631 €`
* **Immediate Net Savings:** `4.6771 € (96.6% efficiency gain)`

---

## 📊 Day 0 Sizing Engine: CapEx On-Prem GPU vs OpEx Public Cloud

For an enterprise retail workload of **500,000 credit applications / month**, our sizing model established the following financial arbitrage:

* **Public Cloud Pay-As-You-Go (GPT-4o)**:
  * Monthly inference expenditure: **1,462.50 € / month**
  * Inherent data privacy exposure and third-party vendor lock-in (**DORA Art. 28**).
* **On-Premise Sovereign Cluster (4x Nvidia A100 - Llama-3-70B 4-bit)**:
  * Required VRAM: **38.5 GB** (model weights) + **12.8 GB** (KV Cache for 64 concurrent streams) = **51.3 GB**.
  * Amortized monthly server hosting & power: **1,800.00 € / month**.
  * **Break-Even Inflexion Point:** Cost-effective starting at **615,000 transactions / month**.
* **QA Recommendation Submitted to Change Advisory Board (CAB):** Deploy on-prem sovereign vLLM as primary engine with quota-restricted public cloud fallback protected by `FallbackCircuitGuard`.

---

## 📜 Regulatory Compliance & CI/CD Quality Gates

The GitHub Actions CI/CD pipeline enforces 3 blocking Quality Gates:
1. `CPIT_LIMIT`: Unit cost per transaction must not exceed **0.0005 €**.
2. `CACHE_HIT_FLOOR`: Prompt caching ratio must remain above **80.0%**.
3. `AUDIT_SCANNER_SCORE`: Static and dynamic audit scanner must achieve a minimum score of **90/100**.

Current Framework Audit Score: **100.0 / 100 (Grade A - Outstanding)**.

---

## 🎙️ Technical Interview Pitch (STAR Methodology)

> *“In my work at Apex Bank, I architected the AI FinOps framework to ensure our LLM systems were both mathematically profitable and resilient against production failures. My scope extended far beyond traditional functional QA: I modeled unit cost per transaction down to fractions of a cent, engineered circuit breakers to prevent runaway cloud bills when local GPU clusters degrade, and implemented pre-execution filters blocking Denial of Wallet attacks. This framework achieved a 96.5% cost reduction under crisis conditions while ensuring strict DORA and EU AI Act compliance prior to CAB production sign-off.”*
