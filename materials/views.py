from rest_framework import viewsets, generics
from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsModerator, IsOwner
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .paginators import CustomPagination


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated & (IsModerator | IsOwner)]
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='moderator').exists():
            return Course.objects.all()
        return Course.objects.filter(owner=user)


class LessonListCreateAPIView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated & (IsModerator | IsOwner)]
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='moderator').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)


class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class SubscriptionToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course_id")

        course = get_object_or_404(Course, id=course_id)

        subs = Subscription.objects.filter(user=user, course=course)

        if subs.exists():
            subs.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course)
            message = "Подписка добавлена"

        return Response({"message": message})
