from exploit.restore import FileToRestore, restore_files
import json
from pathlib import Path
from pymobiledevice3.services.installation_proxy import InstallationProxyService

class EUTweak:
    def __init__(self, method="2"):
        print("Initializing...")
        self.files = []
        self.set_method(method)

    def set_method(self, method):
        self.method = method
    
    def setup_variables(self, dev_manager):
        try:
            with open(Path.joinpath(Path.cwd(), 'tweak/files/restore.json'), 'r') as json_file:
                json_data = json.load(json_file)

            for file_info in json_data["restore_files"]:
                file_to_restore_empty = FileToRestore(
                    contents=b'', 
                    restore_path=f"/{file_info['path']}", 
                    restore_name=file_info["file"]
                )
                file_to_restore = FileToRestore(
                    contents=open(Path.joinpath(Path.cwd(), f'tweak/files/{file_info["file"]}'), 'rb').read(), 
                    restore_path=f"/{file_info['path']}", 
                    restore_name=file_info["file"]
                )
                self.files.append({
                    "file_to_restore": file_to_restore,
                    "file_to_restore_empty": file_to_restore_empty,
                    "file_info": file_info
                })

            if not self.files:
                print("No valid files to restore.")

        except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
            print(f"Error during setup: {e}")

    def apply(self, dev_manager):
        self.setup_variables(dev_manager)
        for file_entry in self.files:
            file_to_restore = file_entry["file_to_restore"]
            file_info = file_entry["file_info"]
            print(f"Restoring {file_info.get('file')} to {file_info.get('path')}")
            restore_files([file_to_restore], reboot=False, lockdown_client=dev_manager.device.get("ld"))
        restore_files([], reboot=True, lockdown_client=dev_manager.device.get("ld"))
