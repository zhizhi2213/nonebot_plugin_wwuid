@echo off
chcp 65001 > nul
echo ========================================
echo    鸣潮插件单元测试运行脚本
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] 检查测试环境...
pip show pytest > nul 2>&1
if errorlevel 1 (
    echo pytest 未安装，正在安装...
    pip install pytest pytest-asyncio pytest-mock
) else (
    echo pytest 已安装
)

echo.
echo [2/3] 安装插件依赖...
pip install -e . > nul 2>&1

echo.
echo [3/3] 运行测试...
echo.
pytest tests/ -v --tb=short

if errorlevel 1 (
    echo.
    echo ========================================
    echo    测试失败！请检查错误信息
    echo ========================================
) else (
    echo.
    echo ========================================
    echo    所有测试通过！
    echo ========================================
)

pause
