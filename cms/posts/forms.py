from django import forms

from .models import PostDraft


class PostDraftForm(forms.ModelForm):
    class Meta:
        model = PostDraft
        fields = ["title", "slug", "tags", "categories", "abbrlink", "content_markdown"]
        widgets = {
            "content_markdown": forms.Textarea(attrs={"rows": 18}),
        }
