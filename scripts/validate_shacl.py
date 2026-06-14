from pyshacl import validate
from rdflib import Graph

# Data graph (oyunlar)
data_graph = Graph()
data_graph.parse("vgco_abox.ttl", format="turtle")

# Shapes graph (kurallar)
shapes_graph = Graph()
shapes_graph.parse("vgco_shapes.ttl", format="turtle")

# Validation çalıştır
conforms, results_graph, results_text = validate(
    data_graph,
    shacl_graph=shapes_graph,
    inference='rdfs',
    abort_on_first=False,
    meta_shacl=False,
    debug=False
)
# İstatistikleri çıkar
import re
violations = re.findall(r'Focus Node: (\S+)', results_text)
constraints = re.findall(r'Source Shape:.*?sh:path (\S+)', results_text)

print(f"=== SHACL VALIDATION SUMMARY ===")
print(f"Total violations: {len(violations)}")
print(f"Affected games: {len(set(violations))}")
print(f"\nViolations by constraint:")
from collections import Counter
for constraint, count in Counter(constraints).most_common():
    print(f"  {constraint}: {count}")
print()
print(f"Conforms: {conforms}\n")
print(results_text)

# Sonuçları dosyaya kaydet
with open("shacl_report.txt", "w", encoding="utf-8") as f:
    f.write(f"Conforms: {conforms}\n\n")
    f.write(results_text)

print("\nRapor 'shacl_report.txt' dosyasına kaydedildi.")