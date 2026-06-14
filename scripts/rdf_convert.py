import json, html, re
from rdflib import Graph, Namespace, URIRef, Literal, RDF, RDFS, XSD

# Ontology'nizin gerçek namespace'i
BFO = Namespace("http://purl.obolibrary.org/obo/BFO_0000030#")
VGCO = Namespace("https://github.com/basakkocan/VGCO/ontology/vgco/")

g = Graph()
g.bind("bfo", BFO)
g.bind("vgco", VGCO)

ESRB_MAP = {
    "everyone":      "EveryoneRating",
    "teen":          "TeenRating", 
    "mature":        "Mature17Plus",
    "adults-only":   "AdultsOnly",
    "rating-pending":"RatingPending",
}

def clean(text):
    return re.sub(r'<.*?>', '', html.unescape(text or "")).strip()

with open("games.jsonl", encoding="utf-8") as f:
    for line in f:
        d = json.loads(line)
        game = URIRef(BFO[d['slug'].replace("-", "_")])
        
        g.add((game, RDF.type, BFO.VideoGame))
        g.add((game, BFO.title,    Literal(d["name"])))
        g.add((game, BFO.rawgId,   Literal(d["id"], datatype=XSD.integer)))
        g.add((game, BFO.slug,     Literal(d["slug"])))

        if d.get("metacritic"):
            g.add((game, BFO.metacriticScore, Literal(d["metacritic"], datatype=XSD.integer)))
        if d.get("rating"):
            g.add((game, BFO.rating,          Literal(d["rating"],     datatype=XSD.decimal)))
        if d.get("ratings_count"):
            g.add((game, BFO.ratingsCount,    Literal(d["ratings_count"], datatype=XSD.integer)))
        if d.get("released"):
            g.add((game, BFO.releaseDate,     Literal(d["released"] + "T00:00:00", datatype=XSD.dateTime)))
        if d.get("playtime"):
            g.add((game, BFO.playtimeHours,   Literal(d["playtime"],   datatype=XSD.integer)))
        if d.get("website"):
            g.add((game, BFO.officialWebsite, Literal(d["website"],    datatype=XSD.anyURI)))
        if d.get("background_image"):
            g.add((game, BFO.coverImageUrl,   Literal(d["background_image"], datatype=XSD.anyURI)))
        if d.get("description_raw"):
            g.add((game, BFO.description,     Literal(clean(d["description_raw"]))))

        for genre in d.get("genres", []):
            g.add((game, BFO.hasGenre, URIRef(BFO[genre['slug'].replace("-","_").title()])))

        for p in d.get("platforms", []):
            slug = p["platform"]["slug"].replace("-","_").title()
            g.add((game, BFO.availableOn, URIRef(BFO[slug])))

        for dev in d.get("developers", []):
            g.add((game, BFO.developedBy, URIRef(BFO[dev['slug'].replace("-","_").title()])))

        for pub in d.get("publishers", []):
            g.add((game, BFO.publishedBy, URIRef(BFO[pub['slug'].replace("-","_").title()])))

        for tag in d.get("tags", []):
            g.add((game, BFO.hasTag, URIRef(BFO[tag['slug'].replace("-","_").title()])))

        esrb = d.get("esrb_rating")
        if esrb and esrb.get("slug") in ESRB_MAP:
            g.add((game, BFO.hasESRBRating, URIRef(BFO[ESRB_MAP[esrb["slug"]]])))
        else:
            g.add((game, BFO.hasESRBRating, URIRef(BFO["RatingPending"])))
            

g.serialize("vgco_abox.ttl", format="turtle")
print(f"Tamamlandı: {len(g)} triple kaydedildi.")