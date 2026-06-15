import requests, time, json, os
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    
API_KEY = "d497ff2ef2264be29ddb2351235d1f8f"
BASE    = "https://api.rawg.io/api"

def get(endpoint, params={}):
    params["key"] = API_KEY
    r = requests.get(f"{BASE}{endpoint}", params=params)
    r.raise_for_status()
    return r.json()

existing_ids = set()
if os.path.exists("games.jsonl"):
    with open("games.jsonl", encoding="utf-8") as f:
        for line in f:
            d = json.loads(line)
            existing_ids.add(d["id"])
    print(f"Mevcut: {len(existing_ids)} oyun zaten var, devam ediliyor...")

games_out = open("games.jsonl", "a", encoding="utf-8")  
params = {
    "metacritic": "80,100",
    "dates": "2015-01-01,2025-12-31",
    "page_size": 20
}
url = f"{BASE}/games"
count = len(existing_ids)

while url and count < 500:
    data = requests.get(url, params={**params, "key": API_KEY}).json()
    
    for game in data["results"]:
        if count >= 500:
            break
        if game["id"] in existing_ids:
            continue  
            
        detail = get(f"/games/{game['id']}")
        game["description_raw"] = detail.get("description_raw", "")
        game["playtime"]        = detail.get("playtime", None)
        game["website"]         = detail.get("website", "")
        game["developers"] = detail.get("developers", [])
        game["publishers"] = detail.get("publishers", [])
        games_out.write(json.dumps(game, ensure_ascii=False) + "\n")
        count += 1
        print(f"  {count}: {game['name']}")
        time.sleep(0.5)

    url = data.get("next")
    params = {}

games_out.close()
print(f"Tamamlandı: {count} oyun.")
