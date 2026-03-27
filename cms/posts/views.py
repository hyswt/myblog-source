from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostDraftForm
from .models import PostDraft
from .services import PublishError, publish_post_to_github


@login_required
def logout_view(request):
    if request.method == "POST":
        auth_logout(request)
        messages.success(request, "你已安全退出登录。")
        return redirect("/admin/login/")
    return redirect("/")


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
        return redirect("posts:dashboard")

    try:
        result = publish_post_to_github(post)
        messages.success(request, f"发布成功：{result['path']}")
    except PublishError as exc:
        messages.error(request, f"发布失败：{exc}")

    return redirect("posts:dashboard")
