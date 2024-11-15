from .views import OtpSejamViewset ,RegisterViewset , ChangePasswordViewset , ForgotPasswordViewset ,ProfileViewset , UserViewset , UserDetailViewset
from django.urls import path

urlpatterns = [
    path('register/otp/', OtpSejamViewset.as_view(), name='otp-sejam'),
    path('register/', RegisterViewset.as_view(), name='register'),
    path('change-password/', ChangePasswordViewset.as_view(), name='change-password'),
    path('forgot-password/', ForgotPasswordViewset.as_view(), name='forgot-password'),
    path('user/profile/', ProfileViewset.as_view(), name='user-profile'),
    path('users/', UserViewset.as_view(), name='users'),
    path('users/<int:pk>/', UserDetailViewset.as_view(), name='user-detail-for-admin'),
]
