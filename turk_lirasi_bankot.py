from ultralytics import YOLO
import cv2
import os
import sys
from tkinter import Tk, filedialog
from datetime import datetime
import time  

# =====================
# KLASÖR AYARLARI
# =====================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "turk_lirasi_banknot_tanima_model.pt")
OUTPUT_DIR = os.path.join(BASE_DIR, "results")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# =====================
# MODEL PARAMETRELERİ
# =====================
CONF = 0.25
IMGSZ = 704
IOU = 0.60
SAVE_FPS = 25
SLOW_FACTOR = 4

# =====================
# TKINTER (dosya seçici)
# =====================
root = Tk()
root.withdraw()

def pick_file(title, filetypes):
    path = filedialog.askopenfilename(title=title, filetypes=filetypes)
    return path if path else None

def timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

# =====================
# MODEL YÜKLE (1 KERE)
# =====================
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"❌ Model bulunamadı: {MODEL_PATH}")

model_dosya_adi = os.path.basename(MODEL_PATH)
print(f"🧠 Model yükleniyor: {model_dosya_adi}")

# Yapay bir bekleme süresi ekleyelim (Gerçekçilik için)
time.sleep(1.5)

model = YOLO(MODEL_PATH)

# Yükleme bittikten sonra küçük bir analiz süresi daha ekleyebiliriz
print("🔍 Parametreler kontrol ediliyor...")
time.sleep(1.0)
print("✅ Model hazır")
time.sleep(1.0)
# =====================
# ANA MENÜ DÖNGÜSÜ
# =====================
while True:
    print("\n==============================")
    print("🤖 YOLO TÜRK LİRASI BANKNOT TANIMA TEST MENÜSÜ")
    print("==============================")
    print("1 - Görsel Test")
    print("2 - Video Test")
    print("3 - Kamera Test")
    print("Q - Çıkış")
    print("==============================")

    secim = input("Seçimin: ").strip().lower()
    ts = timestamp()

    # =====================
    # GÖRSEL TEST
    # =====================
    if secim == "1":
        image_path = pick_file(
            "Görsel Seç",
            [("Image Files", "*.jpg *.jpeg *.png *.bmp *.webp")]
        )

        if not image_path:
            print("❌ Görsel seçilmedi.")
            continue

        result = model.predict(
            image_path,
            conf=CONF,
            iou=IOU,
            imgsz=IMGSZ,
            verbose=False
        )[0]

        frame = result[0].plot()
        out_path = os.path.join(OUTPUT_DIR, f"image_{ts}.jpg")
        cv2.imwrite(out_path, frame)

        print(f"✅ Kaydedildi: {out_path}")

        
        WINDOW_NAME = "Gorsel_Tahmin_Ekrani_QKapatmak_Icin"
        cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(WINDOW_NAME, 960, 800)

        cv2.imshow(WINDOW_NAME, frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # =====================
    # VİDEO TEST
    # =====================
    elif secim == "2":
        video_path = pick_file(
            "Video Seç",
            [("Video Files", "*.mp4 *.avi *.mov *.mkv")]
        )

        if not video_path:
            print("❌ Video seçilmedi.")
            continue

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print("❌ Video açılamadı.")
            continue

        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        out_path = os.path.join(OUTPUT_DIR, f"video_{ts}.mp4")
        writer = cv2.VideoWriter(
            out_path,
            cv2.VideoWriter_fourcc(*"mp4v"),
            SAVE_FPS,
            (w, h)
        )

        print("🎞 Video işleniyor | Q = Çık")

        while True:
            ok, frame_raw = cap.read()
            if not ok:
                break

            result = model.predict(
                frame_raw,
                conf=CONF,
                iou=IOU,
                imgsz=IMGSZ,
                verbose=False
            )[0]

            frame = result.plot()

            for _ in range(SLOW_FACTOR):
                writer.write(frame)


            WINDOW_NAME = "YOLO Video Test"
            cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
            cv2.resizeWindow(WINDOW_NAME, 960, 860)

            cv2.imshow(WINDOW_NAME, frame)
            if cv2.waitKey(1) & 0xFF in (ord("q"), ord("Q")):
                break

        cap.release()
        writer.release()
        cv2.destroyAllWindows()

        print(f"✅ Video kaydedildi: {out_path}")

    # =====================
    # KAMERA TEST
    # =====================
    elif secim == "3":
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("❌ Kamera açılamadı.")
            continue

        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) or 1280
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) or 720

        out_path = os.path.join(OUTPUT_DIR, f"camera_{ts}.mp4")
        writer = cv2.VideoWriter(
            out_path,
            cv2.VideoWriter_fourcc(*"mp4v"),
            SAVE_FPS,
            (w, h)
        )

        print("📷 Kamera açık | Q = Çık")

        while True:
            ok, frame_raw = cap.read()
            if not ok:
                break

            result = model.predict(
                frame_raw,
                conf=CONF,
                iou=IOU,
                imgsz=IMGSZ,
                verbose=False
            )[0]

            frame = result.plot()
            writer.write(frame)

            cv2.imshow("YOLO Kamera Test", frame)
            if cv2.waitKey(1) & 0xFF in (ord("q"), ord("Q")):
                break

        cap.release()
        writer.release()
        cv2.destroyAllWindows()

        print(f"✅ Kamera videosu kaydedildi: {out_path}")

    # =====================
    # ÇIKIŞ
    # =====================
    elif secim == "q":
        print("👋 Güle güle.")
        break

    else:
        print("❌ Geçersiz seçim. Tekrar dene.")
