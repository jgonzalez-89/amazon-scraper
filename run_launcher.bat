@echo off

rem Activar el entorno virtual
call venv\Scripts\activate.bat

rem Ejecutar launcher.py
python launcher.py

rem Desactivar el entorno virtual
call deactivate.bat