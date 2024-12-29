from .views import PermissionListView , SetUserPermissionView , PermissionListForUserView
from django.urls import path

urlpatterns = [
    path('permissions/', PermissionListView.as_view(), name='permission-list'),
    path('set-user-permission/', SetUserPermissionView.as_view(), name='set-user-permission'),
    path('permissions-for-user/', PermissionListForUserView.as_view(), name='permissions-for-user'),
]

