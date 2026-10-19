"""Nghiệm thu P0 #6 — tệp Excel độc khi Khoa nhập liệu: XML bomb, zip bomb, tệp không phải Excel.

Tệp độc dựng từ chính tệp mẫu của app (create_sample_excel), chỉ sửa nội dung XML bên trong.
Mong đợi: báo lỗi, không lỗi 500, không treo, không ghi gì vào CSDL.
"""

import io
import time
import zipfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import TestCase, override_settings

from accounts.models import User
from catalog.importer import MAX_UNZIPPED_BYTES, create_sample_excel, import_excel_data
from catalog.models import Student, Topic

BOMB = (
    '<?xml version="1.0"?><!DOCTYPE lolz [<!ENTITY lol "lol">'
    + "".join(f'<!ENTITY lol{i} "{("&lol" + (str(i - 1) if i > 1 else "") + ";") * 10}">' for i in range(1, 10))
    + "]>"
)


def _rewrite(xlsx: bytes, member: str, fn) -> bytes:
    """Chép tệp zip, thay nội dung một thành phần bằng fn(nội dung cũ)."""
    src, out = zipfile.ZipFile(io.BytesIO(xlsx)), io.BytesIO()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for item in src.infolist():
            data = src.read(item.filename)
            z.writestr(item, fn(data) if item.filename == member else data)
    return out.getvalue()


def _sheet(xlsx: bytes) -> str:
    return next(n for n in zipfile.ZipFile(io.BytesIO(xlsx)).namelist() if n.startswith("xl/worksheets/sheet"))


@override_settings(RECOMMEND_SEMANTIC=False, RECOMMEND_LLM=False)
class MaliciousExcelUploads(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo", students=5, lecturers=2, topics=4, verbosity=0)
        cls.sample = create_sample_excel()

    def _counts(self):
        return Student.objects.count(), Topic.objects.count(), User.objects.count()

    def test_xml_bomb_rejected_quickly(self):
        sheet = _sheet(self.sample)
        body = lambda d: d.split(b"?>", 1)[-1].replace(b"<sheetData>", b"<sheetData>&lol9;", 1)  # noqa: E731
        bomb = _rewrite(self.sample, sheet, lambda d: BOMB.encode() + body(d))
        before, t = self._counts(), time.monotonic()
        ok, errors, _ = import_excel_data(io.BytesIO(bomb), dry_run=False)
        self.assertFalse(ok)
        self.assertTrue(errors)
        self.assertLess(time.monotonic() - t, 5)
        self.assertEqual(self._counts(), before)

    def test_zip_bomb_under_upload_limit_rejected_before_parsing(self):
        sheet = _sheet(self.sample)
        pad = b" " * (MAX_UNZIPPED_BYTES + 10 * 1024 * 1024)  # khoảng trắng hợp lệ trong XML, nén còn vài chục KB
        bomb = _rewrite(self.sample, sheet, lambda d: d.replace(b"</sheetData>", pad + b"</sheetData>", 1))
        self.assertLess(len(bomb), 5 * 1024 * 1024, "tệp độc phải lọt qua giới hạn tải lên 5 MB")
        before, t = self._counts(), time.monotonic()
        ok, errors, _ = import_excel_data(io.BytesIO(bomb))
        self.assertFalse(ok)
        self.assertIn("quá giới hạn", errors[0])
        self.assertLess(time.monotonic() - t, 3)
        self.assertEqual(self._counts(), before)

    def test_bad_files_through_faculty_upload_page(self):
        self.client.login(username="khoa01", password="123456")
        before = self._counts()
        for name, content in [
            ("bao-cao.xlsx", b"day khong phai excel"),
            ("virus.exe", b"MZ\x90\x00"),
            ("rong.xlsx", b""),
        ]:
            resp = self.client.post("/khoa/nhap-excel/", {"file": SimpleUploadedFile(name, content)})
            self.assertLess(resp.status_code, 500, name)
        self.assertEqual(self._counts(), before)

    def test_valid_sample_still_imports(self):
        """Lớp chặn mới không được chặn nhầm tệp mẫu hợp lệ."""
        ok, errors, stats = import_excel_data(io.BytesIO(self.sample), dry_run=True)
        self.assertTrue(ok, errors)
        self.assertGreater(sum(stats.values()), 0)
