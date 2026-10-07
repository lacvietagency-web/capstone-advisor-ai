from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from accounts.views import home, root
from allocate import views as av
from catalog import views as cv
from reports import views as rv

urlpatterns = [
    path("", root),
    path("trang-chu/", home, name="home"),
    path("dang-nhap/", auth_views.LoginView.as_view(), name="login"),
    path("dang-xuat/", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "doi-mat-khau/",
        auth_views.PasswordChangeView.as_view(
            template_name="registration/password_change_form.html",
        ),
        name="password_change",
    ),
    path(
        "doi-mat-khau/xong/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="registration/password_change_done.html",
        ),
        name="password_change_done",
    ),
    path(
        "doi-mat-khau/",
        auth_views.PasswordChangeView.as_view(
            template_name="registration/password_change_form.html",
        ),
        name="doi_mat_khau",
    ),
    path(
        "doi-mat-khau/xong/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="registration/password_change_done.html",
        ),
        name="doi_mat_khau_done",
    ),
    path("ho-so/", cv.student_profile, name="student_profile"),
    path("nguyen-vong/", cv.student_preferences, name="student_preferences"),
    path("ket-qua/", av.student_allocation_result, name="student_allocation_result"),
    path("de-tai/", cv.lecturer_topics, name="lecturer_topics"),
    path("de-tai/them/", cv.lecturer_topic_edit, name="lecturer_topic_new"),
    path("de-tai/<int:pk>/sua/", cv.lecturer_topic_edit, name="lecturer_topic_edit"),
    path("de-tai/<int:pk>/dang-ky/", cv.lecturer_registrations, name="lecturer_registrations"),
    path("khoa/phan-cong/", av.allocation_dashboard, name="allocation_dashboard"),
    path("khoa/nhap-excel/", cv.faculty_import, name="faculty_import"),
    path("khoa/nhap-excel/mau.xlsx", cv.faculty_import_sample, name="faculty_import_sample"),
    path("khoa/thong-ke/", rv.faculty_statistics, name="faculty_statistics"),
    path("ho-so-giang-vien/", cv.lecturer_profile, name="lecturer_profile"),
    path("ho-so-giang-vien/<int:pk>/", cv.lecturer_profile, name="lecturer_profile_detail"),
    path("danh-sach-de-tai/", cv.topic_list, name="topic_list"),
    path("danh-sach-de-tai/<int:pk>/", cv.topic_detail, name="topic_detail"),
    path("quan-tri/", admin.site.urls),
]
