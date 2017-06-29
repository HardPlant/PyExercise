import socket
import message
from message import message
from message_header import BodyRequest
from message_header import BodyResponse
from message_header import BodyData
from message_header import BodyResult

class MessageUtil:
    @staticmethod
    def send(sock, msg):
        sent = 0
        buffer = msg.GetBytes()
        while sent < msg.GetSize():
            sent += sock.send(buff)

    def recvFromBuffer(bufferSize):    
        totalRecv = 0
        sizeToRead = bufferSize
        hBuffer = bytes() #buffer to recv()

        #read header
        while sizeToRead > 0:
            buffer = sock.recv(sizeToRead)
            if not buffer:
                return None
            hBuffer += buffer
            totalRecv += len(buffer)
            sizeToRead -= len(buffer)

        return hBuffer
        
    def getBodyType(header, bBuffer):
        if header.MSGTYPE == message.REQ_FILE_SEND:
            body = BodyRequest(bBuffer)
        elif header.MSGTYPE == message.REP_FILE_SEND:
            body = BodyResponse(bBuffer)
        elif header.MSGTYPE == message.FILE_SEND_DATA:
            body = BodyData(bBuffer)
        elif header.MSGTYPE == message.FILE_SEND_RES:
            body = BodyResult(bBuffer)
        else:
            raise Exception("Unknown MSGTYPE : {0}".
            format(header.MSGTYPE))
    
    @staticmethod
    def receive(sock):
        hBuffer = recvFromBuffer(16)
        header = Header(hBuffer)

        bBuffer = recvFromBuffer(header.BODYLEN)
        body = getBodyType(header, bBuffer)

        msg = Message()
        msg.Header = header
        msg.Body = body

        return msg
