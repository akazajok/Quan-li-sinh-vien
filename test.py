import re
s = "D21CNTT02"
s = [int(c) if c.isdigit() else c.lower() for c in re.split(r'(\d+)', s)]
print(s)