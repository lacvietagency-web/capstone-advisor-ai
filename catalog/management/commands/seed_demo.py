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
from catalog.models import (
    Course,
    Field,
    Lecturer,
    Major,
    Preference,
    RegistrationPeriod,
    Skill,
    Student,
    StudentCourseResult,
    StudentInterest,
    StudentSkill,
    Topic,
    TopicPrerequisite,
    TopicSkill,
)
from recommend.engine import Profile, eligible

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
COURSES = [
    ("INT1001", "Lập trình cơ bản", "Phần mềm doanh nghiệp"),
    ("INT2002", "Cơ sở dữ liệu", "Dữ liệu"),
    ("INT2003", "Lập trình Web", "Web"),
    ("INT3004", "Trí tuệ nhân tạo", "Trí tuệ nhân tạo"),
    ("INT3005", "Học máy", "Trí tuệ nhân tạo"),
    ("INT2006", "Mạng máy tính", "Hệ thống & Mạng"),
    ("INT3007", "Lập trình di động", "Di động"),
    ("INT3008", "An toàn thông tin", "An toàn thông tin"),
    ("INT2009", "Phân tích thiết kế hệ thống", "Phần mềm doanh nghiệp"),
    ("INT3010", "Hệ thống nhúng", "IoT"),
]
TOPIC_PATTERNS = {
    "Web": ["Website thương mại điện tử {x}", "Hệ thống quản lý {x} trên nền web", "Cổng thông tin {x}"],
    "Trí tuệ nhân tạo": [
        "Chatbot hỗ trợ {x} ứng dụng LLM",
        "Hệ thống gợi ý {x} bằng học máy",
        "Nhận diện {x} bằng học sâu",
    ],
    "Dữ liệu": ["Phân tích dữ liệu {x} và trực quan hóa", "Kho dữ liệu và báo cáo {x}"],
    "Di động": ["Ứng dụng di động quản lý {x}", "Ứng dụng Flutter hỗ trợ {x}"],
    "Hệ thống & Mạng": ["Giám sát hệ thống mạng {x}", "Triển khai hạ tầng {x} bằng container"],
    "An toàn thông tin": ["Phát hiện tấn công {x}", "Đánh giá bảo mật {x}"],
    "IoT": ["Hệ thống IoT giám sát {x}", "Nhà thông minh điều khiển {x}"],
    "Phần mềm doanh nghiệp": ["Phần mềm quản lý {x} cho doanh nghiệp", "Hệ thống ERP mini cho {x}"],
}
OBJECTS = [
    "bán hàng",
    "thư viện",
    "phòng khám",
    "ký túc xá",
    "chuỗi cà phê",
    "nhân sự",
    "kho hàng",
    "tuyển sinh",
    "giao thông",
    "nông nghiệp",
    "khách sạn",
    "học tập trực tuyến",
    "sự kiện",
    "bãi đỗ xe",
    "điểm danh",
]
LAST = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Vũ", "Đặng", "Bùi", "Đỗ", "Ngô"]
MID = ["Văn", "Thị", "Đức", "Minh", "Hoàng", "Thu", "Quang", "Ngọc"]
FIRST = [
    "An",
    "Bình",
    "Cường",
    "Dũng",
    "Giang",
    "Hà",
    "Hùng",
    "Lan",
    "Long",
    "Mai",
    "Nam",
    "Phúc",
    "Quân",
    "Sơn",
    "Thành",
    "Trang",
    "Tuấn",
    "Vy",
    "Yến",
    "Kiên",
]
CAREERS = [
    "Backend Developer",
    "Frontend Developer",
    "AI Engineer",
    "Data Analyst",
    "Mobile Developer",
    "DevOps Engineer",
    "Security Analyst",
    "Business Analyst",
]


BUSINESS_MODELS = (
    Preference,
    TopicSkill,
    TopicPrerequisite,
    Topic,
    StudentSkill,
    StudentInterest,
    StudentCourseResult,
    Student,
    Lecturer,
    RegistrationPeriod,
    Skill,
    Course,
    Field,
    Major,
)


class Command(BaseCommand):
    help = "Tạo dữ liệu mô phỏng (xoá dữ liệu nghiệp vụ cũ, giữ tài khoản admin)."

    def add_arguments(self, parser):
        parser.add_argument("--students", type=int, default=100)
        parser.add_argument("--lecturers", type=int, default=15)
        parser.add_argument("--topics", type=int, default=50)
        parser.add_argument("--seed", type=int, default=42)

    @transaction.atomic
    def handle(self, *args, **o):
        self.rnd = random.Random(o["seed"])
        self.extra = random.Random(
            o["seed"] + 1
        )  # riêng cho các trường V3.5 → dữ liệu cũ (và kết quả phân công) không đổi
        self._reset()
        # tài khoản Khoa demo (khớp gợi ý ở trang đăng nhập); admin superuser vẫn giữ nguyên
        kh, _ = User.objects.update_or_create(
            username="khoa01",
            defaults=dict(
                role=User.Role.ADMIN,
                last_name="Cán bộ",
                first_name="Khoa",
                is_active=True,
                is_staff=True,
                is_superuser=True,
            ),
        )
        kh.set_password("123456")
        kh.save()
        self._catalog()
        lecturers = [self._lecturer(i) for i in range(1, o["lecturers"] + 1)]
        topics = [self._topic(i, self.rnd.choice(lecturers)) for i in range(o["topics"])]
        # mức "hot" của đề tài theo luật lũy thừa: vài đề tài rất được săn đón, phần lớn ít người chọn
        hotness = [1 / (k + 1) ** 1.2 for k in range(len(topics))]
        self.rnd.shuffle(hotness)
        period = RegistrationPeriod.objects.create(
            name="Đợt đăng ký ĐATN 2026",
            start_at=timezone.now() - timedelta(days=3),
            end_at=timezone.now() + timedelta(days=11),
        )
        for i in range(1, o["students"] + 1):
            self._student(i, topics, hotness, period)
        top = sorted(((Preference.objects.filter(topic=t, rank=1).count(), t.title) for t in topics), reverse=True)[:5]
        self.stdout.write(
            self.style.SUCCESS(
                f"Đã tạo {o['students']} SV, {o['lecturers']} GV, {o['topics']} đề tài, {len(self.skills)} kỹ năng. "
                f"Đề tài hot nhất (số NV1): {top}. Mật khẩu mọi tài khoản demo: 123456 (sv001, gv001, khoa01)"
            )
        )

    def _reset(self):
        User.objects.filter(is_superuser=False).delete()
        for model in BUSINESS_MODELS:
            model.objects.all().delete()

    def _catalog(self):
        self.major = Major.objects.create(name="Công nghệ thông tin")
        self.fields = {name: Field.objects.create(name=name) for name in FIELDS}
        self.skills = {s: Skill.objects.create(name=s, field=self.fields[f]) for f, ss in FIELDS.items() for s in ss}
        self.courses = {c: Course.objects.create(code=c, name=n, field=self.fields[f]) for c, n, f in COURSES}
        self.course_field = {c: f for c, _, f in COURSES}

    def _person(self, prefix, i, role):
        return User.objects.create_user(
            f"{prefix}{i:03d}",
            password="123456",
            role=role,
            last_name=f"{self.rnd.choice(LAST)} {self.rnd.choice(MID)}",
            first_name=self.rnd.choice(FIRST),
        )

    def _lecturer(self, i):
        user = self._person("gv", i, User.Role.LECTURER)
        # GV trùng họ tên trông như lỗi nhân đôi trong thống kê → đổi tên, không dùng rnd để giữ nguyên dữ liệu còn lại
        taken = {(u.last_name, u.first_name) for u in User.objects.filter(role=User.Role.LECTURER).exclude(pk=user.pk)}
        if (user.last_name, user.first_name) in taken:
            user.first_name = next(f for f in FIRST if (user.last_name, f) not in taken)
            user.save(update_fields=["first_name"])
        lec = Lecturer.objects.create(
            user=user,
            max_students=self.rnd.choice([4, 5, 6, 8]),
        )
        lec.fields.set(self.rnd.sample(list(self.fields.values()), 2))
        fill_lecturer_details(lec, self.extra)
        return lec

    def _unique_title(self, title, skill):
        """Tên đề tài không trùng mà không cần đánh số "(12)": bản trùng được ghi rõ hướng công nghệ.

        Không rút thêm số ngẫu nhiên → dữ liệu demo (và các chỉ số phân công) giữ nguyên như trước.
        """
        if not Topic.objects.filter(title=title).exists():
            return title
        k, candidate = 2, f"{title} — hướng {skill}"
        while Topic.objects.filter(title=candidate).exists():
            candidate, k = f"{title} — hướng {skill}, nhóm {k}", k + 1
        return candidate

    def _topic(self, i, lec):
        rnd = self.rnd
        f = rnd.choice(list(lec.fields.all()))
        title = rnd.choice(TOPIC_PATTERNS[f.name]).format(x=rnd.choice(OBJECTS))
        used = ", ".join(rnd.sample(FIELDS[f.name], min(2, len(FIELDS[f.name]))))
        t = Topic.objects.create(
            lecturer=lec,
            title=self._unique_title(title, used.split(", ")[0]),
            difficulty=rnd.choice([1, 2, 2, 3]),
            description=f"Xây dựng {title.lower()}. Đề tài thuộc lĩnh vực {f.name}, yêu cầu vận dụng {used}.",
            min_gpa=rnd.choice([0, 2.0, 2.5]),
            capacity=rnd.choice([1, 1, 2]),
        )
        t.fields.set([f] + ([rnd.choice(list(self.fields.values()))] if rnd.random() < 0.3 else []))
        for s in rnd.sample(FIELDS[f.name], min(3, len(FIELDS[f.name]))):
            TopicSkill.objects.create(
                topic=t, skill=self.skills[s], required_level=rnd.randint(2, 4), is_mandatory=rnd.random() < 0.25
            )
        same_field = [c for c, cf in self.course_field.items() if cf == f.name]
        if same_field and rnd.random() < 0.6:
            TopicPrerequisite.objects.create(topic=t, course=self.courses[same_field[0]], min_score=5)
        fill_topic_details(t)
        return t

    def _student(self, i, topics, hotness, period):
        rnd = self.rnd
        focus = rnd.sample(list(FIELDS), 2)
        st = Student.objects.create(
            user=self._person("sv", i, User.Role.STUDENT),
            student_code=f"2023{i:04d}",
            major=self.major,
            gpa=round(min(4, max(1.5, rnd.gauss(2.8, 0.5))), 2),
            about=f"Em thích {focus[0].lower()} và {focus[1].lower()}, muốn làm "
            f"{rnd.choice(CAREERS)}. Đã làm đồ án môn về {rnd.choice(OBJECTS)}.",
        )
        st.user.email = f"{st.student_code}@sv.capstone.edu.vn"  # email demo theo MSSV, không rút thêm số ngẫu nhiên
        st.user.save(update_fields=["email"])
        for f in focus:
            StudentInterest.objects.create(student=st, field=self.fields[f], level=rnd.randint(2, 3))
            for s in rnd.sample(FIELDS[f], min(3, len(FIELDS[f]))):
                StudentSkill.objects.create(student=st, skill=self.skills[s], level=rnd.randint(1, 5))
        for c in rnd.sample(list(self.courses.values()), 6):
            score = round(min(10, max(3, rnd.gauss(7, 1.3))), 1)
            StudentCourseResult.objects.create(student=st, course=c, score=score)
        # SV chỉ đăng ký được đề tài đủ điều kiện (lọc cứng như form thật); đề tài hot dễ được chọn hơn
        profile = Profile(st)
        pool = [(t, h) for t, h in zip(topics, hotness, strict=True) if eligible(profile, t)[0]]
        chosen = []
        while pool and len(chosen) < 3:
            t = rnd.choices([t for t, _ in pool], weights=[h for _, h in pool])[0]
            chosen.append(t)
            pool = [(x, h) for x, h in pool if x != t]
        for rank, t in enumerate(chosen, 1):
            Preference.objects.create(student=st, topic=t, period=period, rank=rank, submitted_at=timezone.now())


TITLES = ["ThS.", "ThS.", "TS.", "TS.", "PGS.TS."]


DEPARTMENTS = {
    "Web": "Công nghệ phần mềm",
    "Di động": "Công nghệ phần mềm",
    "Trí tuệ nhân tạo": "Khoa học máy tính",
    "Dữ liệu": "Hệ thống thông tin",
    "Phần mềm doanh nghiệp": "Hệ thống thông tin",
    "Hệ thống & Mạng": "Mạng máy tính",
    "An toàn thông tin": "An toàn thông tin",
    "IoT": "Kỹ thuật máy tính",
}


def fill_lecturer_details(lec, rnd):
    """Học hàm, bộ môn (theo lĩnh vực đầu), SĐT, giới thiệu, từ khoá cho GV demo. Bộ sinh số riêng."""
    names = [f.name for f in lec.fields.order_by("pk")]
    lec.department = DEPARTMENTS.get(names[0], "Công nghệ phần mềm") if names else "Công nghệ phần mềm"
    lec.academic_title = rnd.choice(TITLES)
    lec.phone = "09" + "".join(str(rnd.randint(0, 9)) for _ in range(8))
    lec.bio = (
        f"Giảng viên {lec.department}, hướng nghiên cứu {', '.join(names).lower()}; hướng dẫn đồ án ứng dụng thực tế."
    )
    lec.keywords = ", ".join(n.lower() for n in names)
    lec.save(update_fields=["department", "academic_title", "phone", "bio", "keywords"])


def fill_topic_details(topic):
    """Mục tiêu + công nghệ gợi ý mặc định cho đề tài demo (lấy từ kỹ năng yêu cầu) khi chưa có bản do AI viết."""
    skills = [ts.skill.name for ts in topic.skills.select_related("skill")]
    topic.objectives = (
        f"Xây dựng sản phẩm {topic.title.lower()} chạy được, có tài liệu thiết kế và kiểm thử; "
        f"đánh giá trên dữ liệu thực tế của bài toán."
    )
    topic.technologies = ", ".join(skills)[:255]
    topic.save(update_fields=["objectives", "technologies"])
