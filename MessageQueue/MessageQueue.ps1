Param(
    [ValidateSet("discovery", "check")]
    [String[]]
    $option = "discovery",

    [parameter(Mandatory=$True)]
    [String[]]
    $queueName
)

if ($option -eq "discovery") {
    $listQueueName = Get-MsmqQueue -Name $queueName 2> $null
    $json = @{data = @()}

    ForEach($q in $listQueueName) {
      $itemName = $q.QueueName -replace "^[A-Za-z0-9\$]+\\", ""
      $json['data'] += @{ '{#NAME}' = $itemName }
    }

    $json = ConvertTo-Json $json
    Write-Output $json
}

if ($option -eq "check") {
    $zabbix_sender = 'C:\Zabbix_agent\bin\win64\zabbix_sender.exe'
    $hostName = (Get-Content -Path C:\zabbix_agent\conf\zabbix_agentd.win.conf | Where-Object {$_ -like "Hostname=*"}).Split('=')[1]
    $zabbixServer = (Get-Content -Path C:\zabbix_agent\conf\zabbix_agentd.win.conf | Where-Object {$_ -like "ServerActive=*"}).Split('=')[1]
    Get-MsmqQueue -Name $queueName 2> $null | Select-Object -Property QueueName, MessageCount | ForEach-Object {
        $itemName = $_.QueueName
        $itemName = $itemName.split('\')[1]
        $value =  $_.MessageCount
        cmd.exe /c $zabbix_sender -z $zabbixServer -s $hostName -k check[$itemName] -o $value > Out-Null
    }
	Write-Output 1
}
