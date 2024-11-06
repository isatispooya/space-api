from .views import CompanyViewset
from django.urls import path

urlpatterns = [
    path('company/', CompanyViewset.as_view(), name='company'),
]
