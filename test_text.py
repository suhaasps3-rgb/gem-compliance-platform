import fitz
doc = fitz.open('backend/static/debarment_demo.pdf')
text = " ".join(page.get_text() for page in doc)
print(repr(text))
