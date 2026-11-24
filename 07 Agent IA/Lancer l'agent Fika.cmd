@echo off
chcp 65001 >nul
title Fika - l'agent de recherche IKEASTRE
cd /d "%~dp0agent"
echo.
echo   FIKA  -  l'agent de recherche IKEASTRE
echo   Mission ^> Planifier ^> Agir ^> Observer ^> Verifier ^> Tableau source et date
echo.
echo   1  Verifier nos hypotheses (questions de l'atelier)
echo   2  Veille concurrentielle Gen Z (6 enseignes x 6 criteres)
echo   3  Les deux a la suite
echo.
set /p choix="  Ton choix (1, 2 ou 3) : "
if "%choix%"=="1" python lancer.py 1
if "%choix%"=="2" python lancer.py 2
if "%choix%"=="3" python lancer.py 12
echo.
echo   Les tableaux sont dans le dossier livrables.
start "" "%~dp0livrables"
pause
