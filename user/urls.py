from .views import OtpSejamViewset , CaptchaViewset ,RegisterViewset
from django.urls import path

urlpatterns = [
    path('captcha/', CaptchaViewset.as_view(), name='captcha'),
    path('register/otp/', OtpSejamViewset.as_view(), name='otp-sejam'),
    path('register/', RegisterViewset.as_view(), name='register'),
]
