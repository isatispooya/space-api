from .views import  CaptchaViewset, GroupManagementViewSet , UserToGroupViewSet
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    
)
urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('captcha/', CaptchaViewset.as_view(), name='captcha'),
    path('groups/', GroupManagementViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='group-list'),
    
    path('groups/<int:pk>/', GroupManagementViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='group-detail'),
    path('user-to-group/', UserToGroupViewSet.as_view({'post': 'assign_group'}), name='user-to-group'),
]


