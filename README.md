

# **Python Barrier Client**

This is a Python Barrier Client that can run on CPython, CircuitPython, and MicroPython. The Python script can either use native HID Mouse/Keyboard or a CH9329 via serial. Below, I will describe the different use cases. The CH9329 Actor only has a vertical wheel as it does not implement a horizontal wheel. The HID Actor implements both vertical and horizontal wheels.

## **Windows/Linux/Mac**

Only Windows was tested, but it should work on all PC environments.

- **ACTOR_TYPE=HID:** Uses the pyinput library for native keyboard/mouse. On Windows, the script must be run as an Administrator, as any window that is elevated will give keyboard/mouse control.
- **ACTOR_TYPE=CH9329:** Uses serial connected to CH9329. See docs for correct wiring and configuration. In the script, modify the SERIAL_PORT variable.

## **CircuitPython**

Rename `PY_Barrier.py` to `code.py`. Copy `code.py` and `boot.py` to the root. All other libraries should be copied to the `lib` directory.

- **ACTOR_TYPE=HID:** Uses native HID USB. Tested on ESP32-S3 and Pi_Pico_W. ESP32-S3 requires the latest version (9.0 Absolute Newest >= PR9134) as it fixes USB HID lag issues. Other boards that support HID should also work. Click "Available on these boards" on the following link: [USB HID CircuitPython Documentation](https://docs.circuitpython.org/en/latest/shared-bindings/usb_hid/index.html)
- **ACTOR_TYPE=CH9329:** Uses serial connected to CH9329. In the script, modify the CP_TX_PIN and CP_RX_PIN variables.

## **MicroPython**

Rename `PY_Barrier.py` to `code.py`. Copy `code.py` and `boot.py` to the root. All other libraries should be copied to the `lib` directory.

- **ACTOR_TYPE=HID:** Uses native HID USB. At the time of writing it only on rp2 and samd boards.  Only tested on Pi_Pico_W. Requires MicroPython version >= 1.23-preview. There is an `MP_USB_INSTALL.py` script to install the required imports, which is only required to run once. Refer to (https://github.com/micropython/micropython-lib/pull/558) and (https://github.com/micropython/micropython/pull/9497).
- **ACTOR_TYPE=CH9329:** Uses serial connected to CH9329. In the script, modify the MP_TX_PIN and MP_RX_PIN variables.

## **TODOs**

- Test on Mac/Linux
- ~~Get MicroPython working with no Mouse Lag~~
- ~~Complete MicroPython Keyboard~~
- Custom USB VID, PID, USB Descriptions
- Automatic CH9329 configuration
- Support TLS
- Clipboard Support full duplex for native PC
- Clipboard Support half duplex with hotkey
- Bluetooth Support

