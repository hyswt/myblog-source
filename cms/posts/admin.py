from django.contrib import admin, messages

from .models import PostDraft
from .services import PublishError, publish_post


@admin.register(PostDraft)
class PostDraftAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "is_published", "updated_at", "published_at")
    search_fields = ("title", "slug", "tags", "categories")
    list_filter = ("is_published", "updated_at")
    readonly_fields = ("created_at", "updated_at", "published_at")
    actions = ("publish_selected_posts",)
    fieldsets = (
        ("文章内容", {"fields": ("title", "slug", "content_markdown")}),
        ("元信息", {"fields": ("tags", "categories", "abbrlink")}),
        ("发布状态", {"fields": ("is_published", "published_at")}),
        ("审计", {"fields": ("created_at", "updated_at")}),
    )

    @admin.action(description="发布选中文章到站点")
    def publish_selected_posts(self, request, queryset):
        success_count = 0
        for post in queryset:
            try:
                publish_post(post)
                success_count += 1
            except PublishError as exc:
                self.message_user(
                    request,
                    f"《{post.title}》发布失败: {exc}",
                    level=messages.ERROR,
                )
        if success_count:
            self.message_user(request, f"成功发布 {success_count} 篇文章。", level=messages.SUCCESS)
