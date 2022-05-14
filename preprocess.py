import os
import subprocess
from tqdm import tqdm

MAX_CHAR_LENGTH = 512
MIN_CHAR_LENGTH = 256

NEW_LINE_CHAR = "<N>"


full_paths = []
for dirpath, dirnames, filenames in os.walk('repos'):
    for f in filenames:
        full_path = os.path.join(dirpath, f)
        if full_path.endswith('.py'):
            full_paths.append(full_path)

fpaths_len = len(full_paths)
print(f"Full paths count: {fpaths_len}")


with open('data.txt', 'w', encoding='utf-8') as f:
    with tqdm(total=fpaths_len) as progress_bar:
        for full_path in full_paths:
            try:
                d = open(full_path, 'r', encoding='utf-8').read()
                fd = d.replace('\n', NEW_LINE_CHAR)
                if 100 < len(d) <= MAX_CHAR_LENGTH:
                    f.write(fd+'\n')

                else:
                    sd = fd.split(f"{NEW_LINE_CHAR}{NEW_LINE_CHAR}")
                    substring = ""
                    for s in sd:
                        substring += s + f"{NEW_LINE_CHAR}{NEW_LINE_CHAR}"
                        if MIN_CHAR_LENGTH <= len(substring) <= MAX_CHAR_LENGTH:
                            f.write(substring+'\n')
                            substring = ""
            except Exception as e:
                print(e)
            progress_bar.update(1)
