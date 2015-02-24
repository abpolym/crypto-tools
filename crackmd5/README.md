# Hashkiller Commandline MD5 Cracker

This tool cracks the CAPTCHA used by <http://www.hashkiller.co.uk/md5-decrypter.aspx> and allows to crack md5 hashes using the hashkiller platform via the commandline.

## Usage:

```bash
$ python go.py "$(echo -n superman | md5)"
We did need [5] tries to crack this md5... damn :(
84d961568a65073a3bcf0eb216b2a576 MD5 :superman
```

## Tools needed

`tesseract` : `brew install tesseract` (OSX) or `sudo apt-get install tesseract-ocr` or just [compile from source](https://code.google.com/p/tesseract-ocr/), if you are superawesome.
