import urllib.parse

L = []

# Opening file
bases = []
with open('sqli_base.txt', 'r') as f:
    for line in f:
        bases.append(line.strip())

comments = []
with open('sqli_comments.txt', 'r') as f:
    for line in f:
        comments.append(line.strip())
quotes = []
with open('sqli_quotes.txt', 'r') as f:
    for line in f:
        quotes.append(line.strip())

pause_methods = []
with open('sqli_pause_methods.txt', 'r') as f:
    for line in f:
        pause_methods.append(line.strip())






counter = 0
# Using for loop
for base in bases:
    for comment in comments:
        for pause_method in pause_methods:
            for quote in quotes:
                counter += 1
                x = base.strip().replace('{sqli}', pause_method.strip())
                x = x.replace('{comment}', comment.strip())
                x = x.replace('{quote}', quote.strip())
                print("Line: {}".format(x))
                if x + '\n' not in L:
                    L.append(x + '\n')
            
 



# Writing to file
output_file = open('./output/sqli_payloads.txt', 'w')
output_file.writelines(L)
output_file.close()
 





L_url = []
for x in L:
    L_url.append(urllib.parse.quote(x.replace('\n', '')) + '\n')

# Writing to file
output_file = open('./output/sqli_payloads_urlencoded.txt', 'w')
output_file.writelines(L_url)
output_file.close()
 
