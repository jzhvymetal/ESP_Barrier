import sys
import struct

def char4_to_N_ui32(s):
    return ((ord(s[3]) << 24) & 0xFF000000) | \
           ((ord(s[2]) << 16) & 0x00FF0000) | \
           ((ord(s[1]) << 8) & 0x0000FF00) | \
           (ord(s[0]) & 0x000000FF)

class EmuMessageTypes:
    kMsgNull            = char4_to_N_ui32("NULL")  # Added for coding purposes
    kMsgDMouseMoves     = char4_to_N_ui32("MMOV")  # Never received, Used for all mouse move cases
    kMsgDMouseMove      = char4_to_N_ui32("DMMV")
    kMsgDMouseRelMove   = char4_to_N_ui32("DMRM")
    kMsgCKeepAlive      = char4_to_N_ui32("CALV")
    kMsgHello           = char4_to_N_ui32("Barr")
    kMsgHelloBack       = char4_to_N_ui32("TXHB")  # Never received, changed from "Barr" to TXHB to prevent duplicated case
    kMsgCNoop           = char4_to_N_ui32("CNOP")
    kMsgCClose          = char4_to_N_ui32("CBYE")
    kMsgCEnter          = char4_to_N_ui32("CINN")
    kMsgCLeave          = char4_to_N_ui32("COUT")
    kMsgCClipboard      = char4_to_N_ui32("CCLP")
    kMsgCScreenSaver    = char4_to_N_ui32("CSEC")
    kMsgCResetOptions   = char4_to_N_ui32("CROP")
    kMsgCInfoAck        = char4_to_N_ui32("CIAK")
    kMsgDKeys           = char4_to_N_ui32("KKEY")  # Never received, Used for all keyboard key cases
    kMsgDKeyDown        = char4_to_N_ui32("DKDN")
    kMsgDKeyDown1_0     = char4_to_N_ui32("DKDN")
    kMsgDKeyUp          = char4_to_N_ui32("DKUP")
    kMsgDKeyUp1_0       = char4_to_N_ui32("DKUP")
    kMsgDKeyRepeat      = char4_to_N_ui32("DKRP")
    kMsgDKeyRepeat1_0   = char4_to_N_ui32("DKRP")
    kMsgDMouseButtons   = char4_to_N_ui32("MBTN")  # Never received, Used for all mouse button cases
    kMsgDMouseDown      = char4_to_N_ui32("DMDN")
    kMsgDMouseUp        = char4_to_N_ui32("DMUP")
    kMsgDMouseWheel     = char4_to_N_ui32("DMWM")
    kMsgDMouseWheel1_0  = char4_to_N_ui32("DMWM")
    kMsgDClipboard      = char4_to_N_ui32("DCLP")
    kMsgDInfo           = char4_to_N_ui32("DINF")
    kMsgDSetOptions     = char4_to_N_ui32("DSOP")
    kMsgDFileTransfer   = char4_to_N_ui32("DFTR")
    kMsgDDragInfo       = char4_to_N_ui32("DDRG")
    kMsgQInfo           = char4_to_N_ui32("QINF")
    kMsgEIncompatible   = char4_to_N_ui32("EICV")
    kMsgEBusy           = char4_to_N_ui32("EBSY")
    kMsgEUnknown        = char4_to_N_ui32("EUNK")
    kMsgEBad            = char4_to_N_ui32("EBAD")

def start(stream, device_name):


    try:
        MAXBUF = 1024
        buffer = bytearray(MAXBUF)
        while True:
            mv = memoryview(buffer)[:MAXBUF]
            if(1):
                nbytes = stream.recv_into(buffer,4)
                if not nbytes:
                    print("Error: No stream size data")
                    break
                frame_size = struct.unpack('!I', bytes(mv[:4]))[0]
                nbytes = stream.recv_into(buffer,frame_size )
                if not nbytes:
                    print("Error: No stream message data")
                    break
               
                protocol_type = struct.unpack('I', bytes(mv[:4]))[0]
                #Clear out buffer
                data_out=b""
                
                protocol_event_prev=""
                while protocol_type != protocol_event_prev:
                    #loop if protocol_type by another protocol_type
                    protocol_event_prev = protocol_type
                    event_msg=""
                    found=1
                    
                    if protocol_type == EmuMessageTypes.kMsgHello: #"Barrier%2i%2i"
                        major, minor = struct.unpack('!HH', bytes(mv[7:frame_size]))
                        event_msg="Major="+ str(major) + " Minor=" + str(minor)
                        protocol_type = EmuMessageTypes.kMsgHelloBack
                        
                    elif protocol_type == EmuMessageTypes.kMsgDKeyUp: # "DKUP%2i%2i%2i",
                       KeyId, KeyModifiers, KeyButton = struct.unpack('!HHH', bytes(mv[4:frame_size]))
                       keyboard_act.release(KeyId, KeyModifiers, KeyButton)                       
                    elif protocol_type == EmuMessageTypes.kMsgDKeyDown:  #"DKDN%2i%2i%2i"
                       KeyId, KeyModifiers, KeyButton = struct.unpack('!HHH', bytes(mv[4:frame_size]))
                       keyboard_act.press(KeyId, KeyModifiers, KeyButton)
                    elif protocol_type == EmuMessageTypes.kMsgDKeyRepeat:  #"DKRP%2i%2i%2i%2i"
                       KeyId, KeyModifiers, KeyRepeat, KeyButton = struct.unpack('!HHHH', bytes(mv[4:frame_size]))
                       keyboard_act.repeat(KeyId, KeyModifiers, KeyButton)                            
                    elif protocol_type == EmuMessageTypes.kMsgDMouseMove: #"DMMV%2i%2i"
                       mx, my = struct.unpack('!HH', bytes(mv[4:frame_size]))
                       mouse_act.move(mx, my)
                    elif protocol_type == EmuMessageTypes.kMsgDMouseDown: #"DMDN%1i"
                       mb = struct.unpack('!B', bytes(mv[4:frame_size]))[0]
                       mouse_act.press(mb)
                    elif protocol_type == EmuMessageTypes.kMsgDMouseUp: #"DMUP%1i"
                       mb = struct.unpack('!B', bytes(mv[4:frame_size]))[0]
                       mouse_act.release(mb)
                    elif protocol_type == EmuMessageTypes.kMsgDMouseWheel: #DMWM%2i%2i"
                       wx, wy = struct.unpack('!hh', bytes(mv[4:frame_size]))
                       mouse_act.wheel(wx // 120, wy // 120)   
                    elif protocol_type == EmuMessageTypes.kMsgCKeepAlive: #CALV
                        data_out = struct.pack('!I4s' , 4 , b"CALV",) 
                    elif protocol_type == EmuMessageTypes.kMsgHelloBack: #"Barrier%2i%2i%s"
                        device_name_bytes = device_name.encode('utf-8')
                        device_name_len = len(device_name_bytes)
                        frame_size = device_name_len + 15
                        data_out = struct.pack('!I7sHHI%ds' % device_name_len, frame_size, b"Barrier", major, minor, device_name_len, device_name_bytes)      
                    elif protocol_type == EmuMessageTypes.kMsgQInfo: #"QINF"
                        protocol_type =EmuMessageTypes.kMsgDInfo  
                    elif protocol_type == EmuMessageTypes.kMsgDInfo: #"DINF%2i%2i%2i%2i%2i%2i%2i",
                        x=0     	# x coordinate of leftmost pixel on secondary screen,
                        y=0     	# y coordinate of topmost pixel on secondary screen
                        w=DEVICE_W  # w width of secondary screen in pixels
                        h=DEVICE_H 	# h height of secondary screen in pixels
                        z=0     	# size of warp zone, (obsolete)
                        mx=0    	# mx position of the mouse on the secondary screen.
                        my=0    	# my position of the mouse on the secondary screen.
                        data_out = struct.pack('!I4sHHHHHHH' , 18 , b"DINF", x,y,w,h,z,mx,my)
                                               
                    else:
                        #DEBUG print("[*] Error: protocol_type=",protocol_type,"not found.")
                        found=0
  
                    if found:
                        pass
                        #DEBUG print("[*] Event: ", protocol_event_prev,  event_msg)
  
                    if(len(data_out)>0):
                        stream.sendall(data_out)
                        #DEBUG print("[*] Trasmitted:", data_out, " Size:", len(data_out), " Type:",  protocol_type)
                #break

    except Exception as e:
        print(f"Exception: {e}")
        print("Error on line {}".format(sys.exc_info()[-1].tb_lineno))
        # Handle error appropriately

# Example usage:
if __name__ == "__main__":
    HOST = "192.168.10.186"
    PORT = 24800
    DEVICE_NAME = "ExampleDevice"
    DEVICE_W=1920
    DEVICE_H=1080
    TIMEOUT=10
    SSID="SSID"
    AP_PASS="PASS"
    
    
    
    print(sys.implementation.name)


    if sys.implementation.name == "cpython":
        import socket
        
        # Establish TCP connection
        stream=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Turn off Nagle algorithm
        stream.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        # Set read timeout
        stream.settimeout(TIMEOUT)
        # Connect Stream
        stream.connect((HOST, PORT))

        
        Actor_Type='PC'
        if Actor_Type=='PC':
            from PC_KM_ACTORS import Mouse, Keyboard
            mouse_act=Mouse()
            keyboard_act=Keyboard()
        elif Actor_Type=='CH9329':
            from CH9329_KM_ACTORS import Mouse, Keyboard
            from serial import Serial  #python3 -m pip install pyserial
            ser = Serial("COM14", 115200, timeout=0)
            mouse_act=Mouse(ser)
            keyboard_act=Keyboard(ser)
        else:
            class Mouse:
                def move(self, x, y):
                    print("Mouse: X=" + str(x) + " Y=" + str(y))
                    return
                def press(self, b):   
                    return
                def release(self, b):  
                    return
                def wheel(self, x, y): 
                    return
            class Keyboard:
                def press(self, b):   
                    return
                def release(self, b):  
                    return
                def repeat(self, b):  
                    return                
            mouse_act=Mouse()
            keyboard_act=Keyboard()
        
        
    elif sys.implementation.name == "circuitpython":
        DEVICE_NAME = "ExampleDevice2"
        import wifi
        import socketpool
        import ipaddress
        import os
        import microcontroller

        print(microcontroller.cpu.frequency)


        Actor_Type='HID'
        if Actor_Type=='CH9329':
            from CH9329_KM_ACTORS import Mouse, Keyboard
            
            import board
            import busio            
            ser = busio.UART(board.GPIO16, board.GPIO17, baudrate=115200, timeout=0)
            mouse_act=Mouse(ser)
            keyboard_act=Keyboard(ser)
            
        else:
            import usb_hid
            from adafruit_hid import find_device
            barrier_mouse_btn_map = [ 
            7,	# 0 None #7 will mean none
            0,	# 1 LEFT
            2,	# 2 MIDDLE
            1,	# 3 RIGHT
            3,	# 5 X
            4,	# 6 X2
            ]
            
            class Mouse(object):
                mx=0
                my=0
                mb=0
                mwx=0
                mwy=0
                sw=1920
                sh=1080
                def __init__(self):
                    self._mouse_device = find_device(usb_hid.devices, usage_page=0x1, usage=0x02)
                    self.report = bytearray(6)
                
                def send_mouse_data(self):
                    cx = (32767 * self.mx) // self.sw 
                    cy = (32767 * self.my) // self.sh
                    self.report = struct.pack("<BHHb",self.mb, cx, cy,self.mwy)
                    self._mouse_device.send_report(self.report)
                def move(self, px, py):
                    self.mx=px
                    self.my=py
                    self.send_mouse_data()
                    return
                def press(self, b):
                    self.mb= self.mb | (1 << barrier_mouse_btn_map[b])  # Set bit at b of mb, bit locations= 0:LEFT 1:MIDDLE 2:RIGHT
                    self.send_mouse_data()
                    return
                def release(self, b):
                    self.mb = self.mb & ~(1 << barrier_mouse_btn_map[b])  # Reset bit at b of mb, bit locations= 0:LEFT 1:MIDDLE 2:RIGHT      
                    self.send_mouse_data()
                    return
                def wheel(self, x, y):
                    self.mwx=x
                    self.mwy=y
                    self.send_mouse_data()
                    #Reset Wheel values
                    self.mwx=0
                    self.mwy=0
                    return
        
            class Keyboard:
                def press(self, b):   
                    return
                def release(self, b):  
                    return
                def repeat(self, b):  
                    return            
            mouse_act=Mouse()
            keyboard_act=Keyboard()

            
            
            
        print("Connecting to wifi")
        wifi.radio.connect(SSID, AP_PASS)
        pool = socketpool.SocketPool(wifi.radio)

        print("Self IP", wifi.radio.ipv4_address)
        server_ipv4 = ipaddress.ip_address(pool.getaddrinfo(HOST, PORT)[0][4][0])
        print("Server ping", server_ipv4, wifi.radio.ping(server_ipv4), "ms")
        # Establish TCP connection
        stream = pool.socket(pool.AF_INET, pool.SOCK_STREAM)
        # Turn off Nagle algorithm
        stream.setsockopt(pool.IPPROTO_TCP, pool.TCP_NODELAY, 1)
        # Set read timeout
        stream.settimeout(TIMEOUT)
        # Connect Stream
        stream.connect((HOST, PORT))
    elif sys.implementation.name == "micropython":
        DEVICE_NAME = "ExampleDevice2"
        import network
        
        Actor_Type='CH9329'
        if Actor_Type=='CH9329':
            from CH9329_KM_ACTORS import Mouse, Keyboard
            
            from machine import UART
            
            ser = UART(1, 115200, tx=16, rx=17, timeout=1)
            mouse_act=Mouse(ser)
            keyboard_act=Keyboard(ser)
            
        else:    
            class Mouse:
                def move(self, x , y):
                    print("Mouse: X=" + str(x) + " Y=" + str(y))
                    return
                def press(self, b):
                    return
                def release(self, b):
                    return
                def wheel(self, x, y): 
                    return
            class Keyboard:
                def press(self, b):   
                    return
                def release(self, b):  
                    return
                def repeat(self, b):  
                    return            
            mouse_act=Mouse()
            keyboard_act=Keyboard()
        
        sta_if = network.WLAN(network.STA_IF)
        if not sta_if.isconnected():
            print('connecting to network...')
            sta_if.active(True)
            sta_if.connect(SSID, AP_PASS)
            while not sta_if.isconnected():
                pass
        print('network config:', sta_if.ifconfig())


        import socket
        class MP_socket(socket.socket):
            def recv_into(self, buffer, nbytes):
                return super().readinto(buffer, nbytes)

        # Establish TCP connection
        stream = MP_socket(socket.AF_INET, socket.SOCK_STREAM)
        # Turn off Nagle algorithm
        #stream.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        # Set read timeout
        stream.settimeout(TIMEOUT)
        # Connect Stream
        stream.connect((HOST, PORT))

        
    # Start the communication
    start(stream, DEVICE_NAME)