import pandas as pd 
import numpy as np
import re
import math
from collections import Counter

def compute_similarity(x:object,y:object)->float:
    """_summary_

    Args:
        x (object): featurized vector
        y (object): featurized vector

    Returns:
        float: cosine similarity
    """    
    return np.dot(x,y)/(np.linalg.norm(x)*np.linalg.norm(y)) 
 

def compute_k_similar_jobs(x:object,df:pd.DataFrame,url_col:str,k:int=5)->list:
    """Fetch top k jobs, given featurized resume X, dataset of jobs df, where url_col denotes the name of column, which stores job_urls

    Args:
        x (object): featurized resume
        df (pd.DataFrame): featurized dataset of all jobs
        url_col (str): name of column, that stores url
        k (int, optional): How many jobs we want to retrieve. Defaults to 5.

    Returns:
        list: list of top k jobs for our candidate, based on resume
    """    
    top_jobs=[]
    #PLACEHOLDER for dropping unnecessary columns. Only feature columns should stay
    temp_df=pd.append(df,x) #append the resume as last row
    np_df=temp_df.to_numpy() #cast to np.array for easier manipulation
    d= np_df.T @ np_df #matrix multiplication
    norm = (x * x).sum(0, keepdims=True) ** .5 #computing norm
    sims=d / norm / norm.T #computing cosine similarity
    sim_job=sims[-1] #we are only interested in last row as that is the one which has similarities from resume
    ind = np.argpartition(sim_job, -k)[-k:] #find the top k max indices in this row
    for i in ind:  #iteratively append job url as out list
        top_jobs.append(df.iloc[i,:][url_col])
    return top_jobs

def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


def text_to_vector(text):
    word = re.compile(r'\w+')
    words = word.findall(text)
    return Counter(words)


def get_result(content_a, content_b):
    """
    print(get_result('I love github', 'Who love github')) 
    """
    text1 = content_a
    text2 = content_b

    vector1 = text_to_vector(text1)
    vector2 = text_to_vector(text2)

    cosine_result = get_cosine(vector1, vector2)
    return cosine_result
