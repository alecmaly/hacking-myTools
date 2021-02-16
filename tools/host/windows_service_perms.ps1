

# Source: http://woshub.com/set-permissions-on-windows-service


$str = 'D:(A;;CCLCSWLOCRRC;;;AU)(A;;CCDCLCSWRPWPDTLOCRSDRCWDWO;;;BA)(A;;CCLCSWRPWPDTLOCRRC;;;SY)S:(AU;FA;CCDCLCSWRPWPDTLOCRSDRCWDWO;;;WD)'

#lab
# $str = 'D:(A;;CCLCSWRPWPDTLOCRRC;;;SY)(A;;CCDCLCSWRPWPDTLOCRSDRCWDWO;;;BA)(A;;CCLCSWRPWPLORC;;;WD)'


# example
$str = "D:(A;;CCLCSWRPWPDTLOCRRC;;;SY)(A;;CCDCLCSWRPWPDTLOCRSDRCWDWO;;;BA)(A;;CCLCSWLOCRRC;;;IU)(A;;CCLCSWLOCRRC;;;SU)(A;;RPWPCR;;;S-1-5-21-2133228432-2794320136-1823075350-1000)S:(AU;FA;CCDCLCSWRPWPDTLOCRSDRCWDWO;;;WD)"








$assignable_permissions = @()
$assignable_permissions += (New-Object PSObject -Property @{name='CC'; value='SERVICE_QUERY_CONFIG (request service settings)'})
$assignable_permissions += (New-Object PSObject -Property @{name='LC'; value='SERVICE_QUERY_STATUS (service status polling)'})
$assignable_permissions += (New-Object PSObject -Property @{name='SW'; value='SERVICE_ENUMERATE_DEPENDENTS'})
$assignable_permissions += (New-Object PSObject -Property @{name='LO'; value='SERVICE_INTERROGATE'})
$assignable_permissions += (New-Object PSObject -Property @{name='CR'; value='SERVICE_USER_DEFINED_CONTROL'})
$assignable_permissions += (New-Object PSObject -Property @{name='RC'; value='READ_CONTROL'})
$assignable_permissions += (New-Object PSObject -Property @{name='RP'; value='SERVICE_START'})
$assignable_permissions += (New-Object PSObject -Property @{name='WP'; value='SERVICE_STOP'})
$assignable_permissions += (New-Object PSObject -Property @{name='DT'; value='SERVICE_PAUSE_CONTINUE'})


$common_users_and_groups = @()
$common_users_and_groups += (New-Object PSObject -Property @{name='DT'; value='SERVICE_PAUSE_CONTINUE'})
$common_users_and_groups += (New-Object PSObject -Property @{name='AO'; value='Account operators'})
$common_users_and_groups += (New-Object PSObject -Property @{name='RU'; value='Alias to allow previous Windows 2000'})
$common_users_and_groups += (New-Object PSObject -Property @{name='AN'; value='Anonymous logon'})
$common_users_and_groups += (New-Object PSObject -Property @{name='AU'; value='Authenticated users'})
$common_users_and_groups += (New-Object PSObject -Property @{name='BA'; value='Built-in administrators'})
$common_users_and_groups += (New-Object PSObject -Property @{name='BG'; value='Built-in guests'})
$common_users_and_groups += (New-Object PSObject -Property @{name='BO'; value='Backup operators'})
$common_users_and_groups += (New-Object PSObject -Property @{name='BU'; value='Built-in users'})
$common_users_and_groups += (New-Object PSObject -Property @{name='CA'; value='Certificate server administrators'})
$common_users_and_groups += (New-Object PSObject -Property @{name='CG'; value='Creator group'})
$common_users_and_groups += (New-Object PSObject -Property @{name='CO'; value='Creator owner'})
$common_users_and_groups += (New-Object PSObject -Property @{name='DA'; value='Domain administrators'})
$common_users_and_groups += (New-Object PSObject -Property @{name='DC'; value='Domain computers'})
$common_users_and_groups += (New-Object PSObject -Property @{name='DD'; value='Domain controllers'})
$common_users_and_groups += (New-Object PSObject -Property @{name='DG'; value='Domain guests'})
$common_users_and_groups += (New-Object PSObject -Property @{name='DU'; value='Domain users'})
$common_users_and_groups += (New-Object PSObject -Property @{name='EA'; value='Enterprise administrators'})
$common_users_and_groups += (New-Object PSObject -Property @{name='ED'; value='Enterprise domain controllers'})
$common_users_and_groups += (New-Object PSObject -Property @{name='WD'; value='Everyone'})
$common_users_and_groups += (New-Object PSObject -Property @{name='PA'; value='Group Policy administrators'})
$common_users_and_groups += (New-Object PSObject -Property @{name='IU'; value='Interactively logged-on user'})
$common_users_and_groups += (New-Object PSObject -Property @{name='LA'; value='Local administrator'})
$common_users_and_groups += (New-Object PSObject -Property @{name='LG'; value='Local guest'})
$common_users_and_groups += (New-Object PSObject -Property @{name='LS'; value='Local service account'})
$common_users_and_groups += (New-Object PSObject -Property @{name='SY'; value='Local system'})
$common_users_and_groups += (New-Object PSObject -Property @{name='NU'; value='Network logon user'})
$common_users_and_groups += (New-Object PSObject -Property @{name='NO'; value='Network configuration operators'})
$common_users_and_groups += (New-Object PSObject -Property @{name='NS'; value='Network service account'})
$common_users_and_groups += (New-Object PSObject -Property @{name='PO'; value='Printer operators'})
$common_users_and_groups += (New-Object PSObject -Property @{name='PS'; value='Personal self'})
$common_users_and_groups += (New-Object PSObject -Property @{name='PU'; value='Power users'})
$common_users_and_groups += (New-Object PSObject -Property @{name='RS'; value='RAS servers group'})
$common_users_and_groups += (New-Object PSObject -Property @{name='RD'; value='Terminal server users'})
$common_users_and_groups += (New-Object PSObject -Property @{name='RE'; value='Replicator'})
$common_users_and_groups += (New-Object PSObject -Property @{name='RC'; value='Restricted code'})
$common_users_and_groups += (New-Object PSObject -Property @{name='SA'; value='Schema administrators'})
$common_users_and_groups += (New-Object PSObject -Property @{name='SO'; value='Server operators'})
$common_users_and_groups += (New-Object PSObject -Property @{name='SU'; value='Service logon user'})


function analyze-perm ($str) {
   
    foreach ($perm in ($str.split('('))) {
        if (!$perm) {
            continue
        }

        write-host 
        write-host $perm

        # get Allow / Deny
        If ($perm[0] -eq 'A') {
            write-host 'Allow' -ForegroundColor Green
        } elseif ($perm[0] -eq 'D') {
            write-host 'Deny' -ForegroundColor Red
        }


        # get user / group
        $user_group_code = $perm.split(';')[$perm.split(';').length-1].split(')')[0]
        $found_common_user = $null
        $found_common_user = $common_users_and_groups | where Name -eq $user_group_code

        If ($found_common_user) {
            $color = 'Yellow'
            If ($found_common_user.value.ToLower() -like "*everyone*" -or 
                $found_common_user.value.ToLower() -like "*user*" -or 
                $found_common_user.value.ToLower() -like "*guest*" -or 
                $found_common_user.value.ToLower() -like "*anonymous*" 
            ) {
                $color = 'red'
            }

            write-host "USER/GROUP ($($found_common_user.value))" -ForegroundColor $color
        } else {
            write-host "USER/GROUP NOT FOUND ($user_group_code)" -ForegroundColor Yellow
        }

        $permissions = $perm.split(';')[2]
        # get perms
        foreach ($assignable_permission in $assignable_permissions) {
            $color = 'white'
            If ($permissions -like "*"+$assignable_permission.name+"*") {
                if ($assignable_permission.value -eq 'SERVICE_START' -or $assignable_permission.value -eq 'SERVICE_STOP') {
                    $color = 'red'
                }
                write-host "`t$($assignable_permission.value)" -ForegroundColor $color
            }
        }

    }

}




###### MAIN LOOP #####

do {
    write-host "`n`n`nCMD: sc.exe sdshow SERVICE"
    $str = read-host -Prompt "copy/paste permission string: " 


    write-host FUll Perm:..... $str -ForegroundColor Green

    # analyze D:
    $matches = $null
    $null = $str -match "D:.*?(S:|$)"
    If ($matches) {
        $tmp_str = $matches[0].replace('S:', '').substring(2)

        write-host "[+] Analyzing... D: — Discretionary ACL (DACL)`n" -ForegroundColor Cyan
        write-host $tmp_str
        analyze-perm -str $tmp_str
    }

    # analyse S:

    $matches = $null
    $null = $str -match "S:.*?(D:|$)"
    If ($matches) {
        $tmp_str = $matches[0].replace('D:', '').substring(2)

        write-host -Message  "`n`n[+] Analyzing... S: — System Access Control List (SACL)`n" -ForegroundColor Cyan
        write-host $tmp_str
        analyze-perm -str $tmp_str
    }


} while ($true)

