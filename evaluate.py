from featurizer import InputType, preprocess, create_feature_vectors
from similarity_utils import compute_similarity
from labeler import perform_labeling
import numpy as np
import os
from collections import defaultdict

EXTRA_FILE = os.path.join("extracurricular_scrapper", "combined_extracurricular.csv")
RESUME_FILE = "UpdatedResumeDataset.csv"
JOB_FILE = "raw_data_v2.csv"
JOB_FILE_LABELED = "raw_data_v2_labeled.csv"

'''
Takes in a feature vector for one resume, then the inputs as well as the feature vectors for all jobs
Returns a list of k recommended jobs
'''
def top_k_jobs(resume_vector, jobs_vectors, k=5):
    cosine_similarities = np.array([compute_similarity(resume_vector, vec) 
        for vec in jobs_vectors])
    top_k_indices = np.argpartition(cosine_similarities, -k)[-k:]
    return np.array(top_k_indices)

def evaluate_accuracy(job_recommendations, job_labels, resume_inputs, split_by_type=True):
    num_correct = 0
    num_correct_by_type = defaultdict(lambda: 0)
    count_by_type = defaultdict(lambda: 0)
    num_examples, k = job_recommendations.shape
    for i, rec in enumerate(job_recommendations):
        true_label = resume_inputs[i]['Category']
        predicted_labels = []
        for idx in rec:
            predicted_labels += job_labels[idx]
        correct = true_label in predicted_labels
        num_correct += correct
        num_correct_by_type[true_label] += correct
        count_by_type[true_label] += 1
    print(f"Overall accuracy with K={k}: {num_correct / num_examples}")
    if split_by_type:
        for candidate_type in num_correct_by_type.keys():
            accuracy = num_correct_by_type[candidate_type] / count_by_type[candidate_type]
            print(f"{candidate_type} accuracy with K={k}: {accuracy}")

def compute_all_accuracies(feature_vectors: dict, inputs: dict, k_values: list, split_by_type: bool):
    for k in k_values:
        job_recommendations = np.vstack([
            top_k_jobs(resume_vector, feature_vectors[InputType.JOB.value], k=k)
            for resume_vector in feature_vectors[InputType.RESUME.value]
        ])
        job_labels = perform_labeling(raw_data=JOB_FILE, output_filename=JOB_FILE_LABELED)
        evaluate_accuracy(job_recommendations, job_labels, inputs[InputType.RESUME.value])

if __name__ == "__main__":
    feature_vectors = {}
    inputs = {}
    for i, filename in enumerate([EXTRA_FILE, RESUME_FILE, JOB_FILE]):
        input_type = [key.value for key in InputType][i]
        inputs[input_type] = preprocess(filename, job_file=JOB_FILE, max_lines=1000)
        feature_vectors[input_type] = create_feature_vectors(inputs[input_type], input_type)
    k_values = [1, 3, 5, 10]
    compute_all_accuracies(feature_vectors, inputs, k_values, split_by_type=True)
