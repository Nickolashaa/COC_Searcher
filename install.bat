@echo off
chcp 65001 >nul
cls

echo.
echo [91m░█████╗░██╗░░░░░░█████╗░░██████╗██╗░░██╗
echo ██╔══██╗██║░░░░░██╔══██╗██╔════╝██║░░██║
echo ██║░░╚═╝██║░░░░░███████║╚█████╗░███████║
echo ██║░░██╗██║░░░░░██╔══██║░╚═══██╗██╔══██║
echo ╚█████╔╝███████╗██║░░██║██████╔╝██║░░██║
echo ░╚════╝░╚══════╝╚═╝░░╚═╝╚═════╝░╚═╝░░╚═╝

echo ░█████╗░███████╗
echo ██╔══██╗██╔════╝
echo ██║░░██║█████╗░░
echo ██║░░██║██╔══╝░░
echo ╚█████╔╝██║░░░░░
echo ░╚════╝░╚═╝░░░░░

echo ░█████╗░██╗░░░░░░█████╗░███╗░░██╗░██████╗
echo ██╔══██╗██║░░░░░██╔══██╗████╗░██║██╔════╝
echo ██║░░╚═╝██║░░░░░███████║██╔██╗██║╚█████╗░
echo ██║░░██╗██║░░░░░██╔══██║██║╚████║░╚═══██╗
echo ╚█████╔╝███████╗██║░░██║██║░╚███║██████╔╝
echo ░╚════╝░╚══════╝╚═╝░░╚═╝╚═╝░░╚══╝╚═════╝░

echo.
echo [92mПривет! Я помогу установить все зависимости. Нажми любую клавишу для продолжения...
pause >nul

set OS_NAME=
for /f "tokens=2 delims==" %%A in ('wmic os get Caption /value ^| findstr /i "Windows"') do set OS_NAME=Windows
if "%OS_NAME%"=="" set OS_NAME=Linux

echo [95mОбнаружена операционная система: %OS_NAME%

echo [96m1/3 Устанавливаю базовые зависимости...
pip install -r requirements.txt

echo [93mХотите использовать GPU для ускорения? (y/n):
set /p use_gpu=
if /i "%use_gpu%"=="y" (
    echo [96m2/3 Устанавливаю поддержку GPU...
    if "%OS_NAME%"=="Windows" (
        pip install paddlepaddle-gpu==2.5.0 paddleocr -f https://www.paddlepaddle.org.cn/whl/windows/mkl/avx/stable.html
    ) else (
        pip install paddlepaddle-gpu==2.5.0 paddleocr -f https://www.paddlepaddle.org.cn/whl/linux/mkl/avx/stable.html
    )
) else (
    echo [93mПропускаю установку GPU.
)

echo [92m3/3 Установка завершена! Запускайте программу: python main.py
echo.
pause
