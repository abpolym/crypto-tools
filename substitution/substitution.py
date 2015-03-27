import collections, operator, re, string, sys

# Frequency of letters etc according to http://www.cryptograms.org/letter-frequencies.php
# Other stats (TODO) http://scottbryce.com/cryptograms/stats.htm

# Letters
fletters = "etaoinshrdlucmfwgypbvkxjqz"

fbigrams = [
	"th",
	"he",
	"in",
	"er",
	"an",
	"re",
	"nd",
	"on",
	"en",
	"at",
	"ou",
	"ed",
	"ha",
	"to",
	"or",
	"it",
	"is",
	"hi",
	"es",
	"ng"
]

ftrigrams = [
	"the",
	"and",
	"ing",
	"her",
	"hat",
	"his",
	"tha",
	"ere",
	"for",
	"ent",
	"ion",
	"ter",
	"was",
	"you",
	"ith",
	"wer",
	"all",
	"wit",
	"thi",
	"tio"
]

fquadrigams = [
	"that",
	"ther",
	"with",
	"tion",
	"here",
	"ould",
	"ight",
	"have",
	"hich",
	"whic",
	"this",
	"thin",
	"they",
	"atio",
	"ever",
	"from",
	"ough",
	"were",
	"hing",
	"ment"
]

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
	for line in f: lines.append(line.rstrip('\n'))
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
	#findMatches(matches, fbireps, bireps, mflet, mllet)
	#print 'Finding matches for ['+mflet+'] to ['+mllet+']'
	# Find matches for 2-grams
	findMatches(matches, fbigrams, bigrams, mflet, mllet)
	# Find matches for 3-grams
	findMatches(matches, ftrigrams, trigrams, mflet, mllet)
	# Find matches for 4-grams
	findMatches(matches, fquadrigams, quadrigams, mflet, mllet)
if len(sys.argv)!=3: sys.exit(2)

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

lines = linefy(sys.argv[1])
barrier = int(sys.argv[2])

bireps = []
bigrams = []
trigrams = []
quadrigams = []
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
				quadrigams.append(word[i:i+4])
		for char in word:
			if char==' ': continue
			d[char] += 1

letters = sortD(d.items())
bigrams = sortC(bigrams)
trigrams = sortC(trigrams)
quadrigams = sortC(quadrigams)
bireps = sortC(bireps)

#printFreq(letters, fletters)
#printFreq(bigrams, fbigrams)
#printFreq(trigrams, ftrigrams)
#printFreq(quadrigams, fquadrigams)
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
