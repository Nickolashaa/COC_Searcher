@echo off
chcp 65001 >nul
cls

echo [92mАктивирую виртуальное окружение...
call venv\Scripts\activate

echo [96mЗапускаю main.py...
python main.py

echo [93mПрограмма завершена. Для выхода нажмите любую клавишу.
pause >nul
