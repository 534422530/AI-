@echo off
chcp 65001 >nul
echo ========================================
echo   opencode 迁移到 F 盘 - 环境变量设置
echo ========================================
echo.

:: 设置用户环境变量
setx OPENCODE_CONFIG_DIR "F:\laosi\.opencode" >nul 2>&1
setx LAOSI_HOME "F:\laosi\.laosi" >nul 2>&1

echo [√] 环境变量已设置完成！
echo.
echo    OPENCODE_CONFIG_DIR = F:\laosi\.opencode
echo    LAOSI_HOME = F:\laosi\.laosi
echo.
echo [!] 请重启终端使环境变量生效
echo.
pause
