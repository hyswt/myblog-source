# 绑定到 skyinfin.com（Django 动态站）

目标：让动态站与后台都在 Django 服务上运行，推荐先使用子域名：

- `cms.skyinfin.com`（先验证）

## 建议架构（动态站）

- Django 前台+后台：`cms.skyinfin.com`（Railway）
- 前台首页：`/`
- 后台控制台：`/cms/`
- 管理后台：`/admin/`

## 步骤（Railway）

1. 将本仓库推送到 GitHub（包含根目录 `railway.json` 与 `Dockerfile`）
2. 在 Railway 创建项目并选择 `Deploy from GitHub Repo`，连接 `hyswt/myblog-source`
3. Railway 会按仓库内配置自动构建并启动 Django CMS
4. 在 Railway 项目变量中配置：
   - `DJANGO_SECRET_KEY`（随机强密钥）
   - `DJANGO_DEBUG=false`
   - `DJANGO_ALLOWED_HOSTS=cms.skyinfin.com,127.0.0.1,localhost`
   - `DJANGO_CSRF_TRUSTED_ORIGINS=https://cms.skyinfin.com`
   - `CMS_ADMIN_USERNAME=admin`
   - `CMS_ADMIN_EMAIL=admin@example.com`
   - `CMS_ADMIN_PASSWORD=<你的后台密码>`
   - `CMS_SETUP_KEY=<紧急重置管理员的密钥，可选但推荐>`
5. 给项目添加 PostgreSQL（Railway 插件），并把连接串赋值给 `DATABASE_URL`
6. 在 Railway 绑定自定义域名 `cms.skyinfin.com`
7. 在 DNS 增加 CNAME：
   - 主机记录：`cms`
   - 记录值：Railway 提供的目标域名（如 `xxx.up.railway.app`）
8. 等证书生效后访问：
   - `https://cms.skyinfin.com/`（前台）
   - `https://cms.skyinfin.com/cms/`（后台）
   - `https://cms.skyinfin.com/admin/`（Django Admin）

## 说明

如果要把主域名切到 Django 动态站，可在验证稳定后把 `www.skyinfin.com` 也指向 Railway；否则先保留现网，使用 `cms.skyinfin.com` 进行在线写作与预览。
