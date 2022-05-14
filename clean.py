import os
import time


path = 'repos'

for dirpath, dirnames, filenames in os.walk(path):
    for f in filenames:
        full_path = os.path.join(dirpath, f)
        if full_path.endswith('.py'):
            print((f"Keeping {full_path}"))
        else:
            print((f"Deleting {full_path}"))
            os.remove(full_path)