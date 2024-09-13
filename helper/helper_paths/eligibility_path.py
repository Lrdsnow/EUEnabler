from pathlib import Path

# Paths to plist files
file_path = Path.joinpath(Path.cwd(), 'eligibility.plist')
with open(file_path, 'rb') as file:
    eligibility_data = file.read()
file_path = Path.joinpath(Path.cwd(), 'Config.plist')
with open(file_path, 'rb') as file:
    config_data = file.read()