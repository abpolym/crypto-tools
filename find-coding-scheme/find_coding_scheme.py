import sys
import re

# first argument: unknown coding text
if len(sys.argv) != 2: sys.exit(2)
estr=sys.argv[1]

b64rex = re.compile('^[A-Za-z0-9+/]+[=]{0,2}$')
if(b64rex.match(estr)): print 'base64'

uurex = re.compile('^(begin.*\n)?[\x20-\x60\n]+(end[\n]?)?$')
if(uurex.match(estr)): print 'uuencode'
