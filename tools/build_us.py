"""Build the player databases for 321 Gridiron (pro football), 321 Hoops (pro basketball)
and 321 College Football.

Usage: python3 tools/build_us.py <data dir> <out dir> [nfl|nba|cfb ...]

<data dir> layout (tools/fetch_us_data.sh creates it):
  nfl/roster_YYYY.csv (nflverse rosters 1920-), nfl/teams_colors_logos.csv
  nba/repo/Data/Player Season Info.csv, Player Totals.csv (sumitrodatta/bball-reference-datasets)
  cfb/cfb_rosters_YYYY.csv (cfbfastR-data, 2004-), cfb/cfb_team_info_YYYY.parquet

Output format = the soccer app's format (schema 2) plus per-player stints with seasons:
  players: [name, altNames, [[teamIndex, firstSeason, lastSeason], ...], weight]
  clubs:   [{name, short, league (tab group), colors, pattern, current, tm (permanent id), pool, tier, aliases}]
"""
import collections, datetime, glob, html, json, os, re, sys, unicodedata
import pandas as pd

D, OUT = sys.argv[1], sys.argv[2]
WHICH = sys.argv[3:] or ['nfl', 'nba', 'cfb']
DB_VERSION = int(os.environ.get('DB_VERSION') or datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d%H'))


def norm(s):
    s = unicodedata.normalize('NFKD', str(s)).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', ' ', s).strip()


def hexcol(c, fallback):
    c = str(c or '').strip().lstrip('#')
    return c.upper() if re.fullmatch(r'[0-9A-Fa-f]{6}', c) else fallback


# Famous nicknames / first-name-only references accepted as answers (applied to the best-known
# player with that exact name, i.e. the one with the highest weight).
NICKNAMES = {
    'nba': {
        "Shaquille O'Neal": ['Shaq'], 'Magic Johnson': ['Magic'], 'Earvin Johnson': ['Magic Johnson', 'Magic'],
        'LeBron James': ['LeBron', 'King James'], 'Kareem Abdul-Jabbar': ['Kareem', 'Lew Alcindor'],
        'Giannis Antetokounmpo': ['Giannis', 'Greek Freak'], 'Wilt Chamberlain': ['Wilt', 'Wilt the Stilt'],
        'Kobe Bryant': ['Kobe'], 'Dwyane Wade': ['D Wade'], 'Julius Erving': ['Dr J'],
        'Penny Hardaway': ['Penny'], 'Anfernee Hardaway': ['Penny Hardaway', 'Penny'],
        'Nikola Jokic': ['Joker'], 'Luka Doncic': ['Luka'], 'Allen Iverson': ['AI', 'The Answer'],
        'Hakeem Olajuwon': ['Hakeem', 'The Dream'], 'Dikembe Mutombo': ['Deke'], 'Tim Duncan': ['Big Fundamental'],
        'Anthony Davis': ['The Brow'], 'Karl-Anthony Towns': ['KAT'], 'Kevin Garnett': ['KG'],
        'Kevin Durant': ['KD'], 'Chris Paul': ['CP3'], 'Victor Wembanyama': ['Wemby'],
    },
    'nfl': {
        'Deion Sanders': ['Prime Time'], 'Walter Payton': ['Sweetness'], 'Calvin Johnson': ['Megatron'],
        'Rob Gronkowski': ['Gronk'], 'Marshawn Lynch': ['Beast Mode'], 'Odell Beckham': ['OBJ'],
        'Odell Beckham Jr.': ['OBJ'], 'Darrelle Revis': ['Revis Island'], 'Christian McCaffrey': ['CMC'],
        'LaDainian Tomlinson': ['LT'], 'Joe Namath': ['Broadway Joe'],
    },
    'cfb': {},
}


def add_nicknames(sport, players):
    table = NICKNAMES.get(sport, {})
    best = {}
    for i, row in enumerate(players):
        if row[0] in table and (row[0] not in best or row[3] > players[best[row[0]]][3]):
            best[row[0]] = i
    for name, i in best.items():
        players[i][1] = sorted(set(players[i][1]) | set(table[name]))


def write(name, groups, clubs, players, popular):
    add_nicknames(name, players)
    out = {'version': 2, 'schema': 2, 'dbVersion': DB_VERSION, 'leagues': groups, 'clubs': clubs,
           'popular': popular, 'players': players}
    path = os.path.join(OUT, f'{name}_db.json')
    json.dump(out, open(path, 'w'), ensure_ascii=False, separators=(',', ':'))
    print(f'{name}: {len(clubs)} teams, {len(players)} players -> {path} ({os.path.getsize(path)//1024} KB)')

# ------------------------------------------------------------------ NFL franchises
NFL = {  # abbr: (id, city, nickname, conf, division, aliases)
 'ARI': (3800, 'Arizona', 'Cardinals', 'NFC', 'NFC West', ['st louis cardinals', 'phoenix cardinals', 'chicago cardinals', 'cards']),
 'ATL': (200, 'Atlanta', 'Falcons', 'NFC', 'NFC South', []),
 'BAL': (325, 'Baltimore', 'Ravens', 'AFC', 'AFC North', []),
 'BUF': (610, 'Buffalo', 'Bills', 'AFC', 'AFC East', []),
 'CAR': (750, 'Carolina', 'Panthers', 'NFC', 'NFC South', []),
 'CHI': (810, 'Chicago', 'Bears', 'NFC', 'NFC North', ['da bears']),
 'CIN': (920, 'Cincinnati', 'Bengals', 'AFC', 'AFC North', []),
 'CLE': (1050, 'Cleveland', 'Browns', 'AFC', 'AFC North', []),
 'DAL': (1200, 'Dallas', 'Cowboys', 'NFC', 'NFC East', ['boys']),
 'DEN': (1400, 'Denver', 'Broncos', 'AFC', 'AFC West', []),
 'DET': (1540, 'Detroit', 'Lions', 'NFC', 'NFC North', ['portsmouth spartans']),
 'GB': (1800, 'Green Bay', 'Packers', 'NFC', 'NFC North', ['pack']),
 'HOU': (2120, 'Houston', 'Texans', 'AFC', 'AFC South', []),
 'IND': (2200, 'Indianapolis', 'Colts', 'AFC', 'AFC South', ['baltimore colts']),
 'JAX': (2250, 'Jacksonville', 'Jaguars', 'AFC', 'AFC South', ['jags']),
 'KC': (2310, 'Kansas City', 'Chiefs', 'AFC', 'AFC West', ['dallas texans']),
 'LV': (2520, 'Las Vegas', 'Raiders', 'AFC', 'AFC West', ['oakland raiders', 'los angeles raiders', 'oakland']),
 'LAC': (4400, 'Los Angeles', 'Chargers', 'AFC', 'AFC West', ['san diego chargers', 'san diego', 'la chargers']),
 'LA': (2510, 'Los Angeles', 'Rams', 'NFC', 'NFC West', ['st louis rams', 'la rams', 'cleveland rams']),
 'MIA': (2700, 'Miami', 'Dolphins', 'AFC', 'AFC East', ['fins']),
 'MIN': (3000, 'Minnesota', 'Vikings', 'NFC', 'NFC North', ['vikes']),
 'NE': (3200, 'New England', 'Patriots', 'AFC', 'AFC East', ['pats', 'boston patriots']),
 'NO': (3300, 'New Orleans', 'Saints', 'NFC', 'NFC South', []),
 'NYG': (3410, 'New York', 'Giants', 'NFC', 'NFC East', ['ny giants', 'g men']),
 'NYJ': (3430, 'New York', 'Jets', 'AFC', 'AFC East', ['ny jets', 'new york titans']),
 'PHI': (3700, 'Philadelphia', 'Eagles', 'NFC', 'NFC East', ['philly']),
 'PIT': (3900, 'Pittsburgh', 'Steelers', 'AFC', 'AFC North', []),
 'SEA': (4600, 'Seattle', 'Seahawks', 'NFC', 'NFC West', ['hawks']),
 'SF': (4500, 'San Francisco', '49ers', 'NFC', 'NFC West', ['niners', 'sf']),
 'TB': (4900, 'Tampa Bay', 'Buccaneers', 'NFC', 'NFC South', ['bucs']),
 'TEN': (2100, 'Tennessee', 'Titans', 'AFC', 'AFC South', ['houston oilers', 'oilers', 'tennessee oilers']),
 'WAS': (5110, 'Washington', 'Commanders', 'NFC', 'NFC East', ['redskins', 'washington football team', 'commies']),
}
NFL_SHORT = {'LA': 'LAR'}


def nfl_franchise(code, y):
    """Historic team code + season -> current franchise abbr (None = defunct franchise)."""
    direct = {'ATL', 'CAR', 'DEN', 'GB', 'IND', 'JAX', 'NE', 'NO', 'NYG', 'NYJ', 'PHI', 'PIT', 'SEA', 'SF', 'TB', 'TEN',
              'LV', 'LAC', 'ARI'}
    if code in direct:
        return code
    alt = {'ARZ': 'ARI', 'PHO': 'ARI', 'CHC': 'ARI', 'BLT': 'BAL', 'CLV': 'CLE', 'HST': 'HOU', 'SL': 'LA', 'RAM': 'LA',
           'RAI': 'LV', 'OAK': 'LV', 'SD': 'LAC', 'NYT': 'NYJ', 'TEX': 'KC', 'COW': 'DAL', 'CHB': 'CHI', 'CHS': 'CHI',
           'DEC': 'CHI', 'POR': 'DET'}
    if code in alt:
        return alt[code]
    rules = {
        'BUF': (1960, None, 'BUF'), 'CIN': (1968, None, 'CIN'), 'MIA': (1966, None, 'MIA'), 'MIN': (1961, None, 'MIN'),
        'DET': (1934, None, 'DET'), 'DAL': (1960, None, 'DAL'), 'WAS': (1937, None, 'WAS'), 'KC': (1963, None, 'KC'),
        'CHI': (1960, None, 'CHI'),
    }
    if code in rules:
        lo, hi, t = rules[code]
        return t if y >= lo and (hi is None or y <= hi) else None
    if code == 'HOU':
        return 'TEN' if y <= 1996 else 'HOU'
    if code == 'BAL':
        return 'IND' if 1953 <= y <= 1983 else ('BAL' if y >= 1996 else None)
    if code == 'CLE':
        return 'LA' if 1937 <= y <= 1945 else ('CLE' if y >= 1946 else None)
    if code == 'STL':
        return 'ARI' if 1960 <= y <= 1987 else ('LA' if 1995 <= y <= 2001 else None)
    if code == 'LA':
        return 'LA' if (1950 <= y <= 1981 or y >= 2016) else ('LAC' if y == 1960 else None)
    if code == 'BOS':
        return 'WAS' if 1932 <= y <= 1936 else ('NE' if 1960 <= y <= 1970 else None)
    if code == 'NY':
        return 'NYG' if 1925 <= y <= 1959 else None
    return None


def load_nfl():
    """Returns {player_key: {'name', 'stints': {abbr: [first,last]}, 'colleges': set, 'seasons': n}}."""
    frames = []
    for f in sorted(glob.glob(f'{D}/nfl/roster_*.csv')):
        frames.append(pd.read_csv(f, dtype=str, low_memory=False,
                                  usecols=lambda c: c in {'season', 'team', 'full_name', 'college', 'gsis_id', 'birth_date', 'status'}))
    r = pd.concat(frames, ignore_index=True)
    r['season'] = r.season.astype(int)
    players = {}
    for row in r.itertuples(index=False):
        fr = nfl_franchise(row.team, row.season)
        teams = [fr] if fr else []
        if row.team == 'P-P':
            teams = ['PHI', 'PIT']
        elif row.team == 'C-P':
            teams = ['ARI', 'PIT']
        if not teams or not isinstance(row.full_name, str):
            continue
        gid = row.gsis_id if isinstance(row.gsis_id, str) else None
        bd = row.birth_date if isinstance(row.birth_date, str) else ''
        key = gid or f'n:{norm(row.full_name)}:{bd}'
        p = players.setdefault(key, {'name': row.full_name, 'stints': {}, 'colleges': set(), 'seasons': set(), 'last': 0})
        if row.season >= p['last']:
            p['name'], p['last'] = row.full_name, row.season
        for t in teams:
            s = p['stints'].setdefault(t, [row.season, row.season])
            s[0], s[1] = min(s[0], row.season), max(s[1], row.season)
        if not isinstance(row.status, str) or row.status in ('ACT', 'RES', 'INA', 'PUP', 'RET', 'TRD', 'TRC', 'TRT'):
            p['seasons'].add(row.season)
        if isinstance(row.college, str):
            for part in html.unescape(row.college).split(';'):
                part = part.strip()
                if part and part.lower() not in ('no college', 'none'):
                    p['colleges'].add(part)
    # Merge records of the same person split across gsis/no-gsis eras (same name + birth date)
    print('nfl roster players', len(players))
    return players


def nfl_teams(prefix_pool=None, id_offset=0):
    tc = pd.read_csv(f'{D}/nfl/teams_colors_logos.csv', dtype=str).set_index('team_abbr')
    clubs, index = [], {}
    order = sorted(NFL, key=lambda a: (NFL[a][3], NFL[a][4], NFL[a][2]))
    for a in order:
        tid, city, nick, conf, div, al = NFL[a]
        row = tc.loc[a] if a in tc.index else None
        p = hexcol(row.team_color if row is not None else '', '333333')
        s = hexcol(row.team_color2 if row is not None else '', 'FFFFFF')
        index[a] = len(clubs)
        clubs.append({'name': f'{city} {nick}', 'short': NFL_SHORT.get(a, a), 'league': conf,
                      'colors': [p, s], 'pattern': 'solid', 'current': True, 'tm': tid + id_offset,
                      'pool': prefix_pool or '', 'tier': '', 'sort': div,
                      'aliases': sorted({nick.lower(), city.lower(), a.lower(), NFL_SHORT.get(a, a).lower(), *al})})
    return clubs, index


def build_nfl():
    players = load_nfl()
    clubs, index = nfl_teams()
    out = []
    for p in players.values():
        if len(p['stints']) < 2:
            continue
        stints = sorted([[index[t], s[0], s[1]] for t, s in p['stints'].items()], key=lambda x: x[1])
        out.append([p['name'], [], stints, max(1, len(p['seasons']))])
    out.sort(key=lambda x: -x[3])
    groups = [{'name': 'AFC', 'country': 'American Football Conference', 'flag': ''},
              {'name': 'NFC', 'country': 'National Football Conference', 'flag': ''}]
    write('nfl', groups, clubs, out, list(range(len(clubs))))
    return players

# ------------------------------------------------------------------ NBA franchises
NBA = {  # code: (id, city, nickname, conf, primary, secondary, short, aliases, historic codes)
 'ATL': (1, 'Atlanta', 'Hawks', 'East', 'C8102E', 'FDB927', 'ATL', ['st louis hawks', 'milwaukee hawks', 'tri cities blackhawks'], ['TRI', 'MLH', 'STL']),
 'BOS': (2, 'Boston', 'Celtics', 'East', '007A33', 'BA9653', 'BOS', ['celts', 'cs'], []),
 'BRK': (3, 'Brooklyn', 'Nets', 'East', '000000', 'FFFFFF', 'BKN', ['new jersey nets', 'nj nets', 'new york nets'], ['NYN', 'NJN']),
 'CHO': (4, 'Charlotte', 'Hornets', 'East', '1D1160', '00788C', 'CHA', ['bobcats', 'charlotte bobcats'], ['CHH', 'CHA']),
 'CHI': (5, 'Chicago', 'Bulls', 'East', 'CE1141', '000000', 'CHI', [], []),
 'CLE': (6, 'Cleveland', 'Cavaliers', 'East', '860038', 'FDBB30', 'CLE', ['cavs'], []),
 'DAL': (7, 'Dallas', 'Mavericks', 'West', '00538C', 'B8C4CA', 'DAL', ['mavs'], []),
 'DEN': (8, 'Denver', 'Nuggets', 'West', '0E2240', 'FEC524', 'DEN', [], []),
 'DET': (9, 'Detroit', 'Pistons', 'East', 'C8102E', '1D42BA', 'DET', ['fort wayne pistons'], ['FTW']),
 'GSW': (10, 'Golden State', 'Warriors', 'West', '1D428A', 'FFC72C', 'GSW', ['dubs', 'san francisco warriors', 'philadelphia warriors'], ['PHW', 'SFW']),
 'HOU': (11, 'Houston', 'Rockets', 'West', 'CE1141', '000000', 'HOU', ['san diego rockets'], ['SDR']),
 'IND': (12, 'Indiana', 'Pacers', 'East', '002D62', 'FDBB30', 'IND', [], []),
 'LAC': (13, 'LA', 'Clippers', 'West', 'C8102E', '1D428A', 'LAC', ['clips', 'san diego clippers', 'buffalo braves', 'los angeles clippers'], ['BUF', 'SDC']),
 'LAL': (14, 'Los Angeles', 'Lakers', 'West', '552583', 'FDB927', 'LAL', ['minneapolis lakers', 'la lakers'], ['MNL']),
 'MEM': (15, 'Memphis', 'Grizzlies', 'West', '5D76A9', '12173F', 'MEM', ['vancouver grizzlies', 'grizz'], ['VAN']),
 'MIA': (16, 'Miami', 'Heat', 'East', '98002E', 'F9A01B', 'MIA', [], []),
 'MIL': (17, 'Milwaukee', 'Bucks', 'East', '00471B', 'EEE1C6', 'MIL', [], []),
 'MIN': (18, 'Minnesota', 'Timberwolves', 'West', '0C2340', '236192', 'MIN', ['wolves', 'twolves'], []),
 'NOP': (19, 'New Orleans', 'Pelicans', 'West', '0C2340', 'C8102E', 'NOP', ['new orleans hornets', 'pels'], ['NOH', 'NOK']),
 'NYK': (20, 'New York', 'Knicks', 'East', '006BB6', 'F58426', 'NYK', ['knickerbockers'], []),
 'OKC': (21, 'Oklahoma City', 'Thunder', 'West', '007AC1', 'EF3B24', 'OKC', ['sonics', 'seattle supersonics', 'supersonics'], ['SEA']),
 'ORL': (22, 'Orlando', 'Magic', 'East', '0077C0', 'C4CED4', 'ORL', [], []),
 'PHI': (23, 'Philadelphia', '76ers', 'East', '006BB6', 'ED174C', 'PHI', ['sixers', 'syracuse nationals'], ['SYR']),
 'PHO': (24, 'Phoenix', 'Suns', 'West', '1D1160', 'E56020', 'PHX', [], []),
 'POR': (25, 'Portland', 'Trail Blazers', 'West', 'E03A3E', '000000', 'POR', ['blazers'], []),
 'SAC': (26, 'Sacramento', 'Kings', 'West', '5A2D81', '63727A', 'SAC', ['kansas city kings', 'cincinnati royals', 'rochester royals'], ['ROC', 'CIN', 'KCO', 'KCK']),
 'SAS': (27, 'San Antonio', 'Spurs', 'West', 'C4CED4', '000000', 'SAS', [], []),
 'TOR': (28, 'Toronto', 'Raptors', 'East', 'CE1141', '000000', 'TOR', ['raps'], []),
 'UTA': (29, 'Utah', 'Jazz', 'West', '002B5C', 'F9A01B', 'UTA', ['new orleans jazz'], ['NOJ']),
 'WAS': (30, 'Washington', 'Wizards', 'East', '002B5C', 'E31837', 'WAS', ['bullets', 'washington bullets', 'baltimore bullets', 'chicago zephyrs'], ['CHP', 'CHZ', 'CAP', 'WSB']),
}


def nba_franchise(code, y):
    if code == 'BAL':
        return 'WAS' if 1964 <= y <= 1973 else None
    for k, v in NBA.items():
        if code == k or code in v[8]:
            return k
    return None


def build_nba():
    info = pd.read_csv(f'{D}/nba/repo/Data/Player Season Info.csv', dtype=str)
    info = info[info.lg.isin(['NBA', 'BAA'])]
    info['season'] = info.season.astype(int)
    tot = pd.read_csv(f'{D}/nba/repo/Data/Player Totals.csv', dtype=str, usecols=['season', 'lg', 'player_id', 'team', 'g'])
    tot = tot[tot.lg.isin(['NBA', 'BAA']) & ~tot.team.str.match(r'^\dTM$|^TOT$', na=False)]
    games = tot.assign(g=pd.to_numeric(tot.g, errors='coerce').fillna(0)).groupby('player_id').g.sum().to_dict()
    clubs, index = [], {}
    for k in sorted(NBA, key=lambda c: (NBA[c][3], NBA[c][1])):
        tid, city, nick, conf, p, s, short, al, hist = NBA[k]
        index[k] = len(clubs)
        clubs.append({'name': f'{city} {nick}', 'short': short, 'league': conf, 'colors': [p, s], 'pattern': 'solid',
                      'current': True, 'tm': tid, 'pool': '', 'tier': '',
                      'aliases': sorted({nick.lower(), city.lower(), short.lower(), k.lower(), *al})})
    players = {}
    for row in info.itertuples(index=False):
        fr = nba_franchise(row.team, row.season)
        if not fr:
            continue
        p = players.setdefault(row.player_id, {'name': row.player, 'stints': {}})
        st = p['stints'].setdefault(fr, [row.season, row.season])
        st[0], st[1] = min(st[0], row.season), max(st[1], row.season)
    out = []
    for pid, p in players.items():
        if len(p['stints']) < 2:
            continue
        stints = sorted([[index[t], s[0], s[1]] for t, s in p['stints'].items()], key=lambda x: x[1])
        out.append([p['name'], [], stints, max(1, int(games.get(pid, 0)) // 10)])
    out.sort(key=lambda x: -x[3])
    groups = [{'name': 'East', 'country': 'Eastern Conference', 'flag': ''},
              {'name': 'West', 'country': 'Western Conference', 'flag': ''}]
    write('nba', groups, clubs, out, list(range(len(clubs))))

# ------------------------------------------------------------------ College
POWER = {'SEC', 'Big Ten', 'Big 12', 'ACC'}
COLLEGE_ALIASES = {  # pro-roster college spellings -> CFBD school
 'mississippi': 'Ole Miss', 'southern california': 'USC', 'north carolina state': 'NC State', 'n c state': 'NC State',
 'miami fla': 'Miami', 'miami fl': 'Miami', 'miami florida': 'Miami', 'louisiana lafayette': 'Louisiana',
 'southwestern louisiana': 'Louisiana', 'miami o': 'Miami (OH)', 'miami ohio': 'Miami (OH)', 'louisiana monroe': 'UL Monroe',
 'northeast louisiana': 'UL Monroe', 'hawaii': "Hawai'i", 'north carolina charlotte': 'Charlotte', 'unc charlotte': 'Charlotte',
 'university of south florida': 'South Florida', 'ohio u': 'Ohio', 'texas state san marcos': 'Texas State',
 'southwest texas state': 'Texas State', 'umass amherst': 'Massachusetts', 'appalachian state': 'App State',
 'san jose state': 'San José State', 'central florida': 'UCF', 'southern mississippi': 'Southern Miss',
 'brigham young': 'BYU', 'texas christian': 'TCU', 'southern methodist': 'SMU', 'alabama birmingham': 'UAB',
 'nevada las vegas': 'UNLV', 'texas el paso': 'UTEP', 'texas san antonio': 'UTSA', 'middle tennessee state': 'Middle Tennessee',
 'connecticut': 'UConn', 'louisiana state': 'LSU', 'bowling green state': 'Bowling Green', 'sam houston state': 'Sam Houston',
 'pittsburgh': 'Pittsburgh', 'pitt': 'Pittsburgh', 'florida international': 'Florida International', 'fiu': 'Florida International',
 'florida atlantic': 'Florida Atlantic', 'fau': 'Florida Atlantic', 'texas a m': 'Texas A&M', 'virginia tech': 'Virginia Tech',
 'army': 'Army', 'west point': 'Army', 'navy': 'Navy', 'air force': 'Air Force', 'east carolina': 'East Carolina',
 'western kentucky': 'Western Kentucky', 'wake forest': 'Wake Forest', 'georgia tech': 'Georgia Tech',
 'louisiana tech': 'Louisiana Tech', 'tulane': 'Tulane', 'tulsa': 'Tulsa', 'rice': 'Rice', 'temple': 'Temple',
 'kent state': 'Kent State', 'kent': 'Kent State', 'north texas state': 'North Texas', 'north texas': 'North Texas',
 'cal': 'California', 'california berkeley': 'California', 'ucla': 'UCLA', 'usc': 'USC', 'lsu': 'LSU', 'tcu': 'TCU', 'smu': 'SMU',
 'byu': 'BYU', 'ucf': 'UCF', 'uab': 'UAB', 'unlv': 'UNLV', 'utep': 'UTEP', 'utsa': 'UTSA', 'uconn': 'UConn',
 'ole miss': 'Ole Miss', 'jacksonville state': 'Jacksonville State', 'james madison': 'James Madison', 'liberty': 'Liberty',
 'coastal carolina': 'Coastal Carolina', 'georgia southern': 'Georgia Southern', 'georgia state': 'Georgia State',
 'south alabama': 'South Alabama', 'old dominion': 'Old Dominion', 'kennesaw state': 'Kennesaw State', 'delaware': 'Delaware',
 'missouri state': 'Missouri State', 'southwest missouri state': 'Missouri State', 'sacramento state': 'Sacramento State',
 'north dakota state': 'North Dakota State', 'new mexico state': 'New Mexico State', 'arkansas state': 'Arkansas State',
}


def build_cfb(nfl_players):
    ti = pd.read_parquet(sorted(glob.glob(f'{D}/cfb/cfb_team_info_*.parquet'))[-1])
    fbs = ti[ti.classification == 'fbs'].copy()
    fbs['conference'] = fbs.conference.replace({'FBS Independents': 'Independents', 'American Athletic': 'American',
                                                'Mid-American': 'MAC', 'Conference USA': 'C-USA'})
    conf_order = ['SEC', 'Big Ten', 'Big 12', 'ACC', 'Independents', 'American', 'Mountain West', 'Sun Belt', 'MAC', 'C-USA', 'Pac-12']
    clubs, index, by_norm = [], {}, {}
    fbs = fbs.sort_values(['conference', 'school'])
    for c in conf_order:
        for t in fbs[fbs.conference == c].itertuples(index=False):
            power = c in POWER or t.school == 'Notre Dame'
            al = {norm(x) for x in [t.school, t.abbreviation, t.alt_name1, t.alt_name2, t.alt_name3, t.mascot,
                                    f'{t.school} {t.mascot}'] if isinstance(x, str) and x and x != 'null'}
            index[t.school] = len(clubs)
            clubs.append({'name': t.school, 'short': str(t.abbreviation or t.school[:4]).upper()[:4], 'league': c,
                          'colors': [hexcol(t.color, '444444'), hexcol(t.alt_color, 'FFFFFF')], 'pattern': 'solid',
                          'current': True, 'tm': int(t.team_id), 'pool': 'college', 'tier': 'power' if power else 'other',
                          'aliases': sorted(al)})
            for a in al:
                by_norm.setdefault(a, set()).add(t.school)
    pro_clubs, pro_index = nfl_teams(prefix_pool='pro', id_offset=1_000_000)
    for c in pro_clubs:
        c['league'] = f'Pro · {c["league"]}'
    off = len(clubs)
    clubs += pro_clubs
    pro_index = {k: v + off for k, v in pro_index.items()}

    def school_of(s):
        k = norm(s)
        if k in COLLEGE_ALIASES:
            return COLLEGE_ALIASES[k]
        hits = by_norm.get(k)
        return next(iter(hits)) if hits and len(hits) == 1 else None

    # College careers from 2004+ rosters (transfers tracked by athlete id, plus same-name hand-offs)
    frames = [pd.read_csv(f, dtype=str, usecols=['athlete_id', 'first_name', 'last_name', 'team', 'season'])
              for f in sorted(glob.glob(f'{D}/cfb/cfb_rosters_*.csv'))]
    r = pd.concat(frames, ignore_index=True)
    r = r[r.team.isin(index.keys())]
    r['season'] = r.season.astype(int)
    r['name'] = (r.first_name.fillna('') + ' ' + r.last_name.fillna('')).str.strip()
    ath = {}
    for row in r.itertuples(index=False):
        a = ath.setdefault(row.athlete_id, {'name': row.name, 'stints': {}})
        st = a['stints'].setdefault(row.team, [row.season, row.season])
        st[0], st[1] = min(st[0], row.season), max(st[1], row.season)
    # join records of one person whose id changed when he transferred (same name, back-to-back seasons)
    by_name = collections.defaultdict(list)
    for aid, a in ath.items():
        by_name[norm(a['name'])].append(aid)
    merged = 0
    for nm, ids in by_name.items():
        if len(ids) < 2 or len(ids) > 4:
            continue
        ids.sort(key=lambda i: min(s[0] for s in ath[i]['stints'].values()))
        for i, j in zip(ids, ids[1:]):
            if i not in ath or j not in ath:
                continue
            a, b = ath[i], ath[j]
            a_last = max(s[1] for s in a['stints'].values()); b_first = min(s[0] for s in b['stints'].values())
            if 0 <= b_first - a_last <= 1 and not set(a['stints']) & set(b['stints']):
                for t, s in b['stints'].items():
                    a['stints'][t] = s
                ath[j] = a
                merged += 1
    print('college athletes', len(ath), 'id hand-offs merged', merged)

    people = []  # {'name', 'stints': {club_idx: [f,l]}, 'w'}
    seen = set()
    cfb_by_name = collections.defaultdict(list)
    for aid, a in ath.items():
        if id(a) in seen:
            continue
        seen.add(id(a))
        rec = {'name': a['name'], 'stints': {index[t]: s for t, s in a['stints'].items()}, 'w': sum(s[1] - s[0] + 1 for s in a['stints'].values())}
        people.append(rec)
        cfb_by_name[norm(a['name'])].append(rec)

    # Pro players: pro franchises + their colleges; merged into the college record when it's the same person
    linked = 0
    for p in nfl_players.values():
        colleges = {school_of(c) for c in p['colleges']} - {None}
        if not colleges:
            continue
        col_idx = {index[c] for c in colleges}
        target = None
        for rec in cfb_by_name.get(norm(p['name']), []):
            if col_idx & set(rec['stints']):
                target = rec
                break
        if target is None:
            target = {'name': p['name'], 'stints': {ci: [0, 0] for ci in col_idx}, 'w': 0}
            people.append(target)
        else:
            linked += 1
            for ci in col_idx:
                target['stints'].setdefault(ci, [0, 0])
        for t, s in p['stints'].items():
            target['stints'][pro_index[t]] = s
        target['w'] += 3 * len(p['seasons'])
    print('pro players linked to college rosters', linked)

    out = []
    for rec in people:
        if len(rec['stints']) < 2:
            continue
        stints = sorted([[ci, s[0], s[1]] for ci, s in rec['stints'].items()], key=lambda x: (x[1], x[0]))
        out.append([rec['name'], [], stints, max(1, rec['w'])])
    out.sort(key=lambda x: -x[3])
    groups = [{'name': c, 'country': c, 'flag': ''} for c in conf_order if any(x['league'] == c for x in clubs)]
    groups += [{'name': 'Pro · AFC', 'country': 'Pro teams (AFC)', 'flag': ''}, {'name': 'Pro · NFC', 'country': 'Pro teams (NFC)', 'flag': ''}]
    popular = [i for i, c in enumerate(clubs) if c['pool'] == 'college' and c['tier'] == 'power'] + \
              [i for i, c in enumerate(clubs) if c['pool'] == 'pro']
    write('cfb', groups, clubs, out, popular)


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    nflp = None
    if 'nfl' in WHICH or 'cfb' in WHICH:
        nflp = build_nfl() if 'nfl' in WHICH else load_nfl()
    if 'nba' in WHICH:
        build_nba()
    if 'cfb' in WHICH:
        build_cfb(nflp)
