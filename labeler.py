import pandas as pd
import numpy as np


label_mapping=['Data Science','HR','Advocate','Arts','Web Designing',
 'Mechanical Engineer','Sales','Health and fitness','Civil Engineer'
 'Java Developer','Business Analyst','SAP Developer','Automation Testing'
 'Electrical Engineering','Operations Manager','Python Developer'
 'DevOps Engineer','Network Security Engineer','PMO','Database','Hadoop'
 'ETL Developer','DotNet Developer','Blockchain','Testing']


def generate_label(mapping:list,description:str)->list:
    """Given a string and a list of all possible label, return a subset of labels which 
    were present in the provided string.

    Args:
        mapping (list): list of all possible labels for given job
        description (str): string, where we want to check for occurrence of labels.

    Returns:
        list: subset of labels, that were present in given string
    """    
    labels=[]
    for l in mapping:
        if l.lower() in description.lower():
            labels.append(l)
    return labels

def perform_labeling(raw_data, output_filename):

    rw_df=pd.read_csv(raw_data)


    data=pd.read_csv('https://raw.githubusercontent.com/rodrigoruz/CS221/main/extracurricular_scrapper/combined_extracurricular.csv')


    candidates_tags=[]

    for x in data['Tags']:
    #iterating through all tags in extracurriculars
        try:

            candidates_tags.append(generate_label(label_mapping,x))

        except:

            candidates_tags.append([])

    candidates_desc=[]

    for x in data['Description']:

        try:

            candidates_desc.append(generate_label(label_mapping,x))

        except:

            candidates_desc.append([])

    candidates_req=[]
    for x in data['Requirements']:
        try:
            candidates_req.append(generate_label(label_mapping,x))
        except:
            candidates_req.append([])


    conc_list=[list(set(a + b + c)) for a, b, c in list(zip(candidates_desc, candidates_tags,candidates_req))] #merging all possible tags from 3 different sources and removing duplicates

    data['Label']=conc_list


    candidates_job_desc=[]
    for x in rw_df.desc:
        #labeling in jobs dataset
        try:
            candidates_job_desc.append(generate_label(label_mapping,x))
        except:
            candidates_job_desc.append([])

    rw_df['label']=candidates_job_desc
    rw_df.to_csv(output_filename, encoding='utf-8')
    return rw_df['label'].tolist()