import os
from hmac import compare_digest

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
            # Self-heal admin credentials drift in cloud deployments.
            # If runtime env credentials match user input, force-sync admin user
            # and retry authentication once.
            self._try_sync_admin_credentials(account=account, password=password)
            self.user_cache = authenticate(self.request, username=username, password=password)
        if self.user_cache is None:
            raise forms.ValidationError("账号或密码错误。")
        if not self.user_cache.is_active:
            raise forms.ValidationError("账号已被禁用。")
        return cleaned_data

    def get_user(self):
        return self.user_cache

    def _try_sync_admin_credentials(self, account: str, password: str):
        admin_username = (os.getenv("CMS_ADMIN_USERNAME") or "").strip()
        admin_email = (os.getenv("CMS_ADMIN_EMAIL") or "").strip()
        admin_password = os.getenv("CMS_ADMIN_PASSWORD") or ""

        if not admin_username or not admin_password:
            return

        account_lower = account.lower()
        matched_account = account_lower in {admin_username.lower(), admin_email.lower()}
        matched_password = compare_digest(password, admin_password)
        if not (matched_account and matched_password):
            return

        User = get_user_model()
        user, _ = User.objects.get_or_create(
            username=admin_username,
            defaults={
                "email": admin_email or f"{admin_username}@example.com",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        user.email = admin_email or user.email
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(admin_password)
        user.save()
