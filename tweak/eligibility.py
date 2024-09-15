from backend.funcs import get_content, prompt, retrieve_restore_files
from exploit.restore import restore_files
from pathlib import Path
from pymobiledevice3.exceptions import PyMobileDevice3Exception
from time import sleep

class EUTweak:
    def __init__(self, method="1"):
        self.method = method

    def setup_variables(self, lockdown=None):
        file_path = Path.joinpath(Path.cwd(), 'tweak/files/eligibility.plist')
        with open(file_path, 'rb') as file:
            self.eligibility_data = file.read()
        file_path = Path.joinpath(Path.cwd(), 'tweak/files/Config.plist')
        with open(file_path, 'rb') as file:
            self.config_data = file.read()

        self.files_to_restore_empty = retrieve_restore_files(b'', b'')
        self.files_to_restore = retrieve_restore_files(self.eligibility_data, self.config_data)

        self.switcher = {
            "1": lambda: restore_files(self.files_to_restore_empty, reboot=True, lockdown_client=lockdown),
            "2": lambda: restore_files(self.files_to_restore, reboot=True, lockdown_client=lockdown),
            "3": lambda: (restore_files(self.files_to_restore_empty, reboot=True, lockdown_client=lockdown), input("Press Enter after rebooting and unlocking..."), restore_files(self.files_to_restore, reboot=True, lockdown_client=lockdown))
        }

    def apply(self, lockdown=None):
        self.setup_variables()
        try:
            if self.method != "4":
                self.switcher.get(self.method, lambda: print("Invalid choice. Please select 1, 2, or 3."))()
            else:
                while True:
                    restore_files(self.files_to_restore, reboot=True, lockdown_client=lockdown)
                    sleep(30)
        except PyMobileDevice3Exception as e:
            print(f"An error occurred: {e}")
