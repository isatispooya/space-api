from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Correspondence
from .serializers import CorrespondenceSerializer

class CorrespondenceSenderViewset(viewsets.ModelViewSet):
    # تنظیمات ویوست رو اینجا قرار بدید
    pass

class CorrespondenceReceiverViewset(viewsets.ModelViewSet):
    # تنظیمات ویوست رو اینجا قرار بدید
    pass

 