with open('backend/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_str = 'result["extracted"]["entity_name"] = m.group(1).strip()'
new_str = 'result["extracted"]["entity_name"] = m.group(1).strip()\n        print("\\n*** ENTITY MATCHED:", m.group(1).strip(), "***\\n")'

content = content.replace(old_str, new_str)
with open('backend/main.py', 'w', encoding='utf-8') as f:
    f.write(content)
