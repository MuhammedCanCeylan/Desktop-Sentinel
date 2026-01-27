import cv2
import os
import numpy as np
import time

# Klasör kontrolü
if not os.path.exists('yuz_verileri'):
    os.makedirs('yuz_verileri')
else:
    # Eski verileri temizle ki karışmasın
    for f in os.listdir('yuz_verileri'):
        os.remove(os.path.join('yuz_verileri', f))

# Yüz algılayıcı
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

# --- EĞİTİM AŞAMALARI ---
asamalar = [
    {"mesaj": "DUMDUZ MERKEZE BAKIN", "adet": 60},
    {"mesaj": "KAFANIZI HAFIFCE SAGA CEVIRIN", "adet": 60},
    {"mesaj": "KAFANIZI HAFIFCE SOLA CEVIRIN", "adet": 60},
    {"mesaj": "KAMERAYA BIYIKLARINIZ GORUNECEK KADAR YAKLASIN", "adet": 40},
    {"mesaj": "KAFANIZI HAFIF YUKARI KALDIRIN (GURURLU)", "adet": 40}
]

toplam_foto = 0

for asama in asamalar:
    # Aşama öncesi hazırlık uyarısı
    for i in range(3, 0, -1):
        ret, frame = cap.read()
        if not ret: break
        img_h, img_w = frame.shape[:2]
        # Ekranı karart ve mesaj yaz
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (img_w, img_h), (0,0,0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        cv2.putText(frame, f"HAZIRLANIN: {asama['mesaj']}", (50, img_h//2 - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        cv2.putText(frame, f"{i} SANIYE SONRA BASLIYOR...", (50, img_h//2 + 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        cv2.imshow('Profesyonel Yuz Tarama', frame)
        cv2.waitKey(1000)
        
    current_count = 0
    while current_count < asama['adet']:
        ret, frame = cap.read()
        if not ret: break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.2, 5)
        
        img_h, img_w = frame.shape[:2]
        # Talimatı ekrana yaz
        cv2.rectangle(frame, (0,0), (img_w, 60), (0,0,0), -1)
        cv2.putText(frame, asama['mesaj'], (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

        for (x,y,w,h) in faces:
            toplam_foto += 1
            current_count += 1
            # Yüzü kaydet
            cv2.imwrite(f"yuz_verileri/kullanici.{toplam_foto}.jpg", gray[y:y+h, x:x+w])
            cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)
            cv2.putText(frame, f"Kayit: {current_count}/{asama['adet']}", (x, y+h+25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255), 2)

        cv2.imshow('Profesyonel Yuz Tarama', frame)
        if cv2.waitKey(50) & 0xFF == ord('q'): break
    
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()

# --- EĞİTİM KISMI ---
print("\n--- VERİLER TOPLANDI, YAPAY ZEKA EĞİTİLİYOR ---")
print("Bu islem birkac saniye surebilir...")

recognizer = cv2.face.LBPHFaceRecognizer_create()
path = 'yuz_verileri'
image_paths = [os.path.join(path,f) for f in os.listdir(path)]
face_samples = []
ids = []

for image_path in image_paths:
    try:
        PIL_img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if PIL_img is None: continue
        img_numpy = np.array(PIL_img, 'uint8')
        face_samples.append(img_numpy)
        ids.append(1) 
    except: continue

recognizer.train(face_samples, np.array(ids))
recognizer.write('egitim_verisi.yml') 

print(f"\n[MUKEMMEL] Toplam {len(face_samples)} farklı açı ile eğitim tamamlandı!")
print("'egitim_verisi.yml' dosyası hazır.")