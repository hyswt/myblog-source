# 绑定到 skyinfin.com（CMS 后台）

目标：让后台写作地址在你的域名下可访问，推荐使用子域名：

- `cms.skyinfin.com`

## 建议架构

- 现有 Hexo 前台：`www.skyinfin.com`（Vercel）
- Django CMS：`cms.skyinfin.com`（Render / Railway）

这样最稳定，不会和 Hexo 前台路由冲突。

## 步骤（Render）

1. 将本仓库推送到 GitHub（包含根目录 `render.yaml`）
2. 在 Render 里选择 `New +` -> `Blueprint`，连接该仓库并创建
3. Render 会自动创建：
   - Web Service：`skyinfin-cms`
   - PostgreSQL：`skyinfin-cms-db`
4. 在 Render 控制台补充两个敏感环境变量：
   - `GITHUB_TOKEN`
   - `CMS_ADMIN_PASSWORD`
5. 在 Render 给 Web Service 绑定自定义域名：`cms.skyinfin.com`
6. 在 DNS 增加 CNAME：
   - 主机记录：`cms`
   - 记录值：Render 提供的目标域名（如 `xxx.onrender.com`）
7. 等证书生效后访问：`https://cms.skyinfin.com/`

## 说明

如果你坚持使用 `https://www.skyinfin.com/cms/` 这种“路径挂载”，需要网关反向代理（例如 Cloudflare Worker / Nginx），复杂度更高，不建议作为第一版。
