from django.shortcuts import render
from rest_framework.views import APIView
# from GuardPyCaptcha.Captcha import GuardPyCaptcha
from django.utils.decorators import method_decorator
# from ratelimit.decorators import ratelimit
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
import random
from datetime import timedelta
from .models import User , Otp
import json
import requests
import os
from rest_framework.permissions import AllowAny


# class CaptchaViewset(APIView) :
#     @method_decorator(ratelimit(key='ip', rate='5/m', method='GET', block=True))
#     def get (self,request):
#         captcha = GuardPyCaptcha ()
#         captcha = captcha.Captcha_generation(num_char=4 , only_num= True)
#         return Response ({'captcha' : captcha} , status = status.HTTP_200_OK)

class OtpSejamViewset(APIView):
    permission_classes = [AllowAny]
    # @method_decorator(ratelimit(key='ip', rate='5/m', method='POST', block=True))
    def post(self, request):
        uniqueIdentifier = request.data['uniqueIdentifier']
        if not uniqueIdentifier :
            return Response ({'message' : 'کد ملی را وارد کنید'} , status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter (uniqueIdentifier = uniqueIdentifier).first()
        if not user:
            url = "http://31.40.4.92:8870/otp"
            payload = json.dumps({
            "uniqueIdentifier": uniqueIdentifier
            })
            headers = {
            'X-API-KEY': os.getenv('X-API-KEY'),
            'Content-Type': 'application/json'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            if response.status_code >=300 :
                return Response ({'message' :'شما سجامی نیستید'} , status=status.HTTP_400_BAD_REQUEST)
            return Response ({'registered' :False , 'message' : 'کد تایید ارسال شد'},status=status.HTTP_200_OK)

        return Response({'message' : 'اطلاعات شما یافت نشد'},status=status.HTTP_400_BAD_REQUEST)   
                


class RegisterViewset(APIView):
    def post(self, request):
        
        return Response(True, status=status.HTTP_201_CREATED)
