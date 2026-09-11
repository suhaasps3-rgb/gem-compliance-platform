import re
with open('backend/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_regex = r"m = _re.search(r'M/s\.?\s*([A-Z][A-Za-z\s]+)(?=,)', text)"
new_regex = r"m = _re.search(r'(?:M/s\.?\s*|Entity:\s*)([A-Za-z0-9\s]+?)(?:,|\n|Supplier|$)', text, _re.IGNORECASE)"

if old_regex in content:
    content = content.replace(old_regex, new_regex)
    with open('backend/main.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print('Patched regex.')
else:
    print('Could not find old regex.')
