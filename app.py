from exploit.restore import restore_file
from pathlib import Path
import plistlib

region_code = input("Enter YOUR 2-letter region code (default to US): ").strip().upper() or "US"
method = int(input("Choose a method, 1 or 2:")) or 1

def replace_region_code(plist_path, original_code="US", new_code="US"):
    with open(plist_path, 'rb') as f:
        plist_data = plistlib.load(f)
    
    plist_str = str(plist_data)
    updated_plist_str = plist_str.replace(original_code, new_code)
    updated_plist_data = eval(updated_plist_str)  # Convert string back to dictionary

    with open(plist_path, 'wb') as f:
        plistlib.dump(updated_plist_data, f)

file_path = Path.joinpath(Path.cwd(), 'eligibility.plist')
if region_code != "US":
    replace_region_code(file_path, original_code="US", new_code=region_code)
restore_file(fp=file_path, restore_path='/var/db/os_eligibility/', restore_name='eligibility.plist')

file_path = Path.joinpath(Path.cwd(), 'Config.plist')
if region_code != "US":
    replace_region_code(file_path, original_code="US", new_code=region_code)
if method == 1:
    restore_file(fp=file_path, restore_path='/var/MobileAsset/AssetsV2/com_apple_MobileAsset_OSEligibility/purpose_auto/c55a421c053e10233e5bfc15c42fa6230e5639a9.asset/AssetData/', restore_name='Config.plist')
elif method == 2:
    restore_file(fp=file_path, restore_path='/var/MobileAsset/AssetsV2/com_apple_MobileAsset_OSEligibility/purpose_auto/247556c634fc4cc4fd742f1b33af9abf194a986e.asset/AssetData/', restore_name='Config.plist')

print("Reboot to see changes!")
