"""Tạo dữ liệu mô phỏng để chạy thử và làm thực nghiệm.

    python manage.py seed_demo                  # 100 SV, 15 GV, 50 đề tài
    python manage.py seed_demo --students 300   # quy mô lớn hơn

Đặc điểm quan trọng: khoảng 20% đề tài "hot" nhận khoảng 80% nguyện vọng 1 (luật lũy thừa), giống thực tế,
để bài toán phân công có tranh chấp thật. Cùng --seed thì luôn ra cùng một bộ dữ liệu (tái lập được thực nghiệm).
Dữ liệu này CHỈ để kiểm thử kỹ thuật và đo phân công, không dùng làm bằng chứng độ chính xác gợi ý.
"""
import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from accounts.models import User
from catalog.models import (Course, Field, Lecturer, Major, Preference, RegistrationPeriod, Skill, Student,
                            StudentCourseResult, StudentInterest, StudentSkill, Topic, TopicPrerequisite, TopicSkill)

FIELDS = {
    "Web": ["HTML/CSS", "JavaScript", "React", "Django", "Spring Boot", "PHP"],
    "Trí tuệ nhân tạo": ["Python", "Machine Learning", "Deep Learning", "NLP", "LLM/Prompt"],
    "Dữ liệu": ["SQL", "MySQL", "Pandas", "Power BI", "Big Data"],
    "Di động": ["Flutter/Dart", "Android/Kotlin", "React Native"],
    "Hệ thống & Mạng": ["Linux", "Docker", "Windows Server", "Mạng máy tính"],
    "An toàn thông tin": ["Bảo mật web", "Mật mã học", "Pentest"],
    "IoT": ["Arduino/ESP32", "C/C++", "MQTT"],
    "Phần mềm doanh nghiệp": ["Java", "Phân tích thiết kế hệ thống", "UML", "Kiểm thử phần mềm"],
}
COURSES = [("INT1001", "Lập trình cơ bản", "Phần mềm doanh nghiệp"), ("INT2002", "Cơ sở dữ liệu", "Dữ liệu"),
           ("INT2003", "Lập trình Web", "Web"), ("INT3004", "Trí tuệ nhân tạo", "Trí tuệ nhân tạo"),
           ("INT3005", "Học máy", "Trí tuệ nhân tạo"), ("INT2006", "Mạng máy tính", "Hệ thống & Mạng"),
           ("INT3007", "Lập trình di động", "Di động"), ("INT3008", "An toàn thông tin", "An toàn thông tin"),
           ("INT2009", "Phân tích thiết kế hệ thống", "Phần mềm doanh nghiệp"), ("INT3010", "Hệ thống nhúng", "IoT")]
TOPIC_PATTERNS = {
    "Web": ["Website thương mại điện tử {x}", "Hệ thống quản lý {x} trên nền web", "Cổng thông tin {x}"],
    "Trí tuệ nhân tạo": ["Chatbot hỗ trợ {x} ứng dụng LLM", "Hệ thống gợi ý {x} bằng học máy", "Nhận diện {x} bằng học sâu"],
    "Dữ liệu": ["Phân tích dữ liệu {x} và trực quan hóa", "Kho dữ liệu và báo cáo {x}"],
    "Di động": ["Ứng dụng di động quản lý {x}", "Ứng dụng Flutter hỗ trợ {x}"],
    "Hệ thống & Mạng": ["Giám sát hệ thống mạng {x}", "Triển khai hạ tầng {x} bằng container"],
    "An toàn thông tin": ["Phát hiện tấn công {x}", "Đánh giá bảo mật {x}"],
    "IoT": ["Hệ thống IoT giám sát {x}", "Nhà thông minh điều khiển {x}"],
    "Phần mềm doanh nghiệp": ["Phần mềm quản lý {x} cho doanh nghiệp", "Hệ thống ERP mini cho {x}"],
}
OBJECTS = ["bán hàng", "thư viện", "phòng khám", "ký túc xá", "chuỗi cà phê", "nhân sự", "kho hàng", "tuyển sinh",
           "giao thông", "nông nghiệp", "khách sạn", "học tập trực tuyến", "sự kiện", "bãi đỗ xe", "điểm danh"]
LAST = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Vũ", "Đặng", "Bùi", "Đỗ", "Ngô"]
MID = ["Văn", "Thị", "Đức", "Minh", "Hoàng", "Thu", "Quang", "Ngọc"]
FIRST = ["An", "Bình", "Cường", "Dũng", "Giang", "Hà", "Hùng", "Lan", "Long", "Mai", "Nam", "Phúc", "Quân", "Sơn",
         "Thành", "Trang", "Tuấn", "Vy", "Yến", "Kiên"]
CAREERS = ["Backend Developer", "Frontend Developer", "AI Engineer", "Data Analyst", "Mobile Developer",
           "DevOps Engineer", "Security Analyst", "Business Analyst"]


class Command(BaseCommand):
    help = "Tạo dữ liệu mô phỏng (xoá dữ liệu nghiệp vụ cũ, giữ tài khoản admin)."

    def add_arguments(self, parser):
        parser.add_argument("--students", type=int, default=100)
        parser.add_argument("--lecturers", type=int, default=15)
        parser.add_argument("--topics", type=int, default=50)
        parser.add_argument("--seed", type=int, default=42)

    @transaction.atomic
    def handle(self, *args, **o):
        rnd = random.Random(o["seed"])
        User.objects.filter(is_superuser=False).delete()
        for m in (Preference, TopicSkill, TopicPrerequisite, Topic, StudentSkill, StudentInterest, StudentCourseResult,
                  Student, Lecturer, RegistrationPeriod, Skill, Course, Field, Major):
            m.objects.all().delete()

        major = Major.objects.create(name="Công nghệ thông tin")
        fields = {name: Field.objects.create(name=name) for name in FIELDS}
        skills = {s: Skill.objects.create(name=s, field=fields[f]) for f, ss in FIELDS.items() for s in ss}
        courses = {c: Course.objects.create(code=c, name=n, field=fields[f]) for c, n, f in COURSES}

        def person(prefix, i, role):
            u = User.objects.create_user(f"{prefix}{i:03d}", password="123456", role=role,
                                         last_name=f"{rnd.choice(LAST)} {rnd.choice(MID)}", first_name=rnd.choice(FIRST))
            return u

        lecturers = []
        for i in range(1, o["lecturers"] + 1):
            lec = Lecturer.objects.create(user=person("gv", i, User.Role.LECTURER), department="Khoa CNTT",
                                          max_students=rnd.choice([4, 5, 6, 8]))
            lec.fields.set(rnd.sample(list(fields.values()), 2))
            lecturers.append(lec)

        topics = []
        for i in range(o["topics"]):
            lec = rnd.choice(lecturers); f = rnd.choice(list(lec.fields.all()))
            title = rnd.choice(TOPIC_PATTERNS[f.name]).format(x=rnd.choice(OBJECTS))
            t = Topic.objects.create(lecturer=lec, title=f"{title} ({i + 1})", difficulty=rnd.choice([1, 2, 2, 3]),
                                     description=f"Xây dựng {title.lower()}. Đề tài thuộc lĩnh vực {f.name}, yêu cầu "
                                                 f"vận dụng {', '.join(rnd.sample(FIELDS[f.name], min(2, len(FIELDS[f.name]))))}.",
                                     min_gpa=rnd.choice([0, 2.0, 2.5]), capacity=rnd.choice([1, 1, 2]))
            t.fields.set([f] + ([rnd.choice(list(fields.values()))] if rnd.random() < 0.3 else []))
            for s in rnd.sample(FIELDS[f.name], min(3, len(FIELDS[f.name]))):
                TopicSkill.objects.create(topic=t, skill=skills[s], required_level=rnd.randint(2, 4),
                                          is_mandatory=rnd.random() < 0.25)
            fc = [c for c, (_, _, cf) in zip(courses, COURSES) if cf == f.name]
            if fc and rnd.random() < 0.6:
                TopicPrerequisite.objects.create(topic=t, course=courses[fc[0]], min_score=5)
            topics.append(t)

        # mức "hot" của đề tài theo luật lũy thừa: vài đề tài rất được săn đón, phần lớn ít người chọn
        hotness = [1 / (k + 1) ** 1.2 for k in range(len(topics))]; rnd.shuffle(hotness)
        period = RegistrationPeriod.objects.create(name="Đợt đăng ký ĐATN 2026", start_at=timezone.now() - timedelta(days=3),
                                                   end_at=timezone.now() + timedelta(days=11))
        for i in range(1, o["students"] + 1):
            focus = rnd.sample(list(FIELDS), 2)
            st = Student.objects.create(user=person("sv", i, User.Role.STUDENT), student_code=f"2023{i:04d}", major=major,
                                        gpa=round(min(4, max(1.5, rnd.gauss(2.8, 0.5))), 2),
                                        about=f"Em thích {focus[0].lower()} và {focus[1].lower()}, muốn làm "
                                              f"{rnd.choice(CAREERS)}. Đã làm đồ án môn về {rnd.choice(OBJECTS)}.")
            for f in focus:
                StudentInterest.objects.create(student=st, field=fields[f], level=rnd.randint(2, 3))
                for s in rnd.sample(FIELDS[f], min(3, len(FIELDS[f]))):
                    StudentSkill.objects.create(student=st, skill=skills[s], level=rnd.randint(1, 5))
            for c in rnd.sample(list(courses.values()), 6):
                StudentCourseResult.objects.create(student=st, course=c, score=round(min(10, max(3, rnd.gauss(7, 1.3))), 1))
            chosen = []
            while len(chosen) < 3:
                t = rnd.choices(topics, weights=hotness)[0]
                if t not in chosen:
                    chosen.append(t)
            for rank, t in enumerate(chosen, 1):
                Preference.objects.create(student=st, topic=t, period=period, rank=rank)

        top = sorted(((Preference.objects.filter(topic=t, rank=1).count(), t.title) for t in topics), reverse=True)[:5]
        self.stdout.write(self.style.SUCCESS(
            f"Đã tạo {o['students']} SV, {o['lecturers']} GV, {o['topics']} đề tài, {len(skills)} kỹ năng. "
            f"Đề tài hot nhất (số NV1): {top}. Mật khẩu mọi tài khoản demo: 123456 (sv001, gv001…)"))
