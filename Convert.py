class stringConvert:

    def formatBytes(self, size_bytes):
        power = 2**10
        n = 0
        power_labels = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
        while size_bytes > power:
            size_bytes /= power
            n += 1
        return f'{round(size_bytes, 2)}{power_labels[n]}b'

    def plural_s(self, v):
        return 's' if not abs(v) < 1 else ''