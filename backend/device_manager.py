from pymobiledevice3 import usbmux
from pymobiledevice3.lockdown import create_using_usbmux

class DeviceManager:
    def __init__(self):
        self.devices = []
        self.get_devices()
        if len(self.devices) != 0:
            self.set_device(device=0)

    def get_devices(self):
        self.devices.clear()
        connected_devices = usbmux.list_devices()
        uuids = set() # added to avoid devices getting added multiple times

        for device in connected_devices:
            if device.serial in uuids:
                continue
                
            try:
                ld = create_using_usbmux(serial=device.serial)
                vals = ld.all_values
                dev = {
                    "uuid": device.serial,
                    "name": vals['DeviceName'],
                    "version": vals['ProductVersion'],
                    "model": vals['ProductType'],
                    "locale": ld.locale,
                    "ld": ld
                }
                self.devices.append(dev)
                uuids.add(device.serial)
            except Exception as e:
                print(f"ERROR with lockdown device with UUID {device.serial}")

        if len(self.devices) == 0:
            print("No devices found!")
        else:
            print(f"{len(self.devices)} device(s) found!")
    
    def set_device(self, device=0):
        self.device = self.devices[device]