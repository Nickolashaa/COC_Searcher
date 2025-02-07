@echo off
chcp 65001 >nul
cls

echo [92mАктивирую виртуальное окружение...
call .venv\Scripts\activate

echo [96mЗапускаю main.py...
start "" .venv\Scripts\pythonw.exe main.py

exit
