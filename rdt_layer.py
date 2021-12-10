from segment import Segment


# #################################################################################################################### #
# RDTLayer                                                                                                             #
#                                                                                                                      #
# Description:                                                                                                         #
# The reliable data transfer (RDT) layer is used as a communication layer to resolve issues over an unreliable         #
# channel.                                                                                                             #
#                                                                                                                      #
#                                                                                                                      #
# Notes:                                                                                                               #
# This file is meant to be changed.                                                                                    #
#                                                                                                                      #
#                                                                                                                      #
# #################################################################################################################### #


class RDTLayer(object):
    # ################################################################################################################ #
    # Class Scope Variables                                                                                            #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    DATA_LENGTH = 4 # in characters                     # The length of the string data that will be sent per packet...
    FLOW_CONTROL_WIN_SIZE = 15 # in characters          # Receive window size for flow-control
    sendChannel = None
    receiveChannel = None
    dataToSend = ''
    currentIteration = 0                                # Use this for segment 'timeouts'
    dataReceived = ''
    segmentTimeouts = 0
    acknum = 1
    seqnum = 1
    wait_response = False
    # Add items as needed

    # ################################################################################################################ #
    # __init__()                                                                                                       #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def __init__(self):
        self.sendChannel = None
        self.receiveChannel = None
        self.dataToSend = ''
        self.currentIteration = 0
        self.dataReceived = ''
        self.countSegmentTimeouts = 0
        self.DATA_LENGTH = 4
        self.FLOW_CONTROL_WIN_SIZE = 15
        self.acknum = 1
        self.seqnum = 1
        self.wait_response = False
        # Add items as needed

    # ################################################################################################################ #
    # setSendChannel()                                                                                                 #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to set the unreliable sending lower-layer channel                                                 #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def setSendChannel(self, channel):
        self.sendChannel = channel

    # ################################################################################################################ #
    # setReceiveChannel()                                                                                              #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to set the unreliable receiving lower-layer channel                                               #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def setReceiveChannel(self, channel):
        self.receiveChannel = channel

    # ################################################################################################################ #
    # setDataToSend()                                                                                                  #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to set the string data to send                                                                    #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def setDataToSend(self,data):
        self.dataToSend = data

    # ################################################################################################################ #
    # getDataReceived()                                                                                                #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to get the currently received and buffered string data, in order                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def getDataReceived(self):
        # ############################################################################################################ #
        # Identify the data that has been received...


        # ############################################################################################################ #
        return self.dataReceived

    # ################################################################################################################ #
    # processData()                                                                                                    #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # "timeslice". Called by main once per iteration                                                                   #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def processData(self):
        self.currentIteration += 1
        self.processSend()
        self.processReceiveAndSendRespond()

    # ################################################################################################################ #
    # processSend()                                                                                                    #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Manages Segment sending tasks                                                                                    #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def processSend(self):
        #segmentSend = Segment()

        # ############################################################################################################ #

        # You should pipeline segments to fit the flow-control window
        # The flow-control window is the constant RDTLayer.FLOW_CONTROL_WIN_SIZE
        # The maximum data that you can send in a segment is RDTLayer.DATA_LENGTH
        # These constants are given in # characters

        # Somewhere in here you will be creating data segments to send.
        # The data is just part of the entire string that you are trying to send.
        # The seqnum is the sequence number for the segment (in character number, not bytes)

        if self.dataToSend: #only client
            flow_control = 0 #keep track of total length of segments
            if self.wait_response == False: #proceed after receiving acks from server
                prev_seg = self.acknum #keeps track of what data to send
                for i in range(4): #max 4 segments can be sent
                    segmentSend = Segment()
                    data = ""
                    for j in range(self.DATA_LENGTH):
                        if (prev_seg - 1) >= len(self.dataToSend) or flow_control == self.FLOW_CONTROL_WIN_SIZE:
                            break
                        else:
                            data += self.dataToSend[prev_seg - 1] #pack data into segment
                            prev_seg += 1
                            flow_control += 1
                    seqnum = str(prev_seg - len(data))
                    segmentSend.setData(seqnum,data)
                    print("Sending segment: ", segmentSend.to_string())
                    self.sendChannel.send(segmentSend)
                    if (prev_seg - 1) >= len(self.dataToSend) or flow_control == self.FLOW_CONTROL_WIN_SIZE:
                        break
            else:
                print("Waiting to receive acks from the server...")
            self.wait_response = not self.wait_response

    # ################################################################################################################ #
    # processReceive()                                                                                                 #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Manages Segment receive tasks                                                                                    #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def processReceiveAndSendRespond(self):

        # This call returns a list of incoming segments (see Segment class)...
        listIncomingSegments = self.receiveChannel.receive()

        # ############################################################################################################ #
        # What segments have been received?
        # How will you get them back in order?
        # This is where a majority of your logic will be implemented

        # ############################################################################################################ #
        # How do you respond to what you have received?
        # How can you tell data segments apart from ack segemnts?

        # Somewhere in here you will be setting the contents of the ack segments to send.
        # The goal is to employ cumulative ack, just like TCP does...
        if not self.dataToSend: #only server
            for seg in listIncomingSegments:
                segmentAck = Segment()
                if int(seg.seqnum) == self.seqnum: 
                    if "X" in seg.payload: #resend if checksum error packet
                        break
                    acknum = int(seg.seqnum) + len(seg.payload)
                    self.seqnum = acknum
                    self.dataReceived += seg.payload
                    segmentAck.setAck(str(acknum))
                    print("Sending ack: ", segmentAck.to_string())
                    self.sendChannel.send(segmentAck)
                else: #segment sequence number does not match, resend ack to client
                    self.countSegmentTimeouts += 1 
                    segmentAck.setAck(str(self.seqnum))
                    self.sendChannel.send(segmentAck)
                    break

        if self.dataToSend: #only client
            for seg in listIncomingSegments:
                if (int(seg.acknum) - self.acknum) > 4 or (int(seg.acknum) - self.acknum) < 1: #ack number does not match
                    self.countSegmentTimeouts += 1
                if int(seg.acknum) > self.acknum: #ack number matches and update current ack number
                    self.acknum = int(seg.acknum)
