# foto-kita-blur

Cara menjalankan aplikasi "Foto kita blurrrrr":
1. Install library yang dibutuhkan di terminal:
   pip install customtkinter opencv-python mediapipe pillow
2. Download file model AI 'hand_landmarker.task' dari Google.
3. Pastikan file 'main.py' dan 'hand_landmarker.task' berada di satu folder yang sama.
4. Jalankan 'main.py', lalu angkat 2 jari ke kamera untuk mengaktifkan efek blur!

Download hand_landmarker.task disini https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task

pad\stikan folder seperti ini 
📂 foto-kita-blur
├── 📄 main.py              <-- Kode Python (versi stabil 1 tangan)
├── 📄 hand_landmarker.task <-- Model AI dari Google
