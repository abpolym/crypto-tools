import json, os, requests, subprocess, sys
from PIL import Image
from BeautifulSoup import BeautifulSoup
import urllib

def generateImage(image, savefile):
	img = Image.open(image)
	w,h = img.size
	pixels = img.load()
	d = 198
	v = 40
	black = (0,0,0)
	white = (255,255,255)
	default = (d,d,d)

	for x in range(w):
		for y in range(h):
			r,g,b = img.getpixel((x,y))
			if d-v <= r <= d+v or d-v <= g <= d+v or d-v <= b <= d+v: pixels[x,y] = default
			if r > b: pixels[x,y] = default
	img.save(savefile)

def wordOCR(bitmapin):
	FNULL = open(os.devnull, 'w')
	subprocess.call(["tesseract",bitmapin,"/tmp/out","-l","eng","-psm","8"],stdout=FNULL, stderr=subprocess.STDOUT)
	word = open('/tmp/out.txt','r').readline().replace('\n','')
	return word

def postmd5(murl, viewstate, eventvalidation, mshash, captcha, rcookies, useragent):
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
	payload = 'ctl00%24ScriptMan1=ctl00%24content1%24updDecrypt%7Cctl00%24content1%24btnSubmit' + '&'
	payload += '__EVENTTARGET=' + '&'
	payload += '__EVENTARGUMENT=' + '&'
	payload += '__VIEWSTATE='+urllib.quote(viewstate, '') + '&'
	payload += '__EVENTVALIDATION=' + urllib.quote(eventvalidation, '') + '&'
	payload += 'ctl00%24content1%24txtInput='+urllib.quote(mshash, '') + '&'
	payload += 'ctl00%24content1%24txtCaptcha='+urllib.quote(captcha, '') + '&'
	payload += '__ASYNCPOST=true' + '&'
	payload += 'ctl00%24content1%24btnSubmit=Submit'
	return requests.post(murl, data=payload, headers=headers, cookies=rcookies)

def innerHTML(element):
	return element.decode_contents(formatter="html")

def getuseragent():
	useragent = ''
	with open('useragent','r') as f:
		useragent = f.readline().replace('\n','')
		f.close()
	return useragent

def getcreds(parsed_html):
	viewstate = ''
	eventvalidation = ''
	for i in  parsed_html.body.findAll('input'):
		if i['name'] == '__VIEWSTATE': viewstate = i['value']
		if i['name'] == '__EVENTVALIDATION': eventvalidation = i['value']
	return (viewstate, eventvalidation)

def savecaptchaimg(fsave):
	with open(fsave, 'wb') as infile:
		r = requests.get(imgurl, cookies = rcookies, stream=True)
		if not r.ok:
			print 'We could not get the captcha picture... Please panic!'
			sys.exit(3)
		for block in r.iter_content(1024):
			if not block: break
			infile.write(block)

if len(sys.argv)!=2:
	print 'Usage: ./this <md5>'
	sys.exit(2)

mshash = sys.argv[1]
print len(mshash)
baseurl = 'http://www.hashkiller.co.uk/'
if len(mshash) == 32: url = baseurl + 'md5-decrypter.aspx'
elif len(mshash) == 40: url = baseurl + 'sha1-decrypter.aspx'
else:
	print 'md5 or sha1..'
	sys.exit(1)
useragent = getuseragent()
captchafile = '/tmp/in.jpg'
ocrfile = '/tmp/out.bmp'

done=False
tries=0
while not done:
	# First request to get cookies and authentification data as well as the picture link
	r = requests.get(url)
	if r.status_code != 200:
		print 'I think we are banned... Use Tor :D'
		sys.exit(4)

	# Get cookies
	rcookies = r.cookies

	tries+=1
	# Get authentification credentials
	parsed_html = BeautifulSoup(r.text)
	(viewstate, eventvalidation) = getcreds(parsed_html)

	# Get picture link
	imgurl = baseurl + parsed_html.body.find(id='content1_imgCaptcha')['src']

	savecaptchaimg(captchafile)
	generateImage(captchafile, ocrfile)
	captcha = wordOCR(ocrfile)
	if not captcha.isupper() or len(captcha)!=6: continue

	# After determining a possible captcha, we will try to submit it and get the cracked hash
	r = postmd5(url, viewstate, eventvalidation, mshash, captcha, rcookies, useragent)
	if r.status_code != 200:
		print 'SOMETHING WENT WRONG'
		sys.exit(3)
	reshtml = BeautifulSoup(r.text)
	status = reshtml.find(id='content1_lblStatus')
	if str(status) == '<span id="content1_lblStatus">The CAPTCHA code you specifed is wrong. Please try again.</span>': continue
	print 'We did need ['+str(tries)+'] tries to crack this md5... damn :('
	print reshtml.find(id='content1_lblResults').text
	done=True
