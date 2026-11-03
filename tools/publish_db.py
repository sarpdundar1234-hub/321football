"""Publish a freshly built player database to the GitHub Pages site.

Usage: python tools/publish_db.py <built db .json> <site root> [soccer|nfl|nba|cfb]

Writes <site>/db[/<sport>]/<prefix>-<dbVersion>.json and the manifest.json next to it, which the app
checks on launch (see SportConfig.manifestURL). Does nothing when the player data hasn't changed,
and refuses to publish a database that looks broken.
"""
import hashlib, json, os, sys

built, site = sys.argv[1], sys.argv[2]
sport = sys.argv[3] if len(sys.argv) > 3 else 'soccer'
# sport: (folder under the site, file prefix, min players, min teams) — keep in sync with SportConfig.swift
SPORTS = {
    'soccer': ('db', 'football_db', 10_000, 100),
    'nfl': ('db/nfl', 'nfl_db', 5_000, 30),
    'nba': ('db/nba', 'nba_db', 1_500, 30),
    'cfb': ('db/cfb', 'cfb_db', 5_000, 100),
}
folder, prefix, min_players, min_clubs = SPORTS[sport]
db_dir = os.path.join(site, folder)
os.makedirs(db_dir, exist_ok=True)

raw = open(built, 'rb').read()
db = json.loads(raw)
content = {k: v for k, v in db.items() if k != 'dbVersion'}
content_hash = hashlib.sha256(json.dumps(content, sort_keys=True, ensure_ascii=False).encode()).hexdigest()

players, clubs = len(db['players']), len(db['clubs'])
if db.get('schema') != 2 or players < min_players or clubs < min_clubs:
    sys.exit(f'Refusing to publish: schema={db.get("schema")} players={players} clubs={clubs}')

manifest_path = os.path.join(db_dir, 'manifest.json')
old = json.load(open(manifest_path)) if os.path.exists(manifest_path) else None
if old:
    if old.get('contentHash') == content_hash:
        print('Player data unchanged; nothing to publish.')
        sys.exit(0)
    if old.get('players') and players < old['players'] - 50:
        sys.exit(f'Refusing to publish: players dropped from {old["players"]} to {players} (a source is probably broken)')
    if db['dbVersion'] <= old.get('dbVersion', 0):
        sys.exit(f'Refusing to publish: dbVersion {db["dbVersion"]} is not newer than {old["dbVersion"]}')

name = f'{prefix}-{db["dbVersion"]}.json'
open(os.path.join(db_dir, name), 'wb').write(raw)
manifest = {'schema': 2, 'dbVersion': db['dbVersion'], 'file': name, 'bytes': len(raw),
            'players': players, 'clubs': clubs, 'contentHash': content_hash}
json.dump(manifest, open(manifest_path, 'w'), indent=1)

# Keep this version and the previous one (an app may be mid-download); remove older files.
keep = {name, old['file'] if old else None}
for f in os.listdir(db_dir):
    if f.startswith(prefix + '-') and f.endswith('.json') and f not in keep:
        os.remove(os.path.join(db_dir, f))
print(f'Published {folder}/{name}: {players} players, {clubs} teams')
