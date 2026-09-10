# Registers Windows Task Scheduler job: daily 19:18, runs even if you forget.
# Run in PowerShell as your user (no admin needed for logon task):
#   powershell -ExecutionPolicy Bypass -File setup_task.ps1
# To remove:
#   Unregister-ScheduledTask -TaskName "EdgeRewardsDaily" -Confirm:$false

$ProjectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Python = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $Python) { $Python = "python" }
$Script = Join-Path $ProjectDir "edge_rewards_automation.py"

$Action = New-ScheduledTaskAction -Execute $Python -Argument "`"$Script`"" -WorkingDirectory $ProjectDir
$Trigger = New-ScheduledTaskTrigger -Daily -At 19:18
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -WakeToRun
$Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited

Register-ScheduledTask -TaskName "EdgeRewardsDaily" -Action $Action -Trigger $Trigger -Settings $Settings -Principal $Principal -Description "Edge Rewards auto searches daily 20 queries" -Force
Write-Output "Registered EdgeRewardsDaily at 19:18 daily. Check with: Get-ScheduledTask -TaskName EdgeRewardsDaily"
