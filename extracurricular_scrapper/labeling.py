import os
import glob
import pandas as pd
from extractor import extract_job_details
# os.chdir("/..") # if files are located in different directory

filename = 'UpdatedResumeDataSet.csv'
df = pd.read_csv(filename)
category = df.Category.unique()
print(category)
