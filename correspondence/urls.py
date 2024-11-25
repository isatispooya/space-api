from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CorrespondenceSenderViewset, CorrespondenceReceiverViewset

router = DefaultRouter()
router.register(r'sender', CorrespondenceSenderViewset, basename='sender-correspondence')
router.register(r'receiver', CorrespondenceReceiverViewset, basename='receiver-correspondence')

urlpatterns = [
    path('', include(router.urls)),
]