import json

with open('/home/ubuntu/edge_cases_extractions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("JSON is valid!")
print(f"Number of bibliography entries: {len(data['bibliography'])}")
print(f"Number of relationships: {len(data['relationships'])}")
print("\nRelationship IDs:")
for rel in data['relationships']:
    print(f"  - {rel['id']}: {rel['cause_node']} -> {rel['effect_node']}")
