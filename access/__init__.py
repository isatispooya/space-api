from .views import PermissionListView
from django.urls import path

urlpatterns = [
    path('permissions/', PermissionListView.as_view(), name='permission-list'),
]
