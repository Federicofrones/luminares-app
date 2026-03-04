@echo off
title Cinematic Storyteller AI - TTS Server
cd /d "d:\Luminares app\long-tts-app"
echo.
echo ============================================
echo   Cinematic Storyteller AI - TTS Server
echo ============================================
echo.
echo Iniciando servidor...
echo.

REM Espera 2 segundos y abre el navegador
start "" cmd /c "timeout /t 2 /nobreak >nul & start http://localhost:3000"

REM Inicia el servidor (mantiene la ventana abierta)
node server.js

echo.
echo El servidor se detuvo.
pause