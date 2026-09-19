# 🏛️ Apex Bank — AI FinOps Operational Sandbox & Lab

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![BankAI FinOps Quality Gate](https://img.shields.io/badge/FinOps%20Gate-100%25%20Passed-brightgreen.svg)]()
[![EU AI Act Compliance](https://img.shields.io/badge/EU%20AI%20Act-High%20Risk%20Annex%20III-purple.svg)](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
[![DORA Art. 28 Compliant](https://img.shields.io/badge/DORA-ICT%20Third--Party%20Risk-blue.svg)](https://eur-lex.europa.eu/eli/reg/2022/2554/oj)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **An interactive, zero-cost banking sandbox and laboratory to practice, test, and showcase mastery of AI FinOps, financial resilience, and LLM cost governance in regulated tier-1 financial institutions.**

This project serves as a **Portfolio Showcase** for an **AI Test Architect**, **AI QA Lead**, or **FinOps Engineer** targeting tier-1 banks and fintechs.

📘 **Included PDF Guide:** Check out the comprehensive 6-page guide [`BankAI_FinOps_Sandbox_Portfolio_Guide.pdf`](file:///BankAI_FinOps_Sandbox_Portfolio_Guide.pdf) for the step-by-step walkthrough, technical STAR interview pitch script, and training checklist.

---

## 🚀 Problem Statement

In tier-1 commercial and investment banks, deploying Generative AI systems (LLMs, RAG, Vision OCR) introduces 3 critical operational hazards:
1. **Uncontrolled Cost Drift**: Naive prompt assembly, accidental cache-busting, and unconstrained RAG conversation histories multiply token expenses by 5x to 10x.
2. **Denial of Wallet (DoW) Attacks**: Submission of bloated multi-page financial filings exhausts enterprise API budgets in minutes.
3. **Silent Public Cloud Failover Spills**: When sovereign on-premise GPU clusters experience Out-Of-Memory (OOM) failures and fail over to expensive external cloud APIs without budget breakers (**violating DORA Art. 28**).

This Sandbox delivers a **high-fidelity, zero-cost local simulation environment** (no paid cloud accounts or API keys required) to simulate, test, audit, and remediate these failures.

---

## 🏗️ Technical Architecture & Control Gates

```
[Simulated Banking Traffic Engine]
  ├── Retail Credit Decisioning (Basel IV High-Volume Batch)
  ├── Corporate KYC Document Extraction (5th AML Directive)
  └── Private Wealth Advisory Copilot (MiFID II Multi-Turn Chat)
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
                 ┌───────────────────────────┐
                 │  Visual Dashboard & Audit │  ◄── [HTML5 Chart.js + Portfolio Case Study]
                 └───────────────────────────┘
```

---

## ⚡ 1-Minute Quickstart

### 1. Run the Full Simulation & Chaos Suite

```powershell
# From the sandbox directory:
.\sandbox.ps1 run
```
*Executes nominal banking traffic, injects 4 chaos scenarios, prints live telemetry to the console, and generates the interactive HTML dashboard.*

### 2. Open the Interactive Visual Dashboard (Chart.js)

```powershell
.\sandbox.ps1 html
```
*Opens [`bankai_finops_dashboard.html`](file:///bankai_finops_dashboard.html) directly in your browser with real-time KPI cards and comparative financial charts.*

### 3. Run Automated Validation Tests (Pytest)

```powershell
.\sandbox.ps1 test
```
*Executes the 5 Pytest automated assertions validating NFR cost caps, cache retention, and circuit breakers (100% passed in < 0.20s).*

---

## 🛡️ The 4 Financial Chaos & Anomaly Scenarios

The chaos engine in [`chaos/chaos_injector.py`](file:///chaos/chaos_injector.py) allows you to demonstrate real financial savings:

| Chaos Scenario | Production Business Hazard | QA Guardrail Implemented | Net Savings Realized |
| :--- | :--- | :--- | :---: |
| **1. Cache Destruction (Cache-Busting)** | A developer prepends a dynamic timestamp/UUID to the prompt, dropping prefix cache to 0% and tripling API bills. | Automated Pytest assertions on `cache_hit_ratio` and static prompt linting in CI/CD. | **+34.4% Savings** |
| **2. Silent Cloud Fallback Spill** | On-prem sovereign vLLM GPU cluster crashes; traffic silently routes to GPT-4o Cloud with no budget caps. | Sliding window `FallbackCircuitGuard` tripping after 10 requests and failing over to zero-cost deterministic rule engines. | **+73.4% Savings** |
| **3. Denial of Wallet (DoW) Attack** | Submission of 50-page financial statements (350 KB) aimed at quota exhaustion. | Pre-execution validation filter inspecting byte sizes, rejecting malicious payloads at 0€ cost. | **+100.0% Savings (0€ spent)** |
| **4. Runaway Autonomous Agent Loop** | Multi-agent compliance search trapped in an infinite loop (40 recursive turns). | `MaxStepBudgetGuard` enforcing a hard cutoff at turn 5 with escalation to a human reviewer. | **+87.5% Savings** |

> **Consolidated Benchmark Results:**
> * Unprotected Baseline Cost: **4.56 €**
> * QA Guardrail Protected Cost: **0.16 €**
> * **Immediate Net Savings: +4.40 € (96.5% overall financial efficiency gain)**

---

## 💼 Interview & Career Showcase

The generated [`PORTFOLIO_CASE_STUDY.md`](file:///PORTFOLIO_CASE_STUDY.md) file is a recruiter-ready engineering report tailored for banking IT managers.

### Repository Structure

```
bankai_finops_sandbox/
├── engine/
│   ├── banking_llm_mock.py      # High-fidelity banking LLM mock (tokens, cache, latency, 6-decimal pricing)
│   └── workloads.py             # 3 banking workloads (Retail Credit, Corporate KYC, Wealth Copilot)
├── chaos/
│   └── chaos_injector.py        # 4 financial chaos and resilience failure modes
├── dashboard/
│   ├── interactive_console.py   # Terminal telemetry dashboard with metrics cards
│   └── export_html_dashboard.py # Standalone HTML5 Chart.js dashboard generator
├── reports/
│   └── portfolio_generator.py   # PORTFOLIO_CASE_STUDY.md generator
├── tests/
│   └── test_sandbox_scenarios.py # Automated Pytest test suite
├── run_sandbox.py               # Main CLI orchestrator
├── sandbox.ps1                  # PowerShell automation script
├── PORTFOLIO_CASE_STUDY.md      # Recruiter case study report
├── bankai_finops_dashboard.html # Interactive visual dashboard
├── BankAI_FinOps_Sandbox_Portfolio_Guide.pdf # 6-Page PDF Master Guide
└── README.md                    # This documentation
```

---

## 📜 Regulatory Standards Alignment

* **EU Artificial Intelligence Act (Regulation EU 2024/1689)**: Annex III High-Risk Credit Assessment compliance, technical documentation, and non-discrimination auditing.
* **Digital Operational Resilience Act (DORA - Regulation EU 2022/2554)**: Article 28 ICT third-party provider concentration risk management and automated exit/failover testing.
* **Basel IV / European Banking Authority (EBA)**: Debt-to-income caps and risk-weighted assets (RWA) provisioning logic.
