# Django CMS (for Hexo + Vercel)

这个目录提供一个可独立部署的 Django 后台，用于：

- 登录后台维护文章草稿
- 一键发布 Markdown 到 `myblog-source` 仓库的 `source/_posts`
- 由 Vercel 自动构建并上线网站

## 本地启动

1. 安装依赖：
   - `pip install -r requirements.txt`
2. 初始化数据库：
   - `python manage.py migrate`
3. 创建管理员：
   - `python manage.py createsuperuser`
4. 启动服务：
   - `python manage.py runserver`

访问地址：

- 控制台：`http://127.0.0.1:8000/`
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

## 环境变量

复制 `.env.example` 并按实际值配置，至少需要：

- `GITHUB_TOKEN`
- `GITHUB_OWNER`
- `GITHUB_REPO`
- `GITHUB_BRANCH`

`GITHUB_TOKEN` 需要对目标仓库具备 Contents 写权限。

可参考：`deploy_to_skyinfin.md` 将后台绑定到 `cms.skyinfin.com`。
