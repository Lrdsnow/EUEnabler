from exploit.restore import restore_file
from pathlib import Path

file_path = Path.joinpath(Path.cwd(), 'eligibility.plist')
restore_file(fp=file_path, restore_path='/var/db/os_eligibility/', restore_name='eligibility.plist')

file_path = Path.joinpath(Path.cwd(), 'Config.plist')
restore_file(fp=file_path, restore_path='/var/MobileAsset/AssetsV2/com_apple_MobileAsset_OSEligibility/purpose_auto/c55a421c053e10233e5bfc15c42fa6230e5639a9.asset/AssetData/', restore_name='Config.plist')

print("Reboot to see changes!")