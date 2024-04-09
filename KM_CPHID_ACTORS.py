import struct
import usb_hid
import KB_HID_MAP
from usb_hid import Device
import supervisor

barrier_mouse_btn_map = [ 
7,	# 0 None #7 will mean none
0,	# 1 LEFT
2,	# 2 MIDDLE
1,	# 3 RIGHT
3,	# 5 X
4,	# 6 X2
]

#find_device adafruit_hid block if device if USB is ready
def find_hid_device(
    devices: Sequence[object],
    *,
    usage_page: int,
    usage: int,
    timeout: int = None,
) -> object:
    if hasattr(devices, "send_report"):
        devices = [devices]  # type: ignore
    device = None
    for dev in devices:
        if (
            dev.usage_page == usage_page
            and dev.usage == usage
            and hasattr(dev, "send_report")
        ):
            device = dev
            break
    if device is None:
        raise ValueError("Could not find matching HID device.")
    
    return device
        
    

ABS_MOUSE_DEVICE = usb_hid.Device(
    report_descriptor=bytes((
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
    )),
    usage_page=1,
    usage=2,
    in_report_lengths=(7,), # Number of bytes in the send report
    # 1 byte for buttons, 2 bytes for x, 2 bytes for y, 1 byte for wheel
    out_report_lengths=(0,),
    report_ids=(11,),
)


class Mouse(object):

    def __init__(self, sw=1920, sh=1080):
        self.sw=sw
        self.sh=sh
        self._mouse_device = find_hid_device(usb_hid.devices, usage_page=0x1, usage=0x02,timeout=1)
        self.report = bytearray(7)
        self.mx=0
        self.my=0
        self.mb=0
        self.mwx=0
        self.mwy=0
        
    def setScreenSize(self, sw, sh):
        self.sw=sw
        self.sh=sh
            
    def sendReport(self):
        if supervisor.runtime.usb_connected:
            cx = (32767 * self.mx) // self.sw # self.sw 
            cy = (32767 * self.my) // self.sh # self.sh
            self.report = struct.pack("<BHHbb",self.mb, cx, cy,self.mwy,self.mwx)
            self._mouse_device.send_report(self.report)
            
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
    

    
KEYBOARD_DEVICE = usb_hid.Device(
    report_descriptor=bytes((
        0x05, 0x01,        # Usage Page (Generic Desktop)
        0x05, 0x01,        #   Usage Page (Generic Desktop Ctrls)
        0x09, 0x06,        #   Usage (Keyboard)
        0xA1, 0x01,        #   Collection (Application)
        0x85, 0x01,        #   Report ID (1)
        0x05, 0x07,        #   Usage Page (Kbrd/Keypad)
        0x19, 0xE0,        #   Usage Minimum (0xE0)
        0x29, 0xE7,        #   Usage Maximum (0xE7)
        0x15, 0x00,        #   Logical Minimum (0)
        0x25, 0x01,        #   Logical Maximum (1)
        0x75, 0x01,        #   Report Size (1)
        0x95, 0x08,        #   Report Count (8)
        0x81, 0x02,        #   Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
        0x95, 0x01,        #   Report Count (1)
        0x75, 0x08,        #   Report Size (8)
        0x81, 0x01,        #   Input (Const,Array,Abs,No Wrap,Linear,Preferred State,No Null Position)
        0x95, 0x05,        #   Report Count (5)
        0x75, 0x01,        #   Report Size (1)
        0x05, 0x08,        #   Usage Page (LEDs)
        0x19, 0x01,        #   Usage Minimum (Num Lock)
        0x29, 0x05,        #   Usage Maximum (Kana)
        0x91, 0x02,        #   Output (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position,Non-volatile)
        0x95, 0x01,        #   Report Count (1)
        0x75, 0x03,        #   Report Size (3)
        0x91, 0x01,        #   Output (Const,Array,Abs,No Wrap,Linear,Preferred State,No Null Position,Non-volatile)
        0x95, 0x06,        #   Report Count (6)
        0x75, 0x08,        #   Report Size (8)
        0x15, 0x00,        #   Logical Minimum (0)
        0x26, 0xFF, 0x00,  #   Logical Maximum (255)
        0x05, 0x07,        #   Usage Page (Kbrd/Keypad)
        0x19, 0x00,        #   Usage Minimum (0x00)
        0x2A, 0xFF, 0x00,  #   Usage Maximum (0xFF)
        0x81, 0x00,        #   Input (Data,Array,Abs,No Wrap,Linear,Preferred State,No Null Position)
        0xC0,              #   End Collection
    )),
    usage_page=1,
    usage=6,
    in_report_lengths=(8,), # Number of bytes in the send report
    out_report_lengths=(1,),
    report_ids=(1,),
)    
    
class Keyboard(object):
    def __init__(self):
        self.keyboard_device = find_hid_device(usb_hid.devices, usage_page=0x1, usage=0x06, timeout=1)
        self._keyReport = {
            'modifiers': 0,
            'keys': [0] * 6
        }

        # No keyboard LEDs on.
        self.led_status = b"\x00"
        
    def sendReport(self, report):
        if supervisor.runtime.usb_connected:
            report = struct.pack('<BB6B', self._keyReport['modifiers'], 0, *self._keyReport['keys'])
            self.keyboard_device.send_report(report)
        
    def pressRaw(self, k):
        if k >= 0xE0 and k < 0xE8:
            # it's a modifier key
            self._keyReport['modifiers'] |= (1 << (k & 0x0F))
        elif k and k < 0xA5:
            # Add k to the key report only if it's not already present
            # and if there is an empty slot.
            if k not in self._keyReport['keys']:
                empty_slot=None
                for i in range(len(self._keyReport['keys'])):
                    if self._keyReport['keys'][i] == 0x00:
                        empty_slot = i
                        break
                if empty_slot is not None:
                    self._keyReport['keys'][empty_slot] = k
                else:
                    return 0
        else:
            # not a modifier and not a key
            return 0

        self.sendReport(self._keyReport)
        return 1

    def releaseRaw(self, k):
        if k >= 0xE0 and k < 0xE8:
            # it's a modifier key
            self._keyReport['modifiers'] &= ~(1 << (k & 0x0F))
        elif k and k < 0xA5:
            # Test the key report to see if k is present. Clear it if it exists.
            # Check all positions in case the key is present more than once (which it shouldn't be)
            for i in range(len(self._keyReport['keys'])):
                if self._keyReport['keys'][i] == k:
                    self._keyReport['keys'][i] = 0x00
        else:
            # not a modifier and not a key
            return 0

        self.sendReport(self._keyReport)
        return 1    

    def tapRaw(self, k):
        self.pressRaw(k)
        self.releaseRaw(k)
        
    def get_led_states(self):
        """Returns the last received report"""
        # get_last_received_report() returns None when nothing was received
        led_report = self.keyboard_device.get_last_received_report()
        if led_report is not None:
            self.led_status = led_report
     
        return {
            'LED_NUM_LOCK':    bool(self.led_status[0] & KB_HID_MAP.LEDS.NUM_LOCK),
            'LED_CAPS_LOCK':   bool(self.led_status[0] & KB_HID_MAP.LEDS.CAPS_LOCK),
            'LED_SCROLL_LOCK': bool(self.led_status[0] & KB_HID_MAP.LEDS.SCROLL_LOCK)
            }
    
    def syncLocks(self, KeyModifiers):
        led_states = self.get_led_states()
        if (((KB_HID_MAP.MASK_MOD.LED_CAPS_LOCK & KeyModifiers)>0) != led_states['LED_CAPS_LOCK']):
            self.tapRaw(KB_HID_MAP.KEYS.KEY_CAPS_LOCK)
        if (((KB_HID_MAP.MASK_MOD.LED_NUM_LOCK & KeyModifiers)>0) != led_states['LED_NUM_LOCK']):
            self.tapRaw(KB_HID_MAP.KEYS.KEY_NUM_LOCK)
        if (((KB_HID_MAP.MASK_MOD.LED_SCROLL_LOCK & KeyModifiers)>0) != led_states['LED_SCROLL_LOCK']):
            self.tapRaw(KB_HID_MAP.KEYS.KEY_SCROLL_LOCK)
        return
    
    def actionKey(self, KeyId, KeyModifiers, KeyButton, Action):
        
        act_KeyId=KB_HID_MAP.KEYS.KEY_NONE
        if KeyId >= 0xEF00 and KeyId <= 0xEFFF:
            act_KeyId=KB_HID_MAP.MAP_EXT[KeyId-0xEF00]
        elif KeyId >= 0x00 and KeyId <= 0x7F:
            act_KeyId=KB_HID_MAP.MAP_ASCII[KeyId]
        
        if (Action==1 and act_KeyId!=KB_HID_MAP.KEYS.KEY_CAPS_LOCK and act_KeyId!=KB_HID_MAP.KEYS.KEY_NUM_LOCK and act_KeyId!=KB_HID_MAP.KEYS.KEY_SCROLL_LOCK):
            self.syncLocks(KeyModifiers)
        

        
        if(act_KeyId!=KB_HID_MAP.KEYS.KEY_NONE):
            if(Action==1): #1:Press  0:Release
                self.pressRaw(act_KeyId)
            else:
                self.releaseRaw(act_KeyId)
          
        if (Action==0 and act_KeyId==KB_HID_MAP.KEYS.KEY_CAPS_LOCK or act_KeyId==KB_HID_MAP.KEYS.KEY_NUM_LOCK or act_KeyId==KB_HID_MAP.KEYS.KEY_SCROLL_LOCK):
            self.syncLocks(KeyModifiers)
        
        return
    def repeat(self, KeyId, KeyModifiers, KeyButton):
        #Repeat not required when HID is used
        return    
    def press(self, KeyId, KeyModifiers, KeyButton):
        self.actionKey(KeyId, KeyModifiers, KeyButton, 1)
        return
    def release(self, KeyId, KeyModifiers, KeyButton):
        self.actionKey(KeyId, KeyModifiers, KeyButton, 0)
        return
