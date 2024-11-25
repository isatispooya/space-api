from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from django.conf.urls.static import static
from . import settings
from positions.views import PositionViewset
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'positions', PositionViewset)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , include('user.urls')),
    path('' , include('authentication.urls')),
    path('' , include('access.urls')),
    path('' , include('companies.urls')),
    path('' , include(router.urls)),
    path('correspondence/', include('correspondence.urls')),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)