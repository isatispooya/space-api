from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from transactions.models import Payment

# SEP
class VerfiyTransactionSepView(APIView):
    def post(self , request):
        
        pass
        
