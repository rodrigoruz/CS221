import os
import glob
import pandas as pd
os.chdir("/mydir")

extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

print(all_filenames)
