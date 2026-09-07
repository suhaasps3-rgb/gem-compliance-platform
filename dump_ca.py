import pymupdf
doc = pymupdf.open('frontend/public/ca_turnover.pdf')
text = " ".join(p.get_text() for p in doc)
with open('ca_text_dump.txt', 'w', encoding='utf-8') as f:
    f.write(text)
print("Done, length:", len(text))
