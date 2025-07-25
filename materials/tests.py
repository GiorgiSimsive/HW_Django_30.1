from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model


from materials.models import Lesson, Course

User = get_user_model()


class LessonCourseTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # Создаем двух пользователей
        self.user = User.objects.create_user(email="user@example.com", password="pass")
        self.admin = User.objects.create_superuser(email="admin@example.com", password="adminpass")

        # Создаем курс и урок
        self.course = Course.objects.create(title="Курс 1", description="Описание курса")
        self.lesson = Lesson.objects.create(title="Урок 1", description="Описание урока", course=self.course,
                                            owner=self.admin)

    def authenticate_as_user(self):
        self.client.force_authenticate(user=self.user)

    def authenticate_as_admin(self):
        self.client.force_authenticate(user=self.admin)

    def test_list_lessons(self):
        self.authenticate_as_user()
        response = self.client.get('/api/materials/lessons/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_lesson_by_admin(self):
        self.authenticate_as_admin()
        data = {
            "title": "Новый урок",
            "description": "Описание нового урока",
            "course": self.course.id
        }
        response = self.client.post('/api/materials/lessons/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_lesson(self):
        self.authenticate_as_admin()
        url = f'/api/materials/lessons/{self.lesson.id}/'
        data = {"title": "Обновленный заголовок"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Обновленный заголовок")

    def test_delete_lesson(self):
        self.authenticate_as_admin()
        url = f'/api/materials/lessons/{self.lesson.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cannot_create_lesson(self):
        self.authenticate_as_user()
        data = {
            "title": "Недопустимо",
            "description": "Обычный пользователь",
            "course": self.course.id
        }
        response = self.client.post('/api/materials/lessons/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_subscription(self):
        self.authenticate_as_user()
        url = f'/api/materials/courses/{self.course.id}/subscribe/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_duplicate_subscription(self):
        self.authenticate_as_user()
        url = f'/api/materials/courses/{self.course.id}/subscribe/'
        self.client.post(url)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthenticated_cannot_access(self):
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/materials/lessons/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
