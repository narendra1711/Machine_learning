# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 14:33:00 2018
https://docs.python.org/3/library/urllib.parse.html
@author: narendra_mugada
"""

# urllib_parse_urlunparse.py


from urllib.parse import urlparse, urlunparse

baseurl = 'https://www.ndtv.com/latest/'

original = 'https://www.ndtv.com/latest/page-2'

for i in range(0,5):
    print(baseurl+"page-"+str(i))
parsed=urlparse(original)

parsed.params=parsed.params+".com"

unpased=urlunparse(parsed)

print('ORIG  :', original)
parsed = urlparse(original)
print('PARSED:', type(parsed), parsed)
t = parsed[:]
print('TUPLE :', type(t), t)
print('NEW   :', urlunparse(t))

