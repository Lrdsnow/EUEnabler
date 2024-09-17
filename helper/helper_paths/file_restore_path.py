from exploit.restore import restore_files, FileToRestore, restore_file

from . import eligibility_path

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
]

files_to_restore_patches = [  # Files to apply eligibility and config patches
    FileToRestore(
        contents=eligibility_path.eligibility_data,
        restore_path="/var/db/os_eligibility/",
        restore_name="eligibility.plist"
    ),
    FileToRestore(
        contents=eligibility_path.config_data,
        restore_path="/var/MobileAsset/AssetsV2/com_apple_MobileAsset_OSEligibility/purpose_auto/c55a421c053e10233e5bfc15c42fa6230e5639a9.asset/AssetData/",
        restore_name="Config.plist"
    ),
]