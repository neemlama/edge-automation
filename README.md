# Project 00 - Edge Rewards Auto (DevOps Starter)

Laptop-local automation. No cloud needed. Solves: forget to run, away, daily query edits.

## How it works
- `daily_queries.py` builds a pool from `queries_bank.txt` + 12 templates x 40 topics (~500 combos).
- Deterministic pick by date: `random.Random("2026-09-10").sample(pool, 20)`.
  Same day = same 20. Next day = new 20 automatically. No edits.
- `edge_rewards_automation.py` opens them in Edge Bing, logs to `logs/YYYY-MM-DD.log`.
- Config via env: `NUM_SEARCHES` (default 20), `INTERVAL` (default 8), `REWARDS_DATE`, `DRY_RUN=1` for test.

## Quick test (no browser)
```powershell
cd C:\Users\wecal\Documents\Junior-DevOps-Roadmap\projects\project-00-edge-auto
python daily_queries.py --date 2026-09-10 --count 20
$env:DRY_RUN=1; python edge_rewards_automation.py
```

## Daily use
Double-click `run_daily.bat` or run:
```powershell
python edge_rewards_automation.py
```

## Auto schedule (run even if you forget)
Laptop must be on + Edge signed in.
```powershell
powershell -ExecutionPolicy Bypass -File setup_task.ps1
Get-ScheduledTask -TaskName EdgeRewardsDaily
```
Runs daily 08:00. Change time in `setup_task.ps1` if needed.

## DevOps lessons in this project
- Phase 1: Python scripting, env config, logging, Windows scheduler (cron equivalent)
- Next: Git init + push, then Docker + GitHub Actions lint in Phase 2/3
- ToS note: educational use, respect Microsoft Rewards daily limits (~30-35), keep human-like interval.

## Files
- `edge_rewards_automation.py` - runner
- `daily_queries.py` - date-seeded generator
- `queries_bank.txt` - base list
- `run_daily.bat` / `setup_task.ps1` - local scheduling
- `logs/` - daily run logs
