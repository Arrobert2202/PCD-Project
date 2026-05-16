# project 7 — ocr for visually impaired users

flutter app + fastapi backend. the app captures a document photo, sends it to the backend, and reads the extracted text aloud via tts.

---

## backend

```bash
cd backend
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

check it's running: `curl http://localhost:8000/health`

find your laptop's ip (needed for the app): `ipconfig getifaddr en0`

---

## flutter app

```bash
cd flutter_app
flutter pub get
flutter run
```

before running, set your laptop's ip in `lib/config.dart`:

```dart
static String host = '192.168.1.100'; // replace with your actual ip
```

---

## project structure

```
backend/          fastapi server (ocr pipeline)
flutter_app/      flutter frontend (camera + tts)
eval/             evaluation dataset and comparison scripts
```
