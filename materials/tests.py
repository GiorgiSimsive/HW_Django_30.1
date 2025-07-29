from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from materials.models import Course, Subscription, Lesson
from rest_framework import status
from django.urls import reverse

User = get_user_model()


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="user@example.com", password="pass")
        self.course = Course.objects.create(title="Тестовый курс", description="Описание", owner=self.user)
        self.subscribe_url = reverse("subscribe-toggle")

    def test_subscribe_to_course(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.subscribe_url, {"course_id": self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Подписка добавлена")
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_unsubscribe_from_course(self):
        self.client.force_authenticate(user=self.user)
        self.client.post(self.subscribe_url, {"course_id": self.course.id})
        response = self.client.post(self.subscribe_url, {"course_id": self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Подписка удалена")
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_subscribe_unauthorized(self):
        response = self.client.post(self.subscribe_url, {"course_id": self.course.id})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="admin@example.com", password="adminpass")
        self.course = Course.objects.create(title="Course 1", description="Desc", owner=self.user)
        self.lesson = Lesson.objects.create(title="Lesson 1", description="Lesson desc", course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)
        self.lesson_list_url = reverse("lesson-list-create")
        self.lesson_detail_url = reverse("lesson-detail", args=[self.lesson.id])

    def test_create_lesson(self):
        data = {
            "title": "New Lesson",
            "description": "New Desc",
            "course": self.course.id,
            "video_link": "https://youtube.com/example"
        }
        response = self.client.post(self.lesson_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_get_lesson_list(self):
        response = self.client.get(self.lesson_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data["results"]), 1)

    def test_get_lesson_detail(self):
        response = self.client.get(self.lesson_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.lesson.title)

    def test_update_lesson(self):
        data = {
            "title": "Updated Lesson",
            "description": "Updated Desc",
            "course": self.course.id,
            "video_link": "https://youtube.com/example"
        }
        response = self.client.put(self.lesson_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, "Updated Lesson")

    def test_delete_lesson(self):
        response = self.client.delete(self.lesson_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())