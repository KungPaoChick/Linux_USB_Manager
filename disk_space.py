import os
import shutil
from Convert import stringConvert

def disk_space():
    cv = stringConvert()
    total, used, free = shutil.disk_usage(
        '/' if not os.name == 'posix' else ''.join(os.getcwd().split('scripts')))

    data_disk = {
            'du': f'Disk Usage: {cv.formatBytes(used)} / {cv.formatBytes(total)}',
            'fs': f'Free Space: {cv.formatBytes(free)}'
        }
    print(f"\n{data_disk['du']} | {data_disk['fs']}")

if __name__ == '__main__':
    disk_space()
