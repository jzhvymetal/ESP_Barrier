import struct
   
barrier_mouse_btn_map = [ 
7,	# 0 None #7 will mean none
0,	# 1 LEFT
2,	# 2 MIDDLE
1,	# 3 RIGHT
3,	# 5 X
4,	# 6 X2
]    




class Mouse(object):
    def __init__(self, ser):
        self.ser=ser    
    mx=0
    my=0
    mb=0
    mwx=0
    mwy=0
    sw=1920
    sh=1080
    
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

hid_ascii_map= [
 0X00,      # NUL, HEX: 00, Decimal: 0
 0X00,      # SOH, HEX: 01, Decimal: 1
 0X00,      # STX, HEX: 02, Decimal: 2
 0X00,      # ETX, HEX: 03, Decimal: 3
 0X00,      # EOT, HEX: 04, Decimal: 4
 0X00,      # ENQ, HEX: 05, Decimal: 5
 0X00,      # ACK, HEX: 06, Decimal: 6
 0X00,      # BEL, HEX: 07, Decimal: 7
 0X2A,      # BS, HEX: 08, Decimal: 8
 0X2B,      # TAB, HEX: 09, Decimal: 9
 0X00,      # LF, HEX: 0A, Decimal: 10
 0X00,      # VT, HEX: 0B, Decimal: 11
 0X00,      # FF, HEX: 0C, Decimal: 12
 0X00,      # CR, HEX: 0D, Decimal: 13
 0X00,      # SO, HEX: 0E, Decimal: 14
 0X00,      # SI, HEX: 0F, Decimal: 15
 0X00,      # DLE, HEX: 10, Decimal: 16
 0X00,      # DC1, HEX: 11, Decimal: 17
 0X00,      # DC2, HEX: 12, Decimal: 18
 0X00,      # DC3, HEX: 13, Decimal: 19
 0X00,      # DC4, HEX: 14, Decimal: 20
 0X00,      # NAK, HEX: 15, Decimal: 21
 0X00,      # SYN, HEX: 16, Decimal: 22
 0X00,      # ETB, HEX: 17, Decimal: 23
 0X00,      # CAN, HEX: 18, Decimal: 24
 0X00,      # EM, HEX: 19, Decimal: 25
 0X00,      # SUB, HEX: 1A, Decimal: 26
 0X00,      # ESC, HEX: 1B, Decimal: 27
 0X00,      # FS, HEX: 1C, Decimal: 28
 0X00,      # GS, HEX: 1D, Decimal: 29
 0X00,      # RS, HEX: 1E, Decimal: 30
 0X00,      # US, HEX: 1F, Decimal: 31
 0X2C,      # SPACE, HEX: 20, Decimal: 32
 0X1E,      # !, HEX: 21, Decimal: 33
 0X41,      # ", HEX: 22, Decimal: 34
 0X20,      # #, HEX: 23, Decimal: 35
 0X21,      # $, HEX: 24, Decimal: 36
 0X22,      # %, HEX: 25, Decimal: 37
 0X24,      # &, HEX: 26, Decimal: 38
 0X41,      # ', HEX: 27, Decimal: 39
 0X26,      # (, HEX: 28, Decimal: 40
 0X27,      # ), HEX: 29, Decimal: 41
 0X25,      # *, HEX: 2A, Decimal: 42
 0X2E,      # +, HEX: 2B, Decimal: 43
 0X36,      # ,, HEX: 2C, Decimal: 44
 0X2D,      # -, HEX: 2D, Decimal: 45
 0X37,      # ., HEX: 2E, Decimal: 46
 0X38,      # /, HEX: 2F, Decimal: 47
 0X27,      # 0, HEX: 30, Decimal: 48
 0X1E,      # 1, HEX: 31, Decimal: 49
 0X1F,      # 2, HEX: 32, Decimal: 50
 0X20,      # 3, HEX: 33, Decimal: 51
 0X21,      # 4, HEX: 34, Decimal: 52
 0X22,      # 5, HEX: 35, Decimal: 53
 0X23,      # 6, HEX: 36, Decimal: 54
 0X24,      # 7, HEX: 37, Decimal: 55
 0X25,      # 8, HEX: 38, Decimal: 56
 0X26,      # 9, HEX: 39, Decimal: 57
 0X40,      # :, HEX: 3A, Decimal: 58
 0X41,      # ;, HEX: 3B, Decimal: 59
 0X36,      # <, HEX: 3C, Decimal: 60
 0X2E,      # =, HEX: 3D, Decimal: 61
 0X37,      # >, HEX: 3E, Decimal: 62
 0X38,      # ?, HEX: 3F, Decimal: 63
 0X1F,      # @, HEX: 40, Decimal: 64
 0X04,      # A, HEX: 41, Decimal: 65
 0X05,      # B, HEX: 42, Decimal: 66
 0X06,      # C, HEX: 43, Decimal: 67
 0X07,      # D, HEX: 44, Decimal: 68
 0X08,      # E, HEX: 45, Decimal: 69
 0X09,      # F, HEX: 46, Decimal: 70
 0X0A,      # G, HEX: 47, Decimal: 71
 0X0B,      # H, HEX: 48, Decimal: 72
 0X0C,      # I, HEX: 49, Decimal: 73
 0X0D,      # J, HEX: 4A, Decimal: 74
 0X0E,      # K, HEX: 4B, Decimal: 75
 0X0F,      # L, HEX: 4C, Decimal: 76
 0X10,      # M, HEX: 4D, Decimal: 77
 0X11,      # N, HEX: 4E, Decimal: 78
 0X12,      # O, HEX: 4F, Decimal: 79
 0X13,      # P, HEX: 50, Decimal: 80
 0X14,      # Q, HEX: 51, Decimal: 81
 0X15,      # R, HEX: 52, Decimal: 82
 0X16,      # S, HEX: 53, Decimal: 83
 0X17,      # T, HEX: 54, Decimal: 84
 0X18,      # U, HEX: 55, Decimal: 85
 0X19,      # V, HEX: 56, Decimal: 86
 0X1A,      # W, HEX: 57, Decimal: 87
 0X1B,      # X, HEX: 58, Decimal: 88
 0X1C,      # Y, HEX: 59, Decimal: 89
 0X1D,      # Z, HEX: 5A, Decimal: 90
 0X2F,      # [, HEX: 5B, Decimal: 91
 0X31,      # \, HEX: 5C, Decimal: 92
 0X30,      # ], HEX: 5D, Decimal: 93
 0X23,      # ^, HEX: 5E, Decimal: 94
 0X2D,      # _, HEX: 5F, Decimal: 95
 0X35,      # `, HEX: 60, Decimal: 96
 0X04,      # a, HEX: 61, Decimal: 97
 0X05,      # b, HEX: 62, Decimal: 98
 0X06,      # c, HEX: 63, Decimal: 99
 0X07,      # d, HEX: 64, Decimal: 100
 0X08,      # e, HEX: 65, Decimal: 101
 0X09,      # f, HEX: 66, Decimal: 102
 0X0A,      # g, HEX: 67, Decimal: 103
 0X0B,      # h, HEX: 68, Decimal: 104
 0X0C,      # i, HEX: 69, Decimal: 105
 0X0D,      # j, HEX: 6A, Decimal: 106
 0X0E,      # k, HEX: 6B, Decimal: 107
 0X0F,      # l, HEX: 6C, Decimal: 108
 0X10,      # m, HEX: 6D, Decimal: 109
 0X11,      # n, HEX: 6E, Decimal: 110
 0X12,      # o, HEX: 6F, Decimal: 111
 0X13,      # p, HEX: 70, Decimal: 112
 0X14,      # q, HEX: 71, Decimal: 113
 0X15,      # r, HEX: 72, Decimal: 114
 0X16,      # s, HEX: 73, Decimal: 115
 0X17,      # t, HEX: 74, Decimal: 116
 0X18,      # u, HEX: 75, Decimal: 117
 0X19,      # v, HEX: 76, Decimal: 118
 0X1A,      # w, HEX: 77, Decimal: 119
 0X1B,      # x, HEX: 78, Decimal: 120
 0X1C,      # y, HEX: 79, Decimal: 121
 0X1D,      # z, HEX: 7A, Decimal: 122
 0X2F,      # {, HEX: 7B, Decimal: 123
 0X31,      # |, HEX: 7C, Decimal: 124
 0X30,      # }, HEX: 7D, Decimal: 125
 0X35,      # ~, HEX: 7E, Decimal: 126
 0X4C       # DEL, HEX: 7F, Decimal: 127
]

class HID_KEYS:
    
    KEY_NONE =  0X00
    # Modifiers
    KEY_LEFT_CTRL =  0XE0
    KEY_LEFT_SHIFT =  0XE1
    KEY_LEFT_ALT =  0XE2
    KEY_LEFT_GUI =  0XE3
    KEY_RIGHT_CTRL =  0XE4
    KEY_RIGHT_SHIFT =  0XE5
    KEY_RIGHT_ALT =  0XE6
    KEY_RIGHT_GUI =  0XE7

    # Misc keys
    KEY_UP_ARROW =  0X52
    KEY_DOWN_ARROW =  0X51
    KEY_LEFT_ARROW =  0X50
    KEY_RIGHT_ARROW =  0X4F
    KEY_BACKSPACE =  0X2A
    KEY_TAB =  0X2B
    KEY_RETURN =  0X28
    KEY_MENU =  0X65
    KEY_ESC =  0X29
    KEY_INSERT =  0X49
    KEY_DELETE =  0X4C
    KEY_PAGE_UP =  0X61
    KEY_PAGE_DOWN =  0X5B
    KEY_HOME =  0X4A
    KEY_END =  0X4D
    KEY_CAPS_LOCK =  0X39
    KEY_PRINT_SCREEN =  0X46  # Print Screen / SysRq
    KEY_SCROLL_LOCK =  0X47
    KEY_PAUSE =  0X48  # Pause / Break

    # Numeric keypad
    KEY_NUM_LOCK =  0X53
    KEY_KP_SLASH = 0X54
    KEY_KP_ASTERISK = 0X55
    KEY_KP_MINUS = 0X56
    KEY_KP_PLUS = 0X57
    KEY_KP_ENTER =  0X58
    KEY_KP_1 = 0X59
    KEY_KP_2 = 0X5A
    KEY_KP_3 = 0X5B
    KEY_KP_4 = 0X5C
    KEY_KP_5 = 0X5D
    KEY_KP_6 = 0X5E
    KEY_KP_7 = 0X5F
    KEY_KP_8 = 0X60
    KEY_KP_9 = 0X61
    KEY_KP_0 = 0X62
    KEY_KP_DOT = 0X63

    # Function keys
    KEY_F1 =  0X3A
    KEY_F2 =  0X3B
    KEY_F3 =  0X3C
    KEY_F4 =  0X3D
    KEY_F5 =  0X3E
    KEY_F6 =  0X3F
    KEY_F7 =  0X40
    KEY_F8 =  0X41
    KEY_F9 =  0X42
    KEY_F10 =  0X43
    KEY_F11 =  0X44
    KEY_F12 = 0X45
    KEY_F13 =  0X00
    KEY_F14 =  0X00
    KEY_F15 =  0X00
    KEY_F16 =  0X00
    KEY_F17 =  0X00
    KEY_F18 =  0X00
    KEY_F19 =  0X00
    KEY_F20 =  0X00

barrier_keyboard_key_map =[
    HID_KEYS.KEY_NONE,           # EF00
    HID_KEYS.KEY_NONE,           # EF01
    HID_KEYS.KEY_NONE,           # EF02
    HID_KEYS.KEY_NONE,           # EF03
    HID_KEYS.KEY_NONE,           # EF04
    HID_KEYS.KEY_NONE,           # EF05
    HID_KEYS.KEY_NONE,           # EF06
    HID_KEYS.KEY_NONE,           # EF07
    HID_KEYS.KEY_BACKSPACE,      # EF08 - kKeyBackSpace: back space, back char
    HID_KEYS.KEY_TAB,            # EF09 - kKeyTab
    HID_KEYS.KEY_NONE,           # EF0A
    HID_KEYS.KEY_NONE,           # EF0B
    HID_KEYS.KEY_NONE,           # EF0C
    HID_KEYS.KEY_RETURN,         # EF0D - kKeyReturn: Return, enter
    HID_KEYS.KEY_NONE,           # EF0E
    HID_KEYS.KEY_NONE,           # EF0F
    HID_KEYS.KEY_NONE,           # EF10
    HID_KEYS.KEY_NONE,           # EF11
    HID_KEYS.KEY_NONE,           # EF12
    HID_KEYS.KEY_PAUSE,          # EF13 - kKeyPause: Pause, hold
    HID_KEYS.KEY_SCROLL_LOCK,    # EF14 - kKeyScrollLock
    HID_KEYS.KEY_NONE,           # EF15
    HID_KEYS.KEY_NONE,           # EF16
    HID_KEYS.KEY_NONE,           # EF17
    HID_KEYS.KEY_NONE,           # EF18
    HID_KEYS.KEY_NONE,           # EF19
    HID_KEYS.KEY_NONE,           # EF1A
    HID_KEYS.KEY_ESC,            # EF1B - kKeyEscape
    HID_KEYS.KEY_NONE,           # EF1C
    HID_KEYS.KEY_NONE,           # EF1D
    HID_KEYS.KEY_NONE,           # EF1E
    HID_KEYS.KEY_NONE,           # EF1F
    HID_KEYS.KEY_NONE,           # EF20
    HID_KEYS.KEY_NONE,           # EF21
    HID_KEYS.KEY_NONE,           # EF22
    HID_KEYS.KEY_NONE,           # EF23
    HID_KEYS.KEY_NONE,           # EF24
    HID_KEYS.KEY_NONE,           # EF25
    HID_KEYS.KEY_NONE,           # EF26
    HID_KEYS.KEY_NONE,           # EF27
    HID_KEYS.KEY_NONE,           # EF28
    HID_KEYS.KEY_NONE,           # EF29
    HID_KEYS.KEY_NONE,           # EF2A
    HID_KEYS.KEY_NONE,           # EF2B
    HID_KEYS.KEY_NONE,           # EF2C
    HID_KEYS.KEY_NONE,           # EF2D
    HID_KEYS.KEY_NONE,           # EF2E
    HID_KEYS.KEY_NONE,           # EF2F
    HID_KEYS.KEY_NONE,           # EF30
    HID_KEYS.KEY_NONE,           # EF31
    HID_KEYS.KEY_NONE,           # EF32
    HID_KEYS.KEY_NONE,           # EF33
    HID_KEYS.KEY_NONE,           # EF34
    HID_KEYS.KEY_NONE,           # EF35
    HID_KEYS.KEY_NONE,           # EF36
    HID_KEYS.KEY_NONE,           # EF37
    HID_KEYS.KEY_NONE,           # EF38
    HID_KEYS.KEY_NONE,           # EF39
    HID_KEYS.KEY_NONE,           # EF3A
    HID_KEYS.KEY_NONE,           # EF3B
    HID_KEYS.KEY_NONE,           # EF3C
    HID_KEYS.KEY_NONE,           # EF3D
    HID_KEYS.KEY_NONE,           # EF3E
    HID_KEYS.KEY_NONE,           # EF3F
    HID_KEYS.KEY_NONE,           # EF40
    HID_KEYS.KEY_NONE,           # EF41
    HID_KEYS.KEY_NONE,           # EF42
    HID_KEYS.KEY_NONE,           # EF43
    HID_KEYS.KEY_NONE,           # EF44
    HID_KEYS.KEY_NONE,           # EF45
    HID_KEYS.KEY_NONE,           # EF46
    HID_KEYS.KEY_NONE,           # EF47
    HID_KEYS.KEY_NONE,           # EF48
    HID_KEYS.KEY_NONE,           # EF49
    HID_KEYS.KEY_NONE,           # EF4A
    HID_KEYS.KEY_NONE,           # EF4B
    HID_KEYS.KEY_NONE,           # EF4C
    HID_KEYS.KEY_NONE,           # EF4D
    HID_KEYS.KEY_NONE,           # EF4E
    HID_KEYS.KEY_NONE,           # EF4F
    HID_KEYS.KEY_HOME,           # EF50 - kKeyHome
    HID_KEYS.KEY_LEFT_ARROW,     # EF51 - kKeyLeft: Move left, left arrow
    HID_KEYS.KEY_UP_ARROW,       # EF52 - kKeyUp: Move up, up arrow
    HID_KEYS.KEY_RIGHT_ARROW,    # EF53 - kKeyRight: Move right, right arrow
    HID_KEYS.KEY_DOWN_ARROW,     # EF54 - kKeyDown: Move down, down arrow
    HID_KEYS.KEY_PAGE_UP,        # EF55 - kKeyPageUp
    HID_KEYS.KEY_PAGE_DOWN,      # EF56 - kKeyPageDown
    HID_KEYS.KEY_END,            # EF57 - kKeyEnd: EOL
    HID_KEYS.KEY_HOME,           # EF58 - kKeyBegin: BOL
    HID_KEYS.KEY_NONE,           # EF59
    HID_KEYS.KEY_NONE,           # EF5A
    HID_KEYS.KEY_NONE,           # EF5B
    HID_KEYS.KEY_NONE,           # EF5C
    HID_KEYS.KEY_NONE,           # EF5D
    HID_KEYS.KEY_NONE,           # EF5E
    HID_KEYS.KEY_NONE,           # EF5F
    HID_KEYS.KEY_NONE,           # EF60 - kKeySelect: Select, mark
    HID_KEYS.KEY_PRINT_SCREEN,   # EF61 - kKeyPrint
    HID_KEYS.KEY_NONE,           # EF62
    HID_KEYS.KEY_INSERT,         # EF63 - kKeyInsert: Insert, insert here
    HID_KEYS.KEY_NONE,           # EF64
    HID_KEYS.KEY_NONE,           # EF65 - kKeyUndo: Undo, oops
    HID_KEYS.KEY_NONE,           # EF66 - kKeyRedo: Redo, again
    HID_KEYS.KEY_MENU,           # EF67 - kKeyMenu
    HID_KEYS.KEY_NONE,           # EF68
    HID_KEYS.KEY_NONE,           # EF69
    HID_KEYS.KEY_NONE,           # EF6A
    HID_KEYS.KEY_NONE,           # EF6B
    HID_KEYS.KEY_NONE,           # EF6C
    HID_KEYS.KEY_NONE,           # EF6D
    HID_KEYS.KEY_NONE,           # EF6E
    HID_KEYS.KEY_NONE,           # EF6F
    HID_KEYS.KEY_NONE,           # EF70
    HID_KEYS.KEY_NONE,           # EF71
    HID_KEYS.KEY_NONE,           # EF72
    HID_KEYS.KEY_NONE,           # EF73
    HID_KEYS.KEY_NONE,           # EF74
    HID_KEYS.KEY_NONE,           # EF75
    HID_KEYS.KEY_NONE,           # EF76
    HID_KEYS.KEY_NONE,           # EF77
    HID_KEYS.KEY_NONE,           # EF78
    HID_KEYS.KEY_NONE,           # EF79
    HID_KEYS.KEY_NONE,           # EF7A
    HID_KEYS.KEY_NONE,           # EF7B
    HID_KEYS.KEY_NONE,           # EF7C
    HID_KEYS.KEY_NONE,           # EF7D
    HID_KEYS.KEY_NONE,           # EF7E - kKeyAltGr: Character set switch
    HID_KEYS.KEY_NUM_LOCK,       # EF7F - kKeyNumLock
    HID_KEYS.KEY_NONE,           # EF80
    HID_KEYS.KEY_NONE,           # EF81
    HID_KEYS.KEY_NONE,           # EF82
    HID_KEYS.KEY_NONE,           # EF83
    HID_KEYS.KEY_NONE,           # EF84
    HID_KEYS.KEY_NONE,           # EF85
    HID_KEYS.KEY_NONE,           # EF86
    HID_KEYS.KEY_NONE,           # EF87
    HID_KEYS.KEY_NONE,           # EF88
    HID_KEYS.KEY_NONE,           # EF89
    HID_KEYS.KEY_TAB,            # EF8A - kKeyKP_Tab
    HID_KEYS.KEY_NONE,           # EF8B
    HID_KEYS.KEY_NONE,           # EF8C
    HID_KEYS.KEY_KP_ENTER,       # EF8D - kKeyKP_Enter: enter
    HID_KEYS.KEY_NONE,           # EF8E
    HID_KEYS.KEY_NONE,           # EF8F
    HID_KEYS.KEY_NONE,           # EF90
    HID_KEYS.KEY_NONE,           # EF91
    HID_KEYS.KEY_NONE,           # EF92
    HID_KEYS.KEY_NONE,           # EF93
    HID_KEYS.KEY_NONE,           # EF94
    HID_KEYS.KEY_HOME,           # EF95 - NumLock_OFF
    HID_KEYS.KEY_LEFT_ARROW,     # EF96 - NumLock_OFF
    HID_KEYS.KEY_UP_ARROW,       # EF97 - NumLock_OFF
    HID_KEYS.KEY_RIGHT_ARROW,    # EF98 - NumLock_OFF
    HID_KEYS.KEY_DOWN_ARROW,     # EF99 - NumLock_OFF
    HID_KEYS.KEY_PAGE_UP,        # EF9A - NumLock_OFF
    HID_KEYS.KEY_PAGE_DOWN,      # EF9B - NumLock_OFF
    HID_KEYS.KEY_NONE,           # EF9C
    HID_KEYS.KEY_NONE,           # EF9D
    HID_KEYS.KEY_INSERT,         # EF9E - NumLock_OFF
    HID_KEYS.KEY_DELETE,         # EF9F - NumLock_OFF
    HID_KEYS.KEY_NONE,           # EFA0
    HID_KEYS.KEY_NONE,           # EFA1
    HID_KEYS.KEY_NONE,           # EFA2
    HID_KEYS.KEY_NONE,           # EFA3
    HID_KEYS.KEY_NONE,           # EFA4
    HID_KEYS.KEY_NONE,           # EFA5
    HID_KEYS.KEY_NONE,           # EFA6
    HID_KEYS.KEY_NONE,           # EFA7
    HID_KEYS.KEY_NONE,           # EFA8
    HID_KEYS.KEY_NONE,           # EFA9 
    HID_KEYS.KEY_KP_ASTERISK,    # EFAA - kKeyKP_Multiply
    HID_KEYS.KEY_KP_PLUS,        # EFAB - kKeyKP_Add
    HID_KEYS.KEY_NONE,           # EFAC - kKeyKP_Separator: separator, often comma
    HID_KEYS.KEY_KP_MINUS,       # EFAD - kKeyKP_Subtract
    HID_KEYS.KEY_KP_DOT,         # EFAE - kKeyKP_Decimal
    HID_KEYS.KEY_KP_SLASH,       # EFAF - kKeyKP_Divide
    HID_KEYS.KEY_KP_0,           # EFB0 - kKeyKP_0
    HID_KEYS.KEY_KP_1,           # EFB1 - kKeyKP_1
    HID_KEYS.KEY_KP_2,           # EFB2 - kKeyKP_2
    HID_KEYS.KEY_KP_3,           # EFB3 - kKeyKP_3
    HID_KEYS.KEY_KP_4,           # EFB4 - kKeyKP_4
    HID_KEYS.KEY_KP_5,           # EFB5 - kKeyKP_5
    HID_KEYS.KEY_KP_6,           # EFB6 - kKeyKP_6
    HID_KEYS.KEY_KP_7,           # EFB7 - kKeyKP_7
    HID_KEYS.KEY_KP_8,           # EFB8 - kKeyKP_8
    HID_KEYS.KEY_KP_9,           # EFB9 - kKeyKP_9
    HID_KEYS.KEY_NONE,           # EFBA 
    HID_KEYS.KEY_NONE,           # EFBB
    HID_KEYS.KEY_NONE,           # EFBC
    HID_KEYS.KEY_NONE,           # EFBD - kKeyKP_Equal: equals
    HID_KEYS.KEY_F1,             # EFBE - kKeyF1
    HID_KEYS.KEY_F2,             # EFBF - kKeyF2
    HID_KEYS.KEY_F3,             # EFC0 - kKeyF3
    HID_KEYS.KEY_F4,             # EFC1 - kKeyF4
    HID_KEYS.KEY_F5,             # EFC2 - kKeyF5
    HID_KEYS.KEY_F6,             # EFC3 - kKeyF6
    HID_KEYS.KEY_F7,             # EFC4 - kKeyF7
    HID_KEYS.KEY_F8,             # EFC5 - kKeyF8
    HID_KEYS.KEY_F9,             # EFC6 - kKeyF9
    HID_KEYS.KEY_F10,            # EFC7 - kKeyF10
    HID_KEYS.KEY_F11,            # EFC8 - kKeyF11
    HID_KEYS.KEY_F12,            # EFC9 - kKeyF12
    HID_KEYS.KEY_F13,            # EFCA - kKeyF13
    HID_KEYS.KEY_F14,            # EFCB - kKeyF14
    HID_KEYS.KEY_F15,            # EFCC - kKeyF15
    HID_KEYS.KEY_F16,            # EFCD - kKeyF16
    HID_KEYS.KEY_F17,            # EFCE - kKeyF17
    HID_KEYS.KEY_F18,            # EFCF - kKeyF18
    HID_KEYS.KEY_F19,            # EFD0 - kKeyF19
    HID_KEYS.KEY_F20,            # EFD1 - kKeyF20
    HID_KEYS.KEY_NONE,           # EFD2 - kKeyF21
    HID_KEYS.KEY_NONE,           # EFD3 - kKeyF22
    HID_KEYS.KEY_NONE,           # EFD4 - kKeyF23
    HID_KEYS.KEY_NONE,           # EFD5 - kKeyF24
    HID_KEYS.KEY_NONE,           # EFD6 - kKeyF25
    HID_KEYS.KEY_NONE,           # EFD7 - kKeyF26
    HID_KEYS.KEY_NONE,           # EFD8 - kKeyF27
    HID_KEYS.KEY_NONE,           # EFD9 - kKeyF28
    HID_KEYS.KEY_NONE,           # EFDA - kKeyF29
    HID_KEYS.KEY_NONE,           # EFDB - kKeyF30
    HID_KEYS.KEY_NONE,           # EFDC - kKeyF31
    HID_KEYS.KEY_NONE,           # EFDD - kKeyF32
    HID_KEYS.KEY_NONE,           # EFDE - kKeyF33
    HID_KEYS.KEY_NONE,           # EFDF - kKeyF34
    HID_KEYS.KEY_NONE,           # EFE0 - kKeyF35
    HID_KEYS.KEY_LEFT_SHIFT,     # EFE1 - kKeyShift_L: Left shift
    HID_KEYS.KEY_RIGHT_SHIFT,    # EFE2 - kKeyShift_R: Right shift
    HID_KEYS.KEY_LEFT_CTRL,      # EFE3 - kKeyControl_L: Left control
    HID_KEYS.KEY_RIGHT_CTRL,     # EFE4 - kKeyControl_R: Right control
    HID_KEYS.KEY_CAPS_LOCK,      # EFE5 - kKeyCapsLock: Caps lock
    HID_KEYS.KEY_NONE,           # EFE6 - kKeyShiftLock: Shift lock
    HID_KEYS.KEY_NONE,           # EFE7 - kKeyMeta_L: Left meta
    HID_KEYS.KEY_NONE,           # EFE8 - kKeyMeta_R: Right meta
    HID_KEYS.KEY_LEFT_ALT,       # EFE9 - kKeyAlt_L: Left alt
    HID_KEYS.KEY_RIGHT_ALT,      # EFEA - kKeyAlt_R: Right alt
    HID_KEYS.KEY_LEFT_GUI,       # EFEB - kKeySuper_L: Left super
    HID_KEYS.KEY_RIGHT_GUI,      # EFEC - kKeySuper_R: Right super
    HID_KEYS.KEY_NONE,           # EFED - kKeyHyper_L: Left hyper
    HID_KEYS.KEY_NONE,           # EFEE - kKeyHyper_R: Right hyper
    HID_KEYS.KEY_NONE,           # EFEF
    HID_KEYS.KEY_NONE,           # EFF0
    HID_KEYS.KEY_NONE,           # EFF1
    HID_KEYS.KEY_NONE,           # EFF2
    HID_KEYS.KEY_NONE,           # EFF3
    HID_KEYS.KEY_NONE,           # EFF4
    HID_KEYS.KEY_NONE,           # EFF5
    HID_KEYS.KEY_NONE,           # EFF6
    HID_KEYS.KEY_NONE,           # EFF7
    HID_KEYS.KEY_NONE,           # EFF8
    HID_KEYS.KEY_NONE,           # EFF9
    HID_KEYS.KEY_NONE,           # EFFA
    HID_KEYS.KEY_NONE,           # EFFB
    HID_KEYS.KEY_NONE,           # EFFC
    HID_KEYS.KEY_NONE,           # EFFD
    HID_KEYS.KEY_NONE,           # EFFE
    HID_KEYS.KEY_DELETE          # EFFF - kKeyDelete: Delete, rubout
]   

class barrier_modifiers_mask:
    SHIFT = 0x0001
    CTRL = 0x0002
    ALT = 0x0004
    META = 0x0008
    GUI = 0x0010
    altGr = 0x0020
    level5Lock = 0x0040
    reserved = 0x0080
    LED_CAPS_LOCK = 0x1000
    LED_NUM_LOCK = 0x2000
    LED_SCROLL_LOCK = 0x4000
 

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
        print(data_in)
        
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
        print(data_in)

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
        if (((barrier_modifiers_mask.LED_CAPS_LOCK & KeyModifiers)>0) != lock_states['LED_CAPS_LOCK']):
            self.tapRaw(HID_KEYS.KEY_CAPS_LOCK)
        if (((barrier_modifiers_mask.LED_NUM_LOCK & KeyModifiers)>0) != lock_states['LED_NUM_LOCK']):
            self.tapRaw(HID_KEYS.KEY_NUM_LOCK)
        if (((barrier_modifiers_mask.LED_SCROLL_LOCK & KeyModifiers)>0) != lock_states['LED_SCROLL_LOCK']):
            self.tapRaw(HID_KEYS.KEY_SCROLL_LOCK)
        return
    
    def actionKey(self, KeyId, KeyModifiers, KeyButton, Action):
        
        act_KeyId=HID_KEYS.KEY_NONE
        if KeyId >= 0xEF00 and KeyId <= 0xEFFF:
            act_KeyId=barrier_keyboard_key_map[KeyId-0xEF00]
        elif KeyId >= 0x00 and KeyId <= 0x7F:
            act_KeyId=hid_ascii_map[KeyId]
        
        if (Action=='press' and act_KeyId!=HID_KEYS.KEY_CAPS_LOCK and act_KeyId!=HID_KEYS.KEY_NUM_LOCK and act_KeyId!=HID_KEYS.KEY_SCROLL_LOCK):
            self.syncLocks(KeyModifiers)
        

        
        if(act_KeyId!=HID_KEYS.KEY_NONE):
            if(Action=='press'):
                self.pressRaw(act_KeyId)
            else:
                self.releaseRaw(act_KeyId)
          
        if (Action=='release' and act_KeyId==HID_KEYS.KEY_CAPS_LOCK or act_KeyId==HID_KEYS.KEY_NUM_LOCK or act_KeyId==HID_KEYS.KEY_SCROLL_LOCK):
            self.syncLocks(KeyModifiers)
        
        return
    def repeat(self, KeyId, KeyModifiers, KeyButton):
        #Repeat not required when HID is used
        return    
    def press(self, KeyId, KeyModifiers, KeyButton):
        self.actionKey(KeyId, KeyModifiers, KeyButton, 'press')
        return
    def release(self, KeyId, KeyModifiers, KeyButton):
        self.actionKey(KeyId, KeyModifiers, KeyButton, 'release')
        return
 