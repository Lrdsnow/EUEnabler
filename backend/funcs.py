from exploit.restore import FileToRestore

def prompt(options):
    print("Select an option:")
    print("\n".join(options))
    choice = input("Enter your choice: ")
    return choice

def retrieve_restore_files(eligibility_data, config_data):
    files = [
        FileToRestore(contents=eligibility_data, restore_path="/var/db/os_eligibility/", restore_name="eligibility.plist"),
        FileToRestore(contents=config_data, restore_path="/var/MobileAsset/AssetsV2/com_apple_MobileAsset_OSEligibility/purpose_auto/c55a421c053e10233e5bfc15c42fa6230e5639a9.asset/AssetData/", restore_name="Config.plist")
    ]
    return files
