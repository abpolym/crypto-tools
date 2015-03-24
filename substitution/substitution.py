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

d = collections.defaultdict(int)

f = open(sys.argv[1],'r')

bireps = []
bigrams = []
triples = []
quadrigams = []
barrier = int(sys.argv[2])
for line in f:
	line = line.rstrip('\n')
	for word in line.split():
		for x in [match[0] for match in re.findall(r'((\w)\2{1,})', word)]: bireps.append(x)
		if len(word)>=2:
			for i in range(0,len(word)-1):
				bigrams.append(word[i:i+2])
		if len(word)>=3:
			for i in range(0,len(word)-2):
				triples.append(word[i:i+3])
		if len(word)>=4:
			for i in range(0,len(word)-3):
				quadrigams.append(word[i:i+4])
		for char in word:
			if char==' ': continue
			d[char] += 1

letters = sorted(d.items(), key=operator.itemgetter(1), reverse=True)
printFreq(letters, fletters)
print

bigrams = sorted(collections.Counter(bigrams).iteritems(), key=operator.itemgetter(1), reverse=True)
printFreq(bigrams, fbigrams)
print

trigrams = sorted(collections.Counter(triples).iteritems(), key=operator.itemgetter(1), reverse=True)
printFreq(trigrams, ftrigrams)
print

bireps = sorted(collections.Counter(bireps).iteritems(), key=operator.itemgetter(1), reverse=True)
printFreq(bireps, fbireps)
print

quadrigams = sorted(collections.Counter(quadrigams).iteritems(), key=operator.itemgetter(1), reverse=True)
printFreq(quadrigams, fquadrigams)
