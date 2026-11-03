#!/usr/bin/env bash
# Downloads the public sources for 321 Gridiron / 321 Hoops / 321 College Football and builds
# <OUT>/<sport>_db.json with tools/build_us.py.
#
#   bash tools/fetch_us_data.sh nfl|nba|cfb|all
#
# Env: WORK (download dir, default ./us-data), OUT (output dir, default ./us-out), DB_VERSION (optional).
# Sources (all open data on GitHub):
#   nfl  nflverse/nflverse-data releases: roster_<season>.csv (1920→), players.csv, teams_colors_logos.csv
#   nba  sumitrodatta/bball-reference-datasets (Basketball-Reference derived season tables)
#   cfb  sportsdataverse/cfbfastR-data rosters (2004→) + team_info, plus the nfl files above for pro teams
set -euo pipefail
SPORT="${1:-all}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WORK="${WORK:-$PWD/us-data}"
OUT="${OUT:-$PWD/us-out}"
mkdir -p "$WORK/nfl" "$WORK/nba" "$WORK/cfb" "$OUT"
YEAR=$(date -u +%Y)
NFLV=https://github.com/nflverse/nflverse-data/releases/download

get() {  # url dest — retry, keep the old copy if the download fails
  local tmp="$2.part"
  if curl -fsSL --retry 3 --retry-delay 5 -o "$tmp" "$1"; then mv "$tmp" "$2"; else rm -f "$tmp"; echo "warn: could not download $1" >&2; return 1; fi
}

fetch_nfl() {
  echo "== nflverse rosters"
  for y in $(seq 1920 "$YEAR"); do
    # past seasons never change: only fetch them once
    if [[ -s "$WORK/nfl/roster_$y.csv" && $y -lt $((YEAR - 1)) ]]; then continue; fi
    get "$NFLV/rosters/roster_$y.csv" "$WORK/nfl/roster_$y.csv" || [[ $y -eq $YEAR ]]
  done
  get "$NFLV/players/players.csv" "$WORK/nfl/players.csv"
  get "$NFLV/teams/teams_colors_logos.csv" "$WORK/nfl/teams_colors_logos.csv"
}

sparse_clone() {  # repo dir paths...
  local repo=$1 dir=$2; shift 2
  if [[ -d "$dir/.git" ]]; then
    git -C "$dir" fetch -q --depth 1 origin HEAD && git -C "$dir" reset -q --hard FETCH_HEAD
  else
    git clone -q --depth 1 --filter=blob:none --sparse "https://github.com/$repo.git" "$dir"
  fi
  git -C "$dir" sparse-checkout set --no-cone "$@"
}

fetch_nba() {
  echo "== bball-reference-datasets"
  sparse_clone sumitrodatta/bball-reference-datasets "$WORK/nba/repo" "/Data/Player Season Info.csv" "/Data/Player Totals.csv"
}

fetch_cfb() {
  echo "== cfbfastR-data rosters + team info"
  sparse_clone sportsdataverse/cfbfastR-data "$WORK/cfb/repo" "/rosters/csv/" "/team_info/parquet/"
  cp "$WORK"/cfb/repo/rosters/csv/cfb_rosters_*.csv "$WORK/cfb/"
  cp "$WORK"/cfb/repo/team_info/parquet/cfb_team_info_*.parquet "$WORK/cfb/"
}

build() {
  echo "== build $1"
  python3 "$ROOT/tools/build_us.py" "$WORK" "$OUT" "$1"
}

case "$SPORT" in
  nfl) fetch_nfl; build nfl ;;
  nba) fetch_nba; build nba ;;
  cfb) fetch_nfl; fetch_cfb; build cfb ;;
  all) fetch_nfl; fetch_nba; fetch_cfb; build nfl; build nba; build cfb ;;
  *) echo "usage: $0 nfl|nba|cfb|all" >&2; exit 2 ;;
esac
ls -la "$OUT"
