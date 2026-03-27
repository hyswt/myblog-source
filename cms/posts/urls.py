from django.urls import path

from . import views

app_name = "posts"

urlpatterns = [
    path("accounts/login/", views.login_view, name="login"),
    path("accounts/logout/", views.logout_view, name="logout"),
    path("", views.dashboard, name="dashboard"),
    path("posts/new/", views.post_create, name="post_create"),
    path("posts/<int:post_id>/edit/", views.post_edit, name="post_edit"),
    path("posts/<int:post_id>/publish/", views.post_publish, name="post_publish"),
]
