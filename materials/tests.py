from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from materials.models import Course, Subscription
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
