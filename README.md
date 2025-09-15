# QR-Triggered Photography Slideshow (Privacy-Friendly)

This app is designed for hotel stands (e.g., MophieProd): when a guest scans a **QR code** at the camera, 
the app detects the QR and immediately starts a **full-screen diaporama** of that guest’s photos.
No biometric identification or face recognition is used—only a **session code** embedded in the QR.

## Features
- Camera preview with live **QR detection** (OpenCV's `QRCodeDetector`).
- Launch **full-screen slideshow** from `clients/<SESSION_CODE>/`.
- Simple **QR generator** to create printable PNG codes for each guest.
- Works **offline**, cross-platform (Windows/Mac/Linux).

## Quick Start
1. Install Python 3.10+ and pip.
2. Create a virtual env (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   ```
3. Install deps:
   ```bash
   pip install -r requirements.txt
   ```
4. Put your clients’ photos into folders like:
   ```
   clients/
     CLIENT123/
       img1.jpg
       img2.jpg
     MARIA_2025_09/
       photo1.jpg
       photo2.jpg
   ```
5. Generate QR codes (optional helper):
   ```bash
   python qr_tools.py --make CLIENT123 --out qrs/CLIENT123.png
   python qr_tools.py --make MARIA_2025_09 --out qrs/MARIA_2025_09.png
   ```
6. Run the app:
   ```bash
   python app.py --camera 0 --timeout 0
   ```
   - `--camera` selects the webcam index (try 0, 1, 2...).
   - `--timeout` (seconds) auto-exits slideshow after N seconds (0 = loop forever until ESC).

## How It Works
- The camera preview looks for QR codes using OpenCV’s `QRCodeDetector`.
- The QR text is treated as a **session code**. If a folder `clients/<CODE>` exists, the slideshow starts.
- Slideshow keys: **ESC** to return to camera, **SPACE** to pause/play, **→ / ←** to navigate, **Q** to quit app.

## Optional: Presence Wake (Face Detection Only)
You can enable simple **face detection** (not recognition) to wake the screen or show a prompt when a person is detected.
This does **not** identify anyone—only detects that a face-like pattern is present using a Haar cascade.

Enable with:
```bash
python app.py --face-detect
```

## Branding
- Replace window titles, add your logo overlay, or customize the on-screen text in `app.py` / `slideshow.py`.
- For MophieProd, you can drop a transparent PNG logo in `assets/logo.png` and it will overlay on the preview.

## Notes
- This app intentionally avoids biometric identification. If you need per-guest mapping, use QR/NFC or short PINs.
- For a dual-screen kiosk, run the slideshow window on the external display (set it in your OS display settings).

## Troubleshooting
- If the webcam is in use, close other apps.
- If QR isn’t detected, ensure the code is large, high-contrast, and well-lit.
- Use JPG/PNG images; very large images are automatically resized to fit screen.

---
© 2025 - MIT License
