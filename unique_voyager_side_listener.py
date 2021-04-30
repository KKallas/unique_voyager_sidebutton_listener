import sys
import traceback
import time
import socket
import json

UNIQUE_SERIAL_ONLY = True
LIST_VOYAGER_SERIALS = []

voyager_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
voyager_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#voyager_socket.settimeout(0.2)
voyager_address_port = ('', 30000)
voyager_socket.bind(voyager_address_port)

def HandleUniqueSerial(serial,origin):
    print("%s : %s" % (serial,origin[0]))


def HandleMessage(messageDict, origin):
    #print("Message(%s): %s" % (origin, messageDict))

    op_code = None
    serial = None
    if("op_code" in messageDict):
        op_code = messageDict["op_code"]
    if("serial" in messageDict):
        serial = messageDict["serial"]

    if(op_code == None):
        return

    #print("Op code: %s" % op_code)
    if(op_code == "activate_video_trigger"):
        if(serial not in LIST_VOYAGER_SERIALS):
            HandleUniqueSerial(serial,origin)
            if(UNIQUE_SERIAL_ONLY):
                LIST_VOYAGER_SERIALS.append(serial)


while(True):
    #TODO needs to be able to break out of the loop when no packages are incoming
    try:
        (message, origin) = voyager_socket.recvfrom(4096)
        if(message != None):
            messageDict = json.loads(message.decode('utf-8'))
            HandleMessage(messageDict, origin)

    except Exception as e:
        exc_info = sys.exc_info()
        print(str(exc_info))
        traceback.print_exception(*exc_info)

    time.sleep(0.01)
