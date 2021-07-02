import os
import shutil


class Transfer_iso:
    
    def __init__(self, source, target):
        self.source = source
        self.target = target

    def move(self, distribution):
        # the source directory is always the Downloads folder
        # and the target directory would be the Distributions
        # but there would be a user input for the base distro
        # to know where the iso will be transferred

        base_set = {}
        for index, base in enumerate(os.listdir(self.target), start=1):
            base_set[index] = base
            print(f'{index} - {base}')

        try:
            # user can select which directory the image should be transferred
            fmt_path = os.path.split(distribution)[-1]
            select_base = int(input(f'\nEnter index to move "{fmt_path}" to its respectful base: '))

            # after selecting, if the input is valid; the image gets moved
            if select_base in base_set:
                print(f'[!] Moving: {fmt_path} to {base_set[select_base]}...')
                shutil.move(distribution, os.path.join(self.target, base_set[select_base]))

                if fmt_path in os.listdir(os.path.join(self.target, base_set[select_base])):
                    print(f'[*] {fmt_path} has been successfully moved!\n')
            else:
                print('\nAbort!')
        except KeyboardInterrupt:
            print('\nStopped!')

    def get_new_iso(self):
        # goes through the source directory; gets all .iso images
        images = []
        for iso in os.listdir(self.source):
            if iso.endswith('.iso'):
                images.append(os.path.join(self.source, iso))

        if images == []:
            print('[!] No new iso in source directory')
            quit()
        else:
            return images