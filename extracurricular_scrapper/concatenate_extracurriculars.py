import os
import glob
import pandas as pd
# os.chdir("/mydir") # if files are located in different directory

extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
#export to csv
combined_csv.to_csv( "combined_extracurricular.csv", index=False, encoding='utf-8-sig')
