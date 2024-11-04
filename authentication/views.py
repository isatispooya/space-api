from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from GuardPyCaptcha.Captch import GuardPyCaptcha
from rest_framework.response import Response
from rest_framework import status
from user import fun
from user.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
# Create your views here.

class CaptchaViewset(APIView) :
    permission_classes = [AllowAny]
    @method_decorator(ratelimit(key='ip', rate='5/m', method='GET', block=True))
    def get (self,request):
        captcha = GuardPyCaptcha ()
        captcha = captcha.Captcha_generation(num_char=4 , only_num= True)
        return Response ({'captcha' : captcha} , status = status.HTTP_200_OK)
    

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = User.objects.get(username=username)
        
        # تلاش برای احراز هویت
        user = authenticate(username=username, password=password)
        
        if user is None:
            return Response(
                {
                    "detail": "اطلاعات کاربری نادرست است",
                    "debug_info": {
                        "username_received": username,
                        "password_received": "***"
                    }
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
            
        return super().post(request, *args, **kwargs) 