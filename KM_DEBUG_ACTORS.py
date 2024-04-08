class Mouse(object):
    def move(self, px, py):
        print("[*] Event: Mouse Move: X=" + str(px) + " Y=" +  str(py))
        return
    def press(self, b):
        print("[*] Event: Mouse Press: Buttons=" + hex(b))
        return
    def release(self, b):
        print("[*] Event: Mouse Release: Buttons=" + hex(b))
        return
    def wheel(self, x, y):
        print("[*] Event: Mouse Wheel: X=" + str(x) + " Y=" +  str(y))
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