import struct
import KB_HID_MAP
   
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
    def __init__(self, ser, sw, sh):
        self.ser=ser
        self.sw=sw
        self.sh=sh
        
    def setScreenSize(self, sw, sh):
        self.sw=sw
        self.sh=sh
                    
    def send_mouse_data(self):
        data_out=b""
        HEAD = b"\x57\xab"  # Frame header
        ADDR = 0X00  # Address
        CMD = 0X04   # Command
        LEN = 7   # Data Length
        DATA0 = 0X02 # first byte: must be 0x02;
        cx = (4096 * self.mx) // self.sw 
        cy = (4096 * self.my) // self.sh
        data_out = struct.pack('<2sBBBBBHHb',HEAD,ADDR,CMD,LEN,DATA0,self.mb,cx,cy,self.mwy)
        data_out += struct.pack('B', sum(data_out) % 256)
        
        '''DO NOT WAIT OR MOUSE WILL LAG
        while self.ser.read():
            pass
        '''    
        self.ser.write(data_out)
        
        '''DO NOT WAIT OR MOUSE WILL LAG
        data_in = b""
        while len(data_in) < 7:
            chunk = self.ser.read(7 - len(data_in))
            if chunk is not None:
                data_in += chunk
        print(data_in)
        '''
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
 

class Keyboard(object):
    def __init__(self, ser):
        self.ser=ser
        self._keyReport = {
            'modifiers': 0,
            'keys': [0] * 6
        }

    def sendReport(self, report):
        
        # Placeholder for the function to send the report       
        data_out=b""
        HEAD = b"\x57\xab"  # Frame header
        ADDR = 0X00  # Address
        CMD = 0X02   # Command
        LEN = 8   # Data Length
        DATA1=0X00
        data_out = struct.pack('<2sBBBBB6B', HEAD, ADDR, CMD, LEN, self._keyReport['modifiers'], DATA1, *self._keyReport['keys'])
        data_out += struct.pack('B', sum(data_out) % 256)
        
        while self.ser.read():
            pass
        self.ser.write(data_out)
        data_in = b""
        while len(data_in) < 7:
            chunk = self.ser.read(7 - len(data_in))
            if chunk is not None:
                data_in += chunk
        
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

    def get_lock_states(self):
        # Placeholder for the function to send the report       
        data_out=b""
        HEAD = b"\x57\xab"  # Frame header
        ADDR = 0X00  # Address
        CMD = 0X01   # Command
        LEN = 0   # Data Length
        data_out = struct.pack('<2sBBB', HEAD, ADDR, CMD, LEN)
        data_out += struct.pack('B', sum(data_out) % 256)
        
        while self.ser.read():
            pass
        self.ser.write(data_out)
        data_in = b""
        while len(data_in) < 14:
            chunk = self.ser.read(14 - len(data_in))
            if chunk is not None:
                data_in += chunk

        return {
            'LED_NUM_LOCK': data_in[7] & 0b00000001,
            'LED_CAPS_LOCK': (data_in[7] & 0b00000010) >> 1,
            'LED_SCROLL_LOCK': (data_in[7] & 0b00000100) >> 2
            }
    
    def releaseAll(self):     
        self._keyReport['keys'][0]=0
        self._keyReport['keys'][1]=0
        self._keyReport['keys'][2]=0
        self._keyReport['keys'][3]=0
        self._keyReport['keys'][4]=0
        self._keyReport['keys'][5]=0
        self._keyReport['modifiers']=0
        self.sendReport(self._keyReport)

    def syncLocks(self, KeyModifiers):
        lock_states = self.get_lock_states()
        if (((KB_HID_MAP.MASK_MOD.LED_CAPS_LOCK & KeyModifiers)>0) != lock_states['LED_CAPS_LOCK']):
            self.tapRaw(KB_HID_MAP.KEYS.KEY_CAPS_LOCK)
        if (((KB_HID_MAP.MASK_MOD.LED_NUM_LOCK & KeyModifiers)>0) != lock_states['LED_NUM_LOCK']):
            self.tapRaw(KB_HID_MAP.KEYS.KEY_NUM_LOCK)
        if (((KB_HID_MAP.MASK_MOD.LED_SCROLL_LOCK & KeyModifiers)>0) != lock_states['LED_SCROLL_LOCK']):
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
 