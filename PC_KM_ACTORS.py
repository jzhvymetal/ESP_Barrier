from pynput import mouse, keyboard
import platform
import enum

mouse_act = mouse.Controller()
   
mouse_btn_map = [		# Barrier State
mouse.Button.unknown,	# 0 None
mouse.Button.left,		# 1 LEFT
mouse.Button.middle,	# 2 MIDDLE
mouse.Button.right,		# 3 RIGHT
mouse.Button.x1,		# 4 X
mouse.Button.x2			# 5 X2
]    


class Mouse:

    def move(self, x, y):  
        mouse_act.position = (x, y)
        return
    def press(self, b):  
        mouse_act.press(mouse_btn_map[b])  
        return
    def release(self, b):  
        mouse_act.release(mouse_btn_map[b])  
        return
    def wheel(self, x, y): 
        mouse_act.scroll(x,y)  
        return

class KEYS:
    
    KEY_NONE = ''
    # Modifiers
    KEY_LEFT_CTRL = keyboard.Key.ctrl_l
    KEY_LEFT_SHIFT = keyboard.Key.shift_l
    KEY_LEFT_ALT = keyboard.Key.alt_l
    KEY_LEFT_GUI = keyboard.Key.cmd  
    KEY_RIGHT_CTRL = keyboard.Key.ctrl_r
    KEY_RIGHT_SHIFT = keyboard.Key.shift_r
    KEY_RIGHT_ALT = keyboard.Key.alt_r
    KEY_RIGHT_GUI = keyboard.Key.cmd 

    # Misc keys
    KEY_UP_ARROW = keyboard.Key.up
    KEY_DOWN_ARROW = keyboard.Key.down
    KEY_LEFT_ARROW = keyboard.Key.left
    KEY_RIGHT_ARROW = keyboard.Key.right
    KEY_BACKSPACE = keyboard.Key.backspace
    KEY_TAB = keyboard.Key.tab
    KEY_RETURN = keyboard.Key.enter
    KEY_MENU = keyboard.Key.menu 
    KEY_ESC = keyboard.Key.esc
    KEY_INSERT = keyboard.Key.insert
    KEY_DELETE = keyboard.Key.delete
    KEY_PAGE_UP = keyboard.Key.page_up
    KEY_PAGE_DOWN = keyboard.Key.page_down
    KEY_HOME = keyboard.Key.home
    KEY_END = keyboard.Key.end
    KEY_CAPS_LOCK = keyboard.Key.caps_lock
    KEY_PRINT_SCREEN = keyboard.Key.print_screen  # Print Screen / SysRq
    KEY_SCROLL_LOCK = keyboard.Key.scroll_lock
    KEY_PAUSE = keyboard.Key.pause  # Pause / Break

    # Numeric keypad
    KEY_NUM_LOCK = keyboard.Key.num_lock
    KEY_KP_SLASH = '/'
    KEY_KP_ASTERISK = '*'
    KEY_KP_MINUS = '-'
    KEY_KP_PLUS = '+'
    KEY_KP_ENTER = keyboard.Key.enter
    KEY_KP_1 = '1'
    KEY_KP_2 = '2'
    KEY_KP_3 = '3'
    KEY_KP_4 = '4'
    KEY_KP_5 = '5'
    KEY_KP_6 = '6'
    KEY_KP_7 = '7'
    KEY_KP_8 = '8'
    KEY_KP_9 = '9'
    KEY_KP_0 = '0'
    KEY_KP_DOT = '.'

    # Function keys
    KEY_F1 = keyboard.Key.f1
    KEY_F2 = keyboard.Key.f2
    KEY_F3 = keyboard.Key.f3
    KEY_F4 = keyboard.Key.f4
    KEY_F5 = keyboard.Key.f5
    KEY_F6 = keyboard.Key.f6
    KEY_F7 = keyboard.Key.f7
    KEY_F8 = keyboard.Key.f8
    KEY_F9 = keyboard.Key.f9
    KEY_F10 = keyboard.Key.f10
    KEY_F11 = keyboard.Key.f11
    KEY_F12 = keyboard.Key.f12
    KEY_F13 = keyboard.Key.f13
    KEY_F14 = keyboard.Key.f14
    KEY_F15 = keyboard.Key.f15
    KEY_F16 = keyboard.Key.f16
    KEY_F17 = keyboard.Key.f17
    KEY_F18 = keyboard.Key.f18
    KEY_F19 = keyboard.Key.f19
    KEY_F20 = keyboard.Key.f20

keyboard_key_map =[
    KEYS.KEY_NONE,           # EF00
    KEYS.KEY_NONE,           # EF01
    KEYS.KEY_NONE,           # EF02
    KEYS.KEY_NONE,           # EF03
    KEYS.KEY_NONE,           # EF04
    KEYS.KEY_NONE,           # EF05
    KEYS.KEY_NONE,           # EF06
    KEYS.KEY_NONE,           # EF07
    KEYS.KEY_BACKSPACE,      # EF08 - kKeyBackSpace: back space, back char
    KEYS.KEY_TAB,            # EF09 - kKeyTab
    KEYS.KEY_NONE,           # EF0A
    KEYS.KEY_NONE,           # EF0B
    KEYS.KEY_NONE,           # EF0C
    KEYS.KEY_RETURN,         # EF0D - kKeyReturn: Return, enter
    KEYS.KEY_NONE,           # EF0E
    KEYS.KEY_NONE,           # EF0F
    KEYS.KEY_NONE,           # EF10
    KEYS.KEY_NONE,           # EF11
    KEYS.KEY_NONE,           # EF12
    KEYS.KEY_PAUSE,          # EF13 - kKeyPause: Pause, hold
    KEYS.KEY_SCROLL_LOCK,    # EF14 - kKeyScrollLock
    KEYS.KEY_NONE,           # EF15
    KEYS.KEY_NONE,           # EF16
    KEYS.KEY_NONE,           # EF17
    KEYS.KEY_NONE,           # EF18
    KEYS.KEY_NONE,           # EF19
    KEYS.KEY_NONE,           # EF1A
    KEYS.KEY_ESC,            # EF1B - kKeyEscape
    KEYS.KEY_NONE,           # EF1C
    KEYS.KEY_NONE,           # EF1D
    KEYS.KEY_NONE,           # EF1E
    KEYS.KEY_NONE,           # EF1F
    KEYS.KEY_NONE,           # EF20
    KEYS.KEY_NONE,           # EF21
    KEYS.KEY_NONE,           # EF22
    KEYS.KEY_NONE,           # EF23
    KEYS.KEY_NONE,           # EF24
    KEYS.KEY_NONE,           # EF25
    KEYS.KEY_NONE,           # EF26
    KEYS.KEY_NONE,           # EF27
    KEYS.KEY_NONE,           # EF28
    KEYS.KEY_NONE,           # EF29
    KEYS.KEY_NONE,           # EF2A
    KEYS.KEY_NONE,           # EF2B
    KEYS.KEY_NONE,           # EF2C
    KEYS.KEY_NONE,           # EF2D
    KEYS.KEY_NONE,           # EF2E
    KEYS.KEY_NONE,           # EF2F
    KEYS.KEY_NONE,           # EF30
    KEYS.KEY_NONE,           # EF31
    KEYS.KEY_NONE,           # EF32
    KEYS.KEY_NONE,           # EF33
    KEYS.KEY_NONE,           # EF34
    KEYS.KEY_NONE,           # EF35
    KEYS.KEY_NONE,           # EF36
    KEYS.KEY_NONE,           # EF37
    KEYS.KEY_NONE,           # EF38
    KEYS.KEY_NONE,           # EF39
    KEYS.KEY_NONE,           # EF3A
    KEYS.KEY_NONE,           # EF3B
    KEYS.KEY_NONE,           # EF3C
    KEYS.KEY_NONE,           # EF3D
    KEYS.KEY_NONE,           # EF3E
    KEYS.KEY_NONE,           # EF3F
    KEYS.KEY_NONE,           # EF40
    KEYS.KEY_NONE,           # EF41
    KEYS.KEY_NONE,           # EF42
    KEYS.KEY_NONE,           # EF43
    KEYS.KEY_NONE,           # EF44
    KEYS.KEY_NONE,           # EF45
    KEYS.KEY_NONE,           # EF46
    KEYS.KEY_NONE,           # EF47
    KEYS.KEY_NONE,           # EF48
    KEYS.KEY_NONE,           # EF49
    KEYS.KEY_NONE,           # EF4A
    KEYS.KEY_NONE,           # EF4B
    KEYS.KEY_NONE,           # EF4C
    KEYS.KEY_NONE,           # EF4D
    KEYS.KEY_NONE,           # EF4E
    KEYS.KEY_NONE,           # EF4F
    KEYS.KEY_HOME,           # EF50 - kKeyHome
    KEYS.KEY_LEFT_ARROW,     # EF51 - kKeyLeft: Move left, left arrow
    KEYS.KEY_UP_ARROW,       # EF52 - kKeyUp: Move up, up arrow
    KEYS.KEY_RIGHT_ARROW,    # EF53 - kKeyRight: Move right, right arrow
    KEYS.KEY_DOWN_ARROW,     # EF54 - kKeyDown: Move down, down arrow
    KEYS.KEY_PAGE_UP,        # EF55 - kKeyPageUp
    KEYS.KEY_PAGE_DOWN,      # EF56 - kKeyPageDown
    KEYS.KEY_END,            # EF57 - kKeyEnd: EOL
    KEYS.KEY_HOME,           # EF58 - kKeyBegin: BOL
    KEYS.KEY_NONE,           # EF59
    KEYS.KEY_NONE,           # EF5A
    KEYS.KEY_NONE,           # EF5B
    KEYS.KEY_NONE,           # EF5C
    KEYS.KEY_NONE,           # EF5D
    KEYS.KEY_NONE,           # EF5E
    KEYS.KEY_NONE,           # EF5F
    KEYS.KEY_NONE,           # EF60 - kKeySelect: Select, mark
    KEYS.KEY_PRINT_SCREEN,   # EF61 - kKeyPrint
    KEYS.KEY_NONE,           # EF62
    KEYS.KEY_INSERT,         # EF63 - kKeyInsert: Insert, insert here
    KEYS.KEY_NONE,           # EF64
    KEYS.KEY_NONE,           # EF65 - kKeyUndo: Undo, oops
    KEYS.KEY_NONE,           # EF66 - kKeyRedo: Redo, again
    KEYS.KEY_MENU,           # EF67 - kKeyMenu
    KEYS.KEY_NONE,           # EF68
    KEYS.KEY_NONE,           # EF69
    KEYS.KEY_NONE,           # EF6A
    KEYS.KEY_NONE,           # EF6B
    KEYS.KEY_NONE,           # EF6C
    KEYS.KEY_NONE,           # EF6D
    KEYS.KEY_NONE,           # EF6E
    KEYS.KEY_NONE,           # EF6F
    KEYS.KEY_NONE,           # EF70
    KEYS.KEY_NONE,           # EF71
    KEYS.KEY_NONE,           # EF72
    KEYS.KEY_NONE,           # EF73
    KEYS.KEY_NONE,           # EF74
    KEYS.KEY_NONE,           # EF75
    KEYS.KEY_NONE,           # EF76
    KEYS.KEY_NONE,           # EF77
    KEYS.KEY_NONE,           # EF78
    KEYS.KEY_NONE,           # EF79
    KEYS.KEY_NONE,           # EF7A
    KEYS.KEY_NONE,           # EF7B
    KEYS.KEY_NONE,           # EF7C
    KEYS.KEY_NONE,           # EF7D
    KEYS.KEY_NONE,           # EF7E - kKeyAltGr: Character set switch
    KEYS.KEY_NUM_LOCK,       # EF7F - kKeyNumLock
    KEYS.KEY_NONE,           # EF80
    KEYS.KEY_NONE,           # EF81
    KEYS.KEY_NONE,           # EF82
    KEYS.KEY_NONE,           # EF83
    KEYS.KEY_NONE,           # EF84
    KEYS.KEY_NONE,           # EF85
    KEYS.KEY_NONE,           # EF86
    KEYS.KEY_NONE,           # EF87
    KEYS.KEY_NONE,           # EF88
    KEYS.KEY_NONE,           # EF89
    KEYS.KEY_TAB,            # EF8A - kKeyKP_Tab
    KEYS.KEY_NONE,           # EF8B
    KEYS.KEY_NONE,           # EF8C
    KEYS.KEY_KP_ENTER,       # EF8D - kKeyKP_Enter: enter
    KEYS.KEY_NONE,           # EF8E
    KEYS.KEY_NONE,           # EF8F
    KEYS.KEY_NONE,           # EF90
    KEYS.KEY_NONE,           # EF91
    KEYS.KEY_NONE,           # EF92
    KEYS.KEY_NONE,           # EF93
    KEYS.KEY_NONE,           # EF94
    KEYS.KEY_HOME,           # EF95 - NumLock_OFF
    KEYS.KEY_LEFT_ARROW,     # EF96 - NumLock_OFF
    KEYS.KEY_UP_ARROW,       # EF97 - NumLock_OFF
    KEYS.KEY_RIGHT_ARROW,    # EF98 - NumLock_OFF
    KEYS.KEY_DOWN_ARROW,     # EF99 - NumLock_OFF
    KEYS.KEY_PAGE_UP,        # EF9A - NumLock_OFF
    KEYS.KEY_PAGE_DOWN,      # EF9B - NumLock_OFF
    KEYS.KEY_NONE,           # EF9C
    KEYS.KEY_NONE,           # EF9D
    KEYS.KEY_INSERT,         # EF9E - NumLock_OFF
    KEYS.KEY_DELETE,         # EF9F - NumLock_OFF
    KEYS.KEY_NONE,           # EFA0
    KEYS.KEY_NONE,           # EFA1
    KEYS.KEY_NONE,           # EFA2
    KEYS.KEY_NONE,           # EFA3
    KEYS.KEY_NONE,           # EFA4
    KEYS.KEY_NONE,           # EFA5
    KEYS.KEY_NONE,           # EFA6
    KEYS.KEY_NONE,           # EFA7
    KEYS.KEY_NONE,           # EFA8
    KEYS.KEY_NONE,           # EFA9 
    KEYS.KEY_KP_ASTERISK,    # EFAA - kKeyKP_Multiply
    KEYS.KEY_KP_PLUS,        # EFAB - kKeyKP_Add
    KEYS.KEY_NONE,           # EFAC - kKeyKP_Separator: separator, often comma
    KEYS.KEY_KP_MINUS,       # EFAD - kKeyKP_Subtract
    KEYS.KEY_KP_DOT,         # EFAE - kKeyKP_Decimal
    KEYS.KEY_KP_SLASH,       # EFAF - kKeyKP_Divide
    KEYS.KEY_KP_0,           # EFB0 - kKeyKP_0
    KEYS.KEY_KP_1,           # EFB1 - kKeyKP_1
    KEYS.KEY_KP_2,           # EFB2 - kKeyKP_2
    KEYS.KEY_KP_3,           # EFB3 - kKeyKP_3
    KEYS.KEY_KP_4,           # EFB4 - kKeyKP_4
    KEYS.KEY_KP_5,           # EFB5 - kKeyKP_5
    KEYS.KEY_KP_6,           # EFB6 - kKeyKP_6
    KEYS.KEY_KP_7,           # EFB7 - kKeyKP_7
    KEYS.KEY_KP_8,           # EFB8 - kKeyKP_8
    KEYS.KEY_KP_9,           # EFB9 - kKeyKP_9
    KEYS.KEY_NONE,           # EFBA 
    KEYS.KEY_NONE,           # EFBB
    KEYS.KEY_NONE,           # EFBC
    KEYS.KEY_NONE,           # EFBD - kKeyKP_Equal: equals
    KEYS.KEY_F1,             # EFBE - kKeyF1
    KEYS.KEY_F2,             # EFBF - kKeyF2
    KEYS.KEY_F3,             # EFC0 - kKeyF3
    KEYS.KEY_F4,             # EFC1 - kKeyF4
    KEYS.KEY_F5,             # EFC2 - kKeyF5
    KEYS.KEY_F6,             # EFC3 - kKeyF6
    KEYS.KEY_F7,             # EFC4 - kKeyF7
    KEYS.KEY_F8,             # EFC5 - kKeyF8
    KEYS.KEY_F9,             # EFC6 - kKeyF9
    KEYS.KEY_F10,            # EFC7 - kKeyF10
    KEYS.KEY_F11,            # EFC8 - kKeyF11
    KEYS.KEY_F12,            # EFC9 - kKeyF12
    KEYS.KEY_F13,            # EFCA - kKeyF13
    KEYS.KEY_F14,            # EFCB - kKeyF14
    KEYS.KEY_F15,            # EFCC - kKeyF15
    KEYS.KEY_F16,            # EFCD - kKeyF16
    KEYS.KEY_F17,            # EFCE - kKeyF17
    KEYS.KEY_F18,            # EFCF - kKeyF18
    KEYS.KEY_F19,            # EFD0 - kKeyF19
    KEYS.KEY_F20,            # EFD1 - kKeyF20
    KEYS.KEY_NONE,           # EFD2 - kKeyF21
    KEYS.KEY_NONE,           # EFD3 - kKeyF22
    KEYS.KEY_NONE,           # EFD4 - kKeyF23
    KEYS.KEY_NONE,           # EFD5 - kKeyF24
    KEYS.KEY_NONE,           # EFD6 - kKeyF25
    KEYS.KEY_NONE,           # EFD7 - kKeyF26
    KEYS.KEY_NONE,           # EFD8 - kKeyF27
    KEYS.KEY_NONE,           # EFD9 - kKeyF28
    KEYS.KEY_NONE,           # EFDA - kKeyF29
    KEYS.KEY_NONE,           # EFDB - kKeyF30
    KEYS.KEY_NONE,           # EFDC - kKeyF31
    KEYS.KEY_NONE,           # EFDD - kKeyF32
    KEYS.KEY_NONE,           # EFDE - kKeyF33
    KEYS.KEY_NONE,           # EFDF - kKeyF34
    KEYS.KEY_NONE,           # EFE0 - kKeyF35
    KEYS.KEY_LEFT_SHIFT,     # EFE1 - kKeyShift_L: Left shift
    KEYS.KEY_RIGHT_SHIFT,    # EFE2 - kKeyShift_R: Right shift
    KEYS.KEY_LEFT_CTRL,      # EFE3 - kKeyControl_L: Left control
    KEYS.KEY_RIGHT_CTRL,     # EFE4 - kKeyControl_R: Right control
    KEYS.KEY_CAPS_LOCK,      # EFE5 - kKeyCapsLock: Caps lock
    KEYS.KEY_NONE,           # EFE6 - kKeyShiftLock: Shift lock
    KEYS.KEY_NONE,           # EFE7 - kKeyMeta_L: Left meta
    KEYS.KEY_NONE,           # EFE8 - kKeyMeta_R: Right meta
    KEYS.KEY_LEFT_ALT,       # EFE9 - kKeyAlt_L: Left alt
    KEYS.KEY_RIGHT_ALT,      # EFEA - kKeyAlt_R: Right alt
    KEYS.KEY_LEFT_GUI,       # EFEB - kKeySuper_L: Left super
    KEYS.KEY_RIGHT_GUI,      # EFEC - kKeySuper_R: Right super
    KEYS.KEY_NONE,           # EFED - kKeyHyper_L: Left hyper
    KEYS.KEY_NONE,           # EFEE - kKeyHyper_R: Right hyper
    KEYS.KEY_NONE,           # EFEF
    KEYS.KEY_NONE,           # EFF0
    KEYS.KEY_NONE,           # EFF1
    KEYS.KEY_NONE,           # EFF2
    KEYS.KEY_NONE,           # EFF3
    KEYS.KEY_NONE,           # EFF4
    KEYS.KEY_NONE,           # EFF5
    KEYS.KEY_NONE,           # EFF6
    KEYS.KEY_NONE,           # EFF7
    KEYS.KEY_NONE,           # EFF8
    KEYS.KEY_NONE,           # EFF9
    KEYS.KEY_NONE,           # EFFA
    KEYS.KEY_NONE,           # EFFB
    KEYS.KEY_NONE,           # EFFC
    KEYS.KEY_NONE,           # EFFD
    KEYS.KEY_NONE,           # EFFE
    KEYS.KEY_DELETE          # EFFF - kKeyDelete: Delete, rubout
]   

class KeyModifiersMask:
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
 

def get_lock_state():
    system = platform.system()
    if system == "Windows":
        import ctypes
        return {
            'LED_CAPS_LOCK': ctypes.windll.user32.GetKeyState(0x14) & 0xffff != 0,
            'LED_SCROLL_LOCK': ctypes.windll.user32.GetKeyState(0x91) & 0xffff != 0,
            'LED_NUM_LOCK': ctypes.windll.user32.GetKeyState(0x90) & 0xffff != 0
        }
    elif system == "Linux":
        import subprocess
        xset_output = subprocess.check_output(["xset", "-q"]).decode("utf-8")
        return {
            'LED_CAPS_LOCK': "Caps Lock: on" in xset_output,
            'LED_SCROLL_LOCK': "Scroll Lock: on" in xset_output,
            'LED_NUM_LOCK': "Num Lock: on" in xset_output
        }
    elif system == "Darwin":
        from Quartz import CGEventCreateKeyboardEvent, kCGEventFlagMaskAlphaShift, kCGEventFlagMaskNumericPad
        def get_mac_lock_state(virtual_keycode):
            event = CGEventCreateKeyboardEvent(None, virtual_keycode, True)
            return bool(event.getFlags() & kCGEventFlagMaskAlphaShift)
        return {
            'LED_CAPS_LOCK': get_mac_lock_state(0x39),
            'LED_SCROLL_LOCK': get_mac_lock_state(0x6C),
            'LED_NUM_LOCK': get_mac_lock_state(0x47) or get_mac_lock_state(kCGEventFlagMaskNumericPad)
        }
    else:
        raise NotImplementedError("Unsupported platform")

keyboard_act = keyboard.Controller()

class Keyboard:
    def syncLocks(self, KeyModifiers):
        lock_states = get_lock_state()
        
        if (((KeyModifiersMask.LED_CAPS_LOCK & KeyModifiers)>0) != lock_states['LED_CAPS_LOCK']):
            keyboard_act.tap(KEYS.KEY_CAPS_LOCK)
        if (((KeyModifiersMask.LED_NUM_LOCK & KeyModifiers)>0) != lock_states['LED_NUM_LOCK']):
            keyboard_act.tap(KEYS.KEY_NUM_LOCK)
        if (((KeyModifiersMask.LED_SCROLL_LOCK & KeyModifiers)>0) != lock_states['LED_SCROLL_LOCK']):
            keyboard_act.tap(KEYS.KEY_SCROLL_LOCK)
        return
    
    def actionKey(self, KeyId, KeyModifiers, KeyButton, Action):
        act_KeyId=KEYS.KEY_NONE
        if KeyId >= 0xEF00 and KeyId <= 0xEFFF:
            act_KeyId=keyboard_key_map[KeyId-0xEF00]
        else:
            act_KeyId=chr(KeyId)
            if act_KeyId.isalpha(): 
                act_KeyId = act_KeyId.lower()  #Caps Locks in syc always send lower case

        if (Action=='press' and act_KeyId!=KEYS.KEY_CAPS_LOCK and act_KeyId!=KEYS.KEY_NUM_LOCK and act_KeyId!=KEYS.KEY_SCROLL_LOCK):
            self.syncLocks(KeyModifiers)
             
        if(act_KeyId!=KEYS.KEY_NONE):
            if(Action=='press'):
                keyboard_act.press(act_KeyId)
            else:
                keyboard_act.release(act_KeyId)

        if (Action=='release' and act_KeyId==KEYS.KEY_CAPS_LOCK or act_KeyId==KEYS.KEY_NUM_LOCK or act_KeyId==KEYS.KEY_SCROLL_LOCK):
            self.syncLocks(KeyModifiers)
  
        return
    def repeat(self, KeyId, KeyModifiers, KeyButton):
        self.actionKey(KeyId, KeyModifiers, KeyButton, 'press') 
        return     
    def press(self, KeyId, KeyModifiers, KeyButton):
        self.actionKey(KeyId, KeyModifiers, KeyButton, 'press')
        return
    def release(self, KeyId, KeyModifiers, KeyButton):
        self.actionKey(KeyId, KeyModifiers, KeyButton, 'release')
        return
 