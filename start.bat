@echo off
echo Battery Monitor - Demarrage
echo ============================

REM Verifier si Python est installe
py --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installe ou non accessible via 'py'
    echo Veuillez installer Python depuis https://python.org
    pause
    exit /b 1
)

REM Installer les dependances si necessaire
echo Installation des dependances...
py -m pip install -r requirements.txt

REM Demarrer l'application
echo Demarrage de Battery Monitor...
echo Appuyez sur Ctrl+C pour arreter
echo.
py main.py

pause
