# Team Axolotl
# Connor Ettinger
# Steganography Encoding and Decoding Program

import sys
from sys import stdout

CMND_ARGS = {
  "store_mode" : -1,
  "bit_mode" : -1,
  "offset" : 0,
  "interval" : 1,
  "wrapper" : "",
  "hidden" : "",
  "backwards" : False
}
SENTINEL = bytearray([0,255,0,0,255,0]) #0x0 0xff 0x0 0x0 0xff 0x0

########################## Define functions ##########################
# parse the command line arguements
def parse_args():
  for arg in sys.argv:
    # handle use mode (if it's in store or retrieve mode)
    if arg == "-r" and CMND_ARGS["store_mode"] == -1:
      CMND_ARGS["store_mode"] = 0
      continue
    elif arg == "-s" and CMND_ARGS["store_mode"] == -1:
      CMND_ARGS["store_mode"] = 1
      continue
    # can't have store and retrieve set at the same time
    # if store_mode isn't -1, it's already been set, so we're not allowed to have it set again
    elif (arg == "-s" or arg == "-r") and CMND_ARGS["store_mode"] != -1:
      write_and_exit("Error: Cannot have both -s and -r set, please try again")

    # handle data mode (if it's in bit or byte mode)
    if arg == "-B" and CMND_ARGS["bit_mode"] == -1:
      CMND_ARGS["bit_mode"] = 0
      continue
    elif arg == "-b" and CMND_ARGS["bit_mode"] == -1:
      CMND_ARGS["bit_mode"] = 1
      continue
    # can't have bit and byte set at the same time
    # if bit_mode isn't -1, it's already been set, so we're not allowed to have it set again
    elif (arg == "-b" or arg == "-B") and CMND_ARGS["bit_mode"] != -1:
      write_and_exit("Error: Cannot have both -b and -B set, please try again")

    # get offset
    if arg.startswith("-o"):
      try:
        CMND_ARGS["offset"] = int(arg[2:])
      except ValueError:
        write_and_exit("Error: offset is not an int, please try again")
      except:
        write_and_exit("Error: something is wrong with offset")

    # get interval
    if arg.startswith("-i"):
      try:
        CMND_ARGS["interval"] = int(arg[2:])
      except ValueError:
        write_and_exit("Error: interval is not an int, please try again")
      except:
        write_and_exit("Error: something is wrong with interval")

    # get wrapper
    if arg.startswith("-w"):
      CMND_ARGS["wrapper"] = arg[2:]

    # get hidden
    if arg.startswith("-h"):
      CMND_ARGS["hidden"] = arg[2:]

    # handle backwards
    if arg == "--backwards" or arg == "--reverse":
      CMND_ARGS["backwards"] = True
    
    # handle help
    if arg == "--help":
      str = "Team Axolotol's Steganography Encoding and Decoding Program\n"
      str += "Useage: python steg.py -(s | r) -(b | B) -o[val] -i[val] -w[file_path] -h[file_path] [OPTIONS]\n\n"
      str += "-s: run in storage/encode mode (mutally exclusive from -r)\n"
      str += "-r: run in retrevial/decode mode (mutally exclusive from -s)\n"
      str += "-b: encode/decode in bit mode [less noticable, takes more space] (mutally exclusive from -B)\n"
      str += "-B: encode/decode in byte mode [more noticable, takes less space] (mutally exclusive from -b)\n"
      str += "-o[val]: the offset, val must be an int. If not specified, defaults to 0. Example usage: -o1024\n"
      str += "-i[val]: the interval, val must be an int. If not specified, defaults to 1. Example usage: -i8\n"
      str += "-w[file_path]: the path to the wrapper file. If -s, this is the file where the data will be stored. If -r, this is the file the data will be extracted from. Example usage: -wfile.bmp\n"
      str += "-h[file_path]: the path to the hidden file. This is the file that will be encode in the wrapper. Only required for storage mode. Example usage: -hfile.bmp\n"
      str += "\nOTHER OPTIONS:\n--backwards, --reverse: store/read data from right-to-left instead of left-to-right\n"
      str += "--help: display this help message"
      write_and_exit(str, False)

  # now, all of the args should be set, so make sure we're not missing anything/there's no conflicting arguements
  check_args()

# make sure we're not missing anything/there's no conflicting arguements
def check_args():
  if CMND_ARGS["store_mode"] == -1: # make sure the usage mode has been set
    write_and_exit("Error: Useage mode not set.\nPlease run with arguements \"-s\" for store mode or \"-r\" for retrieve mode")
  elif CMND_ARGS["bit_mode"] == -1: # make sure the data mode has been set
    write_and_exit("Error: Data mode not set.\nPlease run with arguements \"-b\" for bit mode or \"-B\" for byte mode")
  elif CMND_ARGS["wrapper"] == "": # make sure the wrapper has been set
    write_and_exit("Error: Wrapper not set.\nPlease please specify a file in the current directory to be the wrapper using \"-w[file_name]\"")
  elif CMND_ARGS["hidden"] == "" and CMND_ARGS["store_mode"]: # if we're storing, make sure the file to be hidden has been set
    write_and_exit("Error: hidden file not specified while in store mode.\nPlease please specify a file in the current directory to be hidden using \"-h[file_name]\", or run in retrevial mode using \"-r\"")

# this writes something to stdout, then exits the program
def write_and_exit(to_be_written,display_help=True):
  sys.stderr.write(to_be_written + "\n")
  if display_help:
    sys.stderr.write("Type \"steg.py --help\" for more info")
  sys.stderr.flush()
  sys.exit()

# Byte Storage
# this function been pretty much directly translated from the pseudocode given in the assignment file
def byte_storage(wrap_bytes,hidden_bytes,interval,offset):
  i = 0
  while(i < len(hidden_bytes)):
    wrap_bytes[offset] = hidden_bytes[i]
    offset += interval
    i += 1

  j = 0
  while(j < len(SENTINEL)):
    wrap_bytes[offset] = SENTINEL[j]
    offset += interval
    j += 1
  return(wrap_bytes)

# Byte Retrevial
# this function been pretty much directly translated from the pseudocode given in the assignment file
def byte_extraction(wrap_bytes,interval,offset):
  extracted_byte_arr = bytearray()
  matched_bytes = 0 # number of consecutive bytes that match the sentinel
  while(offset < len(wrap_bytes)):
    if(matched_bytes > 5):
      # if we matched all 6 bits of the sentinel, we've reached the end of the hidden file, so return the extracted_byte_arr
      return(extracted_byte_arr)

    curr_byte = wrap_bytes[offset]
    # check if the current byte matches a sentinel byte
    if(curr_byte == SENTINEL[matched_bytes]):
      # if so, we need to check further
      matched_bytes += 1
      offset += interval
      continue
    else:
      # if not, then we add this byte to the extracted_byte_arr
      # but first, we need to check if there were any previously matched sentinel bytes
      if(matched_bytes > 0):
        # if there were, we add all matched partial sentinel bytes to extracted_byte_arr
        for i in range(0,matched_bytes):
          extracted_byte_arr += SENTINEL[i].to_bytes(1,'big')
        # reset our counter of matched bits
        matched_bytes = 0
      # now add this byte to extracted_byte_arr
      extracted_byte_arr += curr_byte.to_bytes(1,'big')
      offset += interval
  # theoretically, this part of the code should be unreachable
  sys.stderr.write("SENTINEL not detected... weird\n")
  sys.stderr.flush()
  return(extracted_byte_arr)

# Bit Storage
def bit_storage(wrap_bytes,hidden_bytes,interval,offset):
  # add all of the hidden bytes to the wrapper
  i = 0
  while(i < len(hidden_bytes)):
    for _ in range(8):
      wrap_bytes[offset] = wrap_bytes[offset] & 0b11111110
      wrap_bytes[offset] = wrap_bytes[offset] | ((hidden_bytes[i] & 0b10000000) >> 7)
      # constrain the number to a byte
      hidden_bytes[i] = (hidden_bytes[i] << 1) & (2 ** 8 -1) # B = (B << 1) & (2 ** 8 - 1)
      offset += interval

    i += 1

  # append the sentinal to the wrapper
  j = 0
  while(j < len(SENTINEL)):
    for _ in range(8):
      wrap_bytes[offset] = wrap_bytes[offset] & 0b11111110
      wrap_bytes[offset] = wrap_bytes[offset] | ((SENTINEL[j] & 0b10000000) >> 7)
      # constrain the number to a byte
      SENTINEL[j] = (SENTINEL[j] << 1) & (2 ** 8 -1)
      offset += interval

    j += 1
  return(wrap_bytes)

# Bit Retrevial
def bit_extraction(wrap_bytes,interval,offset):
  extracted_byte_arr = bytearray()
  matched_bytes = 0 # number of consecutive bytes that match the sentinel
  while(offset < len(wrap_bytes)):
    if(matched_bytes > 5):
      # if we matched all 6 bits of the sentinel, we've reached the end of the hidden file, so return the hidden file
      return(extracted_byte_arr)

    # extract the value of the current byte
    curr_byte = 0
    for i in range(8):
      curr_byte = curr_byte | (wrap_bytes[offset] & 0b00000001)
      if i < 7:
        curr_byte = (curr_byte << 1) & (2 ** 8 -1) # constrain the number to a byte
        offset += interval

    # now that we have curr_byte as a byte, check if curr_byte matches a sentinel byte
    if(curr_byte == SENTINEL[matched_bytes]):
      # if so, we need to check further
      matched_bytes += 1
      offset += interval
      continue
    else:
      # if not, then we add this byte to the extracted_byte_arr
      # but first, we need to check if there were any previously matched sentinel bytes
      if(matched_bytes > 0):
        # if there were, we add all matched partial sentinel bytes to extracted_byte_arr
        for j in range(0,matched_bytes):
          extracted_byte_arr += SENTINEL[j].to_bytes(1,'big')
        # reset our counter of matched bits
        matched_bytes = 0

      # if not, we can add this byte to hidden_bytes
      extracted_byte_arr += curr_byte.to_bytes(1,'big')
      offset += interval

  # theoretically, this part of the code should be unreachable
  sys.stderr.write("SENTINEL not detected... weird")
  sys.stderr.flush()
  return(extracted_byte_arr)



############################## MAIN ########################################
# parse command line args, add them to CMND_ARGS dictonary
parse_args()

# turn the wrapper into a bytearray
with open(CMND_ARGS["wrapper"], "rb") as wrp:
  wrapper_byte_array = bytearray(wrp.read())

# if you need to read from right to left (as hinted at for cyberstorm)
if CMND_ARGS["backwards"]:
  wrapper_byte_array.reverse()

# handle store mode
if CMND_ARGS["store_mode"]:
  # if store moade is activated, turn hidden into a bytearray
  with open(CMND_ARGS["hidden"], "rb") as hid:
    hidden_byte_array = bytearray(hid.read())

  # if you need to read from right to left (as hinted at for cyberstorm)
  if CMND_ARGS["backwards"]:
    hidden_byte_array.reverse()

  if CMND_ARGS["bit_mode"]:
    modified_wrapper = bit_storage(wrapper_byte_array,hidden_byte_array,CMND_ARGS["interval"], CMND_ARGS["offset"])
  else:
    modified_wrapper = byte_storage(wrapper_byte_array,hidden_byte_array,CMND_ARGS["interval"], CMND_ARGS["offset"])
  stdout.buffer.write(modified_wrapper)
# handle extract mode
else:
  if CMND_ARGS["bit_mode"]:
    hidden_byte_array = bit_extraction(wrapper_byte_array,CMND_ARGS["interval"], CMND_ARGS["offset"])
  else:
    hidden_byte_array = byte_extraction(wrapper_byte_array,CMND_ARGS["interval"], CMND_ARGS["offset"])
  stdout.buffer.write(hidden_byte_array)