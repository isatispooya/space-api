from django.shortcuts import render
from .models import Position
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny , IsAuthenticated  , IsAdminUser
from .serializers import PositionSerializer
from rest_framework.response import Response
from rest_framework import status



class PositionViewset(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):

        pass 

