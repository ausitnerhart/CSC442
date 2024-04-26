# Team Axolotl
# Caje Auchard, Holden Wells
# Chat Timing Covert Channel Program
# 4/26/2024

from socket import *
from time import time
from sys import stdout
DEBUG = False

ZERO = .025     # Delay time indicating 0
ONE = .1        # Delay time indicating 1
MOE = .04       # The margins in which a 1 or 0 is accepted 

# Dr. Timo's Server
ip = "138.47.99.64"
port = 31337

# Our Local Server
# ip = "localhost"
# port = 1337

s = socket(AF_INET, SOCK_STREAM)

s.connect((ip,port))

stdout.write("[Connection Established]\n")
stdout.flush()

# Recieves message character by character and captures delay time between character retrievals
# Delays are captured as 0 or 1 and added to the covert_bin string
# msg stores the overt channel and detects when recieving "EOF"
covert_bin = ""
data = s.recv(4096).decode()

msg = ""
while (True):
    msg += data
    stdout.write(data)
    stdout.flush()
    t0 = time()
    data = s.recv(4096).decode()
    t1 = time()
    delta = round(t1-t0,3)
    if DEBUG:
        stdout.write("{}\n".format(str(delta)))
        stdout.flush()
    if (delta >= ONE-.04):
        covert_bin += "1"
    else:
        covert_bin += "0"
    if 'EOF' in msg:
        break

# Break the string into chunks of 8-bits and store them into an array
asciiArray = []
for i in range(0, len(covert_bin), 8):
    asciiArray.append(covert_bin[i:i+8])

# Iterate through the array, evaluating each 8-bit ascii value, appending it to the resulting expression.
finalStr = ""
for j in asciiArray:
    intForm = int(j, 2)
    chrForm = chr(intForm)
    finalStr = (finalStr + chrForm)
    if 'EOF' in finalStr:
        break

# Write the resulting expression to the terminal
stdout.write("\n")
stdout.flush()
stdout.write(finalStr)
stdout.flush()
stdout.write("\n")
stdout.flush()
s.close()