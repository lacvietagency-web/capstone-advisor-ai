"""Nhập Sinh viên / Giảng viên / Đề tài / Kỹ năng từ file Excel [UC15] (tách khỏi services.py cho gọn).

Tuân thủ kiến trúc chia tầng: logic nghiệp vụ tập trung tại services.py,
view và command chỉ đóng vai trò điều phối.
"""

import re
import unicodedata
from decimal import Decimal, InvalidOperation
from io import BytesIO
from pathlib import Path

import openpyxl
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import transaction
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

from accounts.models import User
from catalog.models import Field, Lecturer, Major, Skill, Student, Topic

SHEET_ALIASES = {
    "SinhVien": {"sinhvien", "sinh vien", "sinh_vien", "sinh viên", "students", "student"},
    "GiangVien": {"giangvien", "giang vien", "giang_vien", "giảng viên", "lecturers", "lecturer"},
    "DeTai": {"detai", "de tai", "de_tai", "đề tài", "topics", "topic"},
    "KyNang": {"kynang", "ky nang", "ky_nang", "kỹ năng", "skills", "skill"},
}

COL_ALIASES = {
    "SinhVien": {
        "code": {"ma", "mã", "ma_sv", "mã sinh viên", "student_code", "code", "mssv", "masv"},
        "last_name": {"ho", "họ", "ho_dem", "họ đệm", "họ và tên đệm", "last_name"},
        "first_name": {"ten", "tên", "first_name"},
        "gpa": {"gpa", "diem", "điểm", "diem_gpa", "điểm gpa"},
        "email": {"email", "e-mail", "mail"},
        "major": {"chuyen_nganh", "chuyên ngành", "major", "nganh", "ngành"},
        "about": {"about", "gioi_thieu", "giới thiệu", "ghi_chu", "ghi chú"},
    },
    "GiangVien": {
        "code": {"ma", "mã", "ma_gv", "mã giảng viên", "username", "code", "msgv", "magv"},
        "last_name": {"ho", "họ", "ho_dem", "họ đệm", "last_name"},
        "first_name": {"ten", "tên", "first_name"},
        "email": {"email", "e-mail", "mail"},
        "department": {"bo_mon", "bộ môn", "khoa", "department"},
        "max_students": {"chi_tieu", "chỉ tiêu", "max_students", "so_sv_toi_da", "chỉ tiêu hướng dẫn"},
        "fields": {"linh_vuc", "lĩnh vực", "fields", "chuyen_mon", "chuyên môn"},
    },
    "DeTai": {
        "title": {"ten_de_tai", "tên đề tài", "tieu_de", "tiêu đề", "title", "de_tai", "đề tài"},
        "lecturer": {"ma_giang_vien", "mã giảng viên", "ma_gv", "magv", "giang_vien", "giảng viên", "lecturer"},
        "description": {"mo_ta", "mô tả", "description", "noi_dung", "nội dung"},
        "fields": {"linh_vuc", "lĩnh vực", "fields"},
        "difficulty": {"do_kho", "độ khó", "difficulty"},
        "min_gpa": {"gpa_toi_thieu", "gpa tối thiểu", "min_gpa", "diem_toi_thieu", "điểm tối thiểu"},
        "capacity": {"so_luong", "số lượng", "suc_chua", "sức chứa", "capacity", "so_sv", "số sinh viên tối đa"},
    },
    "KyNang": {
        "name": {"ten_ky_nang", "tên kỹ năng", "ky_nang", "kỹ năng", "name", "skill", "ten", "tên"},
        "field": {"linh_vuc", "lĩnh vực", "field", "thuoc_linh_vuc", "thuộc lĩnh vực"},
    },
}

DIFFICULTY_MAP = {
    "1": Topic.Difficulty.EASY,
    "2": Topic.Difficulty.MEDIUM,
    "3": Topic.Difficulty.HARD,
    "dễ": Topic.Difficulty.EASY,
    "de": Topic.Difficulty.EASY,
    "trung bình": Topic.Difficulty.MEDIUM,
    "trung binh": Topic.Difficulty.MEDIUM,
    "khó": Topic.Difficulty.HARD,
    "kho": Topic.Difficulty.HARD,
}


def normalize_str(val) -> str:
    """Chuẩn hóa chuỗi văn bản: loại bỏ khoảng trắng dư thừa."""
    if val is None:
        return ""
    return str(val).strip()


def normalize_token(val) -> str:
    """Chuẩn hóa tiêu đề cột/sheet: chữ thường, không dấu, không ký tự đặc biệt."""
    text = normalize_str(val).lower()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return re.sub(r"[\s_-]+", " ", text).strip()


def validate_gpa_score(val, row_idx: int, sheet_name: str, errors: list[str]) -> Decimal | None:
    """Kiểm tra và chuẩn hóa điểm GPA theo thang 4.

    Công thức kiểm tra:
        0.0 <= GPA <= 4.0
    """
    if val is None or normalize_str(val) == "":
        errors.append(f"Sheet {sheet_name}, dòng {row_idx}: Thiếu điểm GPA.")
        return None
    try:
        score = Decimal(str(val).strip())
    except (InvalidOperation, ValueError):
        errors.append(f"Sheet {sheet_name}, dòng {row_idx}: GPA '{val}' không phải số hợp lệ.")
        return None

    if not (Decimal("0.0") <= score <= Decimal("4.0")):
        errors.append(
            f"Sheet {sheet_name}, dòng {row_idx}: GPA {score} không hợp lệ. Điểm GPA thang 4 phải thuộc [0.0, 4.0]."
        )
        return None
    return round(score, 2)


def validate_email_address(val, row_idx: int, sheet_name: str, errors: list[str]) -> str | None:
    """Kiểm tra định dạng email theo chuẩn Django RFC."""
    email = normalize_str(val)
    if not email:
        errors.append(f"Sheet {sheet_name}, dòng {row_idx}: Thiếu địa chỉ email.")
        return None
    try:
        validate_email(email)
    except ValidationError:
        errors.append(f"Sheet {sheet_name}, dòng {row_idx}: Email '{email}' không đúng định dạng.")
        return None
    return email


def validate_positive_integer(
    val, default: int, row_idx: int, sheet_name: str, field_label: str, errors: list[str]
) -> int | None:
    """Kiểm tra số nguyên dương n >= 1.

    Công thức:
        n in Z, n >= 1
    """
    if val is None or normalize_str(val) == "":
        return default
    try:
        num = int(float(str(val).strip()))
    except (ValueError, TypeError):
        errors.append(f"Sheet {sheet_name}, dòng {row_idx}: {field_label} '{val}' không phải số nguyên hợp lệ.")
        return None

    if num < 1:
        errors.append(f"Sheet {sheet_name}, dòng {row_idx}: {field_label} ({num}) phải là số nguyên dương (>= 1).")
        return None
    return num


def validate_topic_difficulty(val, row_idx: int, errors: list[str]) -> int | None:
    """Xác định độ khó đề tài từ giá trị bảng tính.

    Công thức phân loại:
        D in {1: Dễ, 2: Trung bình, 3: Khó}
    """
    if val is None or normalize_str(val) == "":
        return Topic.Difficulty.MEDIUM
    token = normalize_str(val).lower()
    if token in DIFFICULTY_MAP:
        return DIFFICULTY_MAP[token]
    errors.append(
        f"Sheet DeTai, dòng {row_idx}: Độ khó '{val}' không hợp lệ. Chỉ chấp nhận 1 (Dễ), 2 (Trung bình), 3 (Khó)."
    )
    return None


def match_column_headers(header_row: tuple, sheet_key: str) -> dict[str, int]:
    """Ánh xạ tên cột chuẩn với chỉ số cột thực tế trong sheet."""
    mapping = {}
    aliases = COL_ALIASES[sheet_key]
    for idx, cell_val in enumerate(header_row):
        norm = normalize_token(cell_val)
        for canon_col, alias_set in aliases.items():
            if canon_col not in mapping and any(normalize_token(a) == norm for a in alias_set):
                mapping[canon_col] = idx
    return mapping


def _read_sheet_rows(ws, sheet_key: str, errors: list[str]) -> list[tuple[int, dict[str, any]]]:
    """Đọc và ánh xạ các hàng dữ liệu của một sheet thành từ điển."""
    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        return []
    col_map = match_column_headers(rows[0], sheet_key)
    result = []
    for r_idx, row in enumerate(rows[1:], start=2):
        if all(c is None or normalize_str(c) == "" for c in row):
            continue
        row_dict = {}
        for col_name, c_idx in col_map.items():
            row_dict[col_name] = row[c_idx] if c_idx < len(row) else None
        result.append((r_idx, row_dict))
    return result


# ---------------------------------------------------------------- Parse từng sheet
def _parse_ky_nang_sheet(ws, errors: list[str]) -> list[dict]:
    """Phân tích và kiểm tra tính hợp lệ của sheet Kỹ năng."""
    rows = _read_sheet_rows(ws, "KyNang", errors)
    seen_names = set()
    items = []
    for r_idx, r in rows:
        name = normalize_str(r.get("name"))
        if not name:
            errors.append(f"Sheet KyNang, dòng {r_idx}: Thiếu tên kỹ năng bắt buộc.")
            continue
        if name.lower() in seen_names:
            errors.append(f"Sheet KyNang, dòng {r_idx}: Kỹ năng '{name}' bị trùng lặp trong tệp Excel.")
            continue
        seen_names.add(name.lower())
        field = normalize_str(r.get("field"))
        items.append({"name": name, "field": field, "row": r_idx})
    return items


def _parse_giang_vien_sheet(ws, errors: list[str]) -> list[dict]:
    """Phân tích và kiểm tra tính hợp lệ của sheet Giảng viên."""
    rows = _read_sheet_rows(ws, "GiangVien", errors)
    seen_codes = set()
    items = []
    for r_idx, r in rows:
        code = normalize_str(r.get("code"))
        first_name = normalize_str(r.get("first_name"))
        if not code:
            errors.append(f"Sheet GiangVien, dòng {r_idx}: Thiếu mã giảng viên bắt buộc.")
        elif code.lower() in seen_codes:
            errors.append(f"Sheet GiangVien, dòng {r_idx}: Mã giảng viên '{code}' bị trùng lặp trong tệp Excel.")
        # gv001 ≡ GV001 (trong tệp cũng so không phân biệt hoa thường)
        elif User.objects.filter(username__iexact=code).exists():
            errors.append(f"Sheet GiangVien, dòng {r_idx}: Tên đăng nhập/Mã GV '{code}' đã tồn tại trong hệ thống.")
        seen_codes.add(code.lower() if code else "")

        if not first_name:
            errors.append(f"Sheet GiangVien, dòng {r_idx}: Thiếu tên giảng viên bắt buộc.")

        email = validate_email_address(r.get("email"), r_idx, "GiangVien", errors)
        max_st = validate_positive_integer(r.get("max_students"), 5, r_idx, "GiangVien", "Chỉ tiêu hướng dẫn", errors)

        items.append(
            {
                "code": code,
                "first_name": first_name,
                "last_name": normalize_str(r.get("last_name")),
                "email": email or "",
                "department": normalize_str(r.get("department")) or "Khoa CNTT",
                "max_students": max_st or 5,
                "fields": [f.strip() for f in normalize_str(r.get("fields")).split(",") if f.strip()],
                "row": r_idx,
            }
        )
    return items


def _parse_de_tai_sheet(ws, available_lecturer_codes: set[str], errors: list[str]) -> list[dict]:
    """Phân tích và kiểm tra tính hợp lệ của sheet Đề tài."""
    rows = _read_sheet_rows(ws, "DeTai", errors)
    items = []
    for r_idx, r in rows:
        title = normalize_str(r.get("title"))
        lec_code = normalize_str(r.get("lecturer"))
        if not title:
            errors.append(f"Sheet DeTai, dòng {r_idx}: Thiếu tên đề tài bắt buộc.")
        if not lec_code:
            errors.append(f"Sheet DeTai, dòng {r_idx}: Thiếu mã giảng viên hướng dẫn.")
        elif (
            lec_code.lower() not in available_lecturer_codes
            and not Lecturer.objects.filter(user__username__iexact=lec_code).exists()
            and not Lecturer.objects.filter(user__email__iexact=lec_code).exists()
        ):
            errors.append(f"Sheet DeTai, dòng {r_idx}: Không tìm thấy giảng viên với mã '{lec_code}'.")

        diff = validate_topic_difficulty(r.get("difficulty"), r_idx, errors)
        min_gpa_raw = r.get("min_gpa")
        min_gpa = Decimal("0.0")
        if min_gpa_raw is not None and normalize_str(min_gpa_raw) != "":
            parsed_gpa = validate_gpa_score(min_gpa_raw, r_idx, "DeTai", errors)
            min_gpa = parsed_gpa if parsed_gpa is not None else Decimal("0.0")

        capacity = validate_positive_integer(r.get("capacity"), 1, r_idx, "DeTai", "Số lượng sinh viên tối đa", errors)

        items.append(
            {
                "title": title,
                "lecturer_code": lec_code,
                "description": normalize_str(r.get("description")) or title,
                "fields": [f.strip() for f in normalize_str(r.get("fields")).split(",") if f.strip()],
                "difficulty": diff or Topic.Difficulty.MEDIUM,
                "min_gpa": min_gpa,
                "capacity": capacity or 1,
                "row": r_idx,
            }
        )
    return items


def _parse_sinh_vien_sheet(ws, errors: list[str]) -> list[dict]:
    """Phân tích và kiểm tra tính hợp lệ của sheet Sinh viên."""
    rows = _read_sheet_rows(ws, "SinhVien", errors)
    seen_codes = set()
    items = []
    for r_idx, r in rows:
        code = normalize_str(r.get("code"))
        first_name = normalize_str(r.get("first_name"))
        if not code:
            errors.append(f"Sheet SinhVien, dòng {r_idx}: Thiếu mã sinh viên bắt buộc.")
        elif code.lower() in seen_codes:
            errors.append(f"Sheet SinhVien, dòng {r_idx}: Mã sinh viên '{code}' bị trùng lặp trong tệp Excel.")
        elif (
            Student.objects.filter(student_code__iexact=code).exists()
            or User.objects.filter(username__iexact=code).exists()
        ):
            errors.append(f"Sheet SinhVien, dòng {r_idx}: Mã sinh viên '{code}' đã tồn tại trong hệ thống.")
        seen_codes.add(code.lower() if code else "")

        if not first_name:
            errors.append(f"Sheet SinhVien, dòng {r_idx}: Thiếu tên sinh viên bắt buộc.")

        gpa = validate_gpa_score(r.get("gpa"), r_idx, "SinhVien", errors)
        email = validate_email_address(r.get("email"), r_idx, "SinhVien", errors)

        items.append(
            {
                "code": code,
                "first_name": first_name,
                "last_name": normalize_str(r.get("last_name")),
                "gpa": gpa,
                "email": email or "",
                "major": normalize_str(r.get("major")) or "Công nghệ thông tin",
                "about": normalize_str(r.get("about")),
                "row": r_idx,
            }
        )
    return items


# ---------------------------------------------------------------- Ghi CSDL
def _save_imported_skills(items: list[dict]) -> int:
    """Ghi danh sách kỹ năng vào CSDL."""
    count = 0
    for item in items:
        field_obj = None
        if item["field"]:
            field_obj, _ = Field.objects.get_or_create(name=item["field"])
        Skill.objects.update_or_create(name=item["name"], defaults={"field": field_obj})
        count += 1
    return count


def _save_imported_lecturers(items: list[dict]) -> tuple[int, dict[str, Lecturer]]:
    """Ghi danh sách giảng viên và tài khoản vào CSDL."""
    count = 0
    created_map = {}
    for item in items:
        user = User.objects.create_user(
            username=item["code"],
            email=item["email"],
            first_name=item["first_name"],
            last_name=item["last_name"],
            role=User.Role.LECTURER,
        )
        user.set_password("123456")
        user.save()

        lec = Lecturer.objects.create(user=user, department=item["department"], max_students=item["max_students"])
        if item["fields"]:
            field_objs = [Field.objects.get_or_create(name=fname)[0] for fname in item["fields"]]
            lec.fields.set(field_objs)
        created_map[item["code"].lower()] = lec
        count += 1
    return count, created_map


def _save_imported_topics(items: list[dict], new_lecturers: dict[str, Lecturer]) -> int:
    """Ghi danh sách đề tài vào CSDL."""
    count = 0
    for item in items:
        code_lower = item["lecturer_code"].lower()
        lec = new_lecturers.get(code_lower)
        if not lec:
            lec = (
                Lecturer.objects.filter(user__username__iexact=item["lecturer_code"]).first()
                or Lecturer.objects.filter(user__email__iexact=item["lecturer_code"]).first()
            )
        topic = Topic.objects.create(
            lecturer=lec,
            title=item["title"],
            description=item["description"],
            difficulty=item["difficulty"],
            min_gpa=item["min_gpa"],
            capacity=item["capacity"],
            status=Topic.Status.OPEN,
        )
        if item["fields"]:
            field_objs = [Field.objects.get_or_create(name=fname)[0] for fname in item["fields"]]
            topic.fields.set(field_objs)
        count += 1
    return count


def _save_imported_students(items: list[dict]) -> int:
    """Ghi danh sách sinh viên và tài khoản vào CSDL."""
    count = 0
    for item in items:
        user = User.objects.create_user(
            username=item["code"],
            email=item["email"],
            first_name=item["first_name"],
            last_name=item["last_name"],
            role=User.Role.STUDENT,
        )
        user.set_password("123456")
        user.save()

        major, _ = Major.objects.get_or_create(name=item["major"])
        Student.objects.create(
            user=user,
            student_code=item["code"],
            major=major,
            gpa=item["gpa"],
            about=item["about"],
        )
        count += 1
    return count


# ---------------------------------------------------------------- Điểm nhập dữ liệu chính
def import_excel_data(file_or_path, dry_run: bool = False) -> tuple[bool, list[str], dict[str, int]]:
    """Nhập dữ liệu từ tệp Excel với bảo toàn giao dịch ACID (UC15).

    Công thức tổng hợp dữ liệu thành công:
        N_tong = N_SV + N_GV + N_DeTai + N_KyNang

    Nếu phát hiện bất kỳ lỗi nào, toàn bộ giao dịch được hoàn tác (rollback),
    đảm bảo tính toàn vẹn tuyệt đối của cơ sở dữ liệu.
    dry_run=True: chạy đủ các bước ghi trong giao dịch rồi hoàn tác — trả về đúng số dòng SẼ nhập, không lưu gì.
    """
    stats = {"students": 0, "lecturers": 0, "topics": 0, "skills": 0}
    errors = []

    try:
        if hasattr(file_or_path, "read"):
            wb = openpyxl.load_workbook(file_or_path, data_only=True)
        else:
            wb = openpyxl.load_workbook(str(file_or_path), data_only=True)
    except Exception as e:
        return False, [f"Tệp không đúng định dạng Excel (.xlsx) hợp lệ: {e}"], stats

    sheet_map = {}
    for name in wb.sheetnames:
        norm = normalize_token(name)
        for canon, alias_set in SHEET_ALIASES.items():
            if canon not in sheet_map and any(normalize_token(a) == norm for a in alias_set):
                sheet_map[canon] = wb[name]

    if not sheet_map:
        return (
            False,
            [
                "Không tìm thấy sheet hợp lệ nào trong tệp (cần ít nhất một trong các sheet: "
                "SinhVien, GiangVien, DeTai, KyNang)."
            ],
            stats,
        )

    # 1. Parse và xác thực toàn bộ dữ liệu
    skill_items = _parse_ky_nang_sheet(sheet_map["KyNang"], errors) if "KyNang" in sheet_map else []
    lec_items = _parse_giang_vien_sheet(sheet_map["GiangVien"], errors) if "GiangVien" in sheet_map else []
    avail_lec_codes = {item["code"].lower() for item in lec_items if item["code"]}
    topic_items = _parse_de_tai_sheet(sheet_map["DeTai"], avail_lec_codes, errors) if "DeTai" in sheet_map else []
    student_items = _parse_sinh_vien_sheet(sheet_map["SinhVien"], errors) if "SinhVien" in sheet_map else []

    # 2. Nếu có lỗi, trả về danh sách lỗi và không ghi gì vào DB
    if errors:
        return False, errors, stats

    # 3. Giao dịch nguyên tử lưu dữ liệu
    try:
        with transaction.atomic():
            stats["skills"] = _save_imported_skills(skill_items)
            n_lec, new_lecs = _save_imported_lecturers(lec_items)
            stats["lecturers"] = n_lec
            stats["topics"] = _save_imported_topics(topic_items, new_lecs)
            stats["students"] = _save_imported_students(student_items)
            if dry_run:
                transaction.set_rollback(True)
    except Exception as exc:
        return False, [f"Lỗi hệ thống khi lưu dữ liệu vào cơ sở dữ liệu: {exc}"], stats

    return True, [], stats


# ---------------------------------------------------------------- Tạo file Excel mẫu
def create_sample_excel(output_path: str | Path | None = None) -> bytes | Path:
    """Tạo tệp Excel mẫu chuẩn mực catalog/mau_nhap_lieu.xlsx bằng mã nguồn.

    Bao gồm 4 sheet: SinhVien, GiangVien, DeTai, KyNang kèm định dạng header,
    dữ liệu minh họa thực tế và ghi chú định dạng.
    """
    wb = openpyxl.Workbook()
    # Sheet mặc định
    ws_sv = wb.active
    ws_sv.title = "SinhVien"
    ws_gv = wb.create_sheet(title="GiangVien")
    ws_dt = wb.create_sheet(title="DeTai")
    ws_kn = wb.create_sheet(title="KyNang")

    header_font = Font(name="Arial", size=11, bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
    center_align = Alignment(horizontal="center", vertical="center")
    border_thin = Border(
        left=Side(style="thin", color="D9D9D9"),
        right=Side(style="thin", color="D9D9D9"),
        top=Side(style="thin", color="D9D9D9"),
        bottom=Side(style="thin", color="D9D9D9"),
    )

    sheets_data = {
        ws_sv: {
            "headers": ["Mã sinh viên", "Họ đệm", "Tên", "GPA", "Email", "Chuyên ngành", "Ghi chú"],
            "rows": [
                ["20269001", "Nguyễn Văn", "An", 3.50, "an.nv@eaut.edu.vn", "Công nghệ thông tin", "Định hướng AI"],
                ["20269002", "Trần Thị", "Bình", 3.20, "binh.tt@eaut.edu.vn", "Công nghệ thông tin", "Định hướng Web"],
                [
                    "20269003",
                    "Lê Hoàng",
                    "Cường",
                    2.85,
                    "cuong.lh@eaut.edu.vn",
                    "Công nghệ thông tin",
                    "Định hướng Mobile",
                ],
            ],
            "widths": [16, 18, 12, 10, 26, 24, 24],
        },
        ws_gv: {
            "headers": ["Mã giảng viên", "Họ đệm", "Tên", "Email", "Bộ môn", "Chỉ tiêu", "Lĩnh vực"],
            "rows": [
                ["GV101", "Đặng Khánh", "Trung", "trungdk@eaut.edu.vn", "Khoa CNTT", 5, "Web, Trí tuệ nhân tạo"],
                ["GV102", "Nguyễn Thị", "Mai", "mainth@eaut.edu.vn", "Khoa CNTT", 6, "Dữ liệu, Trí tuệ nhân tạo"],
                ["GV103", "Vũ Hoàng", "Long", "longvh@eaut.edu.vn", "Khoa CNTT", 4, "Di động, Web"],
            ],
            "widths": [16, 18, 12, 26, 16, 12, 30],
        },
        ws_dt: {
            "headers": ["Tên đề tài", "Mã giảng viên", "Mô tả", "Lĩnh vực", "Độ khó", "GPA tối thiểu", "Số lượng"],
            "rows": [
                [
                    "Hệ thống gợi ý đề tài tốt nghiệp bằng học máy",
                    "GV101",
                    "Xây dựng cổng thông tin khuyến nghị đề tài sử dụng mô hình kết hợp và xử lý ngôn ngữ tự nhiên",
                    "Trí tuệ nhân tạo, Web",
                    2,
                    2.50,
                    2,
                ],
                [
                    "Phân tích dữ liệu học tập và dự báo kết quả rèn luyện",
                    "GV102",
                    "Ứng dụng thuật toán khai phá dữ liệu hỗ trợ cố vấn học tập cảnh báo học vụ",
                    "Dữ liệu, Trí tuệ nhân tạo",
                    2,
                    2.00,
                    1,
                ],
                [
                    "Ứng dụng di động quản lý giao việc thông minh",
                    "GV103",
                    "Xây dựng ứng dụng di động đa nền tảng Flutter tích hợp thông báo thời gian thực",
                    "Di động",
                    1,
                    0.00,
                    2,
                ],
            ],
            "widths": [38, 16, 45, 26, 10, 14, 12],
        },
        ws_kn: {
            "headers": ["Tên kỹ năng", "Lĩnh vực"],
            "rows": [
                ["Python", "Trí tuệ nhân tạo"],
                ["Machine Learning", "Trí tuệ nhân tạo"],
                ["Django", "Web"],
                ["React", "Web"],
                ["SQL", "Dữ liệu"],
                ["Flutter", "Di động"],
            ],
            "widths": [24, 26],
        },
    }

    for ws, cfg in sheets_data.items():
        ws.append(cfg["headers"])
        for cell in ws[1]:
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = center_align

        for row in cfg["rows"]:
            ws.append(row)

        for row in ws.iter_rows(min_row=1, max_row=ws.max_row, min_col=1, max_col=len(cfg["headers"])):
            for cell in row:
                cell.border = border_thin

        for col_idx, width in enumerate(cfg["widths"], start=1):
            col_letter = openpyxl.utils.get_column_letter(col_idx)
            ws.column_dimensions[col_letter].width = width

    if output_path:
        out_p = Path(output_path)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        wb.save(str(out_p))
        return out_p

    bio = BytesIO()
    wb.save(bio)
    return bio.getvalue()
