from django.utils import timezone
import markdown


class PublishError(Exception):
    pass


def publish_post(post):
    post.is_published = True
    if not post.published_at:
        post.published_at = timezone.now()
    post.save(update_fields=["is_published", "published_at", "updated_at"])
    return {"url": f"/post/{post.slug}/"}


def render_markdown_html(markdown_text: str) -> str:
    return markdown.markdown(
        markdown_text or "",
        extensions=["extra", "fenced_code", "tables", "sane_lists"],
    )
