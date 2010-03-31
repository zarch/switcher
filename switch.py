# -*- coding: utf-8 -*-
import re
from optparse import OptionParser
import ConfigParser


# ===================
# Set command parser
# ===================

parser = OptionParser()

parser.add_option("-a", "--action", dest="action", default = 'test',
                  help="""choose which action you take from configuration file""",
                  metavar="ACTION")

parser.add_option("-c", "--comment", action="store_true", dest="comment", default=True,
                  help="choose if you want comment the line",)

parser.add_option("-u", "--uncomment", action="store_false", dest="comment",
                  help="choose if you want uncomment the line",)

parser.add_option("-f", "--file", default = 'switch.cfg',
                  help="specify the path of your config file",
                  metavar="FILE")

(options, args) = parser.parse_args()

# OptionParser usage:
# $ python swith.py -c -f switch.cfg -a test
# >>> print options
# {'action': 'test', 'comment': True, 'file': 'switch.cfg.py'}
# >>> print options.action
# test


# ========================
# Read configuration file
# ========================

config = ConfigParser.RawConfigParser()
config.read(options.file)

# ConfigParser usage:
# >>> print config.sections()
# ['test', 'proxy']
# >>> print config.items('proxy')
#[('.gitconfig', 'gitproxy = http://proxy.ing.unitn.it:3128'),
# ('.ssh/config', 'ProxyCommand nc.openbsd -X connect %h %p -x proxy:3128'),
# ('/etc/pacman.conf', 'XferCommand = /usr/bin/wget --passive-ftp -c -O %o %u'),
# ('/etc/wgetrc', 'http_proxy = http://proxy.ing.unitn.it:3128/\nftp_proxy = http://proxy.ing.unitn.it:3128/\nuse_proxy = on')]

# Check if action is define in config file
#class ActionNotDefine(Exception): pass

print options.action
print config.sections()
if options.action not in config.sections():
    raise ValueError("Action is not definitone in the configuration file...")

conf = config.items(options.action)
def makedict(conf):
    """Returnurn a dictionary from a file like:

    conf = [('.gitconfig', 'gitproxy = http://proxy.ing.unitn.it:3128'),
            ('.ssh/config', 'ProxyCommand nc.openbsd -X connect %h %p -x proxy:3128'),
            ('/etc/pacman.conf', 'XferCommand = /usr/bin/wget --passive-ftp -c -O %o %u'),
            ('/etc/wgetrc', 'http_proxy = http://proxy.ing.unitn.it:3128/\nftp_proxy = http://proxy.ing.unitn.it:3128/\nuse_proxy = on')]

    return:
    {'.gitconfig'   : ['gitproxy = http://proxy.ing.unitn.it:3128'],
     '.ssh/config', : ['ProxyCommand nc.openbsd -X connect %h %p -x proxy:3128]',
     '/etc/pacman.conf' : ['XferCommand = /usr/bin/wget --passive-ftp -c -O %o %u'],
     '/etc/wgetrc'  : ['http_proxy = http://proxy.ing.unitn.it:3128/',
                       'ftp_proxy = http://proxy.ing.unitn.it:3128/',
                       'use_proxy = on']

    """
    diz = {}
    for f in conf:
        diz[f[0]] = f[1].split("\n")
    return diz

def printdict(diz):
    for k, v in diz.iteritems():
        print k,  ":", v, "\n"

conf = makedict(conf)
print printdict(conf)


def iscomment(row):
    """Return if given row it's comment or not"""
    regexp = re.compile(r"""\s*\#\s*.+""")
    return regexp.match(row)

def modify(row, strlist):
    #print "action:" , row, strlist, action
    for s in strlist:
        if row.find(s) != -1:
            #print "trovato!:", s,  row
            if iscomment(row):
                #print "e' commentata", row
                #if action == 'uncomment':
                if not options.comment:
                    #print "l'azione e' di deccommentare"
                    row = row.replace('#','')
            else:
                #print "non e' commentata",  row
                #if action == 'comment':
                if options.comment:
                    #print "l'azione e' commentare"
                    row = '#' + row
    #print "action: row =" , row, strlist, action
    return row

def writeFile(file, strlist):
    fin = open( file, "r" )
    lines=[]
    for r in fin.readlines():
        #print "modif.", r
        lines.append(modify(r, strlist))
    fin.close()
    fout = open( file, "w" )
    fout.writelines(lines)
    fout.close()


for k, l in conf.iteritems():
    writeFile(k, l)


#riga = "http_proxy = http://proxy.ing.unitn.it:3128/"
#if iscomment(riga):
#    print 'true'
#else:
#    print 'false'

