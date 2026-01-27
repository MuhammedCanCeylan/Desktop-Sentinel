# DOSYA ADI: GozcuApp.py
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import os
import threading
import keyboard
import time
import subprocess
import sys

# Görünüm Ayarları
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Pencere Ayarları
        self.title("GÖZCÜ - Güvenlik Sistemi")
        self.geometry("400x550")
        self.resizable(False, False)

        # Değişkenler
        self.sistem_aktif = False
        self.dinleme_thread = None
        self.klasor_yolu = os.path.dirname(os.path.abspath(__file__))
        
        # Varsayılan dosya yolları
        self.uyari_resmi = os.path.join(self.klasor_yolu, "uyari_resmi.jpg")
        self.egitim_verisi = os.path.join(self.klasor_yolu, "egitim_verisi.yml")
        self.logic_script = os.path.join(self.klasor_yolu, "trap_logic.py")

        # --- ARAYÜZ ELEMANLARI ---
        self.lbl_title = ctk.CTkLabel(self, text="GÖZCÜ KONTROL PANELİ", font=("Roboto", 20, "bold"))
        self.lbl_title.pack(pady=20)

        self.lbl_status = ctk.CTkLabel(self, text="SİSTEM: PASİF", text_color="red", font=("Arial", 14, "bold"))
        self.lbl_status.pack(pady=5)

        self.btn_toggle = ctk.CTkSwitch(self, text="Koruma Modunu Aç", command=self.toggle_system, font=("Arial", 14))
        self.btn_toggle.pack(pady=20)

        self.frame_settings = ctk.CTkFrame(self)
        self.frame_settings.pack(pady=10, padx=20, fill="x")

        self.lbl_sens = ctk.CTkLabel(self.frame_settings, text="Tanıma Hassasiyeti (75 Önerilir)")
        self.lbl_sens.pack(pady=5)
        self.slider_sens = ctk.CTkSlider(self.frame_settings, from_=40, to=100, number_of_steps=60)
        self.slider_sens.set(75)
        self.slider_sens.pack(pady=5)

        self.btn_img = ctk.CTkButton(self.frame_settings, text="Korkunç Resmi Seç", command=self.resim_sec)
        self.btn_img.pack(pady=10)

        self.btn_train = ctk.CTkButton(self, text="YÜZ TARAMAYI BAŞLAT (YENİ)", 
                                       fg_color="#D35B58", hover_color="#C77C78", 
                                       command=self.egitimi_baslat)
        self.btn_train.pack(pady=20, padx=20, fill="x")

        self.lbl_info = ctk.CTkLabel(self, text="Kısayol: Ctrl + Alt + L", font=("Arial", 10), text_color="gray")
        self.lbl_info.pack(side="bottom", pady=10)

        self.start_listener()

    def start_listener(self):
        self.dinleme_thread = threading.Thread(target=self.keyboard_loop, daemon=True)
        self.dinleme_thread.start()

    def keyboard_loop(self):
        while True:
            try:
                if self.sistem_aktif:
                    if keyboard.is_pressed('ctrl+alt+l'):
                        time.sleep(0.5)
                        self.tuzagi_calistir()
                        # Tuzak açıldıktan sonra tekrar tetiklenmemesi için uzun bekleme
                        time.sleep(5) 
                time.sleep(0.1)
            except:
                pass

    def tuzagi_calistir(self):
        hassasiyet = int(self.slider_sens.get())
        print(f"Tuzak Başlatılıyor... Hassasiyet: {hassasiyet}")
        
        # --- DÜZELTME BAŞLIYOR ---
        
        # 1. Dosyaların SADECE İSİMLERİNİ alıyoruz (Yolu siliyoruz)
        script_adi = "trap_logic.py"
        resim_adi = "uyari_resmi.jpg"
        veri_adi = "egitim_verisi.yml"
        
        # 2. Komutu sadece isimlerle hazırlıyoruz
        cmd = [sys.executable, script_adi, resim_adi, veri_adi, str(hassasiyet)]
        
        # 3. cwd=self.klasor_yolu parametresi ile "Bu klasörde çalış" diyoruz.
        # Böylece "Masaüstü" yolunu OpenCV'ye yedirmek zorunda kalmıyoruz.
        subprocess.Popen(cmd, cwd=self.klasor_yolu)

    def toggle_system(self):
        if self.btn_toggle.get() == 1:
            self.sistem_aktif = True
            self.lbl_status.configure(text="SİSTEM: AKTİF (Dinliyor...)", text_color="#00FF00")
        else:
            self.sistem_aktif = False
            self.lbl_status.configure(text="SİSTEM: PASİF", text_color="red")

    def resim_sec(self):
        filename = filedialog.askopenfilename(title="Resim Seç", filetypes=[("Image files", "*.jpg;*.png")])
        if filename:
            self.uyari_resmi = filename
            print(f"Yeni resim seçildi: {filename}")

    def egitimi_baslat(self):
        if os.path.exists("tarama_banka.py"):
            self.lbl_status.configure(text="Eğitim Modu Açılıyor...", text_color="yellow")
            subprocess.Popen([sys.executable, "tarama_banka.py"])
        else:
            tk.messagebox.showerror("Hata", "tarama_banka.py dosyası bulunamadı!")

if __name__ == "__main__":
    app = App()
    app.mainloop()