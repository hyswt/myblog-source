from django.urls import path

from . import views

app_name = "posts"

urlpatterns = [
    path("", views.site_index, name="site_index"),
    path("post/<slug:slug>/", views.site_post_detail, name="site_post_detail"),
    path("cms/", views.dashboard, name="dashboard"),
    path("cms/posts/new/", views.post_create, name="post_create"),
    path("cms/posts/<int:post_id>/edit/", views.post_edit, name="post_edit"),
    path("cms/posts/<int:post_id>/publish/", views.post_publish, name="post_publish"),
    path("cms/logout/", views.logout_view, name="logout"),
    path("cms/setup-admin/", views.setup_admin_view, name="setup_admin"),
]
