import network
import mip
WIFI_SSID = "SSID"
WIFI_PASS = "PASS"
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_SSID,WIFI_PASS)
print(wlan.isconnected())
mip.install("usb-device", index="https://projectgus.github.io/micropython-lib/mip/feature/usbd_python/")
mip.install("usb-device-hid", index="https://projectgus.github.io/micropython-lib/mip/feature/usbd_python/")
