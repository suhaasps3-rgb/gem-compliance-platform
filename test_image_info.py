import pymupdf
doc = pymupdf.open('frontend/public/technical_catalog.pdf')
for page in doc:
    print(page.get_image_info())
