# ReadDoc — OCR Document Reader

scan a document with your phone and have it read aloud. the app sends the photo to a backend running on your laptop over local wi-fi, which extracts the text and sends it back.

---

## 1. backend

run this from the `backend/` folder on your laptop.

```bash
cd backend
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

start the server (run this from inside `backend/` with the venv active):

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

check it's running: `curl http://localhost:8000/health`

get your laptop's local ip (you'll need this for the app):
```bash
ipconfig getifaddr en0   # mac
hostname -I              # linux
```

---

## 2. flutter app

before running, set your laptop's ip in `flutter_app/lib/config.dart`:

```dart
static String host = '192.168.1.100'; // replace with your actual ip
```

make sure your phone and laptop are on the same wi-fi network.

### android

```bash
cd flutter_app
flutter pub get
flutter run --release
```

enable usb debugging on your android phone (settings → developer options → usb debugging), connect via usb, then run the command above.

### ios

```bash
cd flutter_app
flutter pub get
cd ios && pod install && cd ..
flutter run --release
```

**signing**: open `ios/Runner.xcworkspace` in xcode, go to signing & capabilities, select your apple id as the team, and set a unique bundle id like `com.yourname.documentreader`. do this once before running.

connect your iphone via usb, trust the mac when prompted, then run the command above. after the first install you can open the app directly from the home screen without usb.

---

## project structure

```
backend/        fastapi server — ocr pipeline (layout detection + easyocr/tesseract)
flutter_app/    mobile app — camera, http client, tts
eval/           test dataset and evaluation scripts (cer/wer comparison)
```
