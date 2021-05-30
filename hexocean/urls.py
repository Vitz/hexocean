from django.contrib import admin
from django.urls import include, path
from . import views
from rest_framework import routers
from .views import *
from django.conf import settings
from django.conf.urls.static import static


router = routers.DefaultRouter()
router.register(r'f_imgs', ImageViewSet, basename='f_imgs')
router.register(r'links', LinkViewSet, basename='links')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('tmp/<uuid:uuid>/', views.get_temp_url, name="get_temp_url"),
    path('thumb/<uuid:uuid>/', views.get_thumb_url, name="get_thumb_url"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)