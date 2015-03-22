import sys

def seperate(cip):
	msg = ''
	for c in cip:
		if not c.isalpha():
			msg+=c
			continue
		if c.islower(): msg+=labc[(labc.index(c)+rotval)%26]
		else: msg+=uabc[(uabc.index(c)+rotval)%26]
	print msg

def total(cip):
	msg = ''
	for c in cip:
		if not c.isalpha():
			msg+=c
			continue
		msg+=tabc[(tabc.index(c)+rotval)%52]
	print msg

def loweronly(cip):
	msg = ''
	for c in cip:
		if not c.isalpha() or not c.islower():
			msg+=c
			continue
		msg+=labc[(labc.index(c)+rotval)%26]
	print msg

def upperonly(cip):
	msg = ''
	for c in cip:
		if not c.isalpha() or not c.isupper():
			msg+=c
			continue
		msg+=uabc[(uabc.index(c)+rotval)%26]
	print msg
# first arg: rot value
# second arg: ciphertxt
if len(sys.argv) != 3: sys.exit(2)

tabc = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
labc = 'abcdefghijklmnopqrstuvwxyz'
uabc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
rotval = int(sys.argv[1])
cip = sys.argv[2]

seperate(cip)
#total(cip)
#loweronly(cip)
#upperonly(cip)
