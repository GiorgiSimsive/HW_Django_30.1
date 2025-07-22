from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, PaymentViewSet, RegisterView

router = DefaultRouter()
router.register(r'profiles', UserViewSet)
router.register(r'payments', PaymentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
]
