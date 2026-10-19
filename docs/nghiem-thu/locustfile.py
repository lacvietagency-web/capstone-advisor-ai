"""Nghiệm thu P0 #7 — kiểm thử tải bằng Locust: SV 85% · GV 12% · Khoa 3%, nghỉ 2–5 s giữa các thao tác.

Chạy trên bản sao (KHÔNG chạy vào máy thật), CSDL 1.000 SV / 60 GV / 300 đề tài:
    locust -f docs/nghiem-thu/locustfile.py --host http://127.0.0.1:8199 --headless -u 100 -r 10 -t 3m --csv out/u100
Mỗi người dùng ảo đăng nhập thật (lấy csrftoken rồi POST /dang-nhap/), sau đó đi các trang chính của vai mình.
"""

import random
import re

from locust import HttpUser, between, task

PASSWORD = "123456"
N_STUDENTS, N_LECTURERS = 1000, 60


def login(client, username):
    client.get("/dang-nhap/", name="/dang-nhap/ [GET]")
    token = client.cookies.get("csrftoken", "")
    with client.post(
        "/dang-nhap/",
        {"username": username, "password": PASSWORD, "csrfmiddlewaretoken": token},
        headers={"Referer": client.base_url + "/dang-nhap/"},
        name="/dang-nhap/ [POST]",
        allow_redirects=False,
        catch_response=True,
    ) as r:
        if r.status_code != 302:
            r.failure(f"đăng nhập {username} thất bại: {r.status_code}")


class Student(HttpUser):
    weight = 85
    wait_time = between(2, 5)

    def on_start(self):
        login(self.client, f"sv{random.randint(1, N_STUDENTS):03d}")
        self.topic_ids = []

    @task(3)
    def home(self):
        self.client.get("/trang-chu/", name="SV /trang-chu/")

    @task(3)
    def topics(self):
        r = self.client.get("/danh-sach-de-tai/?page=" + str(random.randint(1, 5)), name="SV /danh-sach-de-tai/")
        self.topic_ids = re.findall(r"/danh-sach-de-tai/(\d+)/", r.text) or self.topic_ids

    @task(2)
    def topic_detail(self):
        if self.topic_ids:
            self.client.get(f"/danh-sach-de-tai/{random.choice(self.topic_ids)}/", name="SV /danh-sach-de-tai/<id>/")

    @task(2)
    def preferences(self):
        self.client.get("/nguyen-vong/", name="SV /nguyen-vong/")

    @task(1)
    def profile(self):
        self.client.get("/ho-so/", name="SV /ho-so/")

    @task(1)
    def result(self):
        self.client.get("/ket-qua/", name="SV /ket-qua/")


class Lecturer(HttpUser):
    weight = 12
    wait_time = between(2, 5)

    def on_start(self):
        login(self.client, f"gv{random.randint(1, N_LECTURERS):03d}")
        self.own = []

    @task(2)
    def home(self):
        self.client.get("/trang-chu/", name="GV /trang-chu/")

    @task(2)
    def my_topics(self):
        r = self.client.get("/de-tai/", name="GV /de-tai/")
        self.own = re.findall(r"/de-tai/(\d+)/dang-ky/", r.text) or self.own

    @task(3)
    def registrations(self):
        if self.own:
            self.client.get(f"/de-tai/{random.choice(self.own)}/dang-ky/", name="GV /de-tai/<id>/dang-ky/")

    @task(1)
    def profile(self):
        self.client.get("/ho-so-giang-vien/", name="GV /ho-so-giang-vien/")


class Faculty(HttpUser):
    weight = 3
    wait_time = between(2, 5)

    def on_start(self):
        login(self.client, "khoa01")

    @task(2)
    def dashboard(self):
        self.client.get("/trang-chu/", name="Khoa /trang-chu/")

    @task(2)
    def allocation(self):
        self.client.get("/khoa/phan-cong/", name="Khoa /khoa/phan-cong/")

    @task(1)
    def statistics(self):
        self.client.get("/khoa/thong-ke/", name="Khoa /khoa/thong-ke/")
