"""
Austin Erhart
03.20.24
Vigenere Cipher
"""
import sys
import signal

#alphabet used in cypher
alph = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

"""
function takes two arguements
encode: plaintext that get encoded via the cypher
key: key used for encoding text

loops over plaintext message increasing the encoder index (letter positioning) every loop
if a whitespace character is found loop skips over encoding and adds a space to the final text
if char is a letter it encodes the letter based grabbing the index of both the plaintext and key and increments both

returns string message
"""
def encryptMessage(encode, key):

    """
    function takes two arguements
    encoderIndex: index of letter position in plaintext
    keyIndex: index of key positioning

    finds the index of the plaintext character in alph and adds it to the index of the key character from alph 
    (key character is determined by the modulus of the length of the key and the current index positioning)
    modulus by 26 to determine index of encoded letter

    returns index of encoded letter from alph
    """
    def encrypt(encoderIndex, keyIndex):
        return (alph.index(encode[encoderIndex].lower())+alph.index(key[keyIndex%len(key)]))%26
    
    encoderIndex = 0
    keyIndex = 0
    message = ""
    for _ in range(len(encode)):
        if(encode[encoderIndex].isspace()):
            encoderIndex += 1
            message += " "
        else:
            if(encode[encoderIndex].isupper()):
                message += alph[encrypt(encoderIndex, keyIndex)].upper() 
            else:
                 message += alph[encrypt(encoderIndex, keyIndex)]
            encoderIndex += 1
            keyIndex += 1
    return message

"""
function takes two arguements
encode: encoded text that gets decoded via the cypher
key: key used for decoding text

loops over encoded text message increasing the decoder index (letter positioning) every loop
if a whitespace character is found loop skips over decoding and adds a space to the final text
if char is a letter it decodes the letter based grabbing the index of both the encoded text and key and increments both

returns string message
"""
def decryptMessage(decode, key):

    """
    function takes two arguements
    decoderIndex: index of letter position in encoded text
    keyIndex: index of key positioning

    adds 26
    finds the index of the encoded text character in alph and subtracts it from the index of the key character from alph 
    (key character is determined by the modulus of the length of the key and the current index positioning)
    modulus by 26 to determine index of decoded letter

    returns index of decoded letter from alph
    """
    def decrypt(decoderIndex, keyIndex):
        return (26+alph.index(decode[decoderIndex].lower())-alph.index(key[keyIndex%len(key)]))%26

    decoderIndex = 0
    keyIndex = 0
    message = ""
    for _ in range(len(decode)):
        if(decode[decoderIndex].isspace()):
            decoderIndex += 1
            message += " "
        else:
            if(decode[decoderIndex].isupper()):
                message += alph[decrypt(decoderIndex, keyIndex)].upper() 
            else:
                 message += alph[decrypt(decoderIndex, keyIndex)]  
            decoderIndex += 1
            keyIndex += 1
    return message


def main():

    """
    Grabs CTRL + C shortcut to avoid any error messages appearing and exits program
    """
    def sig_interrupt_handler(signal, frame):
        print()
        sys.exit(-1)

    signal.signal(signal.SIGINT, sig_interrupt_handler)

    """
    Ensures user input is within the 3 specified parameters 'file' 'flag' 'key'

    Grabs the stdin from the user and continues until uses keyboard interrupts
    """
    if(len(sys.argv) < 4 and len(sys.argv) > 2):
        key = sys.argv[2].lower()
        if(sys.argv[1] == '-d'):
            for line in sys.stdin:
                decode = line.strip()
                print(decryptMessage(decode, key))

        elif(sys.argv[1] == '-e'):
            for line in sys.stdin:
                encode = line.strip()
                print(encryptMessage(encode, key))
        else:
            print("Error: Incorrect input. Use: python3 '-d' 'key' | python3 '-e' 'key'")
    else:
        print("Error: Incorrect number of arguments. Use: python3 '-d' 'key' | python3 '-e' 'key'")

    

if __name__ == '__main__':
    main()

