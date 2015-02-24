# Hashkiller Commandline MD5 Cracker

Crack md5 or sha1 hashsums using the commandline.
This tool cracks the CAPTCHA used by <http://www.hashkiller.co.uk/md5-decrypter.aspx>.

## Usage:

```bash
$ python go.py "$(echo -n superman | md5)"
We did need [5] tries to crack this md5... damn :(
84d961568a65073a3bcf0eb216b2a576 MD5 :superman
```

## Configuration

```bash
$ echo "Yourcustomvaliduseragenthere" > useragent
```

## Tools needed

`tesseract` :

* `brew install tesseract` (OSX) or
* `sudo apt-get install tesseract-ocr` or
* just [compile from source](https://code.google.com/p/tesseract-ocr/), if you are superawesome.
