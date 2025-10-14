from celery import shared_task
from django.utils.timezone import now
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

User = get_user_model()


@shared_task
def print_hello():
    print(f"Hello from Celery! Time: {now()}")


@shared_task
def deactivate_inactive_users():
    one_month_ago = timezone.now() - timedelta(days=30)
    users_to_deactivate = User.objects.filter(is_active=True, last_login__lt=one_month_ago)

    count = users_to_deactivate.update(is_active=False)
    return f"Деактивировано пользователей: {count}"
