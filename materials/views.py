from rest_framework import viewsets, generics, status
from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsModerator, IsOwner
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .paginators import CustomPagination
from .services.stripe_service import create_stripe_product, create_stripe_price, create_checkout_session, create_stripe_checkout_session
from .tasks import send_course_update_email


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

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        old_updated = instance.updated_at if hasattr(instance, "updated_at") else None

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if serializer.validated_data:
            subscribers = Subscription.objects.filter(course=instance).select_related("user")
            user_emails = [s.user.email for s in subscribers if s.user.email]

            if user_emails:
                send_course_update_email.delay(course_title=instance.title, user_emails=user_emails)

        return Response(serializer.data, status=status.HTTP_200_OK)


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


class StripePaymentView(APIView):
    def post(self, request):
        name = request.data.get("name")
        amount = request.data.get("amount")

        product_id = create_stripe_product(name)
        price_id = create_stripe_price(product_id, amount)
        session_url = create_checkout_session(
            price_id,
            success_url="http://localhost:8000/success/",
            cancel_url="http://localhost:8000/cancel/"
        )

        return Response({"checkout_url": session_url})


class PaymentSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        course_id = request.data.get("course_id")
        course = Course.objects.get(id=course_id)

        session_url = create_stripe_checkout_session(request.user, course)
        return Response({"checkout_url": session_url})
