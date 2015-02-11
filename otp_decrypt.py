import sys
from os import listdir
from os.path import isfile, join
def xor_strings(xs, ys):
	return "".join(chr(ord(x) ^ ord(y)) for x, y in zip(xs, ys))

def most_common(lst):
	return max(set(lst), key=lst.count)

# first argument = to decrypt message
# second argument = folder containing all other encrypted messages
if len(sys.argv) != 3: sys.exit(2)
#ciptxt = sys.argv[1].decode('hex')
with open(sys.argv[1],"r") as f: ciptxt = f.read().replace('\n', '').decode('hex')
hlptxts = [ sys.argv[2]+"/"+f for f in listdir(sys.argv[2]) if isfile(join(sys.argv[2],f)) ]
xorarr = [0] * len(hlptxts)
#print hlptxts
for i, f in enumerate(hlptxts):
	with open (f, "r") as f: hlptxts[i]=f.read().replace('\n','').decode('hex')

for i, h in enumerate(hlptxts):
	xorarr[i] = xor_strings(ciptxt, h)

refs=len(xorarr)
string=''
specchars=['@','\\',')','(','.',',', '$']
for z in range(0,len(ciptxt)):
	if len(xorarr) == 0: break
	refs=len(xorarr)
	tmp = []
	syms = 0
	lowers = 0
	zeros=0
	for i, x in enumerate(xorarr):
		if (z+1)==len(x): xorarr.remove(x)
		if x[z] in specchars:
			syms+=1
			continue
		if x[z]=='\x00':
			zeros+=1
			continue
		if not x[z].isalpha(): continue
		if x[z].islower():
			lowers+=1
			tmp.append(x[z].upper())
			continue
		tmp.append(x[z].lower())
#	print str(tmp) + " SYM: " + str(syms)
	if len(tmp) == 0:
		if z!=0 and string[z-1]==',':
			#print string[:len(string)-1].encode('hex') + "\n"
			print string[:z-1]
			string = string[:len(string)-1]+"X"
		string+='.'
		continue
	mc = most_common(tmp)
	if (len(tmp)-tmp.count(mc)) >= (refs-zeros)/2:# and len(tmp)-tmp.count(mc)>=tmp.count(mc):
		if z!=0 and string[z-1]==' ': string = string[:z-1]+","
		string+=" "
		continue
	if lowers==0 and (syms>=tmp.count(mc) or tmp.count(mc)<len(tmp)/2):
		string+="."
		continue
	#print len(tmp)
	if z!=0 and string[z-1]==',': string = string[:z-1]+"."
	string+=most_common(tmp)
print string.encode('hex')
#for i in xorarr[0]: print i.encode('hex')
#for i in xorarr:
	#print str(len(i)) + " vs " + str(len(ciptxt))
	#print min(len(i),len(ciptxt))
	#print xorarr
