"""music URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from soundsofmusic import views as v
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', v.home),
    path('home', v.home),
    path('lessons', v.lessons),
    path('bass\lesson1.html', v.lessons),
    path('blesson1', v.blesson1),
    path('capture', v.capture),
    path('progress', v.progress),
    path('rewards', v.rewards),
    path('login', v.login),
    path('signup', v.signup),
    path('signup_good', v.signup_good),
    path('external/', v.external),
    path('listen', v.listen),
    path('output',v.output)
]

urlpatterns += staticfiles_urlpatterns()
#+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)