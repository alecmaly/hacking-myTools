#!/bin/bash

if [ "$#" -lt 3 ]; then
    echo "USAGE: ./mysqlenum <host> <username> <password> [database]"
fi



host=$1
username=$2
password=$3
database=$4


if [ "$#" -eq 3 ]; then
    mysql --host=$host --user=$username --password=$password -e 'show databases'
fi



if [ "$#" -eq 4 ]; then
    # dump tables to file
    mysql -u $username --password=$password -h $host -e "use $database; show tables" > tables.txt

    # analyze tables
    cat tables.txt | sed 's/\s//g' | tr -d '|' | xargs -I{} sh -c "echo;echo TABLE: {}; echo mysql -u $username --password=$password -h $host -e \'use $database\; SELECT \* FROM {}\;\' \| grep -i pass --color=always | bash"
fi

rm tables.txt 2>/dev/null
