from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Company
from .serializers import CompanySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


class CompanyViewset(APIView):
    def post(self, request):
        permission_classes = [IsAuthenticated]
        data = request.data
        company = Company.objects.create(**data)
        serializer = CompanySerializer(company)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



