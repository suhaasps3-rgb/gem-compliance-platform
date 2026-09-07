import pymupdf
doc = pymupdf.open('frontend/public/technical_catalog.pdf')
page = doc[0]

rect = page.rect
bottom_rect = pymupdf.Rect(0, rect.height * 0.3, rect.width, rect.height)
pix = page.get_pixmap(clip=bottom_rect)

samples = pix.samples
n = pix.n # 3 for RGB, 4 for RGBA
blue_pixel_count = 0

# Fast heuristic: sample every 10th pixel to detect blue/violet
# Blue/Violet typically means B > R + 20 and B > G + 20 and B > 80
for i in range(0, len(samples), n * 10):
    r = samples[i]
    g = samples[i+1]
    b = samples[i+2]
    if b > r + 20 and b > g + 20 and b > 80:
        blue_pixel_count += 1

print(f"Blue pixel count: {blue_pixel_count}")
