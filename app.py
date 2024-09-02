import restore
from pathlib import Path
import plistlib

region_code = input("Enter your 2-letter region code (default to US): ").strip().upper() or "US"

def replace_region_code(plist_path, original_code="US", new_code="US"):
    with open(plist_path, 'rb') as f:
        plist_data = plistlib.load(f)
    
    plist_str = str(plist_data)
    updated_plist_str = plist_str.replace(original_code, new_code)
    updated_plist_data = eval(updated_plist_str)  # Convert string back to dictionary

    with open(plist_path, 'wb') as f:
        plistlib.dump(updated_plist_data, f)

file_path = Path.joinpath(Path.cwd(), 'eligibility.plist')
replace_region_code(file_path, original_code="US", new_code=region_code)
restore_file(fp=file_path, restore_path='/var/db/os_eligibility/', restore_name='eligibility.plist')

file_path = Path.joinpath(Path.cwd(), 'Config.plist')
replace_region_code(file_path, original_code="US", new_code=region_code)
restore_file(fp=file_path, restore_path='/var/MobileAsset/AssetsV2/com_apple_MobileAsset_OSEligibility/purpose_auto/c55a421c053e10233e5bfc15c42fa6230e5639a9.asset/AssetData/', restore_name='Config.plist')

print("Reboot to see changes!")