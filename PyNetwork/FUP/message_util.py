import socket
import message
from message import Message
from message_header import Header
from message_body import BodyRequest
from message_body import BodyResponse
from message_body import BodyData
from message_body import BodyResult

class MessageUtil:
    @staticmethod
    def send(sock, msg):
        sent = 0
        buffer = msg.GetBytes()
        while sent < msg.GetSize():
            sent += sock.send(buffer)
    @staticmethod
    def recvFromBuffer(sock, bufferSize):    
        totalRecv = 0
        sizeToRead = bufferSize
        hBuffer = bytes() #buffer to recv()

        #read header
        while sizeToRead > 0:
            buffer = sock.recv(sizeToRead)
            if not buffer:
                print("null")
                return None
            hBuffer += buffer
            totalRecv += len(buffer)
            sizeToRead -= len(buffer)
        return hBuffer
    
    @staticmethod
    def getBodyType(header, bBuffer):
        if header.MSGTYPE == message.REQ_FILE_SEND:
            print("BodyRequest")
            return BodyRequest(bBuffer)
        elif header.MSGTYPE == message.REP_FILE_SEND:
            print("BodyResponse")
            return BodyResponse(bBuffer)
        elif header.MSGTYPE == message.FILE_SEND_DATA:
            print("BodyData")
            return BodyData(bBuffer)
        elif header.MSGTYPE == message.FILE_SEND_RES:
            print("BodyResult")
            return BodyResult(bBuffer)
        else:
            raise Exception("Unknown MSGTYPE : {0}".
            format(header.MSGTYPE))
    
    @staticmethod
    def receive(sock):
        hBuffer = MessageUtil.recvFromBuffer(sock, 16)
        header = Header(hBuffer)
        bBuffer = MessageUtil.recvFromBuffer(sock, header.BODYLEN)
        body = MessageUtil.getBodyType(header, bBuffer)

        msg = Message()
        msg.Header = header
        msg.Body = body
        return msg
