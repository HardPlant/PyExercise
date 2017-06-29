# PyExercise
* File Upload Protocol
- Protocol[Header[16],Body[N]]
- Header[MSGID[4],MSGTYPE[4],BODYLEN[4],FRAGMENTED[1],LASTMSG[1],SEQ[2]] (16Byte)
    * MSGID[4] : Message ID
    * MSGTYPE[4] : Message Type
        - 0x01 : Transfer Request
        - 0x02 : Transfer Response
        - 0x03 : Transfer Data
        - 0x04 : Receive Result
    * BODYLEN[4] : Length(Byte)
    * FRAGMENTED[1]
        - Unfragmented : 0x0
        - Fragmented : 0x1
    * LASTMSG[1]
        - Not last : 0x0
        - Last : 0x1
    * SEQ[2] : Segment Number