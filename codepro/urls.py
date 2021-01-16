"""codepro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path,include
from rest_framework import routers
from vaccine import views

router = routers.DefaultRouter()


router.register(r"volunteerdashboard",views.VolunteerDashboard,basename='voluneteerdashboard')
router.register(r"volunteerregister",views.Register,basename = 'register')
router.register(r"volunteerlogin",views.LoginViewSet,basename = 'login')
router.register(r"vaccine/all-result",views.AllResult,basename = 'vaccine')
router.register(r"vaccine/result",views.Result,basename = 'result')
router.register(r"makerregister",views.RegisterMakerViewset,basename = 'makerregister')
router.register(r"makerlogin",views.LoginMakerViewset,basename = 'makerlogin')
router.register(r"makerdashboard",views.MakerDashboard,basename = 'makerdashboard')
router.register(r"makerdashboardfull",views.MakerDashboardFull,basename = 'makerdashboardfull')
urlpatterns = [
    path(r"admin/", admin.site.urls),
    path(r"", include(router.urls)),
    #path(r"result",views.Filter_Data.as_view()),
    #path(r"login",views.Login),
]
