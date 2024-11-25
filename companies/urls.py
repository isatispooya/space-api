from .views import CompanyViewset, CompanyDetailView 
from django.urls import path

urlpatterns = [
    path('company/', CompanyViewset.as_view(), name='company'),
    path('company/<int:id>/', CompanyDetailView.as_view(), name='company-detail'),

]
