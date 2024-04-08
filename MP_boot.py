import usb.device
from KM_MPHID_ACTORS import MouseInterface
usb.device.get().init(MouseInterface , builtin_driver=True)

