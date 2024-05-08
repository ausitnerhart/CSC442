import sys

DEBUG = False
keyfilename = "key"
ENCODING = 'utf-8'

def debug(message):
    if DEBUG:
        print(message)

# read the key from the key file
with open(keyfilename, 'rb') as f:
    lines = f.readlines()
    while len(lines) > 1:
        lines[0] = lines[0] + lines[1]
        del lines[1]

lines = lines[0]
key = lines

debug("Key: ")
debug(lines.decode(ENCODING, errors='ignore'))

# read the ciphertext from stdin
plaintext = sys.stdin.buffer.readlines()
while len(plaintext) > 1:
    plaintext[0] = plaintext[0] + plaintext[1]
    del plaintext[1]

plaintext = plaintext[0]

debug("Plaintext: ")
debug(plaintext.decode(ENCODING, errors='ignore'))

# make the key at least as long as the plaintext
while len(key) < len(plaintext):
    key = key + lines

# xor each byte of the plaintext with the key 
debug(f"plain len = {len(plaintext)}")
debug(f"key len = {len(key)}")

diff = 0
# diff = len(key) - len(plaintext) # uncomment this line to right align the key and plaintext for xor


result = bytes([plaintext[i] ^ key[diff+i] for i in range(len(plaintext))])

debug("Result: ")
sys.stdout.buffer.write(result)

sys.stdout.flush()
