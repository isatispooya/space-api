from django.urls import path , include
from .views import UserLoginLogView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'', UserLoginLogView, basename='user_login_log')

urlpatterns = [
    path('', include(router.urls)),
    path('userloginlog/logout/', UserLoginLogView.as_view({'post': 'logout'}), name='user-logout'),
]
