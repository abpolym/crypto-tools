# Caesar Rot Implementation

```
usage: rot.py [-h] [-s] [-t] [-l] [-u] rotvalue text

positional arguments:
  rotvalue         The rotation value
  text             The text to rotate

optional arguments:
  -h, --help       show this help message and exit
  -s, --seperate   Rotate Lower and Upper case letters seperately
  -t, --total      Rotate Lower and Upper case letters together
  -l, --loweronly  Rotate Lower case letters only
  -u, --upperonly  Rotate Upper case letters only
```

Sample usage:

```bash
0∣19ː39∣rot▶ for i in {1..52}; do python rot.py -t $i xLMWmWewIGVIXxIbX; done
yMNXnXfxJHWJYyJcY
zNOYoYgyKIXKZzKdZ
[...]
SghrHrzRdbqdsSdws
ThisIsASecretText
UijtJtBTfdsfuUfyu
[...]
sGHRhRZrDBQDSsDWS
tHISiSasECRETtEXT
uIJTjTbtFDSFUuFYU
[...]
xLMWmWewIGVIXxIbX
```
