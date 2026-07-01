import cv2
import mediapipe as mp
import customtkinter as ctk
from PIL import Image, ImageTk

# --- CONFIG WINDOW ---
ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.title("Foto kita blurrrrr - Versi 1 Tangan")
app.geometry("1280x720")

label = ctk.CTkLabel(app, text="", anchor="center")
label.pack(fill="none", expand=True)

# CAMERA + HANDS
cap = cv2.VideoCapture(0)

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

# Kita set num_hands=1 agar fokus deteksi satu tangan aja, jadi prosesnya jauh lebih ringan
options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path="hand_landmarker.task"),
    running_mode=VisionRunningMode.IMAGE,
    num_hands=1, 
    min_hand_detection_confidence=0.6
)
detector = HandLandmarker.create_from_options(options)

def count_fingers(hand_landmarks):
    try:
        tip_ids = [4, 8, 12, 16, 20]
        fingers = []

        # Jempol
        if hand_landmarks[4].x < hand_landmarks[3].x:
            fingers.append(1)
        else:
            fingers.append(0)

        # Jari telunjuk sampai kelingking
        for i in tip_ids[1:]:
            if hand_landmarks[i].y < hand_landmarks[i - 2].y:
                fingers.append(1)
            else:
                fingers.append(0)

        return sum(fingers)
    except Exception:
        return 0

def update():
    try:
        ret, frame = cap.read()
        if not ret or frame is None:
            app.after(30, update)
            return

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        result = detector.detect(mp_image)

        blur = False

        # Logika 1 tangan: Cukup cek apakah ada tangan yang ngangkat 2 jari
        if result.hand_landmarks:
            for hand_landmarks in result.hand_landmarks:
                if count_fingers(hand_landmarks) == 2:
                    blur = True
                    break # Kalau sudah ketemu 1 tangan yang pas, langsung break loop

        if blur:
            frame = cv2.GaussianBlur(frame, (51, 51), 0) 

        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        imgtk = ImageTk.PhotoImage(img)

        label.imgtk = imgtk
        label.configure(image=imgtk)

    except Exception as e:
        print(f"Sistem mengabaikan error: {e}")

    app.after(30, update)

def close():
    try:
        cap.release()
        detector.close()
    except:
        pass
    app.destroy()

app.protocol("WM_DELETE_WINDOW", close)

update()
app.mainloop()