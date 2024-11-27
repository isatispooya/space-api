from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

from positions.views import PositionViewset

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

# سرو فایل‌های استاتیک و مدیا در هر حالت
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)