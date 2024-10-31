from django.shortcuts import render
from rest_framework.views import APIView
from GuardPyCaptcha.Captch import GuardPyCaptcha
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from rest_framework.response import Response
from rest_framework import status

class CaptchaViewset(APIView) :
    @method_decorator(ratelimit(key='ip', rate='5/m', method='GET', block=True))
    def get (self,request):
        captcha = GuardPyCaptcha ()
        captcha = captcha.Captcha_generation(num_char=4 , only_num= True)
        return Response ({'captcha' : captcha} , status = status.HTTP_200_OK)

class OtpSejamViewset(APIView):
    
    pass