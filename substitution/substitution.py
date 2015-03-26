import collections, operator, re, sys

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
	print 'IND: ' + str(index)
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
	print str(flet) + " is now " + str(llet)
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

if len(sys.argv)!=3: sys.exit(2)

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

printFreq(letters, fletters)
printFreq(bigrams, fbigrams)
#printFreq(trigrams, ftrigrams)
#printFreq(quadrigams, fquadrigams)
#printFreq(bireps, fbireps)


matches = {}


for x in range(0,len(letters)):
	#print matches
	index = x
	assign(matches, letters[index][0], fletters[index])

	fdict = getGramDict(fbigrams, fletters, index)
	if len(fdict)==0:
		#print 'Something really terrible happened'
		continue
		sys.exit(4)
	ldict = getGramDict(bigrams, letters, index)
	if len(ldict)==0:
		print 'We have to figure out what to do now...'
		sys.exit(5)
	assign(matches, ldict[0][1][0][1], fdict[0][1][1])

print matches
