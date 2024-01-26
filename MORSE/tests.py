fontFile = open("FF.dat", "rb")
contents = fontFile.read()
print(contents)
font = bytearray(contents)
print(font)


 fontDataPixelValues = font[(ord("text"[0])-32)*8 + col]