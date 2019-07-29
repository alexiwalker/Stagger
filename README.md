# Stagger
Python Steganography

-----

Stagger is a Python Steganography module developed for practice and not intended for serious usage. It currently has 2 encodings: 

Linear (concurrent pixel least significant bits encoding) and, 
Stagger (next pixels index incremented by the first 6 bits, +1(decimal) of the current pixel's red channel, eg red b"10011001" would increment pixel index by 100110 -> 38 -> +1 39)

----


## usage

all encodings are instantiated as an object which extends the core.Protocol class

~~~

a = src.Linear("test.png")

a.encode_message("This is how the stagger naive encoding is used", "test2.png")

b = src.Linear("test2.png")

message = b.extract_message()

print(message)


~~~~

Stagger comes bundled with a console interface and a GUI. The console will offer only encoding and decoding, while the GUI will offer encode, decode, visual analysis and image rendering

