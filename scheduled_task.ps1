$name = 'Cumpus Network'
$exe = (Get-Command pythonw).path
$params = 'main.py'
$location = Get-Location

Unregister-ScheduledTask -TaskName $name -Confirm:$false -ErrorAction:SilentlyContinue  

$action = New-ScheduledTaskAction -Execute "$exe" -Argument "$params" -WorkingDirectory $location

$triggers = @()
$triggers += New-ScheduledTaskTrigger -Once -At (Get-Date).AddSeconds(7)
$triggers += New-ScheduledTaskTrigger -AtStartup

$CIMTriggerClass = Get-CimClass -ClassName MSFT_TaskEventTrigger -Namespace Root/Microsoft/Windows/TaskScheduler:MSFT_TaskEventTrigger
$trigger = New-CimInstance -CimClass $CIMTriggerClass -ClientOnly
$trigger.Subscription = 
@"
<QueryList><Query Id="0" Path="System"><Select Path="System">*[System[Provider[@Name='Microsoft-Windows-Power-Troubleshooter'] and (EventID=1)]]
</Select></Query></QueryList>
"@
$trigger.Enabled = $True 
$triggers += $trigger

Register-ScheduledTask -TaskName $name -Action $action -Trigger $triggers
