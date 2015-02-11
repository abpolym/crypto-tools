import sys
from os import listdir
from os.path import isfile, join

abc='abcdefghijklmnopqrstuvwxyz'

def encrypt(code, poem, msg):
	twords = []
	for line in open(poem,'r'):
		for w in line.split(): twords.append(w.lower())

	pwords = ''
	for c in code: pwords += twords[c].lower()
	plen = len(pwords)

	if plen > len(abc): sys.exit(3)
	pcode = [None] * plen
	count = 0
	while(count<plen):
		for al in abc:
			for pc, pl in enumerate(pwords):
				if al!=pl: continue
				pcode[pc]=count
				count+=1

	mwords = ''
	for line in open(msg, 'r'):
		for w in line.split(): mwords+=w.lower()
	mlen = len(mwords)

	cpairs = []
	curlen = plen
	while(curlen<mlen):
		cpairs.append(mwords[curlen-plen:curlen])
		curlen+=plen
	rword = mwords[curlen-plen:curlen]
	rlen = len(rword)
	if rlen < plen: rword += abc[:plen-rlen]
	cpairs.append(rword)

	cip = ''
	for i in code: cip+=abc[i]
	cip+=' '
	for i in pcode:
		for pair in cpairs:
			cip += pair[i]
		cip+=' '
	return cip

def decrypt():
	print 'Decrypt'

# first argument = poem
# second argument = ciphertxt or msg
if len(sys.argv) != 3: sys.exit(2)

code = [0, 5, 13, 16, 19]
print encrypt(code, sys.argv[1], sys.argv[2])
