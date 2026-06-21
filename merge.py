import json

batches = [
    "enriched_batch_0_14.json",
    "enriched_batch_15_29.json",
    "enriched_batch_30_44.json",
    "enriched_batch_45_59.json",
    "enriched_batch_60_72.json"
]

all_algorithms = []
for batch in batches:
    with open(f"c:/Users/alexg/code/leet_practice/{batch}", "r", encoding="utf-8") as f:
        data = json.load(f)
        # Ensure we don't accidentally nest
        if isinstance(data, dict):
             # Some models might return a dict mapping id -> obj
             all_algorithms.extend(list(data.values()))
        else:
             all_algorithms.extend(data)

with open("c:/Users/alexg/code/leet_practice/algorithms.json", "w", encoding="utf-8") as f:
    json.dump(all_algorithms, f, indent=2)

print(f"Merged {len(all_algorithms)} algorithms successfully.")
