import sys

nums = [
	[' '],
	['Q','Z'],
	['A','B','C'],
	['D','E','F'],
	['G','H','I'],
	['J','K','L'],
	['M','N','O'],
	['P','R','S'],
	['T','U','V'],
	['W','X','Y']
]

abcdef='abcdef'

def decrypt(cip):
	global shift
	msg = ''
	for p in xrange(0,len(cip),2):
		#print cip[p]+ '' + cip[p+1]
		if cip[p] not in '0123456789': continue
		if cip[p+1].lower() not in 'abcdef': continue
		#print cip[p] + ' ' + str(abcdef.index(cip[p+1].lower()))
		msg+=nums[(int(cip[p])-shift)%10][abcdef.index(cip[p+1].lower())%3]
		shift+=1
	print msg

def encrypt(msg):
	global shift
	cip = ''
	for c in msg:
		for idx, d in enumerate(nums):
			if c not in d: continue
			for i, x in enumerate(d):
				if x != c: continue
				cip+=str((idx+shift)%10)+abcdef[i%3]
				if len(cip)%32==0: cip+='\n'
				shift+=1
	print cip

if len(sys.argv) != 3: sys.exit(3)
shift = int(sys.argv[1])
try: 
	#encrypt(sys.argv[1])
	decrypt(sys.argv[2])
except IndexError:
	#sys.stderr.write('WRONG NUMBER :)\n')
	sys.exit(4)
