import sys

# first arg: rot value
# second arg: ciphertxt
if len(sys.argv) != 3: sys.exit(2)

tabc = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
labc = 'abcdefghijklmnopqrstuvwxyz'
uabc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
rotval = int(sys.argv[1])
cip = sys.argv[2]

msg = ''
for c in cip:
	if not c.isalpha():
		msg+=c
		continue
	if c.islower(): msg+=labc[(labc.index(c)+rotval)%26]
	else: msg+=uabc[(uabc.index(c)+rotval)%26]
print msg
