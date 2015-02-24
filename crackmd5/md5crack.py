import requests, sys

if len(sys.argv)!=2: sys.exit(2)

md5hash = sys.argv[1]
apikey='83750c877f8523955b3e0204'
rtype = 'crack' # other one is hash.. but we can use md5sum for that, right?
url = 'http://api.md5crack.com/'+rtype+'/'+apikey+'/'+md5hash
r = requests.get(url)
print r.json()
