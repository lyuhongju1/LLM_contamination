import re, sys
t = open(sys.argv[1], encoding='utf-8').read()
BS = chr(92)
def grab(cmd):
    return re.findall(re.escape(BS + cmd + '{') + r'([^}]+)\}', t)
refs, labs = set(grab('ref')), set(grab('label'))
cites = {c.strip() for g in grab('cite') for c in g.split(',')}
bib = set(grab('bibitem'))
print('missing labels', refs - labs)
print('missing bib', cites - bib)
print('unused bib', bib - cites)
print('braces', t.count('{'), t.count('}'))
