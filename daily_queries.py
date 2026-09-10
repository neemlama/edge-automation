"""
Daily query generator - 20 fresh humanized queries per date, no templates.
Pool = queries_bank.txt (300+ ChatGPT-style human queries).
Same date = same 20. New date = new 20 automatically.
Use --random for truly random each run (ignores date).
Usage:
  python daily_queries.py
  python daily_queries.py --date 2026-09-11 --count 20
  python daily_queries.py --random --count 20
"""
import argparse
import os
import random
from datetime import date
from pathlib import Path

BASE_DIR = Path(__file__).parent
BANK_FILE = BASE_DIR / "queries_bank.txt"


def load_bank():
    if not BANK_FILE.exists():
        raise FileNotFoundError(f"Missing {BANK_FILE}")
    raw = [l.strip() for l in BANK_FILE.read_text(encoding="utf-8").splitlines()]
    queries = []
    for l in raw:
        if not l or l.startswith("#"):
            continue
        # strip copy-paste artifacts: surrounding quotes, trailing commas
        q = l.strip().strip(',').strip()
        # remove surrounding single or double quotes
        if len(q) >= 2 and ((q[0] == '"' and q[-1] == '"') or (q[0] == "'" and q[-1] == "'")):
            q = q[1:-1].strip()
        q = q.strip(',').strip()
        if q:
            queries.append(q)
    # de-dupe preserve order
    seen, uniq = set(), []
    for q in queries:
        if q not in seen:
            seen.add(q)
            uniq.append(q)
    return uniq


def get_daily_queries(date_str=None, count=20, truly_random=False):
    pool = load_bank()
    count = min(count, len(pool))
    if truly_random:
        return random.sample(pool, count)
    if date_str is None:
        date_str = os.getenv("REWARDS_DATE", date.today().isoformat())
    rnd = random.Random(date_str)  # deterministic per date
    return rnd.sample(pool, count)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=None, help="YYYY-MM-DD, default today")
    ap.add_argument("--count", type=int, default=int(os.getenv("NUM_SEARCHES", "20")))
    ap.add_argument("--random", action="store_true", help="truly random, ignore date seed")
    ap.add_argument("--out", default=None, help="output file, default queries_today.txt")
    args = ap.parse_args()

    queries = get_daily_queries(args.date, args.count, args.random)
    out = Path(args.out) if args.out else BASE_DIR / "queries_today.txt"
    out.write_text("\n".join(queries) + "\n", encoding="utf-8")
    mode = "random" if args.random else f"date seed {args.date or 'today'}"
    print(f"Mode: {mode} -> {len(queries)} queries -> {out.name} (pool {len(load_bank())})")
    for i, q in enumerate(queries, 1):
        print(f"{i:2d}. {q}")


if __name__ == "__main__":
    main()
