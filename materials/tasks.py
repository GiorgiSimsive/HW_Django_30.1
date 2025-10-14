from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

User = get_user_model()


@shared_task
def send_course_update_email(course_title, user_emails):
    subject = f"Обновление курса: {course_title}"
    message = f"Курс '{course_title}' был обновлён. Проверьте новые материалы."
    from_email = None

    send_mail(subject, message, from_email, user_emails)
