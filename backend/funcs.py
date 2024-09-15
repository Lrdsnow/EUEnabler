from exploit.restore import FileToRestore
from pathlib import Path

def get_content(file_path):
    file_path = Path.joinpath(Path.cwd(), file_path)
    with open(file_path, 'rb') as file:
        file_data = file.read()
    print(f'Retrieved {file_path} content')
    return file_data

def prompt(options):
    print("Select an option:")
    print("\n".join(options))
    choice = input("Enter your choice: ")
    return choice

def retrieve_restore_files(eligibility_data, config_data):
    restore_paths = [
        "/var/MobileAsset/AssetsV2/com_apple_MobileAsset_OSEligibility/purpose_auto/c55a421c053e10233e5bfc15c42fa6230e5639a9.asset/AssetData/",
        "/var/MobileAsset/AssetsV2/com_apple_MobileAsset_OSEligibility/purpose_auto/247556c634fc4cc4fd742f1b33af9abf194a986e.asset/AssetData/",
        "/var/MobileAsset/AssetsV2/com_apple_MobileAsset_OSEligibility/purpose_auto/250df115a1385cfaad96b5e3bf2a0053a9efed0f.asset/AssetData/",
        "/var/MobileAsset/AssetsV2/com_apple_MobileAsset_OSEligibility/purpose_auto/2522c67bd46ddbd1bbadeb7c06bfdf77ddf7cc25.asset/AssetData/"
    ]
    
    files = [
        FileToRestore(contents=eligibility_data, restore_path="/var/db/os_eligibility/", restore_name="eligibility.plist")
    ] + [
        FileToRestore(contents=config_data, restore_path=path, restore_name="Config.plist") for path in restore_paths
    ]
    return files
