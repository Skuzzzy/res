import os.path
import glob

files = glob.glob('./dumps/*.json')
order = sorted([(os.path.getmtime(path), path) for path in files])
for each in order:
    print each
