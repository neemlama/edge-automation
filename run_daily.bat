@echo off
REM Daily runner - double-click or Task Scheduler calls this
cd /d "%~dp0"
set NUM_SEARCHES=20
set INTERVAL=8
python edge_rewards_automation.py
pause
