import switchconf as conf
import re

#print conf.dir()
typ = dir(conf)

typ = typ[5:]
print typ

option = "proxy"
actiontion = "comment"

if option not in typ:
    raise "optionion not in switchconf"

print conf.proxy

for k, l in conf.proxy.iteritems():
    print k, l

def iscomment(row):
    regexp = re.compile(r"""\s*\#\s*.+""")
    return regexp.match(row)

def action(row, strlist, action):
    for s in strlist:
        if row.find(s):
            if iscomment(s):
                if action == 'uncomment':
                    row.replace('#','')
            else:
                if action == 'comment':
                    row = '#' + row
    return row

def modifyFile(file, strlist, action):
    for r in file:
        action(r, strlist, action)



riga = "   #   qwertyu"
if iscomment(riga):
    print 'true'
else:
    print 'false'
