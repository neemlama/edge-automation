@echo off
REM Daily runner - double-click or Task Scheduler calls this
cd /d "%~dp0"
set NUM_SEARCHES=20
set MIN_INTERVAL=4
set MAX_INTERVAL=7
python edge_rewards_automation.py
pause
