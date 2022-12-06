import glob
import pandas as pd

def combine_datasets(all_filenames, output_filename):
    """
    Function that concatenates the files from the job dataset to load the data in the desired format
    """
    #combine all files in the list
    df = pd.concat([pd.read_csv(f) for f in all_filenames ])
    df.to_csv(output_filename, encoding='utf-8')

def load_job_datasets(output_filename):
    extension = 'csv'
    all_filenames = [i for i in glob.glob('raw_data*.{}'.format(extension))]
    combine_datasets(all_filenames, output_filename)
