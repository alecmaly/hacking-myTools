#!/bin/bash

## dumps .mdb (ACCESS) database files to .csv
## dumps to ./output directory where script was ran
## dumps non-empty tables

# make output directory
mkdir output $2>/dev/null

# dump tables
if [[ $# -eq 0 ]] ; then
    echo 'usage: ./dmp_nonempty_tables file.mdb'
    exit 0
fi

# dump table data for nonempty tables
mdb-tables $1 |tr ' ' '\n'>tables


while read p; do
  numlines=$(mdb-export $1 $p|wc -l)

  if [[ "$numlines" -gt "1" ]]; then
    echo dumping $p
    mdb-export $1 $p > ./output/$p.csv
  fi

done <tables
