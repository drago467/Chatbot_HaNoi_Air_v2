import json

with open('emission_sources_pm25_hanoi.json', 'r') as f:
    data = json.load(f)

print("JSON valid!")
print(f"Bibliography: {len(data['bibliography'])} sources")
print(f"Relationships: {len(data['relationships'])} relationships")
print(f"Tier-1 sources: {sum(1 for b in data['bibliography'] if b['tier']=='tier_1')}")
print(f"Tier-2 sources: {sum(1 for b in data['bibliography'] if b['tier']=='tier_2')}")
print("\nRelationship types:")
for r in data['relationships']:
    print(f"  {r['cause_node']} -> {r['effect_node']} ({r['relationship_type']})")
