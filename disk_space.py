import os
import shutil
from Convert import stringConvert


def disk_space():
    total, used, free = shutil.disk_usage(
        '/' if not os.name == 'posix' else str(input('\nEnter (root) USB drive path: ')))

    data_disk = {
            'du': f'Disk Usage: {stringConvert().formatBytes(used)} / {stringConvert().formatBytes(total)}',
            'fs': f'Free Space: {stringConvert().formatBytes(free)}'
        }

    print(f"\n{data_disk['du']} | {data_disk['fs']}")

if __name__ == '__main__':
    disk_space()