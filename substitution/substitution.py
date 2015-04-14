import argparse, collections, operator, re, string, sys

# Frequency of letters etc according to http://www.cryptograms.org/letter-frequencies.php
# Other stats (TODO) http://scottbryce.com/cryptograms/stats.htm

# Bireps according to http://www.counton.org/explorer/codebreaking/frequency-analysis.php
fbireps = [
	"ss",
	"ee",
	"tt",
	"ff",
	"ll",
	"mm",
	"oo"
]

fbireps = [
	'ss',
	'nn',
	'll',
	'ee',
	'mm',
	'tt',
	'rr',
	'dd',
	'ff',
	'aa'
]

def printFreq(sdict, fdict):
	for idx, (k, v) in enumerate(sdict):
		if v < barrier: break
		if idx < len(fdict): print "["+fdict[idx]+"] " + k + ": " + str(v)
		else: print "["+" "*len(fdict[0])+"] " + k + ": " + str(v)
	print

def sortC(col):
	return sorted(collections.Counter(col).iteritems(), key=operator.itemgetter(1), reverse=True)

def sortD(dic):
	return sorted(dic, key=operator.itemgetter(1), reverse=True)

def getGramDict(ngramdict, ngramletters, index):
	found=[]
	for idx, b in enumerate(ngramdict):
		if b[0][0]!=ngramletters[index][0]: continue
		found.append((idx,b))
	return found

def linefy(rfile):
	f = open(rfile,'r')
	lines = []
	for line in f:
		lines.append(re.sub(r'([^\s\w]|_)+','',line.rstrip('\n').lower()))
	f.close()
	return lines

def assign(matches, flet, llet):
	#print 'F : ' + flet + " L: " + llet + " matches: " + str(matches)
	if flet not in matches:
		matches[flet]=[(llet,0)]
	else:
		newmatchesdict = []
		found=False
		for (k, v) in matches[flet]:
			if k==llet:
				found=True
				v+=1
			newmatchesdict.append((k,v))
		if not found: newmatchesdict.append((llet,0))
		matches[flet]=newmatchesdict
	return matches

def find(s, ch):
	return [i for i, ltr in enumerate(s) if ltr == ch]

def findMatches(matches, fngrams, lngrams, nflet, nllet):
	fdict=[]
	for b in fngrams:
		if nflet in b: fdict.append(b)
	ldict=[]
	for b in lngrams:
		if nllet in b[0]: ldict.append(b)

	for w in fdict:
		wc = find(w, nflet)
		for idx, l in enumerate(ldict):
			if find(l[0], nllet)!=wc: continue
			#print "Found word: " + w + ' as ' + l[0]
			for i in set([i for i in range(0,len(w))])-set(wc):
				assign(matches, w[i], l[0][i])#, w[i])
			del ldict[idx]
			if len(wc)==1: break

def findAllMatches(matches, mflet, mllet):
	findMatches(matches, fbireps, bireps, mflet, mllet)
	#print 'Finding matches for ['+mflet+'] to ['+mllet+']'
	# Find matches for 2-grams
	findMatches(matches, fbigrams, bigrams, mflet, mllet)
	# Find matches for 3-grams
	findMatches(matches, ftrigrams, trigrams, mflet, mllet)
	# Find matches for 4-grams
	findMatches(matches, fquadgrams, quadgrams, mflet, mllet)

def nextLetter(matches, mflet, mllet, matched, abcdict):
	highest = 0
	for k,v in matches.iteritems():
		if k in matched: continue
		for (xk, xv) in v:
			if xv<highest: continue
			highest=xv
			mflet=k
			mllet=xk
	matched.append(mflet)
	abcdict.append((mflet,mllet))
	return (mflet, mllet)

def nextULetter(matches, mflet, mllet, matched, vmatched, abcdict, fdict, ldict):
	oldmflet=mflet
	highest = 0
	for k,v in matches.iteritems():
		if k in matched: continue
		for (xk, xv) in v:
			if xv<highest: continue
			if xk in vmatched: continue
			highest=xv
			mflet=k
			mllet=xk
	tmp=[]
	for (k,v) in matches[mflet]:
		if v!=highest: continue
		print '['+mflet+'] could also be ' + str((k,v))
		if k in matched or k in vmatched: continue
		tmp.append((k,distance(fdict, ldict, mflet, k)))
	lowest = 99
	for (k, v) in tmp:
		if lowest<=v: continue
		lowest=v
		mllet=k
	matched.append(mflet)
	vmatched.append(mllet)
	abcdict.append((mflet,mllet))
	return (mflet, mllet)

def printMatches(matches):
	for k, v in matches.iteritems(): print k + " " + str(v)

def distance(fdict, ldict, nflet, nllet):
	fidx = fdict.index(nflet)
	for idx, (k,v) in enumerate(ldict):
		if k!=nllet: continue
		lidx=idx
		break
	return abs(abs(fidx)-abs(lidx))

def loadgram(gfile,length):
	ngramdata = []
	with open(gfile,'r') as f:
		for g in f:
			word = g.split(' ')[0].lower()
			if len(word)!=length: continue
			ngramdata.append(word)
	return ngramdata

def loadletters(lfile):
	abc = ''
	with open(lfile, 'r') as f:
		for g in f:
			letter = g.split(' ')[0].lower()
			if len(letter)!=1: continue
			abc+=letter
	return abc

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('-bf', '--bigram-file', help='Specify a bigram file to be used')
parser.add_argument('-tf', '--trigram-file', help='Specify a trigram file to be used')
parser.add_argument('-qf', '--quadgram-file', help='Specify a quadgram file to be used')
parser.add_argument('-lf', '--letters-file', help='Specify a letters file to be used')
parser.add_argument('-l', '--language', help='Specify which language to be analysed. Default is "en"')
parser.add_argument('fcip', type=str, help='The ciphertext file')
args = parser.parse_args()

# Determine default and given arguments
resources = './res'
if not args.language: args.language='en'
if not args.bigram_file: args.bigram_file = resources+'/'+args.language+'/'+'bigrams.txt'
if not args.trigram_file: args.trigram_file = resources+'/'+args.language+'/'+'trigrams.txt'
if not args.quadgram_file: args.quadgram_file = resources+'/'+args.language+'/'+'quadgrams.txt'
if not args.letters_file: args.letters_file = resources+'/'+args.language+'/'+'monograms.txt'

# Load ngrams and ciphertext from resources
fbigrams = loadgram(args.bigram_file, 2)
ftrigrams = loadgram(args.trigram_file, 3)
fquadgrams = loadgram(args.quadgram_file, 4)
fletters = loadletters(args.letters_file)
lines = linefy(args.fcip)

bireps = []
bigrams = []
trigrams = []
quadgrams = []
d = collections.defaultdict(int)
for line in lines:
	for word in line.split():
		[bireps.append(match[0]) for match in re.findall(r'((\w)\2{1,})', word)]
		if len(word)>=2:
			for i in range(0,len(word)-1):
				bigrams.append(word[i:i+2])
		if len(word)>=3:
			for i in range(0,len(word)-2):
				trigrams.append(word[i:i+3])
		if len(word)>=4:
			for i in range(0,len(word)-3):
				quadgrams.append(word[i:i+4])
		for char in word:
			if char==' ': continue
			d[char] += 1

letters = sortD(d.items())
bigrams = sortC(bigrams)
trigrams = sortC(trigrams)
quadgrams = sortC(quadgrams)
bireps = sortC(bireps)

#printFreq(letters, fletters)
#printFreq(bigrams, fbigrams)
#printFreq(trigrams, ftrigrams)
#printFreq(quadgams, fquadgams)
#printFreq(bireps, fbireps)


matches = {}
# Begin at the first most frequent letter
mflet=fletters[0]
mllet=letters[0][0]
matched = [mflet]
abcdict = [(mflet, mllet)]
# Assign it to the most frequent letter in the english alphabet
assign(matches, mllet, mflet)
findAllMatches(matches, mflet, mllet)
#printMatches(matches)

for i in range(0, len(matches)):
	# Find the letter in the matches with the highest count of matches
	(mflet, mllet) = nextLetter(matches, mflet, mllet, matched, abcdict)
	findAllMatches(matches, mflet, mllet)
	#printMatches(matches)

abcdict = []
matched = []
vmatched = []
for i in range(0,len(matches)):
	oldmflet=mflet
	oldmllet=mllet
	(mflet, mllet) = nextULetter(matches, mflet, mllet, matched, vmatched, abcdict, fletters, letters)
	if oldmflet==mflet and oldmllet==mllet: break
del abcdict[-1]
#for k,v in abcdict: print 'XXX ' + k + ' ' + str(v)
#printFreq(letters, fletters)
#printMatches(matches)

for i in fletters:
	if i in matched: continue
	found=False
	for idx, (k, v) in enumerate(letters):
		if idx >= len(fletters): break
		if k in vmatched: continue
		matched.append(i)
		vmatched.append(k)
		abcdict.append((i,k))
		found=True
		break
	if found: continue
	for x in 'abcdefghijklmnopqrstuvwxyz':
		if x in vmatched: continue
		k=x
		break
	matched.append(i)
	vmatched.append(k)
	abcdict.append((i,k))
origabc=''
tranabc=''
for (k,v) in abcdict:
	origabc+=k
	tranabc+=v
	#print 'XXX ' + k + ' ' + str(v)
print origabc
print tranabc
trans = string.maketrans(tranabc, origabc)
for l in lines:
	print l.translate(trans)
