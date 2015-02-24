import json, os, requests, subprocess, sys
from PIL import Image
from BeautifulSoup import BeautifulSoup
import urllib

if len(sys.argv)!=2: sys.exit(2)

def generateImage(image):
	img = Image.open(image)
	w,h = img.size
	pixels = img.load()
	d = 198
	v = 40
	black = (0,0,0)
	white = (255,255,255)
	default = (d,d,d)

	for x in range(w):
		#print '------[ ' + str(x) + ' ]-------'
		for y in range(h):
			r,g,b = img.getpixel((x,y))
			#if r == 198 and g == 198 and b == 198: pixels[x,y] = (0,0,0)
			#if d-v <= r <= d+v and d-v <= g <= d+v and d-v <= b <= d+v: pixels[x,y] = default
			if d-v <= r <= d+v or d-v <= g <= d+v or d-v <= b <= d+v: pixels[x,y] = default
			if r > b: pixels[x,y] = default
			#print pixels[x,y]

	#img.show()
	img.save('/tmp/out.bmp')

def wordOCR(bitmapin):
	FNULL = open(os.devnull, 'w')
	subprocess.call(["tesseract",bitmapin,"/tmp/out","-l","eng","-psm","8"],stdout=FNULL, stderr=subprocess.STDOUT)
	word = open('/tmp/out.txt','r').readline().replace('\n','')
	if not word.isupper() or len(word)!=6:
		print 'WRONG RESULT: ' + word
		sys.exit(3)
	print sys.argv[1]
	return word

def postmd5(murl, viewstate, eventvalidation, md5hash, captcha, rcookies, useragent):
	headers = {
		u'Cookie':'__cfduid='+rcookies['__cfduid']+'; ASP.NET_SessionId='+rcookies['ASP.NET_SessionId']+'; _gat=1;',
		u'Origin':'http://www.hashkiller.co.uk',
		u'Accept-Encoding':'gzip, deflate',
		u'Accept-Language':'en-US,en;q=0.8',
		u'User-Agent':str(useragent),
		u'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
		u'Accept':'*/*',
		u'Cache-Control':'no-cache',
		u'X-Requested-With':'XMLHttpRequest',
		u'Connection':'keep-alive',
		u'X-MicrosoftAjax':'Delta=true',
		u'Referer':'http://www.hashkiller.co.uk/md5-decrypter.aspx'
	}
	#payload = {
	#	'ctl00%24ScriptMan1':'ctl00%24content1%24updDecrypt%7Cctl00%24content1%24btnSubmit',
	#	'__EVENTTARGET':'',
	#	'__EVENTARGUMENT':'',
	#	'__VIEWSTATE':viewstate,
	#	'__EVENTVALIDATION':eventvalidation,
	#	'ctl00%24content1%24txtInput':md5hash,
	#	'ctl00%24content1%24txtCaptcha':captcha,
	#	'__ASYNCPOST':'true',
	#	'ctl00%24content1%24btnSubmit':'Submit'
	#}
	payload = 'ctl00%24ScriptMan1=ctl00%24content1%24updDecrypt%7Cctl00%24content1%24btnSubmit' + '&'
	payload += '__EVENTTARGET=' + '&'
	payload += '__EVENTARGUMENT=' + '&'
	payload += '__VIEWSTATE='+urllib.quote(viewstate, '') + '&'
	payload += '__EVENTVALIDATION=' + urllib.quote(eventvalidation, '') + '&'
	payload += 'ctl00%24content1%24txtInput='+urllib.quote(md5hash, '') + '&'
	payload += 'ctl00%24content1%24txtCaptcha='+urllib.quote(captcha, '') + '&'
	payload += '__ASYNCPOST=true' + '&'
	payload += 'ctl00%24content1%24btnSubmit=Submit'
	print 'POST TO: ' + murl
	print payload
	#print json.dumps(payload)
	r = requests.post(murl, data=payload, headers=headers, cookies=rcookies)
	return r

def innerHTML(element):
	return element.decode_contents(formatter="html")

#print urllib.quote('ITWE/+=', '')
#sys.exit(3)
#generateImage(sys.argv[1])
baseurl = 'http://www.hashkiller.co.uk/'
url = baseurl+'md5-decrypter.aspx'
r = requests.get(url)
rcookies = r.cookies
print str(r.cookies)
aspnetcookie = r.cookies['ASP.NET_SessionId']
cfduidcookie = r.cookies['__cfduid']
useragent = ''
with open('useragent','r') as f:
	useragent = f.readline().replace('\n','')
print useragent
print aspnetcookie
print cfduidcookie
#print r.text
parsed_html = BeautifulSoup(r.text)
viewstate = ''
eventvalidation = ''
for i in  parsed_html.body.findAll('input'):
	if i['name'] == '__VIEWSTATE': viewstate = i['value']
	if i['name'] == '__EVENTVALIDATION': eventvalidation = i['value']
print viewstate
print eventvalidation
imgurl = baseurl + parsed_html.body.find(id='content1_imgCaptcha')['src']
print imgurl
with open('/tmp/in.jpg', 'wb') as infile:
	r = requests.get(imgurl, cookies = rcookies, stream=True)
	if not r.ok:
		print 'SOMETHING BAD HAPPENED'
		sys.exit(3)
	for block in r.iter_content(1024):
		if not block: break
		infile.write(block)

generateImage('/tmp/in.jpg')
captcha = wordOCR('/tmp/out.bmp')
print 'CAPTCHA: ' + captcha
md5hash = 'b1946ac92492d2347c6235b4d2611184'
#print postmd5('http://localhost', viewstate, eventvalidation, md5hash, captcha).text
r = postmd5(url, viewstate, eventvalidation, md5hash, captcha, rcookies, useragent)
print r.status_code
reshtml = BeautifulSoup(r.text)
print reshtml
print reshtml.find(id='content1_lblStatus')
for i in reshtml.find(id='content1_lblResults'):
	print i
