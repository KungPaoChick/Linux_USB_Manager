import os


def base_dirs():
    dirs_path = os.path.join(os.getcwd().split('scripts')[0], 'Distributions')
    if not os.path.exists(dirs_path):
        base_dirs = ['Arch-based', 'Debian-based', 'Independent',
                     'RedHat-based', 'Ubuntu-based']
        
        os.mkdir(dirs_path)
        for base in base_dirs:
            os.mkdir(os.path.join(dirs_path, base))
    else:
        print('[!] Directory already exists')


if __name__ == '__main__':
    base_dirs()