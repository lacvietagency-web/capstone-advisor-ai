from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import TemplateView

from accounts.views import CaiDatView, home, root
from allocate import views as av
from assistant import views as asv
from catalog import views as cv
from reports import views as rv

urlpatterns = [
    path("", root),
    path("trang-chu/", home, name="home"),
    path("dang-nhap/", auth_views.LoginView.as_view(), name="login"),
    path("trinh-bay/", rv.trinh_bay, name="trinh_bay"),  # trang trình bày cho GVHD, công khai
    path("gop-y/", rv.gop_y, name="gop_y"),
    path("dang-xuat/", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "doi-mat-khau/",
        CaiDatView.as_view(),  # trang Cài đặt: email nhận thông báo + đổi mật khẩu
        name="password_change",
    ),
    path(
        "doi-mat-khau/xong/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="registration/password_change_done.html",
        ),
        name="password_change_done",
    ),
    path("ho-so/", cv.student_profile, name="student_profile"),
    path("nguyen-vong/", cv.student_preferences, name="student_preferences"),
    path("ket-qua/", av.student_allocation_result, name="student_allocation_result"),
    path("de-tai/", cv.lecturer_topics, name="lecturer_topics"),
    path("de-tai/them/", cv.lecturer_topic_edit, name="lecturer_topic_new"),
    path("de-tai/nhap-excel/", cv.lecturer_topic_import, name="lecturer_topic_import"),
    path("de-tai/nhap-excel/mau.xlsx", cv.lecturer_import_sample, name="lecturer_import_sample"),
    path("de-tai/<int:pk>/sua/", cv.lecturer_topic_edit, name="lecturer_topic_edit"),
    path("de-tai/<int:pk>/dang-ky/", cv.lecturer_registrations, name="lecturer_registrations"),
    path("khoa/phan-cong/", av.allocation_dashboard, name="allocation_dashboard"),
    path(
        "khoa/phan-cong/<int:period_id>/sinh-vien/<int:student_id>/",
        av.allocation_student_detail,
        name="allocation_student_detail",
    ),
    path("khoa/nhap-excel/", cv.faculty_import, name="faculty_import"),
    path("khoa/nhap-excel/mau.xlsx", cv.faculty_import_sample, name="faculty_import_sample"),
    path("khoa/thong-ke/", rv.faculty_statistics, name="faculty_statistics"),
    path("khoa/ra-soat-trung-lap/", cv.faculty_duplicates, name="faculty_duplicates"),
    path("ho-so-giang-vien/", cv.lecturer_profile, name="lecturer_profile"),
    path("ho-so-giang-vien/<int:pk>/", cv.lecturer_profile, name="lecturer_profile_detail"),
    path("danh-sach-de-tai/", cv.topic_list, name="topic_list"),
    path("danh-sach-de-tai/<int:pk>/", cv.topic_detail, name="topic_detail"),
    path("tro-ly/hoi/", asv.ask, name="assistant_ask"),
    path("quan-tri/", admin.site.urls),
]

if settings.DEBUG:  # trang mẫu thành phần ATLAS cho đội giao diện
    urlpatterns.append(path("mau-giao-dien/", TemplateView.as_view(template_name="styleguide.html")))
