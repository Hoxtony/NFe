@echo off
setlocal enabledelayedexpansion

:: Caminho para o Python
set "PYTHON_DIR=C:\Users\AppData\Local\Programs\Python\Python313"
set "PYTHON_EXE=%PYTHON_DIR%\python.exe"
set "PYTHONW_EXE=%PYTHON_DIR%\pythonw.exe"
set "SCRIPT_PATH= CAMINHO PARA O PAINEL"

:: Verificar se o Python existe
if not exist "%PYTHON_EXE%" (
    echo 🚨 ERRO: Python não encontrado em "%PYTHON_EXE%"
    pause
    exit /b
)

:: Verificar se pip está disponível
echo Verificando pip...
"%PYTHON_EXE%" -m ensurepip >nul 2>&1
"%PYTHON_EXE%" -m pip --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️ Pip não encontrado. Tentando instalar...
    "%PYTHON_EXE%" -m ensurepip --upgrade
)

:: Verificar se xmltodict está instalado
echo Verificando xmltodict...
"%PYTHON_EXE%" -c "import xmltodict" 2>nul
if errorlevel 1 (
    echo 📦 Instalando xmltodict...
    "%PYTHON_EXE%" -m pip install xmltodict
)

:: Verificar se tkinter está disponível
echo Verificando tkinter...
"%PYTHON_EXE%" -c "import tkinter" 2>nul
if errorlevel 1 (
    echo ❌ ERRO: tkinter não está disponível no Python instalado.
    echo Instale manualmente ou reinstale o Python com suporte a tkinter.
    pause
    exit /b
)

:: Iniciar o painel com pythonw
echo ✅ Tudo pronto. Iniciando o painel...
start "" "%PYTHONW_EXE%" "%SCRIPT_PATH%"
exit /b
