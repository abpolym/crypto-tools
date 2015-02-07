# crypto-tools
Some crypto tools I've written

Example:
```
python otp_decrypt.py orig/1 ciphers/ | xxd -r -p > wut
```

This example is for volga ctf cry200. Rotate the caesar cipher with:

<http://www.xarg.org/tools/caesar-cipher/>

Also this explains everything about OTP: <http://crypto.stackexchange.com/a/6095>.
Another good explanation: <http://travisdazell.blogspot.de/2012/11/many-time-pad-attack-crib-drag.html>

We use probability here, though.

Keystream (correctkey) is from [here](https://ctftime.org/writeup/1024).

This repo is a total mess, I will clean/organize it and improve the code, as soon as I got more time on my hands.
