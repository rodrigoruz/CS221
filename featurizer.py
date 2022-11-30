import numpy as np
import csv
from enum import Enum
import spacy
import similarity_utils

spacy_nlp = spacy.load("en_core_web_sm")
GLOVE_FILE = "glove.6B.50d.txt"
EXTRA_FILE = "OYA_AcademicJobs.csv"
RESUME_FILE = "UpdatedResumeDataset.csv"
JOB_FILE = "raw_data_v2.csv"
EMBEDDING_SIZE = 50
OUTPUT_FILE = "results.txt"

class InputType(Enum):
    JOB = "job profile"
    RESUME = "resume"
    EXTRA = "extracurricular"

def file_to_csv(filename: str, max_lines=100):
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
def create_embedding_dict():
    embeddings_dict = {}
    with open(GLOVE_FILE, 'r', encoding="utf-8") as f:
        for line in f:
            values = line.split()
            word = values[0]
            vector = np.asarray(values[1:], "float32")
            embeddings_dict[word] = vector
    return embeddings_dict

# Featurization method: 
# 1. extract the keywords from the text using SPACY
# 2. Find the GLOVE embedding for the first 5 keywords (based on a precomputed dictionary). Skip if not found
# 3. Concentate the embeddings
# 4. Pad if fewer than 5 keywords were found, to ensure consistent length
def featurize(input: dict, input_type: str, num_keywords=5):
    relevant_fields = {
        InputType.EXTRA.value: ['Requisitos', 'Descripcion'],
        InputType.RESUME.value: ['Resume'],
        InputType.JOB.value: ['quals', 'desc']
    }
    text = " ".join([input[field] for field in relevant_fields[input_type]])
    keywords = spacy_nlp(text).ents
    vector = np.asarray([], dtype="float32")
    for word in keywords[:num_keywords]:
        word_vec = embeddings_dict.get(str(word).lower(), [])
        if len(word_vec) > 0:
            vector = np.concatenate((vector, word_vec))
    padding = [0.0 for i in range(num_keywords * EMBEDDING_SIZE - len(vector))]
    vector = np.concatenate((vector, padding))
    return vector

def create_feature_vectors(csv_data: str, input_type: str):
    return np.vstack((featurize(d, input_type) for d in csv_data))

def save_vectors_to_txt(vectors: list):
    with open(OUTPUT_FILE, 'w') as f:
        text = ""
        for i, input_name in enumerate(["EXTRACURRICULARS", "RESUMES", "JOB PROFILES"]):
            vec_text = "\n ".join([str(list(vec)) for vec in vectors[i]])
            text = f"{text} \n {input_name}:\n{vec_text}"
        f.write(text)

if __name__ == "__main__":
    embeddings_dict = create_embedding_dict()
    extra_csv, resume_csv, job_csv = [file_to_csv(filename) for filename in (EXTRA_FILE, RESUME_FILE, JOB_FILE)]
    params = [(extra_csv, InputType.EXTRA.value), 
        (resume_csv, InputType.RESUME.value), (job_csv, InputType.JOB.value)]
    extracurriculars, resumes, jobs = [create_feature_vectors(csv_file, input_type)
        for csv_file, input_type in params]
    save_vectors_to_txt([extracurriculars, resumes, jobs])
    
    

    

