from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from accounts.views import home, root
from catalog import views as cv

urlpatterns = [
    path("", root),
    path("trang-chu/", home, name="home"),
    path("dang-nhap/", auth_views.LoginView.as_view(), name="login"),
    path("dang-xuat/", auth_views.LogoutView.as_view(), name="logout"),
    path("ho-so/", cv.student_profile, name="student_profile"),
    path("nguyen-vong/", cv.student_preferences, name="student_preferences"),
    path("de-tai/", cv.lecturer_topics, name="lecturer_topics"),
    path("de-tai/them/", cv.lecturer_topic_edit, name="lecturer_topic_new"),
    path("de-tai/<int:pk>/sua/", cv.lecturer_topic_edit, name="lecturer_topic_edit"),
    path("de-tai/<int:pk>/dang-ky/", cv.lecturer_registrations, name="lecturer_registrations"),
    path("quan-tri/", admin.site.urls),
]
