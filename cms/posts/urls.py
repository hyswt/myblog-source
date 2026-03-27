from django.urls import path

from . import views

app_name = "posts"

urlpatterns = [
    path("setup-admin/", views.setup_admin_view, name="setup_admin"),
    path("logout/", views.logout_view, name="logout"),
    path("", views.dashboard, name="dashboard"),
    path("posts/new/", views.post_create, name="post_create"),
    path("posts/<int:post_id>/edit/", views.post_edit, name="post_edit"),
    path("posts/<int:post_id>/publish/", views.post_publish, name="post_publish"),
]
