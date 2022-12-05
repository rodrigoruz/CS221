import os
import glob
import pandas as pd
from extractor import extract_job_details
# os.chdir("/..") # if files are located in different directory
import sys

# setting path
sys.path.append('../extracurricular_scrapper')

# importing
from extracurricular_scrapper.extractor import extract_job_details

# using
geek_method()


filename = 'UpdatedResumeDataSet.csv'
df = pd.read_csv(filename)
category = df.Category.unique()
print(category)

# csv_to_dict_list -> gives list of dictionaries input
