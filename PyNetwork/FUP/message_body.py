from message import ISerializable
import message
import struct
"""
Request Message(0x00)
"""
class BodyRequest(ISerializable):
    def __init__(self, buffer):
        if buffer != None:
            slen = len(buffer)
            #1 unsigned long long, N char
            self.struct_fmt = str.format('=Q{0}s', slen-8)
            self.struct_len = struct.calcsize(self.struct_fmt)
            if slen > 4: # remained char from buffer
                slen = slen - 4
            else:
                slen = 0

            unpacked = struct.unpack(self.struct_fmt,buffer)

            self.FILESIZE = unpacked[0]
            self.FILENAME = unpacked[1].decode(
                #remove packed 00
                encoding='utf.8'.replace('\x00'.'')
            )
        else:
            #buffer == None
            self.struct_fmt = str.format('=Q{0}s', 0)
            self.struct_len = struct.calcsize(self.struct_fmt)
            self.FILESIZE = 0
            self.FILENAME = ''
            
    def GetBytes(self):
        buffer = self.FILENAME.encode(encoding='utf-8')
        #1 ull, n char
        self.struct_fmt = str.format('=Q{0}s',len(buffer))
        
        return struct.pack(
            self.struct_fmt,
            *(
                self.FILESIZE,
                buffer
            )
        )
    def GetSize(self):
        buffer = self.FILENAME.encode(encoding='utf-8')
        #1 ull, n char
        self.struct_fmt = str.format('=Q{0}s',len(buffer))
        self.struct_len = struct.calcsize(self.struct_fmt)
        return self.struct_len

class BodyResponse(ISerializable):
    def __init__(self, buffer):
        #1 uint, 1Byte
        self.struct_fmt = '=IB'
        self.struct_len = struct.calcsize(self.struct_fmt)

        if buffer != None:
            unpacked = struct.unpack(self.struct_fmt,buffer)

            self.MSGID = unpacked[0]
            self.RESPONSE = unpacked[1]
        else:
            #buffer == None
            self.MSGID = 0
            self.RESPONSE = message.DENIED
            
    def GetBytes(self):
        return struct.pack(
            self.struct_fmt,
            *(
                self.MSGID,
                self.RESPONSE
            )
        )
    def GetSize(self):
        return self.struct_len

class BodyData(ISerializable):
    def __init__(self, buffer):
        #1 uint, 1Byte
        self.struct_fmt = '=IB'
        self.struct_len = struct.calcsize(self.struct_fmt)

        if buffer != None:
            unpacked = struct.unpack(self.struct_fmt,buffer)

            self.MSGID = unpacked[0]
            self.RESPONSE = unpacked[1]
        else:
            #buffer == None
            self.MSGID = 0
            self.RESPONSE = message.DENIED
            
    def GetBytes(self):
        return struct.pack(
            self.struct_fmt,
            *(
                self.MSGID,
                self.RESPONSE
            )
        )
    def GetSize(self):
        return self.struct_len