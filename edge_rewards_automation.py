"""
Edge Rewards Automation v2 - laptop scheduler version.
- Picks 20 fresh queries automatically by date (no manual edit).
- Random wait 4-7s between each query (human-like).
- Config via env vars: NUM_SEARCHES, MIN_INTERVAL, MAX_INTERVAL, REWARDS_DATE, DRY_RUN.
- Logs to logs/YYYY-MM-DD.log
Usage:
  python edge_rewards_automation.py
  DRY_RUN=1 python edge_rewards_automation.py
  NUM_SEARCHES=20 MIN_INTERVAL=4 MAX_INTERVAL=7 python edge_rewards_automation.py
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
MIN_INTERVAL = float(os.getenv("MIN_INTERVAL", os.getenv("INTERVAL", "4")))
MAX_INTERVAL = float(os.getenv("MAX_INTERVAL", "7"))
# clamp to sane bounds: 4 <= wait < 7+ (user spec)
MIN_INTERVAL = max(4.0, MIN_INTERVAL)
MAX_INTERVAL = min(9.0, max(MIN_INTERVAL + 0.1, MAX_INTERVAL))
if MAX_INTERVAL > 7.0:
    MAX_INTERVAL = 7.0
    if MIN_INTERVAL > MAX_INTERVAL:
        MIN_INTERVAL = 4.0
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


def run_automation(num_searches=NUM_SEARCHES, min_interval=MIN_INTERVAL, max_interval=MAX_INTERVAL):
    log.info(f"Starting automation date={REWARDS_DATE} searches={num_searches} wait_random={min_interval}-{max_interval}s dry_run={DRY_RUN}")
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
            wait_time = random.uniform(min_interval, max_interval)
            log.info(f"Waiting {wait_time:.1f}s before next...")
            time.sleep(wait_time)
    log.info(f"Done: {ok}/{len(queries)} successful. Log: {LOG_FILE}")
    print(f"\nDone {ok}/{len(queries)}. Log: {LOG_FILE}")


if __name__ == "__main__":
    run_automation()
