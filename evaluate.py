from featurizer import InputType, preprocess, create_feature_vectors
from similarity_utils import compute_similarity
from labeler import perform_labeling
import numpy as np
import os

EXTRA_FILE = os.path.join("extracurricular_scrapper", "combined_extracurricular.csv")
RESUME_FILE = "UpdatedResumeDataset.csv"
JOB_FILE = "raw_data_v2.csv"
JOB_FILE_LABELED = "raw_data_v2_labeled.csv"

'''
Takes in a feature vector for one resume, then the inputs as well as the feature vectors for all jobs
Returns a list of k recommended jobs
'''
def top_k_jobs(resume_vector, jobs_vectors, k=5):
    cosine_similarities = compute_similarity(resume_vector, jobs_vectors)
    top_k_indices = np.argpartition(cosine_similarities, -k)[-k:]
    return np.array(top_k_indices)

def evaluate_accuracy(job_recommendations, job_labels, resume_inputs):
    count = 0
    num_examples, k = job_recommendations.shape
    for i, rec in enumerate(job_recommendations):
        true_label = resume_inputs[i]['Category']
        predicted_labels = []
        for idx in rec:
            predicted_labels += job_labels[idx]
        count += (true_label in predicted_labels)
    print(f"Accuracy with K={k}: {count / num_examples}")

if __name__ == "__main__":
    feature_vectors = {}
    inputs = {}
    for i, filename in enumerate([EXTRA_FILE, RESUME_FILE, JOB_FILE]):
        input_type = [key.value for key in InputType][i]
        inputs[input_type] = preprocess(filename, job_file=JOB_FILE)
        feature_vectors[input_type] = create_feature_vectors(inputs[input_type], input_type)
    job_recommendations = np.vstack([
        top_k_jobs(resume_vector, feature_vectors[InputType.JOB.value])
        for resume_vector in feature_vectors[InputType.RESUME.value]
    ])
    job_labels = perform_labeling(raw_data=JOB_FILE, output_filename=JOB_FILE_LABELED)
    evaluate_accuracy(job_recommendations, job_labels, inputs[InputType.RESUME.value])
