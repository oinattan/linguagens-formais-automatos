@echo off
REM Script helper para Windows: cria venv, instala dependências e executa a GUI
SET VENV_DIR=.venv

IF NOT EXIST %VENV_DIR% (
    python -m venv %VENV_DIR%
)

CALL %VENV_DIR%\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

REM Executar GUI
python -m src.gui

PAUSE
