#!/bin/bash

function findConfigFiles() {
  printf "\n\n[+] possible config files" | grep ".*" --color=always
  find . -type f -iname "*conf*" -or -iname "*setting*" 2>/dev/null

  printf "\n\n[+] possible config directories"| grep ".*" --color=always
  find . -type d -iname "*conf*" -or -iname "*setting*" 2>/dev/null

}

function finddate {
  
  if [ "$#" != 4 ]; then
    echo "Invalid number of parameters"
    echo "Usage: finddate <target_file> <-start_date> <+end_date> <search_dir>"
    echo
    echo "Example (finds files with modified date 3 days before to 5 days after modified date of /tmp/test.txt in '.' directory):"
    echo "finddate /tmp/test.txt 3 5  ."
    return
  fi


  modified_date=$(date -r "$1" '+%Y-%m-%d')
  start_date=$(date -d "$modified_date -$2 days" ''+%Y-%m-%d'')
  end_date=$(date -d "$modified_date +$3 days" ''+%Y-%m-%d'')

  # echo $modified_date
  # echo $start_date
  # echo $end_date
  find "$4" -newermt "$start_date" ! -newermt "$end_date" -type f -not -path "*/lib/*" -not -path "*/lib32/*" -not -path "*/libx32/*" -not -path "*/debconf/*" -not -path "*/usr/share/*" -not -path "*/var/cache/*" -not -path "*/etc/*" -not -path "*/usr/bin/*" -not -path "*/usr/include/*" -not -path "*/boot/*" -not -path "*/sbin/*" 2>/dev/null
}


function greppass {
	# perl
  # grep -ri -e "pass" . --exclude-dir=lib --exclude-dir=debconf 2>/dev/null |cut -c -500 | GREP_COLOR="01;36" grep --color=always -P "('.*?')|(\".*?\")" | grep pass --color=always | sort -u
  grep -ri -e "pass" . --exclude-dir=lib --exclude-dir=debconf 2>/dev/null |cut -c -500 | GREP_COLOR="01;36" grep --color=always -e "^" -e "'[^']*'" -e '"[^"]*"' | grep -i pass --color=always | sort -u
  echo "...DONE..."
}

function grepb64 {
  grep -ri -E '^[A-Za-z0-9+_/]{50,1000}$|^[A-Za-z0-9+_/]{50,}{3}=$|^[A-Za-z0-9+_/]{50,}{2}=$' . --color=always 2>/dev/null
  echo "...DONE..."
}

function grepb64d {
  grep -ri -E '^[A-Za-z0-9+_/]{50,1000}$|^[A-Za-z0-9+_/]{50,}{3}=$|^[A-Za-z0-9+_/]{50,}{2}=$' . --color=never 2>/dev/null | xargs -I{} sh -c "echo '{}' | cut -d':' -f2 | base64 -d" | grep -i -e "^" -e pass --color=always
  echo "...DONE..."
}

function grepb64d2 {
  grep -orI -E '[A-Za-z0-9+/]{4}{2,}([A-Za-z0-9+/]{4}|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)' . --color=never 2>/dev/null | cut -c -500 | xargs -P 4 -I{} sh -c 'filename=`echo "{}" | cut -d":" -f1`;decoded=`echo "{}" | cut -d":" -f2 | base64 -d 2>/dev/null`; printf "$filename -- $decoded\n" 2>/dev/null | grep -v "[^[:print:]]" | grep -v "Binary file" | grep -i -e "^" -e "pass" --color=always'   
}


function mgrep {
  # find all files
  # grep those files for GREP_REGEX match
  # for matching files, grep n lines from START_REGEX
  # print if inside contains MATCH_REGEX

  POSITIONAL=()
  unset START_REGEX
  unset MATCH_REGEX
  unset GREP_COLOR_REGEX
  unset EXCLUDE_HIDDEN
  unset EXCLUDE_DIRECTORIES
  DIRECTORIES="."
  NUM_LINES=10




  while [[ $# -gt 0 ]]
  do
  key="$1"

  case $key in
      -sd|--search-directories)
      DIRECTORIES="$2"
      shift
      shift
      ;;
      -n|--num-lines)
      # NUM_LINES="$2"
      LINE_ESCAPES=$(printf "\\\n.*%.0s" `seq $2`)
      shift # past argument
      shift # past value
      ;;
      -sr|--start-regex)
      START_REGEX="$2"
      shift # past argument
      shift # past value
      ;;
      -mr|--match-regex)
      MATCH_REGEX="$2"
      shift # past argument
      shift # past value
      ;;
      -gc|--grep-color-regex)
      GREP_COLOR_REGEX="$2"
      shift
      shift
      ;;
      -xh|--exclude-hidden)
      EXCLUDE_HIDDEN=(-not -path "*/\.*")
      shift
      ;;
      -xd|--exclude-directories)
      DIRS=($(printf $2 | tr ',' ' '))
      printf "${DIRS[@]}"
      pos=$(( ${#DIRS[*]} - 1 ))
      LAST=${DIRS[$pos]} 
      
      EXCLUDE_DIRECTORIES=( \( )
      for i in $(echo $2 | sed "s/,/ /g")
      do
          if [ $i == $LAST ]; then
            break
          fi

          # call your procedure/other scripts here below
          EXCLUDE_DIRECTORIES+=(-path "*/$i/*" -o )
      done
      
      EXCLUDE_DIRECTORIES+=(-path "*/$LAST/*" \) -prune -false -o )

      echo "${EXCLUDE_DIRECTORIES[@]}"

      # \( -path "*/SharePoint-JSON-Helper/*" -o -path "*/hacking-myTools/*" \) -prune -o
      shift
      shift
      ;;
      -h|--help)
      echo '
DISPLAYING HELP

-sd|--search-directories      : starting directories to search in (e.x.:  -sd ". /var /etc" .. default = ".")
-n|--num-lines                : numbers of lines to match after START_REGEX (default = 10)
-sr|--start-regex             : pattern to start matching on
-mr|--match-regex             : pattern to match on (returned in output)
-gc|--grep-color-regex        : pattern to highlight in output
-xh|--exclude-hidden          : exclude hidden files/directories (start with .)
-xd|--exclude-directories     : exclude directories  (e.x.:  -xd "node_modules,folder2")

Example usage:
mgrep -sr "[sS][qQ][lL]" -n 10 -mr '"'"'0.0.0.0.*\n.*\n\|localhost.*\n.*\n\|127.0.0.1.*\n.*\n'"'"' -gc '"'"'sql\|localhost\|127.0.0.1\|0.0.0.0'"'"' -xh -xd "node_modules"

      '

      return
      ;;
      --default)
      DEFAULT=YES
      shift # past argument
      ;;
      *)    # unknown option
      POSITIONAL+=("$1") # save it in an array for later
      shift # past argument
      ;;
  esac
  done
  set -- "${POSITIONAL[@]}" # restore positional parameters


  # # PRINT ARGUMENTS
  # echo $LINE_ESCAPES
  # echo "num lines  = ${NUM_LINES}"
  # echo "grep regex  = ${GREP_REGEX}"
  # echo "start regex  = ${START_REGEX}"
  # echo "match regex = ${MATCH_REGEX}"
  echo "${EXCLUDE_DIRECTORIES[@]}"

  # Start regex is not set
  if [[ -z ${START_REGEX} ]]; then
    echo "START REGEX NOT SET"
    return 
  fi

  # Match  regex is not set
  if [[ -z ${MATCH_REGEX} ]]; then
    echo "MATCH REGEX NOT SET"
    return
  fi

  
  if [[ -n $1 ]]; then
      echo "Last line of file specified as non-opt/last argument:"
      tail -1 "$1"
  fi

  red=`tput setaf 1`
  orange=`tput setaf 3`
  reset=`tput sgr0`

  # find . -type f -not -path '*/\.*' -readable -exec grep -i $GREP_REGEX '{}' -s -l -I \; 2>/dev/null  | xargs -n 1 -P 8 -L1 -I{} sh -c 'echo; echo "'"$green"'EVALUATING: {}'"$reset"'"; sed -n "/'"$START_REGEX"'/{:start /'"$LINE_ESCAPES"'\|'"$MATCH_REGEX"'/!{N;b start};/'"$MATCH_REGEX"'/Ip}" "{}" | cut -c -500 | grep -i -e "^" -e "'"$GREP_COLOR_REGEX"'"  --color=always'


  # TODO: 
  # 1. omit hidden files flag
  # 2. MATCH_REGEX CASE INSENSITIVE
  # find ${DIRECTORIES[@]} "${EXCLUDE_DIRECTORIES[@]}" "${EXCLUDE_HIDDEN[@]}" -type f -readable | grep -e "^" -e git
  # find ${DIRECTORIES[@]} "${EXCLUDE_DIRECTORIES[@]}" "${EXCLUDE_HIDDEN[@]}" -type f -readable

  # echo "find ${DIRECTORIES[@]} "${EXCLUDE_DIRECTORIES[@]}" "${EXCLUDE_HIDDEN[@]}" -type f -readable | grep -e "^" -e git"
  ## REAL
  find ${DIRECTORIES[@]} "${EXCLUDE_DIRECTORIES[@]}" "${EXCLUDE_HIDDEN[@]}" -type f -readable -exec grep -i $START_REGEX '{}' -s -l -I \; 2>/dev/null  | xargs -L1 -I{} sh -c 'tmp=$(sed -n "/'"$START_REGEX"'/{:start /'"$LINE_ESCAPES"'\|'"$MATCH_REGEX"'/!{N;b start};/'"$MATCH_REGEX"'/Ip}" "{}" | cut -c -500 | grep -i -e "^" -e "'"$GREP_COLOR_REGEX"'" --color=always); if [ ! -z "$tmp" ]; then echo; echo "'"$green"'EVALUATING: {}'"$reset"'"; echo "${tmp}" ; fi'


  printf "\n\n..DONE..\n"
}

## ---------- USAGE --------
## grep passwords from current directory
# greppass

function grepdb {
  ## grepdb: sql followed by host
  mgrep -sr "[sS][qQ][lL]" -n 10 -mr '0.0.0.0.*\n.*\n.*\|localhost.*\n.*\n.*\|127.0.0.1.*\n.*\n.*' -gc 'sql\|localhost\|127.0.0.1\|0.0.0.0' -xd "node_modules" # -xh
  # mongo connection string
  # mgrep -sr "[mM][oO][nN][gG][oO]" -n 10 -mr '0.0.0.0.*\n.*\n.*\|localhost.*\n.*\n.*\|127.0.0.1.*\n.*\n.*' -gc 'mongo\|localhost\|127.0.0.1\|0.0.0.0' -xd "node_modules" # -xh
  grep -ir "mongodb://.*\(localhost\|0.0.0.0\|127.0.0.1\)" . --color=always | grep -v node_modules
}


function grepdbr {
  ## grepdb: host followed by sql
  mgrep -sr '0.0.0.0\|localhost\|127.0.0.1' -n 10 -mr "[sS][qQ][lL]" -gc 'sql\|localhost\|127.0.0.1\|0.0.0.0' -xd "node_modules" # -xh
}



mkdir /tmp/grepoutput 2>/dev/null

function mt {
  printf ">>FUNCTIONS<<\n\nfindConfigFiles\nfinddate /tmp/target.txt 5 5 .\n\ngreppass > /tmp/grepoutput/greppass &\ngrepdb > /tmp/grepoutput/grepdb &\ngrepdbr > /tmp/grepoutput/grepdbr &\ngrepb64d2 > /tmp/grepoutput/grepb64d2 & # useful\ngrepb64 > /tmp/grepoutput/grepb64 &\ngrepb64d > /tmp/grepoutput/grepb64d &\n"
}

mt