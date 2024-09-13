from exploit.restore import restore_files
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
def restore(files, max_retries=3):
    for attempt in range(max_retries):
        try:
            restore_files(files=files, reboot=True)
            break  # Exit loop on success
        except ConnectionAbortedError:
            print(f"Connection aborted, retrying... ({attempt + 1}/{max_retries})")
            sleep(2)  # Pause before retrying
        except Exception as e:
            print(traceback.format_exc())
            break

# Function to prompt the user for an action
def prompt_for_action():
    print("Select an option:")
    print("1. Restore files with no data")
    print("2. Apply eligibility and config patches")
    print("3. Restore files with no data and apply patches")
    choice = input("Enter your choice (1, 2, or 3): ").strip()
    return choice