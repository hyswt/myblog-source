# Decap CMS 接入说明（Hexo + Vercel）

你已经完成项目内的基础接入：

- `source/admin/index.html`
- `source/admin/config.yml`

部署后访问 `/admin` 即可进入后台页面。

## 还需完成的步骤（一次性）

1. 在 GitHub 创建 OAuth App（必需）
   - Homepage URL: `https://www.skyinfin.com/admin/`
   - Authorization callback URL: `https://www.skyinfin.com/api/callback`
   - 创建完成后，得到 `Client ID` 与 `Client Secret`。

2. 在 Vercel 项目中添加环境变量
   - `GITHUB_CLIENT_ID` = 你的 GitHub OAuth App Client ID
   - `GITHUB_CLIENT_SECRET` = 你的 GitHub OAuth App Client Secret
   - 添加后重新部署一次。

3. 确认 Vercel 已连接 `hyswt/myblog` 并开启自动部署
   - 后台发布会提交到 `main` 分支。
   - Vercel 检测到新 commit 后会自动构建上线。

## 日常使用流程

1. 打开 `https://你的域名/admin`
2. 登录 GitHub
3. 新建或编辑文章
4. 点击 Publish
5. 等待 Vercel 自动部署完成

## 说明

- 图片会写入 `source/images/uploads`，文章内引用为 `/images/uploads/...`。
- 文章写入目录为 `source/_posts`，格式为 Markdown Front Matter。
- OAuth 回调函数已经在项目内提供：
  - `api/auth.js`
  - `api/callback.js`
