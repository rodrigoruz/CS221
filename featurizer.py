import numpy as np
import csv
from enum import Enum
import spacy
import similarity_utils
import nltk
import gensim
import os
import utils

nltk.download('punkt')
spacy_nlp = spacy.load("en_core_web_sm")
GLOVE_FILE = "glove.6B.50d.txt"

EMBEDDING_SIZE = 50
OUTPUT_FILE = "results.txt"

class InputType(Enum):
    EXTRA = "extracurricular"
    RESUME = "resume"
    JOB = "job profile"

'''
Input: name of a CSV file containing documents
Output: list of dictionaries. Each dictionary represents one document. This is the dict to feed into the featurizer
'''
def preprocess(filename: str, job_file='raw_data_v2.csv', max_lines=100):
    if not os.path.exists(filename):
        if filename == job_file:
            utils.load_job_datasets(output_filename=job_file)
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        column_names, rows = [], []
        for i, line in enumerate(reader):
            if i == 0:
                column_names = line
            elif i > max_lines:
                break
            else:
                current = { column_names[j]: text 
                    for j, text in enumerate(line) }
                rows.append(current)
    return rows

# Map each word to its GLOVE embedding
# def create_embedding_dict():
#     embeddings_dict = {}
#     with open(GLOVE_FILE, 'r', encoding="utf-8") as f:
#         for line in f:
#             values = line.split()
#             word = values[0]
#             vector = np.asarray(values[1:], "float32")
#             embeddings_dict[word] = vector
#     return embeddings_dict

# Old featurization method: 
# 1. extract the keywords from the text using SPACY
# 2. Find the GLOVE embedding for the first 5 keywords (based on a precomputed dictionary). Skip if not found
# 3. Concentate the embeddings
# 4. Pad if fewer than 5 keywords were found, to ensure consistent length

# New featurization method:
# Feed all tokens into Word2Vec using Continuous Bag of Words model
# This gives us a 2d array of shape (num_words_in_bag, word_embedding_length)
# We average across rows to get a 1d array of shape (1, word_embedding_length)
def featurize(input: dict, input_type: str):
    """
    Parameters: 
    input dictionary that takes keys as column names and values as text
    """
    relevant_fields = {
        InputType.EXTRA.value: ['Description', 'Requirements'],
        InputType.RESUME.value: ['Resume'],
        InputType.JOB.value: ['quals', 'desc']
    }
    text = " ".join([input[field].replace("\n", " ") for field in relevant_fields[input_type]])
    tokens = []
    for i, sentence in enumerate(nltk.sent_tokenize(text)):
        for word in nltk.word_tokenize(sentence):
            tokens.append(word.lower())
    #Bag of words model:
    model = gensim.models.Word2Vec(tokens, min_count=1, vector_size=100, window=5)
    model.save("featurizer.model")
    vector = np.sum(model.syn1neg, axis=0) / model.syn1neg.shape[0]
    # keywords = spacy_nlp(text).ents
    # vector = np.asarray([], dtype="float32")
    # for word in keywords[:num_keywords]:
    #     word_vec = embeddings_dict.get(str(word).lower(), [])
    #     if len(word_vec) > 0:
    #         vector = np.concatenate((vector, word_vec))
    # padding = [0.0 for i in range(num_keywords * EMBEDDING_SIZE - len(vector))]
    # vector = np.concatenate((vector, padding))
    return vector

def create_feature_vectors(current_inputs, input_type):
    return np.vstack([featurize(input, input_type) for input in current_inputs])

def save_vectors_to_txt(vectors: list):
    with open(OUTPUT_FILE, 'w') as f:
        text = ""
        for i, input_name in enumerate(["EXTRACURRICULARS", "RESUMES", "JOB PROFILES"]):
            vec_text = "\n ".join([str(list(vec)) for vec in vectors[i]])
            text = f"{text} \n {input_name}:\n{vec_text}"
        f.write(text)





        
        
    
    
    

    

