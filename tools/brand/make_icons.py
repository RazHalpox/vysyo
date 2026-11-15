"""Logo original de Vysyo : un « V » géométrique blanc sur fond violet, avec un point lumineux.
Génère toutes les icônes (Android, bannière TV, Windows, web) à partir de la même géométrie."""
import sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = sys.argv[1]
FONT = os.path.join(ROOT, "android-native/app/src/main/res/font/sora.ttf")
TOP, BOTTOM = (124, 77, 255), (63, 27, 160)      # dégradé violet
SPARK = (196, 181, 253)

def gradient(size, radius_frac):
    w = h = size
    img = Image.new("RGBA", (w, h))
    px = img.load()
    for y in range(h):
        t = y / (h - 1)
        c = tuple(int(TOP[i] * (1 - t) + BOTTOM[i] * t) for i in range(3)) + (255,)
        for x in range(w):
            px[x, y] = c
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, h - 1], radius=int(w * radius_frac), fill=255)
    img.putalpha(mask)
    return img

def draw_mark(d, s, ox=0, oy=0, color=(255, 255, 255, 255), spark=SPARK + (255,)):
    """Le « V » dans un carré de côté s (géométrie sur une grille de 108)."""
    k = s / 108
    pts = [(34, 38), (54, 74), (74, 38)]
    pts = [(ox + x * k, oy + y * k) for x, y in pts]
    wdt = int(12 * k)
    d.line(pts, fill=color, width=wdt, joint="curve")
    for p in (pts[0], pts[2], pts[1]):
        r = wdt / 2
        d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=color)
    cx, cy, r = ox + 80 * k, oy + 28 * k, 5 * k
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=spark)

def icon(size, round_=False):
    big = size * 4
    img = gradient(big, 0.5 if round_ else 0.22)
    draw_mark(ImageDraw.Draw(img), big)
    return img.resize((size, size), Image.LANCZOS)

def save(img, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path)

res = os.path.join(ROOT, "android-native/app/src/main/res")
for folder, px in {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}.items():
    save(icon(px), f"{res}/mipmap-{folder}/ic_launcher.png")
    save(icon(px, True), f"{res}/mipmap-{folder}/ic_launcher_round.png")

# Bannière Android TV 640x360 : fond sombre, halo violet, logo + nom.
W, H = 1280, 720
ban = Image.new("RGB", (W, H), (14, 10, 28))
glow = Image.new("RGB", (W, H), (0, 0, 0))
ImageDraw.Draw(glow).ellipse([80, 60, 720, 700], fill=(80, 40, 190))
ban = Image.blend(ban, glow.filter(ImageFilter.GaussianBlur(160)), 0.55)
ban = ban.convert("RGBA")
tile = icon(300)
ban.alpha_composite(tile, (150, 210))
d = ImageDraw.Draw(ban)
font = ImageFont.truetype(FONT, 190)
try:
    font.set_variation_by_axes([800])
except Exception:
    pass
d.text((500, 360), "Vysyo", font=font, fill=(255, 255, 255), anchor="lm")
save(ban.convert("RGB").resize((640, 360), Image.LANCZOS), f"{res}/drawable-xhdpi/banner.png")

# Bureau et web.
el = os.path.join(ROOT, "electron/build")
big = icon(1024)
save(big, f"{el}/icon.png")
save(icon(512), f"{el}/icon-512.png")
big.save(f"{el}/icon.ico", sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
print("icônes générées")
