from backend.device_manager import DeviceManager
from backend.funcs import prompt
from pymobiledevice3 import usbmux
from tweak.eligibility import EUTweak

print("Initializing...")

prompt_options = [
    "1. Restore files with no data",
    "2. Apply eligibility and config patches",
    "3. Restore files with no data and apply patches",
    "4. Automated eligibility and config patch spam"
]

dev_manager = DeviceManager()
dev_manager.set_device(device=0)

tweak = EUTweak(prompt(prompt_options))
tweak.apply(lockdown=dev_manager.device.get("ld"))