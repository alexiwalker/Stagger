from lib import linear,stagger
"""
This Is InDev and being tested.  Not ready for usage. 

"""
def main():
    print("Welcome to Stagger Steganography")
    print("Would you like to Encode or Decode a message?")


    _val = int(input("Press 1 for encode, 2 for decode"))

    if _val == 1:
        pass
    elif _val == 2:
        pass
    else:
        print("Invalid selection")
        while _val not in [1,2]:
            _val = int(input("Press 1 for encode, 2 for decode"))

def encode():
    print("Which encoding would you like to use?"
          "\n1) Linear is fast, simple and less secure but can encode a longer message. "
          "\n2) Stagger is slower and more secure but has a restricted message length")

    _val = int(input("> "))
    if _val not in [1,2]:
        print("Invalid selection")
        while _val not in [1,2]:
            _val = int(input("Press 1 for Linear, 2 for Stagger"))

    _message = str(input("Please enter the message you wish to encode"))

    _image = str(input("Please provide the path to the original image"))
    _output = str(input("Please provide the path to the output image"))
    protocol = None
    if _val == 1:
        protocol = linear.Linear(_image)
    elif _val == 2:
        protocol = stagger.Stagger(_image)



    protocol.encode_message(_message,_output)


def decode():
    print("Which decoding would you like to use?"
          "\n1) Linear"
          "\n2) Stagger"
          "\n3) Try all methods until a valid message is found. This may take some time. (NYI")

    _val = int(input("> "))
    if _val not in [1,2]:
        print("Invalid selection")
        while _val not in [1,2]:
            _val = int(input("Press 1 for Linear, 2 for Stagger"))

    _image = str(input("Please provide the path to the encoded image"))
    protocol = None
    if _val == 1:
        protocol = linear.Linear(_image)
    elif _val == 2:
        protocol = stagger.Stagger(_image)


    message = protocol.extract_message()

    print(message)




if __name__ == '__main__':
    main()