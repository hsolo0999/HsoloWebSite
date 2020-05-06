"""webapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from .views import start, about


urlpatterns = [
    path('admin/', admin.site.urls),
    path('parserapp/', include('parserapp.urls')),
    path('notebook/', include('notebook.urls')),
    path('', start, name='app_start'),
    path('accounts/', include('allauth.urls')),
    path('captcha/', include('captcha.urls')),
    path('about/', about, name='wa_about')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
