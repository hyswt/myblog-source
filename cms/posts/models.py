from django.db import models
from django.utils.text import slugify


class PostDraft(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    tags = models.CharField(max_length=300, blank=True, help_text="多个标签用英文逗号分隔")
    categories = models.CharField(max_length=300, blank=True, help_text="多个分类用英文逗号分隔")
    abbrlink = models.PositiveIntegerField(blank=True, null=True)
    content_markdown = models.TextField()
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "文章草稿"
        verbose_name_plural = "文章草稿"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title, allow_unicode=True)[:180] or "post"
            slug = base_slug
            suffix = 1
            while PostDraft.objects.exclude(pk=self.pk).filter(slug=slug).exists():
                slug = f"{base_slug}-{suffix}"
                suffix += 1
            self.slug = slug
        super().save(*args, **kwargs)
