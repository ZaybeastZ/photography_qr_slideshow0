\
import os
import qrcode
import argparse

def make_qr(text: str, out_path: str):
    img = qrcode.make(text)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path)
    print(f"Saved QR to {out_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate QR code PNG for a session code.")
    parser.add_argument("--make", required=True, help="Session code text (e.g., CLIENT123)")
    parser.add_argument("--out", required=True, help="Output PNG path (e.g., qrs/CLIENT123.png)")
    args = parser.parse_args()
    make_qr(args.make, args.out)
