@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo === Synchro du projet IKEA ===
echo.
echo 1/3 Recuperation du travail des autres...
git pull --rebase --autostash
if errorlevel 1 (
  echo.
  echo Conflit ou erreur pendant la recuperation. Demande a ton Claude de regler ca, sans rien ecraser.
  pause
  exit /b 1
)
echo.
echo 2/3 Enregistrement de tes modifs...
git add -A
git diff --cached --quiet
if errorlevel 1 (
  git commit -m "Maj de %USERNAME% le %DATE% %TIME:~0,5%"
) else (
  echo Rien de nouveau de ton cote.
)
echo.
echo 3/3 Envoi...
git push
echo.
echo C'est a jour.
pause
