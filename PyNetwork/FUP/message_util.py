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
        hBuffer = MessageUtil.recvFromBuffer(sock, 16)
        header = Header(hBuffer)
        print(dir(header))
        bBuffer = MessageUtil.recvFromBuffer(sock, header.BODYLEN)
        body = getBodyType(header, bBuffer)

        msg = Message()
        msg.Header = header
        msg.Body = body

        return msg
