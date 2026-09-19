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
        Write-Host "`n[*] Executing full BankAI FinOps Sandbox simulation..." -ForegroundColor Cyan
        python run_sandbox.py --mode all
    }
    "test" {
        Write-Host "`n[*] Running automated Pytest validation test suite..." -ForegroundColor Cyan
        pytest tests/test_sandbox_scenarios.py -v
    }
    "html" {
        Write-Host "`n[*] Opening Interactive HTML5 Dashboard in default browser..." -ForegroundColor Green
        if (Test-Path "bankai_finops_dashboard.html") {
            Start-Process "bankai_finops_dashboard.html"
        } else {
            Write-Host "[!] Compiling dashboard before opening..." -ForegroundColor Yellow
            python run_sandbox.py --mode all
            Start-Process "bankai_finops_dashboard.html"
        }
    }
    "portfolio" {
        Write-Host "`n[*] Generating GitHub Portfolio Case Study..." -ForegroundColor Cyan
        python run_sandbox.py --export-portfolio
        Write-Host "[OK] PORTFOLIO_CASE_STUDY.md successfully updated." -ForegroundColor Green
    }
    "help" {
        Write-Host "==============================================================" -ForegroundColor Yellow
        Write-Host "  APEX BANK AI FINOPS SANDBOX CLI COMMANDS" -ForegroundColor Yellow
        Write-Host "==============================================================" -ForegroundColor Yellow
        Write-Host "  .\sandbox.ps1 run        : Runs simulation, chaos scenarios & exports"
        Write-Host "  .\sandbox.ps1 test       : Runs automated Pytest suite"
        Write-Host "  .\sandbox.ps1 html       : Opens the interactive HTML5 Chart.js dashboard"
        Write-Host "  .\sandbox.ps1 portfolio  : Regenerates PORTFOLIO_CASE_STUDY.md"
        Write-Host "==============================================================" -ForegroundColor Yellow
    }
}
