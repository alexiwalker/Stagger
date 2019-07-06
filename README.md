# Stagger
Python Steganography

-----

Stagger is a Python Steganography module developed by Alex W. and is not intended for serious usage. It currently has 2 encodings: Linear (concurrent pixel least significant bits encoding) and Stagger (next pixels index incremented by the first 6 bits, +1(decimal) of the current pixel's red channel, eg red b"10011001" would increment pixel index by 100110 -> 38 -> +1 39)

----


## usage

all encodings are instantiated as an object.

~~~

a = src.Linear("test.png")

a.encode_message("This is how the stagger naive encoding is used", "test2.png")

# In encode_message, the path provided is where the encoded image is saved.
# If this param is omitted, the encoded image is returned as a list of pixels (each pixel = a tuple of (r,g,b) ints)

b = src.Linear("test2.png")

message = b.extract_message()

print(message)

# will print out the message encoded at a

~~~~



