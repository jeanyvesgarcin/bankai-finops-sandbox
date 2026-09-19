# 🏛️ Apex Bank — AI FinOps Operational Sandbox & Lab

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![BankAI FinOps Quality Gate](https://github.com/jeanyvesgarcin/bankai-finops-sandbox/actions/workflows/finops-quality-gate.yml/badge.svg)](https://github.com/jeanyvesgarcin/bankai-finops-sandbox/actions)
[![EU AI Act Compliance](https://img.shields.io/badge/EU%20AI%20Act-High%20Risk%20Annex%20III-purple.svg)](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
[![DORA Art. 28 Compliant](https://img.shields.io/badge/DORA-ICT%20Third--Party%20Risk-blue.svg)](https://eur-lex.europa.eu/eli/reg/2022/2554/oj)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Un bac à sable bancaire interactif (Sandbox & Lab) à coût zéro pour s'entraîner, tester et démontrer la maîtrise de l'AI FinOps, de la résilience financière et du contrôle des coûts LLM en environnement bancaire régulé.**

Ce projet fait office de **vitrine portfolio (Portfolio Showcase)** pour un poste d'**AI Test Architect**, de **QA Lead IA** ou de **FinOps Engineer** dans le secteur bancaire et financier.

📘 **Manuel PDF Inclus :** Consultez le guide complet de 6 pages [`Guide_Pratique_Sandbox_AI_FinOps_Portfolio.pdf`](file:///Guide_Pratique_Sandbox_AI_FinOps_Portfolio.pdf) pour la démarche pas-à-pas, le script de pitch d'entretien et la checklist d'entraînement.

---

## 🚀 Pourquoi ce Projet ? (Problem Statement)

Dans les banques tier-1, le déploiement de modèles d'IA générative (LLM, RAG, Vision KYC) soulève 3 risques critiques :
1. **L'inflation incontrôlée des coûts (Cost Drift)** : Des prompts mal configurés ou des contextes RAG sans fenêtre glissante multiplient les dépenses par 5x à 10x.
2. **Les attaques par Déni de Portefeuille (Denial of Wallet - DoW)** : L'injection de documents volumineux peut saturer les budgets en quelques minutes.
3. **Les pannes silencieuses de bascule Cloud** : Quand le GPU souverain local tombe et bascule sans disjoncteur vers des APIs publiques payantes à l'usage (**DORA Art. 28**).

Ce Sandbox fournit une **plateforme de simulation haute fidélité à coût 0€** (aucun compte ni clé API payante requise) pour simuler, auditer et résoudre ces pannes.

---

## 🏗️ Architecture du Sandbox

```
[Simulateur de Trafic Bancaire]
  ├── Octroi de Crédit Retail (High Volume)
  ├── Extraction Documentaire KYC (Variable Size)
  └── Copilote Banque Privée MIFID II (Multi-Turn Chat)
                     │
                     ▼
       ┌───────────────────────────┐
       │   QA Pre-Execution Gate   │  ◄── [Rejet Anti-DoW avant appel modèle]
       └─────────────┬─────────────┘
                     ▼
       ┌───────────────────────────┐
       │    Prefix Cache Engine    │  ◄── [Prompt Caching > 80% des tokens]
       └─────────────┬─────────────┘
                     ▼
       ┌───────────────────────────┐
       │   FallbackCircuitGuard    │  ◄── [Disjoncteur sur fenêtre glissante]
       └─────────────┬─────────────┘
                     ▼
       ┌───────────────────────────┐
       │  Visual Dashboard & Audit │  ◄── [HTML5 Chart.js + Rapport Portfolio]
       └───────────────────────────┘
```

---

## ⚡ Démarrage Express en 1 Minute

### 1. Cloner et Lancer le Sandbox

```powershell
# Depuis le dossier du sandbox :
.\sandbox.ps1 run
```
*Le script simule la charge bancaire nominale, injecte les 4 scénarios de chaos, affiche la matrice financière et génère automatiquement le tableau de bord HTML.*

### 2. Ouvrir le Tableau de Bord Visuel Interactif

```powershell
.\sandbox.ps1 html
```
*Ouvre directement [`bankai_finops_dashboard.html`](file:///bankai_finops_dashboard.html) dans votre navigateur avec les graphiques interactifs Chart.js.*

### 3. Lancer les Tests Automatisés (Pytest)

```powershell
.\sandbox.ps1 test
```
*Valide que l'ensemble des disjoncteurs financiers et plafonds NFR sont respectés (100% verts).*

---

## 🛡️ Les 4 Scénarios de Chaos Financier Embarqués

Le simulateur de chaos [`chaos/chaos_injector.py`](file:///chaos/chaos_injector.py) permet de tester et mesurer 4 défaillances réelles :

1. **Destruction du Cache (Cache-Busting)** :
   * *Panne* : Un développeur insère un UUID dynamique au début du prompt système.
   * *Impact sans garde* : Perte instantanée du cache préfixe, coût multiplié par 3.
   * *Protection QA* : Détection automatique de la chute du `cache_hit_ratio` et isolation des variables.
2. **Bascule Silencieuse Non Contrôlée (Silent Fallback)** :
   * *Panne* : Le cluster local vLLM crash et bascule vers GPT-4o Cloud sans alerte.
   * *Impact sans garde* : Dérive financière exponentielle.
   * *Protection QA* : `FallbackCircuitGuard` coupe la bascule après 10 requêtes et passe en mode dégradé.
3. **Bombardement Denial of Wallet (DoW)** :
   * *Panne* : Réception de bilans comptables de 50 pages (350 KB).
   * *Impact sans garde* : Saturation immédiate de l'API Vision/LLM.
   * *Protection QA* : Rejet pré-modèle à coût 0€ avant l'appel API.
4. **Boucle Folle d'Agent Autonome (Runaway Loop)** :
   * *Panne* : Recherche infinie de bénéficiaires effectifs (40 itérations).
   * *Protection QA* : Arrêt d'urgence au 5ème tour avec bascule humaine.

---

## 💼 Valorisation pour votre Portfolio & Recruteurs

Le fichier généré [`PORTFOLIO_CASE_STUDY.md`](file:///PORTFOLIO_CASE_STUDY.md) est une étude de cas complète prête à présenter en entretien d'embauche ou à épingler sur votre profil GitHub.

### Structure des Fichiers

```
bankai_finops_sandbox/
├── engine/
│   ├── banking_llm_mock.py      # Simulateur LLM bancaire (tokens, cache, coûts à 6 décimales)
│   └── workloads.py             # 3 cas d'usage bancaires (Crédit, KYC, Copilote Patrimoine)
├── chaos/
│   └── chaos_injector.py        # Moteur d'injection des 4 anomalies financières
├── dashboard/
│   ├── interactive_console.py   # Tableau de bord télémétrique en console
│   └── export_html_dashboard.py # Générateur du dashboard HTML5 interactif (Chart.js)
├── reports/
│   └── portfolio_generator.py   # Générateur de l'étude de cas PORTFOLIO_CASE_STUDY.md
├── tests/
│   └── test_sandbox_scenarios.py # Suite de validation automatisée Pytest
├── run_sandbox.py               # Orchestrateur CLI principal
├── sandbox.ps1                  # Script de commande express PowerShell
├── PORTFOLIO_CASE_STUDY.md      # Étude de cas portfolio générée
├── bankai_finops_dashboard.html # Tableau de bord visuel interactif
└── README.md                    # Ce guide
```
