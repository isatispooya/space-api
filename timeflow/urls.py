from django.urls import path , include
from .views import UserLoginLogView , LogoutView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'', UserLoginLogView, basename='user_login_log')

urlpatterns = [
    path('', include(router.urls)),
    path('logout/', LogoutView.as_view(), name='user-logout'),
]
