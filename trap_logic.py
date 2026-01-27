# DOSYA ADI: trap_logic.py
import tkinter as tk
from PIL import Image, ImageTk
import pyautogui
import cv2
import os
import sys
import ctypes

# ÇALIŞMA DİZİNİ AYARI (HAYAT KURTARIR)
# Kod nerede çalışıyorsa orayı merkez üs yapar.
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

class TuzakPenceresi:
    def __init__(self, uyari_resmi, egitim_dosyasi, hassasiyet):
        # Sadece dosya isimlerini kullanıyoruz
        self.uyari_resmi_yolu = uyari_resmi
        self.egitim_dosyasi = egitim_dosyasi
        self.hassasiyet = int(hassasiyet)

        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.attributes("-topmost", True)
        self.root.config(cursor="none")
        
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()

        # 1. Ekran Görüntüsü
        try:
            screenshot = pyautogui.screenshot()
            self.img_fake_desktop = ImageTk.PhotoImage(screenshot)
        except:
            self.root.configure(bg="black")
            self.img_fake_desktop = None

        # 2. Uyarı Resmini Hazırla
        try:
            if os.path.exists(self.uyari_resmi_yolu):
                img_scare = Image.open(self.uyari_resmi_yolu)
                img_scare = img_scare.resize((self.width, self.height), Image.Resampling.LANCZOS)
                self.img_scare = ImageTk.PhotoImage(img_scare)
            else:
                # Resim bulunamazsa hata verme, siyah ekran devam etsin
                print(f"Uyarı: {self.uyari_resmi_yolu} bulunamadı.")
                self.img_scare = None
        except:
            self.img_scare = None

        self.panel = tk.Label(self.root, borderwidth=0)
        if self.img_fake_desktop:
            self.panel.configure(image=self.img_fake_desktop)
        self.panel.pack(fill="both", expand=True)

        # 3. Tanıma Sistemi
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        
        if os.path.exists(self.egitim_dosyasi):
            try:
                # OpenCV burada artık sadece "dosya.yml" görüyor, bozuk karakter yok.
                self.recognizer.read(self.egitim_dosyasi)
            except Exception as e:
                print(f"OpenCV Okuma Hatası: {e}")
                self.kapat_ve_cik()
                return
        else:
            print(f"Hata: {self.egitim_dosyasi} bulunamadı!")
            self.kapat_ve_cik()
            return

        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.cap = cv2.VideoCapture(0)
        self.kamera_aktif = True
        self.patron_geldi = False 

        # Olayları Dinle
        self.root.bind('<Button-1>', self.kontrol_ve_islem)
        self.root.bind('<Key>', self.kontrol_ve_islem)

        self.video_loop()
        self.root.mainloop()

    def video_loop(self):
        if not self.kamera_aktif: return

        ret, frame = self.cap.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 5)

            yabanci_var = False
            self.patron_geldi = False

            for (x,y,w,h) in faces:
                try:
                    id, confidence = self.recognizer.predict(gray[y:y+h,x:x+w])
                    if confidence < self.hassasiyet: 
                        self.patron_geldi = True
                    else:
                        yabanci_var = True
                except:
                    pass

            if self.patron_geldi:
                if self.img_fake_desktop and self.panel.cget("image") != str(self.img_fake_desktop):
                    self.panel.configure(image=self.img_fake_desktop)
                    self.root.update()
            
            elif yabanci_var:
                if self.img_scare and self.panel.cget("image") != str(self.img_scare):
                    self.panel.configure(image=self.img_scare)
                    self.root.update()
            
            else:
                if self.img_fake_desktop and self.panel.cget("image") != str(self.img_fake_desktop):
                    self.panel.configure(image=self.img_fake_desktop)
                    self.root.update()

        self.root.after(30, self.video_loop)

    def kontrol_ve_islem(self, event=None):
        if self.patron_geldi:
            ctypes.windll.user32.LockWorkStation()
            os._exit(0) 
        else:
            pass

    def kapat_ve_cik(self):
        self.kamera_aktif = False
        if self.cap is not None: self.cap.release()
        self.root.destroy()

if __name__ == "__main__":
    # Eğer App üzerinden geldiyse argümanları al
    if len(sys.argv) > 3:
        # Gelen argümanlar artık tam yol değil, sadece dosya adıdır.
        # "uyari_resmi.jpg", "egitim_verisi.yml" gibi.
        resim = sys.argv[1]
        egitim = sys.argv[2]
        hassas = sys.argv[3]
        app = TuzakPenceresi(resim, egitim, hassas)
    else:
        # Test amaçlı
        print("Manuel mod...")
        app = TuzakPenceresi("uyari_resmi.jpg", "egitim_verisi.yml", 75)