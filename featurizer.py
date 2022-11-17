import numpy as np
import csv
from enum import Enum
import spacy

spacy_nlp = spacy.load("en_core_web_sm")
GLOVE_FILE = "glove.6B.50d.txt"
EMBEDDING_SIZE = 50

class InputType(Enum):
    JOB = "job profile"
    RESUME = "resume"
    EXTRA = "extracurricular"

def file_to_csv(filename: str):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        column_names, rows = [], []
        for i, line in enumerate(reader):
            if i == 0:
                column_names = line
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
    if input_type == InputType.EXTRA.value:
        text = f"{input['Requisitos']}"
        keywords = spacy_nlp(text).ents
        vector = np.asarray([], dtype="float32")
        for word in keywords[:num_keywords]:
            word_vec = embeddings_dict.get(str(word).lower(), [])
            if len(word_vec) > 0:
                vector = np.concatenate((vector, word_vec))
        padding = [0.0 for i in range(num_keywords * EMBEDDING_SIZE - len(vector))]
        vector = np.concatenate((vector, padding))
        return vector

if __name__ == "__main__":
    embeddings_dict = create_embedding_dict()
    extracurriculars = file_to_csv(filename="OYA_AcademicJobs.csv")
    extra_vectors = []
    for extra in extracurriculars:
        extra_vectors.append(featurize(extra, "extracurricular"))

