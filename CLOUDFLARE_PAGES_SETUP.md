# Cloudflare 在线写作方案（替代 Railway）

这套方案使用：

- 前台博客：Cloudflare Pages（构建 Hexo）
- 后台写作：Decap CMS（`/admin`）
- GitHub OAuth：Cloudflare Workers（免费）

## 1) 配置 Cloudflare Pages

在 Cloudflare Pages 连接仓库 `hyswt/myblog-source`：

- Build command: `npm run build`
- Build output directory: `public`

部署成功后绑定你的域名（如 `www.skyinfin.com`）。

## 2) 部署 OAuth Worker

Worker 代码已在：

- `cloudflare/oauth-worker/src/index.js`

本地部署示例（需要先安装 wrangler 并登录）：

```bash
cd cloudflare/oauth-worker
wrangler secret put GITHUB_CLIENT_ID
wrangler secret put GITHUB_CLIENT_SECRET
wrangler deploy
```

部署后给 Worker 绑定域名，例如：

- `cms-auth.skyinfin.com`

## 3) 配置 GitHub OAuth App

在 GitHub OAuth App 里设置：

- Homepage URL: `https://www.skyinfin.com/admin/`
- Authorization callback URL: `https://cms-auth.skyinfin.com/callback`

## 4) 修改 Decap 配置

编辑 `source/admin/config.yml`，把 backend 改成：

```yml
backend:
  name: github
  repo: hyswt/myblog-source
  branch: main
  base_url: https://cms-auth.skyinfin.com
  auth_endpoint: auth
```

然后提交并等待 Pages 自动部署。

## 5) 使用

- 打开：`https://www.skyinfin.com/admin/`
- 登录 GitHub
- 新建文章并 Publish
- Cloudflare Pages 自动构建上线

## 常见问题

- 登录后报 state 错误：检查是否从 `/admin` 入口点击登录，不要手动直接打开 authorize URL。
- 404：确认 Worker 路径为 `/auth` 与 `/callback` 且域名绑定正确。
- 发布失败：检查 `GITHUB_TOKEN`/OAuth 权限和仓库写权限。
