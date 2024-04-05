
from ftplib import FTP

# number of bits to use from each permission
METHOD = 10

# FTP server details
IP = "138.47.165.156"
PORT = 21
USER = "anonymous"
PASSWORD = ""
FOLDER = "/10"
USE_PASSIVE = True # set to False if the connection times out

# connect and login to the FTP server
ftp = FTP()
ftp.connect(IP, PORT)
ftp.login(USER, PASSWORD)
ftp.set_pasv(USE_PASSIVE)

# navigate to the specified directory and list files
ftp.cwd(FOLDER)
files = []
ftp.dir(files.append)

# exit the FTP server
ftp.quit()


def concat_perms(files:str)-> list[str]:
    """Takes in a file listing and returns a list of
    file permissions from each line"""
    result = [] 
    # iterate through the lines of the listing 
    for file in  files:
        perms = file.split(" ")[0] # get the first part of that line
        perms = perms.strip()
        result.append(perms) 
    return result

def perms_to_binary(permissions:list[str], bits:int)->str:
    """Takes in a list of permissions and the number of bits
    to use from each one. Will return the binary representation
    of the permissions as a string, only using the specified
    number of bits from the permission"""

    # error checking
    if bits > 10:
        print("Cannot take more than 10 bits from permissions")
        exit()
    elif bits < 0:
        print("Cannot take a negative number of bits")
        exit()

    result = ""
    # iterate through each permission in the list
    for perm in permissions:
        # get only the characters we are interested in
        current = perm[10-bits:] # get only the last (bits) bits
        for character in current:
            if character == '-':
                result += "0"
            else:
                result += "1"

    return result


def seven_bit_decode(binary:str)->str:
    """Decode a binary string using seven bit ascii.
    Borrowed from Austin Adams (Binary Decoder)
    """
    # Break the string into chunks of 7-bits and store them into an array
    asciiArray = []
    for i in range(0, len(binary), 7):
        asciiArray.append(binary[i:i+7])
    # Iterate through the array, evaluating each 7-bit ascii value,
    # appending it to the resulting expression.
    finalStr = ""
    for j in asciiArray:
        intForm = int(j, 2)
        chrForm = chr(intForm)
        finalStr = (finalStr + chrForm)
    return finalStr


# main code
if __name__ == '__main__':
    perms = concat_perms(files)
    the_binary = perms_to_binary(perms, METHOD)
    decoded = seven_bit_decode(the_binary)
    print(decoded)




