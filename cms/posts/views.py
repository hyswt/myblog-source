from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import LoginForm, PostDraftForm
from .models import PostDraft
from .services import PublishError, publish_post_to_github


def login_view(request):
    if request.user.is_authenticated:
        return redirect("posts:dashboard")

    form = LoginForm(request=request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        auth_login(request, user)
        if form.cleaned_data.get("remember_me"):
            request.session.set_expiry(7 * 24 * 60 * 60)
        else:
            request.session.set_expiry(0)
        messages.success(request, f"欢迎回来，{user.username}。")
        next_url = request.GET.get("next") or request.POST.get("next") or "/"
        return redirect(next_url)

    return render(request, "registration/login.html", {"form": form})


@login_required
def logout_view(request):
    if request.method == "POST":
        auth_logout(request)
        messages.success(request, "你已安全退出登录。")
        return redirect("/accounts/login/")
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
