#!/usr/bin/env bash
# Đưa bản đã nghiệm thu (nhánh ui/v3) lên bản demo :8099 và GitHub main. Chủ dự án tự chạy:
#   ssh lucifer-agent 'bash /opt/lucifer-agent/workspace/projects/capstone-advisor/v3/docs/nghiem-thu/trien-khai-8099.sh'
# Lần đầu sau khi chạy: mọi phiên đăng nhập cũ bị đăng xuất một lần (khoá bí mật mới lưu ở code/.secret_key).
set -euo pipefail
cd /opt/lucifer-agent/workspace/projects/capstone-advisor/code

cp db.sqlite3 "db.sqlite3.truoc-trien-khai-$(date +%Y%m%d-%H%M)"   # sao lưu CSDL demo
git merge --ff-only ui/v3                                            # chỉ tiến thẳng, không gộp đè
.venv/bin/pip install -q -U "pip>=26.2" "setuptools>=83"             # vá lỗ hổng của chính công cụ cài đặt (pip-audit)
.venv/bin/pip install -q "Django>=5.2.17,<5.3" "defusedxml>=0.7"       # chỉ gói mới; requirements.txt có mysqlclient, máy này không build được
DJANGO_DEBUG=0 .venv/bin/python manage.py migrate
DJANGO_DEBUG=0 .venv/bin/python manage.py check --fail-level ERROR

# Tắt máy chủ cũ theo PID đang giữ cổng 8099 (không pkill theo tên), rồi chạy lại với DEBUG=0
pid=$(ss -ltnpH 'sport = :8099' | grep -o 'pid=[0-9]*' | head -1 | cut -d= -f2 || true)
[ -n "$pid" ] && kill "$pid" && sleep 2
DJANGO_DEBUG=0 setsid nohup .venv/bin/python manage.py runserver 127.0.0.1:8099 --noreload --insecure \
  > /tmp/capstone-8099.log 2>&1 < /dev/null &
sleep 5
curl -fsS -o /dev/null -w "8099: HTTP %{http_code}\n" http://127.0.0.1:8099/dang-nhap/

git push origin HEAD:main
echo "Xong: $(git log --oneline -1)"
