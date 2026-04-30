from PIL import Image
import os

src = r"E:\ScreenTeamLLC\Images\Logo.png"
img = Image.open(src).convert("RGBA")

sizes = {
    "favicon-16x16.png": (16, 16),
    "favicon-32x32.png": (32, 32),
    "apple-touch-icon.png": (180, 180),
    "android-chrome-192x192.png": (192, 192),
    "android-chrome-512x512.png": (512, 512),
}

out = r"E:\ScreenTeamLLC\Images"
for fname, size in sizes.items():
    resized = img.resize(size, Image.LANCZOS)
    resized.save(os.path.join(out, fname))
    print(f"Created {fname}")

ico_path = r"E:\ScreenTeamLLC\favicon.ico"
img16 = img.resize((16, 16), Image.LANCZOS)
img32 = img.resize((32, 32), Image.LANCZOS)
img32.save(ico_path, format="ICO", sizes=[(16, 16), (32, 32)])
print("Created favicon.ico")
