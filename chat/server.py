from socket import *
import time
from binascii import hexlify


ZERO = .025
ONE = .1
JUNK = .069

s = socket(AF_INET, SOCK_STREAM)

port = 1337
s.bind(("",port))
s.listen(0)
print("Server is listening...")

c, addr = s.accept()

covert = "SecretEOF"
covert_bin =""
for i in covert:
    covert_bin += bin(int(hexlify(i.encode()),16))[2:].zfill(8)

z = 0
p = 0
bi = []
while z < len(covert_bin):
    if z % 3 == 0:
        bi.append("2")
    else:
        bi.append(covert_bin[p])
        p+=1
    z+=1
    
msg = "Sing, O goddess, the anger of Achilles son of Peleus, that brought countless ills upon the Achaeans. Many a brave soul did it send hurrying down to Hades, and many a hero did it yield a prey to dogs and vultures, for so were the counsels of Jove fulfilled from the day on which the son of Atreus, king of men, and great Achilles, first fell out with other.EOF"

n = 0
for i in msg:
    c.send(i.encode())
    if (bi[n] == "2"):
        time.sleep(JUNK)
    elif (bi[n] == "0"):
        time.sleep(ZERO)
    else:
        time.sleep(ONE)
    n = (n+1) % len(bi)

c.send("EOF").encode()
print("Message sent...")
c.close()