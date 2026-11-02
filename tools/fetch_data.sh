#!/usr/bin/env bash
# Downloads the public football datasets and builds the player database.
# Usage: tools/fetch_data.sh
#   OUT=path/to/football_db.json  (default: Football321/Resources/football_db.json)
#   WORK=scratch folder           (default: .data)
# Needs python3 with pandas + pyreadr (pip install -r tools/requirements.txt).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WORK="${WORK:-$ROOT/.data}"
OUT="${OUT:-$ROOT/Football321/Resources/football_db.json}"
mkdir -p "$WORK" && cd "$WORK"

M=https://media.githubusercontent.com/media/salimt/football-datasets/main/datalake/transfermarkt
R=https://raw.githubusercontent.com/salimt/football-datasets/main/datalake/transfermarkt
curl -fsSL -o perf.csv     "$M/player_performances/player_performances.csv"
curl -fsSL -o profiles.csv "$R/player_profiles/player_profiles.csv"
curl -fsSL -o teams.csv    "$R/team_details/team_details.csv"
curl -fsSL -o tcs.csv      "$R/team_competitions_seasons/team_competitions_seasons.csv"
curl -fsSL -o big5_std.rds "https://github.com/JaseZiv/worldfootballR_data/releases/download/fb_big5_advanced_season_stats/big5_player_standard.rds"
[ -d tr/transfers ] || git clone -q --depth 1 https://github.com/ewenme/transfers.git tr/transfers
[ -d sq/squads ] || git clone -q --depth 1 https://github.com/ewenme/squads.git sq/squads
[ -d wf ] || git clone -q --depth 1 https://github.com/JaseZiv/worldfootballR_data.git wf
# dcaribou/transfermarkt-datasets (appearances, lineups, transfers; frozen July 2026 but still the newest free source)
if curl -fsSL -o tmds.zip "https://pub-e682421888d945d684bcae8890b0ec20.r2.dev/data/transfermarkt-datasets.zip"; then
  rm -rf tmds && mkdir tmds && unzip -q -o tmds.zip -d tmds && rm -f tmds.zip
elif [ "${ALLOW_PARTIAL:-0}" = "1" ]; then
  echo "WARNING: transfermarkt-datasets download failed; building without it (ALLOW_PARTIAL=1)" >&2
else
  echo "ERROR: transfermarkt-datasets download failed. Set ALLOW_PARTIAL=1 to build without it." >&2
  exit 1
fi

python3 - <<'PY'
import pandas as pd, re
p = pd.read_csv('perf.csv', dtype=str, usecols=['player_id','season_name','competition_id','team_id','team_name','nb_on_pitch'])
p.to_pickle('perf.pkl')
t = pd.read_csv('tcs.csv', dtype=str)
L = ['GB1','ES1','IT1','L1','FR1','TR1','PO1']
x = t[t.competition_id.isin(L) & (t.season_id.astype(int) >= 2010)]
tm = pd.read_csv('teams.csv', dtype=str).drop_duplicates('club_id').set_index('club_id')
g = x.groupby('club_id').agg(league=('competition_id', lambda s: s.mode()[0])).reset_index()
g['name'] = [re.sub(r' \(\d+\)$', '', tm.club_name.get(i, '?')) for i in g.club_id]
g['tname'] = [x[x.club_id == i].team_name.iloc[0] for i in g.club_id]
g.to_csv('canon_raw.csv', index=False)
PY

python3 "$ROOT/tools/build_db.py" "$WORK" "$ROOT/tools" "$OUT"
echo "Built $OUT"
