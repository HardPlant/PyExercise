import os
import sys
import socket
import socketserver
import struct

import message
from message import Message
from message_header import Header
from message_body import BodyRequest
from message_body import BodyResponse
from message_body import BodyData
from message_body import BodyResult

from message_util import MessageUtil


CHUNK_SIZE = 4096
upload_dir = ''

class FileReceiveHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print("클라이언트 접속 : {0}".format(self.client_address[0]))

        client = self.request # client socket
        reqMsg = MessageUtil.receive(client)
    
        if reqMsg.Header.MSGTYPE != message.REQ_FILE_SEND:
            client.close()
            return

        reqBody = BodyRequest(None)

        print(
            "File Upload reqest. Accept? (yes/no)"
        )
        answer = sys.stdin.readline()
        #Accepted Message
        rspMsg = Message()
        rspMsg.Body = BodyResponse(None)
        rspMsg.Body.MSGID = reqMsg.Header.MSGID #reqId -> resId
        rspMsg.Body.RESPONSE = message.ACCEPTED

        rspMsg.Header = Header(None)

        msgId = 0
        rspMsg.Header.MSGID = msgId
        msgId = msgId + 1
        rspMsg.Header.MSGTYPE = message.REP_FILE_SEND
        resMsg.Header.BODYLEN = rspMsg.Body.GetSize()
        resMsg.Header.FRAGMENTED = message.NOT_FRAGMENTED
        resMsg.Header.LASTMSG = message.LASTMSG
        resMsg.Header.SEQ = 0
        
        if answer.strip() == "yes":
            MessageUtil.send(client, rspMsg)
        else:
            #Denied Message
            rspMsg.Body = BodyResponse(None)
            rspMsg.Body.MSGID = rspMsg.Header.MSGID
            rspMsg.Body.RESPONSE = message.DENIED

            MessageUtil.send(client, rspMsg)
            client.close()
            return
        
        #Start file transfer
        print("Transfering file..")
        fileSize = reqMsg.Body.FILESIZE
        fileName = reqMsg.Body.FILENAME
        recvFileSize = 0
        with open(ipload_dir + "\\" + fileName, 'wb') as file:
            dataMsgId = -1
            prevSeq = 0

            while True:
                reqMsg = MessageUtil.receive(client)
                if reqMsg == None:
                    break
                print('#', end='')
                if reqMsg.Header.MSGTYPE != message.FILE_SEND_DATA:
                    break
                
                if dataMsgId == -1:
                    dataMsgId = reqMsg.Header.MSGID # reqId
                elif dataMsgId != reqMsg.Header.MSGID:
                    break
                
                # break if Message Sequence broken
                if prevSeq != reqMsg.Header.SEQ:
                    print("{0}, {1}".format(prevSeq, reqMsg.Header.SEQ))
                    break

                prevSeq += 1
                #from receive server
                recvFileSize += reqMsg.Body.GetSize()
                file.write(reqMsg.Body.GetBytes())
                
                #Exit loop if last message
                if reqMsg.Header.LASTMSG == message.LASTMSG:
                    break

            file.close()

        print()
        print("Received File size : {0} bytes".format(recvFileSize))
        
        #result message
        rstMsg = Message()
        rstMsg.Body = BodyResult(None)
        rstMsg.Body.MSGID = reqMsg.Header.MSGID
        rstMsg.Body.RESULT = message.SUCCESS

        rstMsg.Header = Header(None)
        rstMsg.Header.MSGID = msgId
        msgId += 1
        rstMsg.Header.MSGTYPE = message.FILE_SEND_RES
        rstMsg.Header.BODYLEN = rstMsg.Body.GetSize()
        rstMsg.Header.FRAGMENTED = message.NOT_FRAGMENTED
        rstMsg.Header.LASTMSG = message.LASTMSG
        rstMsg.Header.SEQ = 0

        if fileSize == recvFileSize:
            MessageUtil.send(client, rstMsg)
        else:
            rstMsg.Body = BodyResult(None)
            rstMsg.Body.MSGID = reqMsg.Header.MSGID
            rstMsg.Body.RESULT = message.FAIL
            MessageUtil.send(client, rstMsg)
            
        print("Finished file transfer.")
        client.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage : {0} <Directory>".format(sys.argv[0]))
        sys.exit(0)
    
    upload_dir = sys.argv[1]
    if os.path.isdir(upload_dir) == False:
        os.mkdir(upload_dir)

    bindPort = 5425
    server = None
    try:
        server = socketserver.TCPServer(
            ('',bindPort), FileReceiveHandler
        )
        print("Start File Upload Server")
        server.serve_forever()
    except Exception as err:
        print(err)

    print("Close Server.")

