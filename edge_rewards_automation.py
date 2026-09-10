"""
Edge Rewards Automation v2 - laptop scheduler version.
- Picks 20 fresh queries automatically by date (no manual edit).
- Config via env vars: NUM_SEARCHES, INTERVAL, REWARDS_DATE, DRY_RUN.
- Logs to logs/YYYY-MM-DD.log
Usage:
  python edge_rewards_automation.py
  DRY_RUN=1 python edge_rewards_automation.py
  NUM_SEARCHES=20 INTERVAL=8 python edge_rewards_automation.py
"""
import logging
import os
import random
import shutil
import sys
import time
import urllib.parse
import webbrowser
from datetime import date
from pathlib import Path

BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))
from daily_queries import get_daily_queries

NUM_SEARCHES = int(os.getenv("NUM_SEARCHES", "20"))
INTERVAL = float(os.getenv("INTERVAL", "8"))
REWARDS_DATE = os.getenv("REWARDS_DATE", date.today().isoformat())
DRY_RUN = os.getenv("DRY_RUN", "0") == "1"

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / f"{REWARDS_DATE}.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.FileHandler(LOG_FILE, encoding="utf-8"), logging.StreamHandler()],
)
log = logging.getLogger("edge-auto")


def setup_edge_browser():
    edge_candidates = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    for path in edge_candidates:
        if os.path.exists(path):
            webbrowser.register("edge", None, webbrowser.BackgroundBrowser(path))
            return "edge"
    msedge_path = shutil.which("msedge") or shutil.which("msedge.exe")
    if msedge_path:
        webbrowser.register("edge", None, webbrowser.BackgroundBrowser(msedge_path))
        return "edge"
    try:
        webbrowser.get()
        return None
    except Exception:
        return None


def perform_search(query, is_first_search=False):
    try:
        encoded_query = urllib.parse.quote(query)
        search_url = f"https://www.bing.com/search?q={encoded_query}&form=QBLH&sp=-1&pq={encoded_query}"
        if DRY_RUN:
            log.info(f"DRY-RUN would search: {query}")
            return True
        try:
            browser = webbrowser.get("edge")
        except Exception:
            browser = webbrowser.get()
        if is_first_search:
            browser.open_new(search_url)
        else:
            browser.open(search_url)
        log.info(f"Searched: {query}")
        return True
    except Exception as e:
        log.error(f"Error searching '{query}': {e}")
        return False


def run_automation(num_searches=NUM_SEARCHES, interval=INTERVAL):
    log.info(f"Starting automation date={REWARDS_DATE} searches={num_searches} interval={interval} dry_run={DRY_RUN}")
    if not DRY_RUN:
        log.info("Make sure you are SIGNED IN to Microsoft account in Edge.")
    setup_edge_browser()
    queries = get_daily_queries(REWARDS_DATE, num_searches)
    log.info(f"Picked {len(queries)} queries for {REWARDS_DATE} (deterministic by date)")
    ok = 0
    for i, query in enumerate(queries, 1):
        log.info(f"[{i}/{len(queries)}] {query}")
        if perform_search(query, is_first_search=(i == 1)):
            ok += 1
        if i < len(queries):
            time.sleep(max(1, interval + random.uniform(-0.5, 0.5)))
    log.info(f"Done: {ok}/{len(queries)} successful. Log: {LOG_FILE}")
    print(f"\nDone {ok}/{len(queries)}. Log: {LOG_FILE}")


if __name__ == "__main__":
    run_automation()
