from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from GuardPyCaptcha.Captch import GuardPyCaptcha
from rest_framework.response import Response
from rest_framework import status
from user.models import User
from user import fun
# Create your views here.

class CaptchaViewset(APIView) :
    permission_classes = [AllowAny]
    @method_decorator(ratelimit(key='ip', rate='5/m', method='GET', block=True))
    def get (self,request):
        captcha = GuardPyCaptcha ()
        captcha = captcha.Captcha_generation(num_char=4 , only_num= True)
        return Response ({'captcha' : captcha} , status = status.HTTP_200_OK)
    

class LoginViewset(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        print(request.data)
        user = User.objects.filter(username=request.data.get('username')).first()
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        if not user.check_password(request.data.get('password')):
            return Response({'error': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)
        token = fun.encryptionUser(user)
        return Response({'access': token}, status=status.HTTP_200_OK)
