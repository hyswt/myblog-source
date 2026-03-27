# Django CMS (Dynamic Blog)

这个目录提供一个可独立部署的 Django 动态博客与后台，用于：

- 登录后台维护文章草稿
- 一键发布到数据库并立即在前台展示
- 不依赖 GitHub OAuth 即可在线写作

## 本地启动

1. 安装依赖：
   - `pip install -r requirements.txt`
2. 初始化数据库：
   - `python manage.py migrate`
3. 创建管理员：
   - `python manage.py createsuperuser`
4. 启动服务：
   - `python manage.py runserver`

访问地址（本地）：

- 前台首页：`http://127.0.0.1:8000/`
- 控制台：`http://127.0.0.1:8000/cms/`
- Django Admin：`http://127.0.0.1:8000/admin/`

## 一键自动启动（Windows）

在 `cms/` 目录执行：

- `.\bootstrap.ps1`

脚本会自动完成：

- 创建 `.venv`
- 安装依赖
- 执行迁移
- 创建/更新管理员账号
- 启动 Django

## 环境变量（核心）

复制 `.env.example` 并按实际值配置，至少需要：

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`
- `DJANGO_CSRF_TRUSTED_ORIGINS`
- `CMS_ADMIN_USERNAME`
- `CMS_ADMIN_EMAIL`
- `CMS_ADMIN_PASSWORD`

可参考：`deploy_to_skyinfin.md` 将后台绑定到 `cms.skyinfin.com`。

## 紧急重置管理员（无 Shell）

若无法登录，可在环境变量设置 `CMS_SETUP_KEY`，然后访问：

- `/cms/setup-admin/?key=<CMS_SETUP_KEY>`

在页面中输入新用户名/密码即可重置管理员账号，完成后建议轮换或删除 `CMS_SETUP_KEY`。
