import sys

if sys.implementation.name == "circuitpython":
    import usb_cdc
    #usb_cdc.disable()

    import usb_hid
    from KM_CPHID_ACTORS import ABS_MOUSE_DEVICE
    from KM_CPHID_ACTORS import KEYBOARD_DEVICE

    usb_hid.enable((KEYBOARD_DEVICE, ABS_MOUSE_DEVICE))
elif sys.implementation.name == "micropython":
    import usb.device
    from KM_MPHID_ACTORS import MouseInterface
    usb.device.get().init(MouseInterface , builtin_driver=True)


