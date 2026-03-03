# opencode 迁移到 F 盘配置
# 日期: 2026-03-03

# 1. 设置环境变量 (用户级别)
[Environment]::SetEnvironmentVariable("OPENCODE_CONFIG_DIR", "F:\laosi\.opencode", "User")
[Environment]::SetEnvironmentVariable("LAOSI_HOME", "F:\laosi\.laosi", "User")

# 2. 创建符号链接 (管理员权限运行)
# New-Item -ItemType SymbolicLink -Path "C:\Users\lb\.config\opencode" -Target "F:\laosi\.opencode" -Force

# 3. 或者直接移动配置
# Move-Item "C:\Users\lb\.config\opencode" "F:\laosi\.opencode" -Force

Write-Host "环境变量已设置完成！" -ForegroundColor Green
Write-Host "请重启终端或重新登录使环境变量生效" -ForegroundColor Yellow
Write-Host ""
Write-Host "OPENCODE_CONFIG_DIR = F:\laosi\.opencode" -ForegroundColor Cyan
Write-Host "LAOSI_HOME = F:\laosi\.laosi" -ForegroundColor Cyan
