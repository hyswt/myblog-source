from django import forms
from django.contrib.auth import authenticate, get_user_model

from .models import PostDraft


class PostDraftForm(forms.ModelForm):
    class Meta:
        model = PostDraft
        fields = ["title", "slug", "tags", "categories", "abbrlink", "content_markdown"]
        widgets = {
            "content_markdown": forms.Textarea(attrs={"rows": 18}),
        }


class LoginForm(forms.Form):
    account = forms.CharField(
        label="用户名或邮箱",
        max_length=150,
        widget=forms.TextInput(attrs={"placeholder": "请输入用户名或邮箱"}),
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(attrs={"placeholder": "请输入密码"}),
    )
    remember_me = forms.BooleanField(label="记住我（7天）", required=False)

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.user_cache = None

    def clean(self):
        cleaned_data = super().clean()
        account = (cleaned_data.get("account") or "").strip()
        password = cleaned_data.get("password") or ""
        if not account or not password:
            raise forms.ValidationError("请输入账号和密码。")

        username = account
        if "@" in account:
            User = get_user_model()
            user = User.objects.filter(email__iexact=account).first()
            if user:
                username = user.get_username()

        self.user_cache = authenticate(self.request, username=username, password=password)
        if self.user_cache is None:
            raise forms.ValidationError("账号或密码错误。")
        if not self.user_cache.is_active:
            raise forms.ValidationError("账号已被禁用。")
        return cleaned_data

    def get_user(self):
        return self.user_cache
