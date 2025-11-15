@echo off
chcp 65001 >nul
echo ========================================
echo B站弹幕数据分析系统
echo ========================================
echo.
echo 正在检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.7+
    pause
    exit /b 1
)

echo 正在检查依赖包...
python -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo 正在安装依赖包...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo 依赖安装失败，请手动运行: pip install -r requirements.txt
        pause
        exit /b 1
    )
)

echo.
echo 开始运行主程序...
echo.
python main.py

echo.
echo 按任意键退出...
pause >nul

