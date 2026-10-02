from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from accounts.views import home, root

urlpatterns = [
    path("", root),
    path("trang-chu/", home, name="home"),
    path("dang-nhap/", auth_views.LoginView.as_view(), name="login"),
    path("dang-xuat/", auth_views.LogoutView.as_view(), name="logout"),
    path("quan-tri/", admin.site.urls),
]
