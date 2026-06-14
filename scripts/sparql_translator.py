import os
import re
from pathlib import Path
from dotenv import load_dotenv
from rdflib import Graph, Namespace
from google import genai
from google.genai import types

# Define Namespaces
BFO = Namespace("http://purl.obolibrary.org/obo/BFO_0000030#")
VGCO = Namespace("https://github.com/basakkocan/VGCO/ontology/vgco/")

def load_environment():
    """Locate and load .env file up to the parent directory."""
    current_dir = Path(__file__).resolve().parent
    for parent in [current_dir] + list(current_dir.parents):
        env_path = parent / '.env'
        if env_path.exists():
            load_dotenv(dotenv_path=env_path)
            return True
    return False

def load_ontology_graph():
    """Load schema and instances into an rdflib Graph."""
    repo_root = Path(__file__).resolve().parent.parent
    ttl_path = repo_root / "ontology" / "vgco.ttl"
    abox_path = repo_root / "ontology" / "vgco_abox.ttl"
    
    g = Graph()
    g.bind("bfo", BFO)
    g.bind("vgco", VGCO)
    
    if ttl_path.exists():
        g.parse(str(ttl_path), format="turtle")
    else:
        raise FileNotFoundError(f"Ontology file not found at {ttl_path}")
        
    if abox_path.exists():
        g.parse(str(abox_path), format="turtle")
    else:
        print(f"Warning: ABox data file not found at {abox_path}")
        
    return g

def get_gemini_client():
    """Initialize the Google GenAI client using the environment's API key."""
    load_environment()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set in .env")
    return genai.Client(api_key=api_key)

def clean_sparql_query(response_text: str) -> str:
    """Extract clean SPARQL query from markdown response."""
    # Find code blocks
    match = re.search(r'```(?:sparql)?(.*?)```', response_text, re.DOTALL | re.IGNORECASE)
    if match:
        query = match.group(1).strip()
    else:
        query = response_text.strip()
    return query

def translate_to_sparql(natural_language_query: str) -> str:
    """Translate natural language query to SPARQL using Gemini."""
    client = get_gemini_client()
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    
    # Prompt explaining ontology schema, prefixes, and examples
    system_instruction = """
You are a semantic web assistant specialized in the Video Game Catalog Ontology (VGCO).
Your task is to translate natural language user questions (in English or Turkish) into valid SPARQL SELECT queries.

Ontology Details:
- PREFIX bfo: <http://purl.obolibrary.org/obo/BFO_0000030#>
- PREFIX vgco: <https://github.com/basakkocan/VGCO/ontology/vgco/>
- PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

Classes:
- bfo:VideoGame : A video game.
- bfo:Developer : Game developer studio.
- bfo:Publisher : Game publisher organization.
- bfo:Platform : Platform environment (e.g. bfo:Pc, bfo:Playstation4, bfo:PlayStation5, bfo:XboxSeriesX, etc.).
- bfo:Genre : Game genre (e.g. bfo:ActionRPG, bfo:RPG, bfo:Adventure, bfo:Shooter).
- bfo:Tag : Specific tag (e.g. bfo:OpenWorld, bfo:SoulsLike, bfo:Multiplayer).
- bfo:ESRBRating : Age ratings (e.g. bfo:EveryoneRating, bfo:TeenRating, bfo:Mature17Plus).
- bfo:Store : Storefront where the game is sold (e.g. bfo:Steam, bfo:PlayStationStore).
- bfo:GameSeries : Overarching franchise or game series (e.g. bfo:SoulsSeries).
- bfo:Media : Abstract media class.
- bfo:Screenshot : Gameplay screenshots (subclass of bfo:Media).
- bfo:Trailer : Promotional video trailers (subclass of bfo:Media).

Object Properties:
- bfo:availableOn (domain: bfo:VideoGame, range: bfo:Platform)
- bfo:developedBy (domain: bfo:VideoGame, range: bfo:Developer)
- bfo:publishedBy (domain: bfo:VideoGame, range: bfo:Publisher)
- bfo:hasGenre (domain: bfo:VideoGame, range: bfo:Genre)
- bfo:hasTag (domain: bfo:VideoGame, range: bfo:Tag)
- bfo:hasESRBRating (domain: bfo:VideoGame, range: bfo:ESRBRating)
- bfo:soldOn (domain: bfo:VideoGame, range: bfo:Store)
- bfo:partOfSeries (domain: bfo:VideoGame, range: bfo:GameSeries)
- bfo:hasScreenshot (domain: bfo:VideoGame, range: bfo:Screenshot)
- bfo:hasTrailer (domain: bfo:VideoGame, range: bfo:Trailer)

Datatype Properties:
- bfo:title (range: xsd:string) - The title of the game.
- bfo:metacriticScore (range: xsd:integer) - Metacritic critical score (0-100).
- bfo:rating (range: xsd:decimal) - User rating (0.0 - 5.0).
- bfo:ratingsCount (range: xsd:integer) - Number of ratings.
- bfo:releaseDate (range: xsd:dateTime) - ISO format release date.
- bfo:playtimeHours (range: xsd:integer) - Average playtime in hours.
- bfo:officialWebsite (range: xsd:anyURI) - Website URL.
- bfo:coverImageUrl (range: xsd:anyURI) - Cover art image URL.
- bfo:description (range: xsd:string) - Text summary of the game.
- bfo:mediaUrl (range: xsd:anyURI) - URL pointing to a media asset (screenshot or trailer).
- bfo:slug (range: xsd:string) - URL-friendly slug.

Naming Conventions for IRIs:
- Individual URIs for genres, tags, platforms, developers, and publishers are camel cased or TitleCase and clean. E.g.:
  - PC -> bfo:Pc
  - PlayStation 5 -> bfo:PlayStation5
  - Action RPG -> bfo:ActionRPG
  - FromSoftware -> bfo:FromSoftware
  - Larian Studios -> bfo:LarianStudios
- When the user asks for a specific developer, publisher, tag, or genre, try to use the direct IRI if it's obvious, OR use a FILTER with regex on the title or name if you are unsure of the IRI. E.g.:
  `FILTER(regex(str(?devName), "FromSoftware", "i"))` or matching property names.
- Let's prioritize using `bfo:title ?title` to display game titles instead of the raw resource URI.

Example SPARQL Queries:
1. "PC and PS4 games with Metacritic score above 90":
```sparql
PREFIX bfo: <http://purl.obolibrary.org/obo/BFO_0000030#>
SELECT ?title ?score WHERE {
  ?game a bfo:VideoGame ;
        bfo:title ?title ;
        bfo:availableOn bfo:Pc ;
        bfo:availableOn bfo:Playstation4 ;
        bfo:metacriticScore ?score .
  FILTER(?score > 90)
}
ORDER BY DESC(?score)
LIMIT 10
```

2. "Action games developed by FromSoftware":
```sparql
PREFIX bfo: <http://purl.obolibrary.org/obo/BFO_0000030#>
SELECT ?title ?score WHERE {
  ?game a bfo:VideoGame ;
        bfo:title ?title ;
        bfo:developedBy bfo:FromSoftware ;
        bfo:hasGenre bfo:Action .
  OPTIONAL { ?game bfo:metacriticScore ?score . }
}
```

3. "Hangi platformda kaç oyun var?" (How many games are on each platform?):
```sparql
PREFIX bfo: <http://purl.obolibrary.org/obo/BFO_0000030#>
SELECT ?platform (COUNT(?game) AS ?count) WHERE {
  ?game a bfo:VideoGame ;
        bfo:availableOn ?platform .
}
GROUP BY ?platform
ORDER BY DESC(?count)
```

Rules:
1. Respond ONLY with the SPARQL query code block enclosed in ```sparql ... ```.
2. Do not include any explanations, introduction, or warnings.
3. Ensure the syntax is valid SPARQL 1.1.
4. Support both Turkish and English queries.
"""

    prompt = f"User Question: {natural_language_query}\nSPARQL Query:"
    
    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.0, # deterministic for queries
        )
    )
    
    return clean_sparql_query(response.text)

def execute_sparql(graph: Graph, query_str: str):
    """Execute the SPARQL query on the graph and return results in a serializable list format."""
    results = graph.query(query_str)
    headers = [str(var) for var in results.vars]
    
    rows = []
    for row in results:
        formatted_row = []
        for val in row:
            if val is None:
                formatted_row.append("")
            else:
                # Pretty print URIs if they match namespaces
                val_str = str(val)
                if val_str.startswith(str(BFO)):
                    formatted_row.append("bfo:" + val_str[len(str(BFO)):])
                elif val_str.startswith(str(VGCO)):
                    formatted_row.append("vgco:" + val_str[len(str(VGCO)):])
                else:
                    formatted_row.append(val_str)
        rows.append(formatted_row)
        
    return headers, rows

def translate_and_query(natural_language_query: str, graph: Graph = None):
    """Helper function to translate and execute a query in one go."""
    if graph is None:
        graph = load_ontology_graph()
    
    sparql_query = translate_to_sparql(natural_language_query)
    headers, rows = execute_sparql(graph, sparql_query)
    return sparql_query, headers, rows
