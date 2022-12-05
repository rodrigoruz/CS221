import glob
import pandas as pd

def load_job_dataset():
    """
    Function that concatenates the files from the job dataset to load the data in the desired format
    """
    extension = 'csv'
    all_filenames = [i for i in glob.glob('raw_data*.{}'.format(extension))]
    #combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
    return combined_csv
df = load_job_dataset()
print(df)
