from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import handler404
from ecomWebApp.views import *

urlpatterns = [
    path('admin/', include('adminApp.urls')),
    path('', include('ecomWebApp.urls') ),
    # path('<path>', Error404.as_view(), name='Error404'),

    path("__debug__/", include("debug_toolbar.urls")),

]+ static(settings.STATIC_URL,
           document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                        document_root=settings.MEDIA_ROOT)

