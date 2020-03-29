"""nuaaTimetable URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from timetable import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('home/', views.home),
    path('all_timetable/', views.all_timetable),
    path('pwd_edit/', views.pwd_edit),
    path('aao_login/', views.aao_logins),
]
