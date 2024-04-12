# Import modules needed for command line reading and file redirection
import sys

# Flags used for error checking.
testMode = False 

## MAIN ##
# User should only input 1 file.
if(len(sys.argv) == 1):
    # Collect the file data using stdin and strip the white space characters.
    fileData = sys.stdin.read().strip()
    if(testMode == True):
        print(fileData)
    # Check if the file's data is in 8-bit or 7-bit binary
    if(len(fileData) % 7 == 0):
        if(testMode == True):
            print("\n7-Bit\n")
        # Break the string into chunks of 7-bits and store them into an array
        asciiArray = []
        for i in range(0, len(fileData), 7):
            asciiArray.append(fileData[i:i+7])
        # Iterate through the array, evaluating each 7-bit ascii value, appending it to the resulting expression.
        finalStr = ""
        for j in asciiArray:
            intForm = int(j, 2)
            chrForm = chr(intForm)
            finalStr = (finalStr + chrForm)
        print(finalStr)
    elif(len(fileData) % 8 == 0):
        if(testMode == True):
            print("\n8-Bit\n")
        # Break the string into chunks of 8-bits and store them into an array
        asciiArray = []
        for i in range(0, len(fileData), 8):
            asciiArray.append(fileData[i:i+8])
        # Iterate through the array, evaluating each 8-bit ascii value, appending it to the resulting expression.
        finalStr = ""
        for j in asciiArray:
            intForm = int(j, 2)
            chrForm = chr(intForm)
            finalStr = (finalStr + chrForm)
        print(finalStr)
    else:
        print("\nNeither 7- nor 8-bit binary was found in this file.")
    
# Handle the case where someone inputs more than 1 file.
else:
    print("\nInvalid Entry, Usage: 'python Binary.py < Example.txt'")
