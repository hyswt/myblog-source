import os

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.html import mark_safe

from .forms import PostDraftForm
from .models import PostDraft
from .services import PublishError, publish_post, render_markdown_html


def setup_admin_view(request):
    setup_key = (os.getenv("CMS_SETUP_KEY") or "").strip()
    if not setup_key:
        return render(
            request,
            "posts/setup_admin.html",
            {
                "enabled": False,
                "error": "服务端未配置 CMS_SETUP_KEY，无法使用初始化功能。",
            },
        )

    key = (request.GET.get("key") or request.POST.get("key") or "").strip()
    if key != setup_key:
        return render(
            request,
            "posts/setup_admin.html",
            {
                "enabled": True,
                "error": "密钥无效。请在地址中携带正确 key 参数。",
            },
            status=403,
        )

    if request.method == "POST":
        username = (request.POST.get("username") or "admin").strip()
        email = (request.POST.get("email") or "admin@example.com").strip()
        password = (request.POST.get("password") or "").strip()

        if not username or not password:
            return render(
                request,
                "posts/setup_admin.html",
                {
                    "enabled": True,
                    "key": key,
                    "error": "用户名和密码不能为空。",
                    "username": username,
                    "email": email,
                },
                status=400,
            )

        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email, "is_staff": True, "is_superuser": True},
        )
        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(password)
        user.save()

        return render(
            request,
            "posts/setup_admin.html",
            {
                "enabled": True,
                "key": key,
                "success": f"管理员已{'创建' if created else '更新'}：{username}",
            },
        )

    return render(request, "posts/setup_admin.html", {"enabled": True, "key": key})


@login_required
def logout_view(request):
    if request.method == "POST":
        auth_logout(request)
        messages.success(request, "你已安全退出登录。")
        return redirect("/admin/login/")
    return redirect("/cms/")


def site_index(request):
    posts = PostDraft.objects.filter(is_published=True).order_by("-published_at", "-updated_at")
    return render(request, "site/index.html", {"posts": posts})


def site_post_detail(request, slug):
    post = get_object_or_404(PostDraft, slug=slug, is_published=True)
    content_html = mark_safe(render_markdown_html(post.content_markdown))
    return render(request, "site/post_detail.html", {"post": post, "content_html": content_html})


@login_required
def dashboard(request):
    posts = PostDraft.objects.all()
    return render(request, "posts/dashboard.html", {"posts": posts})


@login_required
def post_create(request):
    if request.method == "POST":
        form = PostDraftForm(request.POST)
        if form.is_valid():
            post = form.save()
            messages.success(request, f"草稿《{post.title}》已保存。")
            return redirect("posts:dashboard")
    else:
        form = PostDraftForm()
    return render(request, "posts/post_form.html", {"form": form, "title": "新建文章"})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(PostDraft, pk=post_id)
    if request.method == "POST":
        form = PostDraftForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            messages.success(request, f"文章《{post.title}》已更新。")
            return redirect("posts:dashboard")
    else:
        form = PostDraftForm(instance=post)
    return render(request, "posts/post_form.html", {"form": form, "title": f"编辑文章：{post.title}"})


@login_required
def post_publish(request, post_id):
    post = get_object_or_404(PostDraft, pk=post_id)
    if request.method != "POST":
        return redirect("/cms/")

    try:
        result = publish_post(post)
        messages.success(request, f"发布成功：{result['url']}")
    except PublishError as exc:
        messages.error(request, f"发布失败：{exc}")

    return redirect("posts:dashboard")
