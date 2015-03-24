import argparse, sys

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
#if len(sys.argv) != 3: sys.exit(2)
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--seperate", help="Rotate Lower and Upper case letters seperately", action="store_true")
parser.add_argument("-t", "--total", help="Rotate Lower and Upper case letters together", action="store_true")
parser.add_argument("-l", "--loweronly", help="Rotate Lower case letters only", action="store_true")
parser.add_argument("-u", "--upperonly", help="Rotate Upper case letters only", action="store_true")
parser.add_argument("rotvalue", type=int, help="The rotation value")
parser.add_argument("text", type=str, help="The text to rotate")
args = parser.parse_args()

tabc = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
labc = 'abcdefghijklmnopqrstuvwxyz'
uabc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
rotval = args.rotvalue
cip = args.text

if args.seperate: seperate(cip)
elif args.total: total(cip)
elif args.loweronly: loweronly(cip)
elif args.upperonly: upperonly(cip)
else: parser.print_help()
