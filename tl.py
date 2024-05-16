## Import the hash library for handling hashes
import hashlib
## Import the "sys" library for system arguments and handling
import sys
## Import the datetime and timedelta assets for time sourcing.
from datetime import datetime, timedelta
## Import the pytz library for timezone handling
import pytz

## Variable used for troubleshooting.
TEST = True
################ YYYY MM DD HH MM SS
TEST_SYS_TIME = "2024 05 10 04 15 41"
TEST_EPOCH_TIME = "2023 01 01 00 00 00"

## Method used to calculate the timelock code.
def calculateTlCode(epoch):
    # Retrieve the current time and format the epoch time 
    if(TEST != True):
        current = datetime.now()
    else:
        # If in test mode, user should have passed in a time for testing.
        current = datetime.strptime(TEST_SYS_TIME, "%Y %m %d %H %M %S")
        # Print the System Time to ensure no errors have occurred.
        print(f"System Time: {current}\n")
    
    # Set the epoch time to a datetime object
    epoch = datetime.strptime(epoch, "%Y %m %d %H %M %S")

    # Get the UTC timezone then convert current and epoch times to UTC
    current = current.astimezone(pytz.utc)
    epoch = epoch.astimezone(pytz.utc)

    # If in test mode, print the epoch time for error checking.
    if(TEST == True):
        print(f"Epoch Time: {epoch}")

    # Have the current time set to the next possible minute. This allows for 1 minute of the same return value.
    if(current.second >= 0):
        #current = current.replace(second=0)
        current += timedelta(minutes=1)
    
    # After playing around with the program, this singular line in this exact position fixes everything.. i dont know why. 
    current -= timedelta(minutes=1)
    if(TEST == True):
        print(f"Current Time: {current}\n")

    # Calculate the time elapsed from current to epoch, and retrieve the seconds within that time.
    elapsed_time = (current - epoch).total_seconds()

    # If in test mode, print the elapsed time for trouble shooting
    if(TEST == True):
        print(f"Elapsed Time: {elapsed_time}")
        print(f"E.T. Remainder: {elapsed_time % 60}\n")
    
    # If there is a remainder from modulos of the elapsed time, subtract it.
    if((elapsed_time % 60) > 0):
        elapsed_time -= (elapsed_time % 60)
        if(TEST == True):
            print(f"Adjusted E.T: {elapsed_time}\n")

    # Retrieve the hash of the elapsed time and save it
    hashed_time = hashlib.md5(str(int(elapsed_time)).encode()).hexdigest()
    # For extra security and randomness to the generation of our hash, hash again
    secure_hash = hashlib.md5(hashed_time.encode()).hexdigest()

    # If in test mode, print the results of the first and second hashes.
    if(TEST == True):
        print(f"1st Hash: {hashed_time}\n2nd Hash: {secure_hash}")

    # Extract the first two instances of letters (ltr), and numbers (rtl) from the secure_hash.
    ltr = ''.join(char for char in secure_hash if char.isalpha())[:2]
    rtl = ''.join(char for char in secure_hash[::-1] if char.isdigit())[:2]
    # If in test mode, print the letters and numbers
    if(TEST == True):
        print(f"Letters: {ltr}\nNumbers: {rtl}")

    # Concatenate the first two letters of the hash from left to right, ([a-f])
    # and the first two integers from right to left, ([0-9])
    coded_time = (ltr + rtl)
    
    # Return the encoded/hashed time.
    return coded_time, secure_hash


## MAIN ##
if(__name__ == "__main__"):
    # If in test mode, print a manually entered epoch time
    if(TEST == True):
        X, Y = calculateTlCode(TEST_EPOCH_TIME)
        Y = Y[(len(Y)+1)//2]
        print(f"\nRESULT: {X},{Y}")
    else:
        # Check if the input is redirected or piped into timelock.py
        if(sys.stdin.isatty()):
            print("Usage: python3 timelock.py < epoch.txt [OR] echo ''<epoch_time>'' | python3 timelock.py ")
        else:
            # Read the input from the redirection file or pipe
            data = sys.stdin.read().strip()
            # Handle the case where the input is a redirection
            if(data.isdigit()):
                epoch = data
            else:
                # Handles the case where the input is pipped in
                epoch = data.split(":")[-1].strip()
            # Print the output of the timelock calculation function
            result, the_hash = calculateTlCode(epoch) 
            middle = the_hash[(len(the_hash)-1)//2]
            print(result, middle)
            
            print(f"disintuitive{result}{middle}")





