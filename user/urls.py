from .views import OtpSejamViewset , CaptchaViewset
from django.urls import path

urlpatterns = [
    path('captcha/', CaptchaViewset.as_view(), name='captcha'),
    path('register/otp/', OtpSejamViewset.as_view(), name='otp-sejam'),
]
