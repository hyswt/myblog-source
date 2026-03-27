import base64
import os
from datetime import datetime

import requests
from django.utils import timezone


class PublishError(Exception):
    pass


def _split_csv(raw_value: str):
    return [item.strip() for item in raw_value.split(",") if item.strip()]


def _build_markdown(post):
    tags = _split_csv(post.tags)
    categories = _split_csv(post.categories)

    lines = ["---"]
    lines.append(f"title: {post.title}")
    lines.append(f"date: {timezone.localtime(post.updated_at).strftime('%Y-%m-%d %H:%M:%S')}")
    if tags:
        if len(tags) == 1:
            lines.append(f"tags: {tags[0]}")
        else:
            lines.append("tags:")
            for tag in tags:
                lines.append(f"  - {tag}")
    if categories:
        if len(categories) == 1:
            lines.append(f"categories: {categories[0]}")
        else:
            lines.append("categories:")
            for category in categories:
                lines.append(f"  - {category}")
    if post.abbrlink:
        lines.append(f"abbrlink: {post.abbrlink}")
    lines.append("---")
    lines.append("")
    lines.append(post.content_markdown.rstrip())
    lines.append("")
    return "\n".join(lines)


def publish_post_to_github(post):
    token = os.getenv("GITHUB_TOKEN")
    owner = os.getenv("GITHUB_OWNER", "hyswt")
    repo = os.getenv("GITHUB_REPO", "myblog-source")
    branch = os.getenv("GITHUB_BRANCH", "main")

    if not token:
        raise PublishError("缺少环境变量 GITHUB_TOKEN")

    file_path = f"source/_posts/{post.slug}.md"
    api_base = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    existing_sha = None
    get_resp = requests.get(api_base, headers=headers, params={"ref": branch}, timeout=20)
    if get_resp.status_code == 200:
        existing_sha = get_resp.json().get("sha")
    elif get_resp.status_code != 404:
        raise PublishError(f"读取 GitHub 文件失败: {get_resp.status_code} {get_resp.text}")

    content = _build_markdown(post)
    payload = {
        "message": f"publish: {post.title}",
        "content": base64.b64encode(content.encode("utf-8")).decode("utf-8"),
        "branch": branch,
        "committer": {
            "name": os.getenv("GIT_COMMITTER_NAME", "cms-bot"),
            "email": os.getenv("GIT_COMMITTER_EMAIL", "cms-bot@example.com"),
        },
    }
    if existing_sha:
        payload["sha"] = existing_sha

    put_resp = requests.put(api_base, headers=headers, json=payload, timeout=30)
    if put_resp.status_code not in (200, 201):
        raise PublishError(f"写入 GitHub 失败: {put_resp.status_code} {put_resp.text}")

    post.is_published = True
    post.published_at = timezone.now()
    post.save(update_fields=["is_published", "published_at", "updated_at"])

    return {
        "path": file_path,
        "repo_url": f"https://github.com/{owner}/{repo}/blob/{branch}/{file_path}",
        "published_at": datetime.now().isoformat(timespec="seconds"),
    }
