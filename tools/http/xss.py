#!/bin/python3 

import sys
from termcolor import colored
import urllib.parse
import html
import pyperclip


# javascript
pyperclip.copy('''function copyToClipboard(text) { const elem = document.createElement('textarea'); elem.value = text; document.body.appendChild(elem); elem.select(); document.execCommand('copy'); document.body.removeChild(elem); }
document.body.innerHTML.match('sdfsdf.*sdfsdf')?.forEach(m => { copyToClipboard(m); console.log(m) })''')


# generate
delimiter = '-'
marker = 'sdfsdf'
base = r''''"`<>&()\+*{};$'''
additional_payloads = [r'${1+1}', r'{{1+1}}', r'<%= 1+1 %>', r'${1+1}', r'%{1+1}', r'@(1+1)', '<><sCrIPt>']
chars = []
for x in list(base) + additional_payloads:
    chars.append(x)
    if x != html.escape(x):
        chars.append(html.escape(x))

print('\npayload')
print(marker + delimiter + delimiter.join(chars) + delimiter + marker)

print('\npayload - urlencoded')
print(urllib.parse.quote(marker + delimiter + delimiter.join(chars) + delimiter + marker))


print('\n\nUseful Links:\nhttps://gchq.github.io/CyberChef/#recipe=URL_Decode()\n')

delimiter = '-'
orig_string = r'''sdfsdf-'-&#x27;-"-&quot;-`-<-&lt;->-&gt;-&-&amp;-(-)-\-+-*-{-}-;-$-${1+1}-{{1+1}}-<><sCrIPt>-&lt;&gt;&lt;sCrIPt&gt;-sdfsdf'''
end_string = r'''sdfsdf-'-&#x27;-"-&quot;-\`-<-&lt;->-&gt;-&-&amp;-(-)-\\-+-*-{-}-;-$-${1+1}-{{1+1}}-<%= 1+1 %>-&lt;%= 1+1 %&gt;-${1+1}-%{1+1}-@(1+1)-<><sCrIPt>-&lt;&gt;&lt;sCrIPt&gt;-sdfsdf'''


print(f'old payload: {orig_string}')
print(f'new  result: {end_string}')
for i in range(0, len(orig_string.split(delimiter))):
    orig = orig_string.split(delimiter)[i]
    new = end_string.split(delimiter)[i]
    if orig == new:
        equality, color = '==', 'green'
    else:
        equality, color = '!=', 'red'
    print(colored(f'{orig:7}   {equality}   {new} ', color))


    #  Interesting conditions
    if new == orig + ' ':
        print(colored(f"[+] space added to |{orig}|, this is interesting!", 'yellow'))
    if orig == '\\' and new == '\\':
        print(colored(f"[+] backslashes are not escaped, this is interesting!", 'yellow'))
    if '&' in urllib.parse.unquote(orig) and ';' in urllib.parse.unquote(orig) and html.unescape(urllib.parse.unquote(orig)) == new:
        print(colored(f"[+] html encoded entity is decoded on page, this is interesting!", 'yellow'))
    if '1+1' in orig and '2' in new:
        print(colored(f"[+] equasion evaluated, this is interesting!", 'yellow'))
    if orig == '<><sCrIPt>' and new == '<><sCrIPt>':
        print(colored(f"[+] script tags allowed, this is interesting!", 'yellow'))