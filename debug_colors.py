import pymupdf
doc = pymupdf.open('frontend/public/work_order_1.pdf')
page = doc[0]
rect = page.rect
bottom_rect = pymupdf.Rect(0, rect.height * 0.7, rect.width, rect.height)
pix = page.get_pixmap(clip=bottom_rect)
samples = pix.samples
n = pix.n
colors = {}
for i in range(0, len(samples), n * 10):
    r = samples[i]
    g = samples[i+1]
    b = samples[i+2]
    # ignore white and light grays
    if r > 240 and g > 240 and b > 240: continue
    # ignore black and dark grays
    if r < 20 and g < 20 and b < 20: continue
    rgb = (r,g,b)
    colors[rgb] = colors.get(rgb, 0) + 1

sorted_colors = sorted(colors.items(), key=lambda x: x[1], reverse=True)
print("Top non-B/W colors:")
for color, count in sorted_colors[:10]:
    print(f"RGB{color}: count {count}")
