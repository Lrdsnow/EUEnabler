from backend.funcs import get_content, prompt, retrieve_restore_files
from exploit.restore import restore_files

print("Initializing...")

# initializing variables

config_data = get_content('Config.plist')
eligibility_data = get_content('eligibility.plist')

files_to_restore_empty = retrieve_restore_files(False)
files_to_restore = retrieve_restore_files(True, eligibility_data, config_data)

prompt_options = [
    "1. Restore files with no data",
    "2. Apply eligibility and config patches",
    "3. Restore files with no data and apply patches"
]

choice = prompt(prompt_options)

switcher = {
    '1': lambda: restore_files(files_to_restore_empty, reboot=True),
    '2': lambda: (input("Press Enter after running method 1..."), restore_files(files_to_restore, reboot=True)),
    '3': lambda: (restore_files(files_to_restore_empty, reboot=True), input("Press Enter after rebooting and unlocking..."), restore_files(files_to_restore, reboot=True))
}

try:
    switcher.get(choice, lambda: print("Invalid choice. Please select 1, 2, or 3."))()
except Exception as e:
    print(f"An error occurred: {e}")