# 绑定到 skyinfin.com（CMS 后台）

目标：让后台写作地址在你的域名下可访问，推荐使用子域名：

- `cms.skyinfin.com`

## 建议架构

- 现有 Hexo 前台：`www.skyinfin.com`（Vercel）
- Django CMS：`cms.skyinfin.com`（Render / Railway）

这样最稳定，不会和 Hexo 前台路由冲突。

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
   - `GITHUB_TOKEN=<可写 myblog-source 的 token>`
   - `GITHUB_OWNER=hyswt`
   - `GITHUB_REPO=myblog-source`
   - `GITHUB_BRANCH=main`
5. 给项目添加 PostgreSQL（Railway 插件），并把连接串赋值给 `DATABASE_URL`
6. 在 Railway 绑定自定义域名 `cms.skyinfin.com`
7. 在 DNS 增加 CNAME：
   - 主机记录：`cms`
   - 记录值：Railway 提供的目标域名（如 `xxx.up.railway.app`）
8. 等证书生效后访问：`https://cms.skyinfin.com/`

## 说明

如果你坚持使用 `https://www.skyinfin.com/cms/` 这种“路径挂载”，需要网关反向代理（例如 Cloudflare Worker / Nginx），复杂度更高，不建议作为第一版。
