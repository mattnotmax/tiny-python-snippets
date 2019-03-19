f = open(r'\\.\C:', 'rb')
mbr = f.read(512)
print(mbr.hex())
print(type(mbr))