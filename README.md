# Stagger
Python Steganography

Note: Stagger is currently being reworked from a single standalone file to a properly structured module. Details in the README reflect how it will be once this transition is complete. This message will be removed at that time


-----

Stagger is a Python Steganography module developed by Alex W. and is not intended for serious usage. It currently has 2 encodings: naive (concurrent least significant bits encoding) and stagger (LSB pixel encoding distributed nonlinearly throughout the image in a way that can be predictably reversed)

----


## usage

all encodings are instantiated as an object.

~~~

a = stagger.naive("test.png")

a.encode_message("This is how the stagger naive encoding is used", "test2.png")

# In encode_message, the path provided is where the encoded image is saved.
# If this param is omitted, the encoded image is returned as a list of pixels (each pixel = a tuple of (r,g,b) ints)

b = stagger.naive("test2.png")

message = b.extract_message()

print(message)

# will print out the message encoded at a

~~~~



