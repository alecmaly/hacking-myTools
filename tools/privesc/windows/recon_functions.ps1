function greppass() {
    echo "[+] grepping passwords... only where password is in quotes ''"
    # powershell.exe -c "findstr /spi pass * | select-string ""(`".*?`")|'.*?'"""
    findstr /spi pass * | select-string "(`".*?`")|'.*?'"
}

function grepdb () {
    # powershell.exe -c "$regex = '(.*sql(.|\n)*(localhost|127.0.0.1|0.0.0.0).*)|(.*(localhost|127.0.0.1|0.0.0.0)(.|\n)*sql.*)'; get-childitem -depth 5 |% { $tmp = $_.FullName; get-content $_.FullName -Raw -erroraction 'silentlycontinue'} | select-string -pattern $regex -AllMatches | % {$_.Matches} | % {write-host "`n`n" $tmp "`n" $_.Value}"
    $regex = '(.*(sql|mongo)(.|\n)*(localhost|127.0.0.1|0.0.0.0).*)|(.*(localhost|127.0.0.1|0.0.0.0)(.|\n)*(sql|mongo).*)'; get-childitem -depth 5 |% { $tmp = $_.FullName; get-content $_.FullName -Raw -erroraction 'silentlycontinue'} | select-string -pattern $regex -AllMatches | % {$_.Matches} | % {write-host "`n`n" $tmp "`n" $_.Value}

}