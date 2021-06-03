from django.contrib import admin
from django.contrib.staticfiles.urls import static
from django.urls import path, include
import Qapp.views as Qapp

from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Qapp.urls')),
    path('accounts/', include('allauth.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
