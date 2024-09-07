from exploit.restore import restore_files, FileToRestore, restore_file

from pymobiledevice3.exceptions import PyMobileDevice3Exception
from pymobiledevice3.services.diagnostics import DiagnosticsService
from pymobiledevice3 import usbmux
from pymobiledevice3.lockdown import create_using_usbmux

from pathlib import Path
from tempfile import TemporaryDirectory
import plistlib
import traceback

region_code = input("Enter YOUR CURRENT 2-letter region code (default to US): ").strip().upper() or "US"
method = int(input("Choose a method, 1 or 2: ") or "1") or 1
print("Please wait...")

def replace_region_code(plist_path, original_code="US", new_code="US"):
    with open(plist_path, 'rb') as f:
        plist_data = plistlib.load(f)
    
    plist_str = str(plist_data)
    updated_plist_str = plist_str.replace(original_code, new_code)
    updated_plist_data = eval(updated_plist_str)  # Convert string back to dictionary

    return plistlib.dumps(updated_plist_data)



file_path = Path.joinpath(Path.cwd(), 'eligibility.plist')
eligibility_data = replace_region_code(file_path, original_code="US", new_code=region_code)

files_to_restore = [
    FileToRestore(
        contents=eligibility_data,
        restore_path="/var/db/os_eligibility/",
        restore_name="eligibility.plist"
    )
]

file_path = Path.joinpath(Path.cwd(), 'Config.plist')
config_data = replace_region_code(file_path, original_code="US", new_code=region_code)
if method == 1:
    files_to_restore.append(
        FileToRestore(
            contents=config_data,
            restore_path="/var/MobileAsset/AssetsV2/com_apple_MobileAsset_OSEligibility/purpose_auto/c55a421c053e10233e5bfc15c42fa6230e5639a9.asset/AssetData/",
            restore_name="Config.plist"
        )
    )
elif method == 2:
    files_to_restore.append(
        FileToRestore(
            contents=config_data,
            restore_path="/var/MobileAsset/AssetsV2/com_apple_MobileAsset_OSEligibility/purpose_auto/247556c634fc4cc4fd742f1b33af9abf194a986e.asset/AssetData/",
            restore_name="Config.plist"
        )
    )

# taken from nugget
try:
    restore_files(files=files_to_restore)
except PyMobileDevice3Exception as e:
    if "Find My" in str(e):
        print("Find My must be disabled in order to use this tool.")
        print("Disable Find My from Settings (Settings -> [Your Name] -> Find My) and then try again.")
    if "File Exists" in str(e):
        print("It seems you tried to run this again without rebooting, please reboot before trying again.")
    if "link error" in str(e):
        print("A Fatal Error occurred, this is not an error with the script, please do not ask for support for this error")
    elif "crash_on_purpose" not in str(e):
        raise e
    else:
        print("Successfully applied! (you should not need to reboot to see changes)")
except Exception as e:
    print(traceback.format_exc())
finally:
    input("Press Enter to exit...")