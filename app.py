from exploit.restore import restore_files, FileToRestore, restore_file

from pymobiledevice3.exceptions import PyMobileDevice3Exception
from pymobiledevice3.services.diagnostics import DiagnosticsService
from pymobiledevice3 import usbmux
from pymobiledevice3.lockdown import create_using_usbmux

from pathlib import Path
from tempfile import TemporaryDirectory
import traceback
import plistlib
import traceback
from time import sleep

# Function to replace the region code in a plist file
def replace_region_code(plist_path, original_code="US", new_code="US"):
    with open(plist_path, 'rb') as f:
        plist_data = plistlib.load(f)

    plist_str = str(plist_data)
    updated_plist_str = plist_str.replace(original_code, new_code)
    updated_plist_data = eval(updated_plist_str)  # Convert string back to dictionary

    return plistlib.dumps(updated_plist_data)

# Function to handle file restoration
def retry_restore(files, max_retries=3):
    for attempt in range(max_retries):
        try:
            restore_files(files=files)
            break  # Exit loop on success
        except ConnectionAbortedError:
            print(f"Connection aborted, retrying... ({attempt + 1}/{max_retries})")
            sleep(2)  # Pause before retrying
        except PyMobileDevice3Exception as e:
            handle_pymobiledevice_exception(e)
            break
        except Exception as e:
            print(traceback.format_exc())
            break

# Exception handling for PyMobileDevice3 exceptions
def handle_pymobiledevice_exception(e):
    if "Find My" in str(e):
        print("Find My must be disabled to use this tool.")
        print("Disable Find My from Settings (Settings -> [Your Name] -> Find My) and try again.")
    elif "File Exists" in str(e):
        print("File already exists at the specified path. Consider removing or overwriting it before retrying.")
    elif "crash_on_purpose" not in str(e):
        raise e
    else:
        print("Successfully applied! (you should not need to reboot to see changes)")

# Function to prompt the user for an action
def prompt_for_action():
    print("Select an option:")
    print("1. Restore files with no data")
    print("2. Apply eligibility and config patches")
    print("3. Restore files with no data and apply patches")
    choice = input("Enter your choice (1, 2, or 3): ").strip()
    return choice

# Get the region code from the user
region_code = input("Enter YOUR CURRENT 2-letter region code (default to US): ").strip().upper() or "US"
print("Please wait...")

# Paths to plist files
file_path = Path.joinpath(Path.cwd(), 'eligibility.plist')
with open(file_path, 'rb') as file:
    eligibility_data = file.read()
file_path = Path.joinpath(Path.cwd(), 'Config.plist')
with open(file_path, 'rb') as file:
    config_data = file.read()

# File definitions for restoring
files_to_restore_empty = [  # Empty restore files
    FileToRestore(
        contents=b'',
        restore_path="/var/db/os_eligibility/",
        restore_name="eligibility.plist"
    ),
    FileToRestore(
        contents=b'',
        restore_path="/var/MobileAsset/AssetsV2/com_apple_MobileAsset_OSEligibility/purpose_auto/c55a421c053e10233e5bfc15c42fa6230e5639a9.asset/AssetData/",
        restore_name="Config.plist"
    ),
    FileToRestore(
        contents=b'',
        restore_path="/var/MobileAsset/AssetsV2/com_apple_MobileAsset_OSEligibility/purpose_auto/247556c634fc4cc4fd742f1b33af9abf194a986e.asset/AssetData/",
        restore_name="Config.plist"
    ),
    FileToRestore(
        contents=b'',
        restore_path="/var/MobileAsset/AssetsV2/com_apple_MobileAsset_OSEligibility/purpose_auto/250df115a1385cfaad96b5e3bf2a0053a9efed0f.asset/AssetData/",
        restore_name="Config.plist"
    ),
]

files_to_restore_patches = [  # Files to apply eligibility and config patches
    FileToRestore(
        contents=eligibility_data,
        restore_path="/var/db/os_eligibility/",
        restore_name="eligibility.plist"
    ),
    FileToRestore(
        contents=config_data,
        restore_path="/var/MobileAsset/AssetsV2/com_apple_MobileAsset_OSEligibility/purpose_auto/c55a421c053e10233e5bfc15c42fa6230e5639a9.asset/AssetData/",
        restore_name="Config.plist"
    ),
    FileToRestore(
        contents=config_data,
        restore_path="/var/MobileAsset/AssetsV2/com_apple_MobileAsset_OSEligibility/purpose_auto/247556c634fc4cc4fd742f1b33af9abf194a986e.asset/AssetData/",
        restore_name="Config.plist"
    ),
    FileToRestore(
        contents=config_data,
        restore_path="/var/MobileAsset/AssetsV2/com_apple_MobileAsset_OSEligibility/purpose_auto/250df115a1385cfaad96b5e3bf2a0053a9efed0f.asset/AssetData/",
        restore_name="Config.plist"
    ),
]

# Prompt the user for action
choice = prompt_for_action()

try:
    if choice == '1':
        retry_restore(files_to_restore_empty)
        print("Reboot the device now.")
        input("Press Enter after rebooting...")
    elif choice == '2':
        print("You need to restore with empty files first before applying patches.")
        print("Reboot the device before proceeding.")
        input("Press Enter after rebooting and restoring with empty files...")
        retry_restore(files_to_restore_patches)
        print("Reboot the device now.")
        input("Press Enter after rebooting...")
    elif choice == '3':
        retry_restore(files_to_restore_empty)  # First restore with empty files
        print("Reboot the device now.")
        input("Press Enter after rebooting...")
        retry_restore(files_to_restore_patches)  # Then restore with patches
        print("Reboot the device now.")
        input("Press Enter after rebooting...")
    else:
        print("Invalid choice. Please select 1, 2, or 3.")
except Exception as e:
    print(traceback.format_exc())
finally:
    input("Press Enter to exit...")
