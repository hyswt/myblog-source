#!/usr/bin/env bash
set -euo pipefail

python manage.py migrate --noinput
python manage.py collectstatic --noinput

python - <<'PY'
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()
from django.contrib.auth import get_user_model

username = os.getenv("CMS_ADMIN_USERNAME")
email = os.getenv("CMS_ADMIN_EMAIL")
password = os.getenv("CMS_ADMIN_PASSWORD")

if username and email and password:
    User = get_user_model()
    user, created = User.objects.get_or_create(
        username=username,
        defaults={"email": email, "is_staff": True, "is_superuser": True},
    )
    user.email = email
    user.is_staff = True
    user.is_superuser = True
    user.set_password(password)
    user.save()
PY

exec gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-10000}
