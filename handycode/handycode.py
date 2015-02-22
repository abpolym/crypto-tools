import sys

nums = [
	['+'],
	[''],
	['a','b','c'],
	['d','e','f'],
	['g','h','i'],
	['j','k','l'],
	['m','n','o'],
	['p','q','r', 's'],
	['t','u','v'],
	['w','x','y', 'z']
]

def decrypt(cip):
	msg = ''
	for i in cip.split():
		msg += nums[int(i[0])][len(i)-1]
	print msg

def encrypt(msg):
	cip = ''
	for c in msg:
		print c
		for idx, d in enumerate(nums):
			if c not in d: continue
			for i, x in enumerate(d):
				if x != c: continue
				cip+=str(idx)*(i+1)+" "
	print cip

if len(sys.argv) != 2: sys.exit(2)
#cip = '7777 33 222 777 33 8'
#decrypt(cip)
#msg = 'secret'
#encrypt(msg)

decrypt(sys.argv[1])
