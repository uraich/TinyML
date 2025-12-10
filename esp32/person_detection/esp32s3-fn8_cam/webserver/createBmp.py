import struct

def printByteArray(data):
    for i in range(len(data)-1):
        print("0x{:02x} ,".format(data[i]),end="")
    print("0x{:02x}".format(data[i-1]))
    
hdr = bytearray(12)
size = 0x846
reserved = 0
offset = 0x38
magic = 'BM'.encode('ascii')
struct.pack_into('ihhi',hdr,0,size,reserved,reserved,offset)
fullHdr = magic + hdr

printByteArray(fullHdr)

