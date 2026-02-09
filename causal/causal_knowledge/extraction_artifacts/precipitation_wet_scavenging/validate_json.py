import json

with open('/home/ubuntu/output/prompt_09_precipitation_wet_scavenging.json', 'r') as f:
    data = json.load(f)

print("JSON valid!")
print(f"Number of relationships: {len(data['relationships'])}")
print(f"Number of sources: {len(data['bibliography'])}")

# Validate required fields
required_rel_fields = ['id', 'cause_node', 'effect_node', 'relationship_type', 'mechanism', 
                       'conditions', 'temporal_lag', 'strength', 'confidence', 
                       'source_url', 'source_title', 'source_authors', 'source_year', 
                       'source_quote', 'source_locator', 'seasonal_variation', 'spatial_scope']

required_bib_fields = ['source_title', 'source_authors', 'source_year', 'source_url', 
                       'source_doi', 'tier', 'relevance_score', 'key_findings']

print("\n--- Validating relationships ---")
for i, rel in enumerate(data['relationships']):
    missing = [f for f in required_rel_fields if f not in rel]
    if missing:
        print(f"Relationship {i+1} ({rel.get('id', 'unknown')}): Missing fields: {missing}")
    else:
        print(f"Relationship {i+1} ({rel['id']}): OK")

print("\n--- Validating bibliography ---")
for i, bib in enumerate(data['bibliography']):
    missing = [f for f in required_bib_fields if f not in bib]
    if missing:
        print(f"Source {i+1}: Missing fields: {missing}")
    else:
        print(f"Source {i+1} ({bib['source_title'][:50]}...): OK")

print("\n--- Summary ---")
print(f"Category: {data['category']}")
print(f"Has handoff_to_other_prompts: {'handoff_to_other_prompts' in data}")
print(f"Has missing_info: {'missing_info' in data}")
print(f"Has contradictions: {'contradictions' in data}")
