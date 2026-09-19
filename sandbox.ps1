# ==========================================================
#   APEX BANK — AI FINOPS SANDBOX AUTOMATION SCRIPT (PS1)
# ==========================================================

param (
    [Parameter(Position=0)]
    [ValidateSet("run", "test", "html", "portfolio", "help")]
    [string]$Action = "run"
)

switch ($Action) {
    "run" {
        Write-Host "`n[*] Execution complete du Sandbox AI FinOps..." -ForegroundColor Cyan
        python run_sandbox.py --mode all
    }
    "test" {
        Write-Host "`n[*] Lancement de la suite de tests Pytest du Sandbox..." -ForegroundColor Cyan
        pytest tests/test_sandbox_scenarios.py -v
    }
    "html" {
        Write-Host "`n[*] Ouverture du Tableau de Bord HTML dans le navigateur..." -ForegroundColor Green
        if (Test-Path "bankai_finops_dashboard.html") {
            Start-Process "bankai_finops_dashboard.html"
        } else {
            Write-Host "[!] Generation prealable du tableau de bord..." -ForegroundColor Yellow
            python run_sandbox.py --mode all
            Start-Process "bankai_finops_dashboard.html"
        }
    }
    "portfolio" {
        Write-Host "`n[*] Generation de l'etude de cas pour Portfolio GitHub..." -ForegroundColor Cyan
        python run_sandbox.py --export-portfolio
        Write-Host "[OK] Fichier PORTFOLIO_CASE_STUDY.md mis a jour." -ForegroundColor Green
    }
    "help" {
        Write-Host "==============================================================" -ForegroundColor Yellow
        Write-Host "  COMMANDES DU SANDBOX AI FINOPS (APEX BANK LAB)" -ForegroundColor Yellow
        Write-Host "==============================================================" -ForegroundColor Yellow
        Write-Host "  .\sandbox.ps1 run        : Execute la simulation et les 4 pannes"
        Write-Host "  .\sandbox.ps1 test       : Lance les tests de validation Pytest"
        Write-Host "  .\sandbox.ps1 html       : Ouvre le tableau de bord HTML interactif"
        Write-Host "  .\sandbox.ps1 portfolio  : Met a jour l'etude de cas Markdown"
        Write-Host "==============================================================" -ForegroundColor Yellow
    }
}
