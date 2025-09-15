\
import os
import cv2
import time
import argparse

from slideshow import SlideshowPlayer

HAAR_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

def draw_text(img, text, x, y):
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 4, cv2.LINE_AA)
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2, cv2.LINE_AA)

def run(camera_index=0, clients_root="clients", face_detect=False, auto_exit_slideshow=0, delay=3.0, logo_path="assets/logo.png"):
    qr = cv2.QRCodeDetector()
    face_cascade = None
    if face_detect:
        face_cascade = cv2.CascadeClassifier(HAAR_PATH)

    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        raise RuntimeError(f"Unable to open camera index {camera_index}")

    cv2.namedWindow("Preview", cv2.WINDOW_NORMAL)
    show_logo = os.path.exists(logo_path)
    logo = None
    if show_logo:
        logo = cv2.imread(logo_path, cv2.IMREAD_UNCHANGED)

    last_face_time = 0

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                time.sleep(0.01)
                continue

            # Optional: face detection to wake/prompt (no identification)
            if face_cascade is not None:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.2, 5)
                if len(faces) > 0:
                    last_face_time = time.time()

            # Draw UI hints
            h, w = frame.shape[:2]
            draw_text(frame, "Scan your QR to start your photos", 20, 40)
            draw_text(frame, "Press Q to quit", 20, 70)
            if time.time() - last_face_time < 3:
                draw_text(frame, "👋 Welcome! Hold your QR in front of the camera", 20, 100)

            # Overlay logo if available
            if show_logo and logo is not None:
                lh, lw = logo.shape[:2]
                scale = 0.3
                lw2 = int(lw * scale)
                lh2 = int(lh * scale)
                logo_small = cv2.resize(logo, (lw2, lh2), interpolation=cv2.INTER_AREA)
                # Place top-right
                y1, y2 = 10, 10 + lh2
                x1, x2 = w - lw2 - 10, w - 10
                if logo_small.shape[2] == 4:
                    # alpha blend
                    alpha = logo_small[:, :, 3] / 255.0
                    for c in range(3):
                        frame[y1:y2, x1:x2, c] = (alpha * logo_small[:, :, c] + 
                                                  (1 - alpha) * frame[y1:y2, x1:x2, c])
                else:
                    frame[y1:y2, x1:x2] = logo_small

            # Try detecting QR
            data, points, _ = qr.detectAndDecode(frame)
            if data:
                session = data.strip()
                target_dir = os.path.join(clients_root, session)
                if os.path.isdir(target_dir):
                    # Launch slideshow
                    cap.release()
                    cv2.destroyWindow("Preview")
                    player = SlideshowPlayer(target_dir, delay=delay, auto_exit_after=auto_exit_slideshow)
                    back = player.play()
                    # Re-open camera if we returned from slideshow
                    cap = cv2.VideoCapture(camera_index)
                    if not cap.isOpened():
                        raise RuntimeError(f"Unable to reopen camera index {camera_index}")
                    cv2.namedWindow("Preview", cv2.WINDOW_NORMAL)
                    continue
                else:
                    draw_text(frame, f"No folder for code: {session}", 20, h - 20)

            cv2.imshow("Preview", frame)
            key = cv2.waitKey(10) & 0xFF
            if key in (ord('q'), ord('Q')):
                break

    finally:
        try:
            cap.release()
        except:
            pass
        cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="QR-triggered slideshow app (privacy-friendly).")
    parser.add_argument("--camera", type=int, default=0, help="Camera index (default 0)")
    parser.add_argument("--clients", type=str, default="clients", help="Clients root folder")
    parser.add_argument("--face-detect", action="store_true", help="Enable basic face detection (no identification)")
    parser.add_argument("--timeout", type=int, default=0, help="Auto-exit slideshow after N seconds (0 = loop)")
    parser.add_argument("--delay", type=float, default=3.0, help="Seconds per image in slideshow")
    parser.add_argument("--logo", type=str, default="assets/logo.png", help="Path to logo overlay (optional)")
    args = parser.parse_args()

    run(camera_index=args.camera, clients_root=args.clients, face_detect=args.face_detect,
        auto_exit_slideshow=args.timeout, delay=args.delay, logo_path=args.logo)
