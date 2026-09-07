from document_parsers import parse_startup
with open('../frontend/public/startup_india_demo.pdf', 'rb') as f:
    res = parse_startup(f.read())
print(res)
