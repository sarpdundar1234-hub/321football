"""Build the 321 Football player-career database from several open Transfermarkt/FBref dumps."""
import sys, os, re, json, glob, unicodedata, collections
import pandas as pd, pyreadr
sys.path.insert(0, sys.argv[2])
from clubs_meta import DISPLAY, LEAGUE, POPULAR, EXTRA, KIT, LEAGUE_META, BIG5, EXTRA_CLUBS

D = sys.argv[1]          # download dir
OUT = sys.argv[3]        # output json path

STOP = set('fc cf afc ac as ss ssc sc cd ud rcd ca sd sl us uc acf bc cfc jk sk fk club de la calcio sad futebol sco hsc fco estac '
           'the of y and spor kulubu sportif'.split())
YOUTH = set('b ii iii c u15 u16 u17 u18 u19 u20 u21 u22 u23 youth reserves reserve castilla primavera juniors academy amateure jong sub'.split())
BAD = {'retired', 'without club', 'unknown', 'career break', 'ablöse', 'own youth', 'without_club', '?', '-', ''}


def strip_acc(s):
    s = s.replace('ı', 'i').replace('İ', 'I').replace('ß', 'ss').replace('ø', 'o').replace('Ø', 'O').replace('æ', 'ae').replace('đ', 'd').replace('ł', 'l')
    return ''.join(c for c in unicodedata.normalize('NFKD', s) if not unicodedata.combining(c))


def toks(s):
    s = strip_acc(str(s)).lower().replace('&', ' and ').replace("'", '')
    s = re.sub(r'\(.*?\)', ' ', s)
    return [t for t in re.split(r'[^a-z0-9]+', s) if t]


def ckey(s):
    return ' '.join(t for t in toks(s) if t not in STOP and not t.isdigit())


def pname(s):
    if not isinstance(s, str) or s.strip().lower() in ('', 'nan'):
        return None
    s = re.sub(r'\s*\(\d+\)\s*$', '', str(s)).strip()
    return s


def nkey(s):
    return ' '.join(toks(pname(s)))

# ---------------------------------------------------------------- clubs
canon = pd.read_csv(f'{D}/canon_raw.csv', dtype=str)
canon = canon[canon.league.isin(BIG5) | canon.club_id.isin(EXTRA_CLUBS)]
# 'current' = played in the league's most recent season in the data (or one of the hand-picked extras)
_tcs = pd.read_csv(f'{D}/tcs.csv', dtype=str, usecols=['club_id', 'competition_id', 'season_id'])
_tcs = _tcs[_tcs.competition_id.isin(BIG5)]
_last = _tcs.season_id.astype(int).max()
CURRENT = set(_tcs[_tcs.season_id.astype(int) == _last].club_id) | set(EXTRA_CLUBS)
clubs = []
cidx = {}
alias = collections.defaultdict(set)
for _, r in canon.iterrows():
    cid = r.club_id
    if cid not in DISPLAY:
        # New club (e.g. newly promoted) without hand-written styling: keep the pipeline running
        # with a neutral crest, and say so in the build log.
        _nm = r['name']
        print(f'WARNING: no DISPLAY/_KIT entry for club {cid} ({_nm}); using a neutral crest')
        DISPLAY[cid] = (_nm, ''.join(w[0] for w in _nm.split()[:3]).upper()[:3] or _nm[:3].upper(), [])
        KIT[cid] = ('4A5A52', 'FFFFFF', 'solid')
    disp, short, al = DISPLAY[cid]
    cidx[cid] = len(clubs)
    clubs.append({'id': cid, 'name': disp, 'short': short, 'league': LEAGUE[r.league], 'aliases': [],
                  'kit': KIT[cid], 'current': cid in CURRENT, 'tm': int(cid)})
    for a in [r['name'], r.tname, disp] + al + EXTRA.get(cid, []):
        k = ckey(a)
        if k:
            alias[k].add(cid)
# remove ambiguous aliases
alias = {k: next(iter(v)) for k, v in alias.items() if len(v) == 1}
alias_tokens = {k: set(k.split()) for k in alias}
GENERIC = set('real sporting athletic olympique stade united city town rovers wanderers inter racing union vitoria nacional deportivo atletico borussia eintracht fortuna hellas paris'.split())
_cache = {}


def match_club(s):
    if s is None or (isinstance(s, float)):
        return None
    if s in _cache:
        return _cache[s]
    res = None
    raw = str(s).strip()
    tk = toks(raw)
    if raw.lower() in BAD or any(t in YOUTH for t in tk):
        _cache[s] = None
        return None
    k = ckey(raw)
    if k in alias:
        res = alias[k]
    elif k:
        ks = set(k.split())
        if not ks <= GENERIC:
            cands = {alias[a] for a, at in alias_tokens.items() if ks <= at}
            if len(cands) == 1:
                res = cands.pop()
    _cache[s] = res
    return res

# ---------------------------------------------------------------- records: (tmid|None, name, birthyear|None, tol, club_id, src)
recs = []
tm_name, tm_by = {}, {}


def tmid(url):
    m = re.search(r'/spieler/(\d+)', str(url))
    return m.group(1) if m else None


def toint(x):
    try:
        return int(float(x))
    except (TypeError, ValueError):
        return None


def year(s):
    m = re.match(r'(\d{4})', str(s))
    return int(m.group(1)) if m else None

# salimt profiles + performances
prof = pd.read_csv(f'{D}/profiles.csv', dtype=str, usecols=['player_id', 'player_name', 'date_of_birth'])
for pid, n, dob in prof.itertuples(index=False):
    if pname(n):
        tm_name[pid] = pname(n)
    tm_by[pid] = year(dob)
perf = pd.read_pickle(f'{D}/perf.pkl')
perf = perf[perf.team_id.isin(cidx)]
for pid, tid in perf[['player_id', 'team_id']].drop_duplicates().itertuples(index=False):
    recs.append((pid, None, None, 0, tid, 'perf'))
print('perf recs', len(recs))


def rds(path):
    return list(pyreadr.read_r(path).values())[0]

# worldfootballR transfermarkt squads (big5 2010-22, Portugal 2017-22)
for f in [f'{D}/wf/data/tm_player_vals/big5_player_vals.rds',
          f'{D}/wf/raw-data/fbref-tm-player-mapping/extra-leagues/initial-match/tm_players_extra_tier1.rds',
          f'{D}/wf/raw-data/fbref-tm-player-mapping/data/tm_data.rds']:
    d = rds(f)
    for r in d.itertuples(index=False):
        pid = tmid(r.player_url)
        if pid:
            pname(r.player_name) and tm_name.setdefault(pid, pname(r.player_name))
            if tm_by.get(pid) is None:
                tm_by[pid] = year(r.player_dob)
        for club in (r.squad,):  # joined_from is unreliable in the 2019/20 scrape
            c = match_club(club)
            if c:
                recs.append((pid, r.player_name, year(r.player_dob), 0, c, 'vals'))
print('after vals', len(recs))

# worldfootballR big-5 transfers 2010-22
d = rds(f'{D}/wf/data/tm_transfers/big_5_transfers.rds')
for r in d.itertuples(index=False):
    pid = tmid(r.player_url)
    a = toint(r.player_age); by = toint(r.season) - a if a else None
    if pid:
        pname(r.player_name) and tm_name.setdefault(pid, pname(r.player_name))
        if tm_by.get(pid) is None and by:
            tm_by[pid] = by
    for club in (r.team_name, r.club_2):
        c = match_club(club)
        if c:
            recs.append((pid, r.player_name, by, 1, c, 'tr5'))
print('after tr5', len(recs))

# ewenme transfers 1992-2022
for f in glob.glob(f'{D}/tr/transfers/data/*.csv'):
    d = pd.read_csv(f)
    for r in d.itertuples(index=False):
        a = toint(r.age); by = toint(r.year) - a if a else None
        for club in (r.club_name, r.club_involved_name):
            c = match_club(club)
            if c:
                recs.append((None, r.player_name, by, 1, c, 'ewt'))
print('after ewt', len(recs))

# ewenme squads 2004-2020
for f in glob.glob(f'{D}/sq/squads/data/*/*.csv'):
    d = pd.read_csv(f)
    for r in d.itertuples(index=False):
        c = match_club(r.club_name)
        if c:
            recs.append((None, r.player_name, year(r.date_of_birth), 0, c, 'ews'))
print('after ews', len(recs))

# FBref big-5 2009/10 - 2025/26
fmap = pd.read_csv(f'{D}/wf/raw-data/fbref-tm-player-mapping/output/fbref_to_tm_mapping.csv', dtype=str, encoding='latin-1')
fb2tm = {u: tmid(t) for u, t in zip(fmap.UrlFBref, fmap.UrlTmarkt)}
d = rds(f'{D}/big5_std.rds')
fbref_alt = collections.defaultdict(set)
for r in d.itertuples(index=False):
    c = match_club(r.Squad)
    if not c:
        continue
    pid = fb2tm.get(r.Url)
    by = toint(r.Born)
    if pid:
        fbref_alt[pid].add(r.Player)
    recs.append((pid, r.Player, by, 0, c, 'fb'))
print('after fb', len(recs))

# dcaribou/transfermarkt-datasets (weekly scrape, frozen July 2026): appearances, bench/lineups,
# transfers and current clubs up to the start of the 2026 summer window. Same Transfermarkt IDs.
import os
TMD = f'{D}/tmds'
if os.path.isdir(TMD):
    _pl = pd.read_csv(f'{TMD}/players.csv.gz', dtype=str, usecols=['player_id', 'name', 'date_of_birth', 'current_club_id'])
    for pid, n, dob, cc in _pl.itertuples(index=False):
        if pname(n):
            tm_name.setdefault(pid, pname(n))
        if tm_by.get(pid) is None:
            tm_by[pid] = year(dob)
        if cc in cidx:
            recs.append((pid, None, None, 0, cc, 'tmd'))
    _pairs = set()
    _ap = pd.read_csv(f'{TMD}/appearances.csv.gz', dtype=str, usecols=['player_id', 'player_club_id'])
    _pairs |= set(map(tuple, _ap.drop_duplicates().values))
    _lu = pd.read_csv(f'{TMD}/game_lineups.csv.gz', dtype=str, usecols=['player_id', 'club_id'])
    _pairs |= set(map(tuple, _lu.drop_duplicates().values))
    _tr = pd.read_csv(f'{TMD}/transfers.csv.gz', dtype=str, usecols=['player_id', 'from_club_id', 'to_club_id'])
    _pairs |= set(map(tuple, _tr[['player_id', 'from_club_id']].values)) | set(map(tuple, _tr[['player_id', 'to_club_id']].values))
    for pid, cid in _pairs:
        if cid in cidx:
            recs.append((pid, None, None, 0, cid, 'tmd'))
    print('after tmds', len(recs))

unmatched = collections.Counter()
for s, v in _cache.items():
    if v is None:
        unmatched[s] += 1

# ---------------------------------------------------------------- entity resolution
by_name = collections.defaultdict(list)   # nkey -> [(tmid, by)]
for pid, n in tm_name.items():
    by_name[nkey(n)].append((pid, tm_by.get(pid)))

ent_clubs = collections.defaultdict(set)
ent_names = collections.defaultdict(set)
ent_by = {}
ent_w = collections.Counter()
anon = collections.defaultdict(list)  # nkey -> list of [by, entkey]


def resolve(name, by, tol):
    k = nkey(name)
    cands = [p for p, b in by_name.get(k, []) if by is None or b is None or abs(b - by) <= tol]
    if len(cands) == 1:
        return cands[0]
    if len(cands) > 1:
        exact = [p for p, b in by_name[k] if b == by]
        if len(exact) == 1:
            return exact[0]
        return None if by is None else 'X:%s:%s' % (k, by)
    # anonymous entity
    for slot in anon[k]:
        if by is None or slot[0] is None or abs(slot[0] - by) <= max(tol, 1):
            return slot[1]
    ek = 'N:%s:%s' % (k, by)
    anon[k].append([by, ek])
    return ek

for pid, name, by, tol, c, src in recs:
    if name is not None and (not isinstance(name, str) or name.strip().lower() in ('', 'nan')):
        name = None
        if pid is None:
            continue
    if pid is None:
        pid = resolve(name, by, tol)
        if pid is None:
            continue
    ent_clubs[pid].add(c)
    ent_w[pid] += 1
    if name and pname(name):
        ent_names[pid].add(pname(name))
    if pid in tm_name:
        ent_names[pid].add(tm_name[pid])

players = []
for e, cs in ent_clubs.items():
    if len(cs) < 2:
        continue
    names = {n for n in ent_names[e] | fbref_alt.get(e, set()) if pname(n)}
    if not names and not tm_name.get(e):
        continue
    primary = tm_name.get(e) or sorted(names, key=len)[-1]
    alts = sorted({n for n in names if nkey(n) != nkey(primary)})
    players.append({'n': primary, 'a': alts, 'c': sorted(cidx[c] for c in cs), 'w': ent_w[e]})
players.sort(key=lambda p: -p['w'])
print('players with >=2 eligible clubs:', len(players))

import datetime
DB_VERSION = int(os.environ.get('DB_VERSION') or datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d%H'))
out = {'version': 2, 'schema': 2, 'dbVersion': DB_VERSION,
       'leagues': [{'name': n, 'country': c, 'flag': f} for n, c, f in LEAGUE_META],
       'clubs': [{'name': c['name'], 'short': c['short'], 'league': c['league'],
                  'colors': [c['kit'][0], c['kit'][1]], 'pattern': c['kit'][2], 'current': c['current'], 'tm': c['tm'],
                  'aliases': sorted({a for a in alias if alias[a] == c['id']})} for c in clubs],
       'popular': [cidx[p] for p in POPULAR if p in cidx],
       'players': [[p['n'], p['a'], p['c'], min(p['w'], 999)] for p in players]}
json.dump(out, open(OUT, 'w'), ensure_ascii=False, separators=(',', ':'))
json.dump(unmatched.most_common(), open(f'{D}/unmatched_clubs.json', 'w'), ensure_ascii=False)
print('clubs', len(clubs))
