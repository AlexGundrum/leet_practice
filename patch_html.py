import json

with open("c:/Users/alexg/code/leet_practice/algorithms.json", "r", encoding="utf-8") as f:
    algs = json.load(f)
    
fallback_str = f"window.fallbackAlgorithms = {json.dumps(algs)};"

with open("c:/Users/alexg/code/leet_practice/index.html", "r", encoding="utf-8") as f:
    html = f.read()
    
html = html.replace("// __FALLBACK_ALGORITHMS_PLACEHOLDER__", fallback_str)

with open("c:/Users/alexg/code/leet_practice/index.html", "w", encoding="utf-8") as f:
    f.write(html)
    
print("Successfully patched index.html with fallback algorithms.")
