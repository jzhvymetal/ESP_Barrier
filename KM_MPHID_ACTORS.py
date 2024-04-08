import usb.device
from usb.device.hid import HIDInterface


ABS_MOUSE_DESC=bytes((
        # Absolute mouse
        0x05, 0x01,    # Usage Page (Generic Desktop)
        0x09, 0x02,  # Usage (Mouse)
        0xA1, 0x01,  # Collection (Application)
        0x09, 0x01,  # Usage (Pointer)
        0xA1, 0x00,  # Collection (Physical)
        0x85, 0x0B,  # Report ID  [11 is SET at RUNTIME]
        # Buttons
        0x05, 0x09,  # Usage Page (Button)
        0x19, 0x01,  # Usage Minimum (0x01)
        0x29, 0x05,  # Usage Maximum (0x05)
        0x15, 0x00,  # Logical Minimum (0)
        0x25, 0x01,  # Logical Maximum (1)
        0x95, 0x05,  # Report Count (5)  Left, Right, Middle, Backward, Forward buttons 
        0x75, 0x01,  # Report Size (1)
        0x81, 0x02,  # Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
        0x95, 0x01,  # Report Count (1)
        0x75, 0x03,  # Report Size (3)  3 bit padding 
        0x81, 0x03,  # Input
        # Movement
        0x05, 0x01,        # Usage Page (Generic Desktop Ctrls)
        0x09, 0x30,        # Usage (X)
        0x09, 0x31,        # Usage (Y)
        0x15, 0x00,        # LOGICAL_MINIMUM (0)
        0x26, 0xFF, 0x7F,  # LOGICAL_MAXIMUM (32767)
        0x75, 0x10,        # REPORT_SIZE (16)
        0x95, 0x02,        # REPORT_COUNT (2)
        0x81, 0x02,        # Input (Data,Var,Rel,No Wrap,Linear,Preferred State,No Null Position)
        # Vertical wheel scroll [-127, 127]
        0x09, 0x38,   # Vertical wheel scroll [-127, 127]
        0x15, 0x81,   # Logical Minimum (-127)
        0x25, 0x7F,   # Logical Maximum (127)
        0x95, 0x01,   # Report Count (1)
        0x75, 0x08,   # Report Size (8)
        0x81, 0x06,   # Input (Data,Var,Rel,No Wrap,Linear,Preferred State,No Null Position)
        # Horizontal wheel scroll [-127, 127]
        0x05, 0x0c,   #USAGE_PAGE (Consumer Devices)
        0x0a, 0x38, 0x02,   # Horizontal scroll [-127, 127]
        0x15, 0x81,   # Logical Minimum (-127)
        0x25, 0x7F,   # Logical Maximum (127)
        0x95, 0x01,   # Report Count (1)
        0x75, 0x08,   # Report Size (8)
        0x81, 0x06,   # Input (Data,Var,Rel,No Wrap,Linear,Preferred State,No Null Position)
        #End Collection
        0xC0,         # End Collection
        0xC0,         # End Collection
    ))

class Mouse(HIDInterface):
        # A basic three button USB mouse HID interface
    def __init__(self, sw, sh, interface_str="MicroPython ABS Mouse"):
        super().__init__(
            ABS_MOUSE_DESC,
            protocol=ABS_MOUSE_DESC[1:2],
            interface_str=0x02,  #_INTERFACE_PROTOCOL_MOUSE = const(0x02)
        )
        self.sw=sw
        self.sh=sh
        self.report = bytearray(7)
        self.mx=0
        self.my=0
        self.mb=0
        self.mwx=0
        self.mwy=0
    
    def sendReport(self):
        if supervisor.runtime.usb_connected:
            cx = (32767 * self.mx) // self.sw # self.sw 
            cy = (32767 * self.my) // self.sh # self.sh
            self.report = struct.pack("<BHHbb",self.mb, cx, cy,self.mwy,self.mwx)
            super().send_report(self.report)
    def move(self, px, py):
        self.mx=px
        self.my=py
        self.sendReport()
        return
    def press(self, b):
        self.mb= self.mb | (1 << barrier_mouse_btn_map[b])  # Set bit at b of mb, bit locations= 0:LEFT 1:MIDDLE 2:RIGHT
        self.sendReport()
        return
    def release(self, b):
        self.mb = self.mb & ~(1 << barrier_mouse_btn_map[b])  # Reset bit at b of mb, bit locations= 0:LEFT 1:MIDDLE 2:RIGHT      
        self.sendReport()
        return
    def wheel(self, x, y):
        self.mwx=x
        self.mwy=y
        self.sendReport()
        #Reset Wheel values
        self.mwx=0
        self.mwy=0
        return



class Keyboard:
    def repeat(self, KeyId, KeyModifiers, KeyButton):
        print("[*] Event: Keyboard Repeat: ID=" + hex(KeyId) + " MOD=" +  hex(KeyModifiers) + " BTN=" +  hex(KeyButton))
        return     
    def press(self, KeyId, KeyModifiers, KeyButton):
        print("[*] Event: Keyboard Press: ID=" + hex(KeyId) + " MOD=" +  hex(KeyModifiers) + " BTN=" +  hex(KeyButton))
        return
    def release(self, KeyId, KeyModifiers, KeyButton):
        print("[*] Event: Keyboard Release: ID=" + hex(KeyId) + " MOD=" +  hex(KeyModifiers) + " BTN=" +  hex(KeyButton))
        return