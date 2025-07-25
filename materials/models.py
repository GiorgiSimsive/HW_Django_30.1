from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    preview = models.ImageField(upload_to='course_previews/', verbose_name='Превью', blank=True, null=True)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name='courses', default=1)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE, verbose_name='Курс')
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    preview = models.ImageField(upload_to='lesson_previews/', verbose_name='Превью', blank=True, null=True)
    video_link = models.URLField(verbose_name='Ссылка на видео', blank=True, null=True)
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name='lessons', default=1)

    def __str__(self):
        return f"{self.title} ({self.course.title})"


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subscriptions')

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.user.email} подписан на {self.course.title}"
