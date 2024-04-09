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
    kMsgDKeyDown        = char4_to_N_ui32("DKDN")
    kMsgDKeyDown1_0     = char4_to_N_ui32("DKDN")
    kMsgDKeyUp          = char4_to_N_ui32("DKUP")
    kMsgDKeyUp1_0       = char4_to_N_ui32("DKUP")
    kMsgDKeyRepeat      = char4_to_N_ui32("DKRP")
    kMsgDKeyRepeat1_0   = char4_to_N_ui32("DKRP")
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

def start(stream, mouse_act, keyboard_act):
    try:
        MAXBUF = 1024
        buffer = bytearray(MAXBUF)
        while True:
            mv = memoryview(buffer)[:MAXBUF]
            try:
                nbytes = stream.recv_into(buffer,4)
                if not nbytes:
                    print("HOST: Error no size data")
                    break
                frame_size = struct.unpack('!I', bytes(mv[:4]))[0]
                nbytes = stream.recv_into(buffer,frame_size )
                if not nbytes:
                    print("HOST: Error no message data")
                    break
            except Exception as e:
                print("HOST: Error with Connnection")
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
                    device_name_bytes = DEVICE_NAME.encode('utf-8')
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
                    pass

                if found:
                    pass
                    #DEBUG print("[*] Event: ", protocol_event_prev,  event_msg)

                if(len(data_out)>0):
                    stream.sendall(data_out)
                    #DEBUG print("[*] Trasmitted:", data_out, " Size:", len(data_out), " Type:",  protocol_type)

    except Exception as e:
        print(f"Exception: {e}")
        print("Error on line {}".format(sys.exc_info()[-1].tb_lineno))
        # Handle error appropriately

def start_cpython():
    import socket
    import time
    
    def millis():
        return time.monotonic_ns()//1000000

    if ACTOR_TYPE=='CH9329':
        from KM_CH9329_ACTORS import Mouse, Keyboard
        from serial import Serial  #python3 -m pip install pyserial
        ser = Serial(SERIAL_PORT, 115200, timeout=0)
        mouse_act=Mouse(ser, DEVICE_W, DEVICE_H)
        keyboard_act=Keyboard(ser)
    elif ACTOR_TYPE=='HID':
        from KM_PC_ACTORS import Mouse, Keyboard
        mouse_act=Mouse()
        keyboard_act=Keyboard()    
    else: #DEBUG OUTPUT ONLY
        from KM_DEBUG_ACTORS import Mouse, Keyboard             
        mouse_act=Mouse()
        keyboard_act=Keyboard()

    while(True):                   
        stream_connected=False
        try:
            print ("HOST: Connecting to " + HOST_IP + ":" + str(HOST_PORT))
            # Establish TCP connection
            stream=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Turn off Nagle algorithm
            stream.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            # Set read timeout
            stream.settimeout(HOST_TIMEOUT)
            # Connect Stream
            stream.connect((HOST_IP, HOST_PORT))
            print ("HOST: Connected")
            stream_connected=True
        except Exception as e:
            stream.close()
            pool=None
            stream=None
            print("HOST: Exception " + str(e)  + "...Retrying")    
        
        if stream_connected:
            # Start the communication
            start(stream, mouse_act, keyboard_act)
            stream.close()

def start_circuitpython():
    import wifi
    import socketpool
    import ipaddress
    import os
    import microcontroller
    from supervisor import ticks_ms as millis
    import time
    
    print(microcontroller.cpu.frequency)

    if ACTOR_TYPE=='CH9329':
        from KM_CH9329_ACTORS import Mouse, Keyboard
        import board
        import busio
        from microcontroller import Pin    
        ser = busio.UART(getattr(microcontroller.pin, CP_TX_PIN), getattr(microcontroller.pin, CP_RX_PIN), baudrate=115200, timeout=0)
        
        mouse_act=Mouse(ser, DEVICE_W, DEVICE_H)
        keyboard_act=Keyboard(ser)
    elif ACTOR_TYPE=='HID':
        from KM_CPHID_ACTORS import Mouse, Keyboard
        mouse_act=Mouse(DEVICE_W, DEVICE_H)
        keyboard_act=Keyboard()
    else: #DEBUG OUTPUT ONLY
        from KM_DEBUG_ACTORS import Mouse, Keyboard             
        mouse_act=Mouse()
        keyboard_act=Keyboard()     
        
    wifi.radio.enabled = True
    while(True):
        while(True): #WIFI Connect Loop
            wifi_connected = wifi.radio.ap_info is not None
            if wifi_connected:
                print("WIFI: Connected with IP=" + str(wifi.radio.ipv4_address))
                break
            else:
                print("WIFI: Connecting to " + WIFI_SSID)
                try:
                    wifi.radio.connect(WIFI_SSID, WIFI_PASS)
                except Exception as e:
                    print("HOST: Exception " + str(e)  + "...Retry in 3s")
                    time.sleep(3)
                    
        stream_connected=False
        try:
            print ("HOST: Connecting to " + HOST_IP + ":" + str(HOST_PORT))
            pool = socketpool.SocketPool(wifi.radio)
            # Establish TCP connection
            stream = pool.socket(pool.AF_INET, pool.SOCK_STREAM)
            # Turn off Nagle algorithm
            stream.setsockopt(pool.IPPROTO_TCP, pool.TCP_NODELAY, 1)
            # Set read timeout
            stream.settimeout(5)
            # Connect Stream
            stream.connect((HOST_IP, HOST_PORT))
            # Set read timeout
            stream.settimeout(HOST_TIMEOUT)
            print ("HOST: Connected")
            stream_connected=True
        except Exception as e:
            stream.close()
            pool=None
            stream=None
            print("HOST: Exception " + str(e)  + "...Retry in 3s")    
            time.sleep(3)
        
        if stream_connected:
            # Start the communication
            start(stream, mouse_act, keyboard_act)
            stream.close()
    
def start_micropython():
    from time import ticks_ms as millis  #Needs testing
    import network
    import socket
    import time
    #Required to make class as MP does not have recv_into function
    class MP_socket(socket.socket):
        def recv_into(self, buffer, nbytes):
            return super().readinto(buffer, nbytes)
    
    
    if ACTOR_TYPE=='CH9329':
        from KM_CH9329_ACTORS import Mouse, Keyboard
        from machine import UART
        ser = UART(1, 115200, tx=MP_TX_PIN, rx=MP_RX_PIN, timeout=1)
        mouse_act=Mouse(ser, DEVICE_W, DEVICE_H)
        keyboard_act=Keyboard(ser)
    elif ACTOR_TYPE=='HID':
        from KM_MPHID_ACTORS import KeyboardInterface as keyboard_act
        from KM_MPHID_ACTORS import MouseInterface as mouse_act
        mouse_act.setScreenSize(DEVICE_W, DEVICE_H)
    else: #DEBUG OUTPUT ONLY
        from KM_DEBUG_ACTORS import Mouse, Keyboard             
        mouse_act=Mouse()
        keyboard_act=Keyboard()    
    
    sta_if = network.WLAN(network.STA_IF)
    while(True):
        while(True): #WIFI Connect Loop
            if sta_if.isconnected():
                print("WIFI: Connected with IP=" + str(sta_if.ifconfig()[0]))
                break
            else:
                sta_if.active(False)
                print("WIFI: Connecting to " + WIFI_SSID)
                try:
                    sta_if.active(True)
                    sta_if.connect(WIFI_SSID, WIFI_PASS)
                    for t in range(0, 120):
                        if interface.isconnected():
                            break
                        print(".")
                        time.sleep_ms(200)
                except Exception as e:
                    print("HOST: Exception " + str(e)  + "...Retry in 3s")
                    time.sleep(3)
                    
        stream_connected=False
        try:
            print ("HOST: Connecting to " + HOST_IP + ":" + str(HOST_PORT))

            # Establish TCP connection
            stream = MP_socket(socket.AF_INET, socket.SOCK_STREAM)
            # Set connect timeout
            stream.settimeout(5)
            # Connect Stream
            stream.connect((HOST_IP, HOST_PORT))
            stream.settimeout(HOST_TIMEOUT)
            print ("HOST: Connected")
            stream_connected=True
        except Exception as e:
            stream.close()
            pool=None
            stream=None
            print("HOST: Exception " + str(e)  + "...Retry in 3s")    
            time.sleep(3)
        
        if stream_connected:
            # Start the communication
            start(stream, mouse_act, keyboard_act)
            stream.close()

# Example usage:
if __name__ == "__main__":
    HOST_IP = "192.168.10.186"
    HOST_PORT = 24800
    HOST_TIMEOUT=10
    DEVICE_NAME = "ExampleDevice"
    DEVICE_W=1920
    DEVICE_H=1080
    WIFI_SSID = "SSID"
    WIFI_PASS = "PASS"
    SERIAL_PORT="COM14"
    CP_TX_PIN="GPIO16"
    CP_RX_PIN="GPIO17"        
    MP_TX_PIN=16
    MP_RX_PIN=17
    ACTOR_TYPE='HID'
    
    print(sys.implementation.name)



    if sys.implementation.name == "cpython":
        start_cpython()
    elif sys.implementation.name == "circuitpython":
        ACTOR_TYPE='HID'
        #ACTOR_TYPE='CH9329'
        DEVICE_NAME = "ExampleDevice2"
        start_circuitpython()
    elif sys.implementation.name == "micropython":
        ACTOR_TYPE='HID'
        DEVICE_NAME = "ExampleDevice2"
        start_micropython()
