import json
import ast

with open('c:/Users/alexg/code/leet_practice/enriched_batch_15_29.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for i, d in enumerate(data):
    for j, tc in enumerate(d.get('test_cases', [])):
        try:
            ast.parse(tc['call'])
            ast.parse(tc['expected'])
        except Exception as e:
            print(f"Error in drill {i} test {j}: {e}")
            print(f"Call: {tc['call']}")
            print(f"Expected: {tc['expected']}")
print("Check complete.")
