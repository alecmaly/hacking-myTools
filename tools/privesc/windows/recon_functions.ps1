function greppass() {
    echo "[+] grepping passwords... only where password is in quotes ''"
    # powershell.exe -c "findstr /spi pass * | select-string ""(`".*?`")|'.*?'"""
    findstr /spi pass * | select-string "(`".*?`")|'.*?'"
}

function grepdb () {
    # powershell.exe -c "$regex = '(.*sql(.|\n)*(localhost|127.0.0.1|0.0.0.0).*)|(.*(localhost|127.0.0.1|0.0.0.0)(.|\n)*sql.*)'; get-childitem -depth 5 |% { $tmp = $_.FullName; get-content $_.FullName -Raw -erroraction 'silentlycontinue'} | select-string -pattern $regex -AllMatches | % {$_.Matches} | % {write-host "`n`n" $tmp "`n" $_.Value}"
    $regex = '(.*(sql|mongo)(.|\n)*(localhost|127.0.0.1|0.0.0.0).*)|(.*(localhost|127.0.0.1|0.0.0.0)(.|\n)*(sql|mongo).*)'; get-childitem -depth 5 |% { $tmp = $_.FullName; get-content $_.FullName -Raw -erroraction 'silentlycontinue'} | select-string -pattern $regex -AllMatches | % {$_.Matches} | % {write-host "`n`n" $tmp "`n" $_.Value}

}


function grepADS () {
    Get-ChildItem -recurse -Path . | ? { $_.LastWriteTime -gt (Get-Date).AddMinutes(-5) }
}


function findLastModified() {
    Param( $minutes )
    Get-ChildItem -recurse -Path . | ? { $_.LastWriteTime -gt (Get-Date).AddMinutes(-$minutes) }    
}

function grepADS () {
    # cmd /c dir /S /r | findstr /C:":`$DATA" /C:"Directory of" | select-string -Pattern "Directory of.*\n"
    # powershell.exe -c "Get-ChildItem -Recurse | ForEach-Object { Get-Item $_.FullName -Stream * } | Where-Object Stream -ne ':$Data' | Select-Object FileName,Stream"
    Get-ChildItem -Recurse | ForEach-Object { Get-Item $_.FullName -Stream * } | Where-Object Stream -ne ':$Data' | Select-Object FileName,Stream
}

function mt () {
    write-host ">> FUNCTIONS <<"
    write-host "greppass"
    write-host "grepdb"
    write-host "grepADS  # alternative data stream"
    write-host "findLastModified -minutes 5"

}