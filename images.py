import os
import json
import shutil
from TransferISO import Manage_iso
from Convert import stringConvert
from argparse import ArgumentParser, RawDescriptionHelpFormatter


class Images:

    def check_new_iso(self):
        source_iso = os.path.join(os.path.expanduser('~'), 'Downloads')
        target = os.path.join(''.join(os.getcwd().split('scripts')), 'Distributions')

        main_class = Manage_iso(source_iso, target)
        new_iso = main_class.get_new_iso()

        total_size = 0
        for image in new_iso:
            fmt_iso = os.path.split(image)[-1]
            size = os.path.getsize(image)
            
            total_size += size
            print(f"[*] Found: {fmt_iso}, {stringConvert().formatBytes(size)}")

        fmt_total = stringConvert().formatBytes(total_size)
        total_disk, used_disk, free_disk = shutil.disk_usage(
            '/' if not os.name == 'posix' else ''.join(os.getcwd().split('scripts')))

        data_disk = {
            'du': f'Disk Usage: {stringConvert().formatBytes(used_disk)} / {stringConvert().formatBytes(total_disk)}',
            'fs': f'Free Space: {stringConvert().formatBytes(free_disk)}',
            'mvd': stringConvert().formatBytes(used_disk + total_size)
        }
        print(f"\nTotal Size: {fmt_total} | {data_disk['du']}")
        print(f"Disk Usage if moved: {data_disk['mvd']}")

        if (used_disk + total_size) >= total_disk:
            print('[!!] There is no sufficient space left')
        else:
            try:
                iso_len = len(new_iso)
                confirm_move = input(f'\nMove {iso_len} iso image{stringConvert().plural_s(iso_len)}? ')
    
                if confirm_move == 'y' or confirm_move == 'Y':    
                    main_class.move(new_iso)
                else:
                    print('\nAbort!')
            except KeyboardInterrupt:
                print('\nStopped!')

    def delete_distro(self):
        source = os.path.join(''.join(os.getcwd().split('scripts')), 'Distributions')

        distributions = []
        for root, dirs, files in os.walk(source):
            for f in files:
                distributions.append(os.path.join(root, f))

        distributions.sort()
        distro_dict = {}
        for index, distro in enumerate(distributions, start=1):
            distro_dict[index] = distro

            distro_size = stringConvert().formatBytes(os.path.getsize(distro))
            print(f'{index} - {os.path.split(distro)[-1]}, {distro_size}')

        try:
            select_delete = int(input('\nEnter the index of the distro you want to delete: '))

            if select_delete in distro_dict:
                target = distro_dict[select_delete]

                fmt_target = os.path.split(target)[-1]
                target_size = stringConvert().formatBytes(os.path.getsize(target))
                
                try:
                    confirm_delete = str(input(f'[!] Deleting "{fmt_target}" will free "{target_size}" of storage, continue? '))
                    if confirm_delete == 'y' or confirm_delete == 'Y':
                        Manage_iso(source, target).delete(target)
                    else:
                        print('\nAbort!')
                except KeyboardInterrupt:
                    print('\nStopped!')

            else:
                print('\nAbort!')
        except KeyboardInterrupt:
            print('\nStopped!')
                
    def count_iso(self):
        images, bases = [], []
        source = JSON_Data().read_json()
        target_path = os.path.join(''.join(os.getcwd().split('scripts')), 'Distributions')
        for root, dirs, files in os.walk(target_path):
            if not dirs == []:
                for category in dirs:
                    bases.append([root, category])
        
            for file in files:
                if file.endswith('.iso'):
                    images.append(os.path.join(root, file))
                else:
                    print(f"{os.path.join(root, file)} is not an image file")
    
        Images().mk_inventory(images, bases) 
        for option in source['config']:
            if option['show-images']:
                for image in images:
                    if not option['root-dir']:
                        print(image.split('Distributions')[1])
                    else:
                        print(image)

        print(f"\niso Images: {len(images)}")

    def mk_inventory(self, iso_files, base_dirs):
        inventory = {'info': [], 'contents': []}
        total = 0
        for base in base_dirs:
            folder_size = 0
            for dir in os.scandir(os.path.join(base[0], base[1])):
                folder_size += os.path.getsize(dir)
                total += os.path.getsize(dir)

            for img in [os.listdir(os.path.join(base[0], base[1]))]:
                iso_dataset = {}
                for iso in img:
                    iso_dataset[iso] = stringConvert().formatBytes(
                    os.path.getsize(os.path.join(base[0], base[1], iso)))
                inventory['contents'].append({
                    base[1]: {'total_iso': len(iso_dataset),
                              'total_size': stringConvert().formatBytes(folder_size),
                              'iso_images': iso_dataset}
                })
        inventory['info'].append({
            'total_iso': len(iso_files),
            'total_size': stringConvert().formatBytes(total)
        })
        return JSON_Data().write_json(inventory)


class JSON_Data:

    def __init__(self, config='config.json', inventory='inventory.json'):
        self.config = config
        self.inventory = inventory

    def read_json(self):
        with open(os.path.join(os.getcwd(), self.config), 'r', encoding='utf-8') as j_source:
            return json.load(j_source)    

    def write_json(self, dataset):
        with open(self.inventory, 'w', encoding='utf-8') as f_source:
            return json.dump(dataset, f_source, indent=2)


if __name__ == '__main__':
    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter)

    parser.add_argument('--check-downloads',
                        action='store_true',
                        help='Checks Downloads directory for new iso downloads')

    parser.add_argument('--delete-iso',
                        action='store_true',
                        help='Deletes a distro/iso image')
    
    args = parser.parse_args()
    if args.check_downloads:
        Images().check_new_iso()
    elif args.delete_iso:
        Images().delete_distro()
    else:
        if os.path.exists(os.path.join(os.getcwd(), 'config.json')):
            Images().count_iso()
        else:
            print("Script cannot cooperate without the following dependency: config.json")
