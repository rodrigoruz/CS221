"""
Extracurricular recommendations done with Spacy. 
Once the document is read, a simple api similarity can be used to find the cosine similarity 
between the document vectors. We need to install the package and download the model:

$ pip install spacy
$ python -m spacy download en_core_web_sm
"""

import pandas as pd
import numpy as np
from pathlib import Path
import plotly.graph_objects as go
import spacy
nlp = spacy.load('en_core_web_sm')

def best_complement(base: str, target: str, list_possible_strings:list):
    """
    This function attempts to make the base string more cosine
    similar to the target string by adding to it a string from the 
    list_possible_strings
    Input:
    base: str, original string
    target: str, target string to which we want the base string to resemble
    list_possible_strings: list[str], list of strings that can complement base

    Returns:
    sim_score: flt, best score
    list_possible_strings.index(i): int, index corresponding to best recommendation in list

    """
    best_option = ""
    sim_score = 0
    doc_base = nlp(base)
    doc_target = nlp(target)
    doc_ideal = nlp(base + ' ' + target)
    original_score = doc_target.similarity(doc_base) # Sanity check: better than original
    ideal_score = doc_target.similarity(doc_ideal) # Sanity check: worse than ideal
    # Compare with the extracurricular dataset
    for i in list_possible_strings:
        doc_new = nlp(base + ' ' + i)
        new_sim_score = doc_target.similarity(doc_new) 
        if new_sim_score > sim_score:
            sim_score = new_sim_score
    return sim_score, list_possible_strings.index(i), original_score

if __name__ == "__main__":
    ####### Obtain job recommendations for each user by running featurizer.py #####
    #run featurizer.py
    new_num_arr = np.load('data.npy') # load the recommended jobs to the user

    ####### Load Extracurricular Dataset #####
    # Obtain extracurricular dataset list with opportunity description
    filename = 'combined_extracurricular_labeled.csv'
    df = pd.read_csv(filename, low_memory=False)
    df =  df[["Label","Title","Description","Tags","Requirements"]] # select relevant columns
    col_list = df.Description.values.tolist() # Using Series.values.tolist()
    col_list = col_list[0:3] # first 4 extracurricular opportunities
    # # Obtain resume dataset
    filename2 = 'UpdatedResumeDataSet.csv'
    df2 = pd.read_csv(Path(__file__).parent/filename2)
    col_list2 = df2.Resume.values.tolist() # Using Series.values.tolist()
    text_user_1 = col_list2[0]
    # print(text_user_1) #CS profile
    
    ###### Obtain data from the recommended jobs ####### 
    filename3 = "../raw_data_0.csv"
    df3 = pd.read_csv(filename3)
    k = 5 # number of recommended jobs by featurizer.py
    for i in range(k):
        job_index = new_num_arr[0][i] # index of the k jobs recommended to the user
        job_desc = df3['desc'][job_index] # description for the job
        job_label = df3['labels'][job_index] # label for the job
        # job_quals = df3['qual'][job_index] # qualifications for the job
        # job_details = df3['details'][job_index] # details for the job
        
        # Compute similarity score for first user
        best_sim_score, best_index, original_score = best_complement(text_user_1,job_desc,col_list)
        # extract best extracurricular recommendation
        if i == 0:
            final_best_sim_score = best_sim_score
            final_best_index = best_index
            final_original_score = original_score
            final_job_label = job_label 
        else:
            # If the recommendation improves in one of the iterations, replace
            if (best_sim_score > final_best_sim_score):
                final_best_sim_score = best_sim_score
                final_best_index = best_index
                final_original_score = original_score
                final_job_label = job_label 

    # Get data of the best extracurricular recommendation
    print(final_best_sim_score, final_best_index, final_original_score)
    label_extracurricular = df['Label'][final_best_index]
    title_extracurricular = df['Title'][final_best_index]

    ## We compare these two to get an accuracy measurement
    print(label_extracurricular,title_extracurricular)
    print(final_job_label) # label for the job
    a_set = set(final_job_label)
    correct_recommendation = any(x in a_set for x in label_extracurricular) # True if label is right, false if its not
    print(correct_recommendation)


    # ##### Create Radar Chart
    # categories = ['Data Science','HR','Advocate','Arts','Web Designing',
    # 'Mechanical Engineer','Sales','Health and fitness','Civil Engineer','Java Developer',
    # 'Business Analyst','SAP Developer','Automation Testing','Electrical Engineering',
    # 'Operations Manager','Python Developer','DevOps Engineer','Network Security Engineer',
    # 'PMO','Database','Hadoop','ETL Developer','DotNet Developer','Blockchain','Testing']

    # fig = go.Figure()

    # fig.add_trace(go.Scatterpolar(
    #     r=[original_score*3, 1.1, 1.1, 1.1, 1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1],
    #     theta=categories,
    #     fill='toself',
    #     name='Product A'
    # ))
    # fig.add_trace(go.Scatterpolar(
    #     r=[best_sim_score*5, 1, 1, 1, 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    #     theta=categories,
    #     fill='toself',
    #     name='Product B',
    #     opacity=0.5
    # ))

    # fig.update_layout(
    # polar=dict(
    #     radialaxis=dict(
    #     visible=True,
    #     range=[0, 5]
    #     )),
    # showlegend=False
    # )

    # fig.show()
