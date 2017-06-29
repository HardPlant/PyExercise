from message import ISerializble
import struct

class Header(ISerializble):
    def __init__(self, buffer):
        """
        unpack message and parse header.
        :param buffer: packed byte
        """
        self.struct_fmt = '=3I2BH' # 3 unsigned int, 2 byte, 1 unsigned short
        self.struct_len = struct.calcsize(self.struct_fmt)

        if buffer != None:
            unpacked = struct.unpack(self.struct_fmt, buffer)

            self.MSGID = unpacked[0]
            self.MSGTYPE = unpacked[1]
            self.BODYLEN = unpacked[2]
            self.FRAGMENTED = unpacked[3]
            self.LASTMSG = unpacked[4]
            self.SEQ = unpacked[5]

    def GetBytes(self):
        """
        :return: packed message
        """
        return struck.pack(
            self.struct_fmt,
            *(
                self.MSGID,
                self.MSGTYPE,
                self.BODYLEN,
                self.FRAGMENTED,
                self.LASTMSG,
                self.SEQ
            ))
    def getSize(self):
        return self.struct_len
