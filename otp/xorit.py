import sys
def xor_strings(xs, ys):
	return "".join(chr(ord(x) ^ ord(y)) for x, y in zip(xs, ys))

if len(sys.argv) != 3: sys.exit(2)
binary_a = sys.argv[1].decode('hex')
binary_b = sys.argv[2].decode('hex')
print xor_strings(binary_a, binary_b).encode("hex")
