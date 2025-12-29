# راه‌اندازی Dorehmi Analyzer (MVP)

پیش‌نیازها:
- Ubuntu 22.04
- Python 3.10+
- ffmpeg (`sudo apt install ffmpeg`)

مراحل:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
make dev
```

مسیرهای ذخیره‌سازی:
- `./storage/uploads` برای آپلودها
- `./storage/results` برای خروجی‌ها
- `./storage/logs` برای لاگ‌ها

در حالت توسعه، `make dev` هم API (پورت 8000) و هم کارگر صف را اجرا می‌کند. UI در آدرس `http://localhost:8000/` قابل مشاهده است.
