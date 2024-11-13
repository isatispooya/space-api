from django.urls import path
from .views import PositionViewset


urlpatterns = [
    path('positions/', PositionViewset.as_view(), name='position'),
]