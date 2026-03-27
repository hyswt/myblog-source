#!/usr/bin/env bash
set -euo pipefail

if [ -f ".venv/bin/python" ]; then
  PYTHON_BIN=".venv/bin/python"
  GUNICORN_BIN=".venv/bin/gunicorn"
else
  PYTHON_BIN="python"
  GUNICORN_BIN="gunicorn"
fi

"$PYTHON_BIN" manage.py migrate --noinput
"$PYTHON_BIN" manage.py collectstatic --noinput

"$PYTHON_BIN" - <<'PY'
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()
from django.contrib.auth import get_user_model

username = (os.getenv("CMS_ADMIN_USERNAME") or "admin").strip()
email = (os.getenv("CMS_ADMIN_EMAIL") or "admin@example.com").strip()
password = (os.getenv("CMS_ADMIN_PASSWORD") or "").strip()

if password:
    User = get_user_model()
    user, created = User.objects.get_or_create(
        username=username,
        defaults={"email": email, "is_staff": True, "is_superuser": True},
    )
    user.email = email
    user.is_staff = True
    user.is_superuser = True
    user.is_active = True
    user.set_password(password)
    user.save()
    action = "created" if created else "updated"
    print(f"[cms] superuser_{action}: username={username}, email={email}")
else:
    print("[cms] skip superuser sync: CMS_ADMIN_PASSWORD is empty")
PY

exec "$GUNICORN_BIN" config.wsgi:application --bind 0.0.0.0:${PORT:-10000}
