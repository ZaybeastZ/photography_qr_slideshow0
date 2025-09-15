\
import os
import cv2
import glob
import time
from typing import List, Optional

class SlideshowPlayer:
    def __init__(self, folder: str, delay: float = 3.0, window_name: str = "Slideshow", auto_exit_after: int = 0):
        self.folder = folder
        self.delay = delay
        self.window_name = window_name
        self.auto_exit_after = auto_exit_after  # seconds; 0 = no auto-exit
        self.images = self._load_images()
        self.index = 0
        self.paused = False
        self.start_time = None

    def _load_images(self) -> List[str]:
        exts = ("*.jpg", "*.jpeg", "*.png", "*.bmp", "*.webp")
        files = []
        for e in exts:
            files.extend(glob.glob(os.path.join(self.folder, e)))
        files.sort()
        if not files:
            raise RuntimeError(f"No images found in: {self.folder}")
        return files

    def _fit_to_screen(self, img, screen_w, screen_h):
        h, w = img.shape[:2]
        scale = min(screen_w / w, screen_h / h)
        new_w = max(1, int(w * scale))
        new_h = max(1, int(h * scale))
        return cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)

    def play(self) -> bool:
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(self.window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        self.start_time = time.time()
        last_switch = time.time()

        # Probe screen size (fallback to 1920x1080 if not available)
        screen_w, screen_h = 1920, 1080

        while True:
            path = self.images[self.index]
            img = cv2.imread(path)
            if img is None:
                # Skip unreadable file
                self.index = (self.index + 1) % len(self.images)
                continue

            # Fit to screen
            disp = self._fit_to_screen(img, screen_w, screen_h)

            # Center on black canvas to avoid stretching
            canvas = cv2.cvtColor(cv2.resize(cv2.cvtColor(disp, cv2.COLOR_BGR2GRAY), (disp.shape[1], disp.shape[0])), cv2.COLOR_GRAY2BGR)  # placeholder to ensure BGR
            canvas = disp  # already BGR

            cv2.imshow(self.window_name, canvas)

            key = cv2.waitKey(10) & 0xFF
            now = time.time()

            if not self.paused and now - last_switch >= self.delay:
                self.index = (self.index + 1) % len(self.images)
                last_switch = now

            # Controls
            if key in (27,):  # ESC -> exit slideshow
                cv2.destroyWindow(self.window_name)
                return True
            elif key in (ord('q'), ord('Q')):
                cv2.destroyAllWindows()
                return False
            elif key in (32,):  # SPACE pause/play
                self.paused = not self.paused
            elif key in (81, ord('h')):  # Left arrow
                self.index = (self.index - 1) % len(self.images)
                last_switch = now
            elif key in (83, ord('l')):  # Right arrow
                self.index = (self.index + 1) % len(self.images)
                last_switch = now

            if self.auto_exit_after > 0 and (now - self.start_time) >= self.auto_exit_after:
                cv2.destroyWindow(self.window_name)
                return True
