# in the first colums give the file path
# in the secon give the row
#-------------------------------
# file path           row
#-------------------------------
# user files
proxy = {
".gitconfig"        : ("gitproxy = http://proxy.ing.unitn.it:3128",),
".ssh/config"       : ("ProxyCommand nc.openbsd -X connect %h %p -x proxy:3128",),

# system files
"/etc/wgetrc"       : ("http_proxy = http://proxy.ing.unitn.it:3128/",
                     "ftp_proxy = http://proxy.ing.unitn.it:3128/",
                     "use_proxy = on",),
"/etc/pacman.conf"  : ("XferCommand = /usr/bin/wget --passive-ftp -c -O %o %u",),
}

#-------------------------------
