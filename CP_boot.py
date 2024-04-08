import usb_cdc
#usb_cdc.disable()

import usb_hid
from KM_CPHID_ACTORS import ABS_MOUSE_DEVICE
from KM_CPHID_ACTORS import KEYBOARD_DEVICE

usb_hid.enable((KEYBOARD_DEVICE, ABS_MOUSE_DEVICE))