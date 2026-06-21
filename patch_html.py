import json
import re

with open("c:/Users/alexg/code/leet_practice/algorithms.json", "r", encoding="utf-8") as f:
    algs = json.load(f)

fallback_str = f"window.fallbackAlgorithms = {json.dumps(algs)};"

with open("c:/Users/alexg/code/leet_practice/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace existing window.fallbackAlgorithms array assignment
html = re.sub(r'window\.fallbackAlgorithms\s*=\s*\[.*?\];', fallback_str, html, flags=re.DOTALL)

with open("c:/Users/alexg/code/leet_practice/index.html", "w", encoding="utf-8") as f:
    f.write(html)
    
print("Successfully patched index.html with new fallback algorithms.")
