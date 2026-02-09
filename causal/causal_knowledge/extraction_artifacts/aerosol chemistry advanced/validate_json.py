import json

with open('/home/ubuntu/output/aerosol_chemistry_advanced.json', 'r') as f:
    data = json.load(f)

print("JSON valid!")
print(f"Category: {data['category']}")
print(f"Sub-focus: {data['sub_focus']}")
print(f"Bibliography: {len(data['bibliography'])} sources")
print(f"Relationships: {len(data['relationships'])} relationships")
print("\nRelationship IDs:")
for rel in data['relationships']:
    print(f"  - {rel['id']}: {rel['cause_node']} -> {rel['effect_node']}")
