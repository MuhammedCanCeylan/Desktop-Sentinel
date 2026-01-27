# 🛡️ Desktop Sentinel

**Desktop Sentinel** is a smart, "honey-pot" style security application for Windows. Unlike traditional lock screens, it mimics your active desktop to fool intruders, utilizes facial recognition to distinguish the owner, and deploys countermeasures (scare tactics) against unauthorized users.

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-Face_Recognition-green?style=for-the-badge&logo=opencv)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-orange?style=for-the-badge)

## 🚀 Features

* **🕵️‍♂️ Honeypot Mechanism:** Instead of a black screen, it takes a screenshot of your current desktop and displays it fullscreen. Intruders think the PC is unlocked.
* **👤 Biometric Authentication:** Uses OpenAI's `LBPHFaceRecognizer` to continuously scan for the owner's face.
* **😱 Intruder Countermeasure:** If an unknown face is detected looking at the screen, a custom warning image (or jump scare) is instantly displayed.
* **🔓 Seamless Unlock:** If the owner is detected, the fake screen persists until a key is pressed, at which point it seamlessly transitions to the real Windows session (or locks the workstation securely).
* **🎛️ Modern Control Panel:** A sleek Dark Mode GUI built with `CustomTkinter` to manage sensitivity, retrain the model, and toggle protection.

## 🛠️ Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/MuhammedCanCeylan/Desktop-Sentinel.git](https://github.com/MuhammedCanCeylan/Desktop-Sentinel.git)
    cd Desktop-Sentinel
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Control Panel:**
    ```bash
    python GozcuApp.py
    ```

## 📖 How to Use

1.  **Training (First Run):**
    * Open the app and click **"YÜZ TARAMAYI BAŞLAT" (Start Face Scan)**.
    * Follow the on-screen instructions (Look center, turn right, turn left) to create a robust biometric profile.
2.  **Configuration:**
    * Select a "Scare Image" using the file picker.
    * Adjust the **Sensitivity Slider** (Recommended: 75).
3.  **Arming the Trap:**
    * Toggle the **"Koruma Modunu Aç" (Protection Mode)** switch.
    * When you leave your desk, press `Ctrl + Alt + L`.
    * The system takes a screenshot and enters "Sentinel Mode".

## 🏗️ Technical Architecture

* **Frontend:** `CustomTkinter` for a modern, responsive Windows 11-style UI.
* **Backend Logic:** `trap_logic.py` handles the detached process management to ensure the GUI remains responsive while the heavy computer vision tasks run in the background.
* **Computer Vision:** `OpenCV` with `Haar Cascades` for face detection and `LBPH` (Local Binary Patterns Histograms) for recognition.
* **System Integration:** `ctypes` and `pyautogui` for interacting with the low-level Windows API (locking workstation, screenshotting).

## ⚠️ Disclaimer

This project is intended for educational and personal security purposes. Please use the "scare" feature responsibly.

---
*Developed by [Muhammed Can Ceylan](https://github.com/MuhammedCanCeylan)*
