"""
Extracurricular recommendations done with Spacy. 
Once the document is read, a simple api similarity can be used to find the cosine similarity 
between the document vectors. We need to install the package and download the model:

$ pip install spacy
$ python -m spacy download en_core_web_sm
"""

# import os
# import glob
import pandas as pd
# from extractor import extract_job_details
# import sys
from pathlib import Path
import spacy
nlp = spacy.load('en_core_web_sm')
string1 = u'Hello hi there!'
string2 = u'Hello hi there!'
string3 = u'Hey whatsup?'
string4 = u'Hey whats the day looking like?'
string5 = u'Hey my name is'
doc1 = nlp(string1)
doc2 = nlp(string2)
doc3 = nlp(string3)
doc4 = nlp(string4)
doc5 = nlp(string5)

# print (doc1.similarity(doc2)) # 1.0
# print (doc2.similarity(doc3)) # 0.3977804622226361
# print (doc1.similarity(doc3)) # 0.3977804622226361
# print (doc1.similarity(doc4)) # 0.4393414342057937
# print (doc1.similarity(doc5)) # 0.29307694741965834

# Problem: How to make doc4 increase similarity from 0.29 to resemble doc 1
# Function that adds the other available strings (str 3 and str 4)and chooses which 
# one best complements str5 to resemble str1

def best_complement(base,target,list_possible_strings):
    """
    This function takes a base string and seeks to make it more cosine
    similar to the target string by adding to it a string from the 
    list_possible_strings
    """
    best_option = ""
    sim_score = 0
    doc_base = nlp(base)
    doc_target = nlp(target)
    doc_ideal = nlp(base + ' ' + target)
    print(doc_target.similarity(doc_base)) # Sanity check: better than original
    print(doc_target.similarity(doc_ideal)) # Sanity check: worse than ideal
    for i in list_possible_strings:
        doc_new = nlp(base + ' ' + i)
        new_sim_score = doc_target.similarity(doc_new) 
        print(list_possible_strings.index(i))
        if new_sim_score > sim_score:
            sim_score = new_sim_score
            print(sim_score,list_possible_strings.index(i))

        # print(string1.similarity(i))
    # Sanity check, the output should be better than adding the target string or the base string
        #  Add the two desired strings, that would be ideal similarity
        # string_ideal = string1 + ' ' + string4
        # doc_ideal = nlp(string_ideal)
        # print (doc1.similarity(doc_ideal))

job1 = """
DESCRIPTION
The WW Targeting team is building the next generation of products and services that will fuel the future growth of Amazon’s ad solutions. Based in the beautiful cities of Edinburgh, Seattle and Boulder, our teams are developing innovations to support advertisers at massive scale. We are responsible for defining and delivering ad targeting products to help advertisers plan media, gain insights about customer behaviours, create audience strategies, and more.

Our products are at the heart of our display advertising business. We ensure that billions of ads served are relevant to our customers. We are highly motivated, collaborative and fun-loving with an entrepreneurial spirit and bias for action. With a broad mandate to experiment and innovate, we are growing at an unprecedented rate with a seemingly endless range of new opportunities.


The advertising industry is going through massive changes to better support user privacy and we are making foundational changes to how digital ads are served in the coming years. We are looking for an outstanding candidate to join us as a full-time Principal Scientist working in a dynamic environment where your products will touch millions of customers every day and have massive impact. If you are a self-starter and enjoy applying cutting edge science to ambiguous real world problems, look no further.


As a Principal Scientist on the Targeting team your core efforts will involve the development of Machine Learning (ML) models which match users to ads to increase relevance for customers and performance for advertisers. You will invent ML targeting and optimization approaches using a broad array of contextual and behavioural signals (when available) and your models will integrate into bidding systems which operate at low latency and a huge scale. The senior nature of this role means you will operate across multiple programs, influencing modelling frameworks and approaches and working closely with scientists, economists, engineers and business leaders to translate business and functional requirements into concrete deliverables, including design, development and testing. You will act as a thought leader and forward thinker on the team anticipating obstacles to success and helping us avoid common failure modes. You will hire and coach junior scientists and partner with engineering leaders to build efficient scalable systems.

This is a unique, high visibility opportunity for a talented, motivated individual to deliver direct impact to Amazon shoppers and advertisers, to have business impact, and to dive deep into high-scale low latency problems at the cutting edge of machine learning and optimization. This role offers a compelling mix of contemporary research problems that are unique to Amazon based on the interplay between retail and advertising, scale and richness of data sets, emphasis on user experience and relevance, and complexity introduced by massive scale and concurrent experimentation across teams. In addition, you will deliver significant customer and business impact by shaping the future of the Amazon advertising experience and delivering growth to the advertising business.


BASIC QUALIFICATIONS
PhD in Computer Science, Mathematics, Statistics, or a related quantitative field. Experience in lieu will be considered.
Proven industry experience building successful production software systems
Extensive experience of applied research
Experience with one of the following areas: machine learning technologies, Reinforcement Learning, Deep Learning, Natural Language Processing (NLP), information retrieval and related applications
Proven ability to implement, operate, and deliver results via innovation at large scale
Experience in modern programming languages (Python, Java, C++, C)
Computer Science fundamentals in data structures, algorithm design, statistics and system design
Experience communicating with executives and non-technical leaders
PREFERRED QUALIFICATIONS
Significant peer reviewed scientific contributions in Reinforcement Learning, Deep Learning, Natural Language Processing, and related field
Extensive experience applying theoretical models in an applied environment
Expertise on a broad set of ML approaches and techniques, ranging from Artificial Neural Networks to Bayesian Non-Parametrics methods
Expert in more than one more major programming languages (C++, Java, or similar) and at least one scripting language (Python or similar)
Strong fundamentals in problem solving, algorithm design and complexity analysis
Experience with defining organizational research and development practices in an industry setting
Proven track in leading, mentoring and growing teams of scientists (teams of five or more scientist)"""

if __name__ == "__main__":

    ####### . Vanilla Example #####
    # list_possible_strings = [string3, string4]
    # best_complement(string5,string1,list_possible_strings)

    ####### Extracurricular Dataset #####
    # Obtain extracurricular dataset list with opportunity description
    filename = 'combined_extracurricular.csv'
    df = pd.read_csv(filename, low_memory=False)
    df =  df[["Label","Title","Description","Tags","Location","Start Date","Requirements"]] # select relevant columns
    col_list = df.Description.values.tolist() # Using Series.values.tolist()
    col_list = col_list[0:200] # first 4 extracurricular opportunities
    # Obtain resume dataset
    filename2 = 'UpdatedResumeDataSet.csv'
    df2 = pd.read_csv(Path(__file__).parent/filename2)
    col_list2 = df2.Resume.values.tolist() # Using Series.values.tolist()
    text_user_1 = col_list2[0]
    # print(text_user_1) #CS profile
    # Obtain Job Dataset
    # filename3 = 'raw_data.csv'
    # print(Path(__file__).parent/filename3)
    # df3 = pd.read_csv(Path(__file__).parent/filename3)
    # print(df3.columns)
    # print(job1)

    # list_possible_strings = [string3, string4]
    best_complement(text_user_1,job1,col_list)
    # docsamplejob = nlp(job1)
    # docsampleuser = nlp(text_user_1)
    # print (docsamplejob.similarity(docsampleuser)) # 1.0
    
