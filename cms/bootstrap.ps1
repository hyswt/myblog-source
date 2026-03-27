param(
  [string]$AdminUsername = "",
  [string]$AdminEmail = "",
  [string]$AdminPassword = ""
)

$ErrorActionPreference = "Stop"

function Get-EnvValue([string]$Name) {
  if (Test-Path ".env") {
    $line = Get-Content ".env" | Where-Object { $_ -match "^$Name=" } | Select-Object -First 1
    if ($line) {
      return ($line -replace "^$Name=", "")
    }
  }
  return ""
}

Write-Host "[1/6] 准备 Python 虚拟环境..."
if (!(Test-Path ".venv")) {
  python -m venv .venv
}

$pythonExe = ".\.venv\Scripts\python.exe"
if (!(Test-Path $pythonExe)) {
  throw "未找到虚拟环境 Python: $pythonExe"
}

Write-Host "[2/6] 安装依赖..."
& $pythonExe -m pip install --upgrade pip
& $pythonExe -m pip install -r requirements.txt

Write-Host "[3/6] 数据库迁移..."
& $pythonExe manage.py migrate

if ([string]::IsNullOrWhiteSpace($AdminUsername)) { $AdminUsername = Get-EnvValue "CMS_ADMIN_USERNAME" }
if ([string]::IsNullOrWhiteSpace($AdminEmail)) { $AdminEmail = Get-EnvValue "CMS_ADMIN_EMAIL" }
if ([string]::IsNullOrWhiteSpace($AdminPassword)) { $AdminPassword = Get-EnvValue "CMS_ADMIN_PASSWORD" }

if ([string]::IsNullOrWhiteSpace($AdminUsername)) { $AdminUsername = "admin" }
if ([string]::IsNullOrWhiteSpace($AdminEmail)) { $AdminEmail = "admin@example.com" }

if ([string]::IsNullOrWhiteSpace($AdminPassword)) {
  Write-Host "未提供管理员密码，自动生成随机密码..."
  $AdminPassword = -join ((48..57 + 65..90 + 97..122) | Get-Random -Count 16 | ForEach-Object {[char]$_})
  Write-Host "CMS_ADMIN_PASSWORD=$AdminPassword"
}

Write-Host "[4/6] 创建或更新管理员账号..."
& $pythonExe manage.py shell -c @"
from django.contrib.auth import get_user_model
User = get_user_model()
username = r'''$AdminUsername'''
email = r'''$AdminEmail'''
password = r'''$AdminPassword'''
user, created = User.objects.get_or_create(username=username, defaults={"email": email, "is_staff": True, "is_superuser": True})
if created:
    user.set_password(password)
    user.save()
else:
    user.email = email
    user.is_staff = True
    user.is_superuser = True
    user.set_password(password)
    user.save()
print("superuser_ready")
"@

Write-Host "[5/6] Django 自检..."
& $pythonExe manage.py check

Write-Host "[6/6] 启动 CMS 服务..."
Write-Host "后台地址: http://127.0.0.1:8000/"
Write-Host "Django Admin: http://127.0.0.1:8000/admin/"
& $pythonExe manage.py runserver
