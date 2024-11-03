from .views import OtpSejamViewset ,RegisterViewset , ChangePasswordViewset
from django.urls import path

urlpatterns = [
    path('register/otp/', OtpSejamViewset.as_view(), name='otp-sejam'),
    path('register/', RegisterViewset.as_view(), name='register'),
    path('change-password/', ChangePasswordViewset.as_view(), name='change-password'),
]
