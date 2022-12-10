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

def evaluate_accuracy(job_recommendations, job_labels, resume_inputs, eval_size=300, split_by_type=True):
    num_correct = 0
    num_correct_by_type = defaultdict(lambda: 0)
    count_by_type = defaultdict(lambda: 0)
    num_examples, k = job_recommendations.shape
    accuracies = {}
    for i, rec in enumerate(job_recommendations):
        if i > eval_size: continue
        true_label = resume_inputs[i]['Category']
        predicted_labels = []
        for idx in rec:
            predicted_labels += job_labels[idx]
        print(true_label, predicted_labels)
        correct = true_label in predicted_labels
        num_correct += correct
        num_correct_by_type[true_label] += correct
        count_by_type[true_label] += 1
    accuracy = num_correct / num_examples
    print(f"Overall accuracy with size={eval_size}: {accuracy}")
    accuracies["overall"] = accuracy
    if split_by_type:
        for candidate_type in num_correct_by_type.keys():
            accuracy = num_correct_by_type[candidate_type] / count_by_type[candidate_type]
            print(f"{candidate_type} accuracy with K={k}: {accuracy}")
            accuracies[candidate_type] = accuracy
    return accuracies

def compute_all_accuracies(feature_vectors: dict, inputs: dict, eval_sizes: list, split_by_type: bool):
    accuracies_by_size = {}
    for size in eval_sizes:
        job_recommendations = np.vstack([
            top_k_jobs(resume_vector, feature_vectors[InputType.JOB.value])
            for resume_vector in feature_vectors[InputType.RESUME.value]
        ])
        np.save('extracurricular_scrapper/data.npy', job_recommendations) # save
        job_labels = perform_labeling(raw_data=JOB_FILE, output_filename=JOB_FILE_LABELED)
        accuracies_by_size[size] = evaluate_accuracy(job_recommendations, job_labels, inputs[InputType.RESUME.value])
    return accuracies_by_size

if __name__ == "__main__":
    feature_vectors = {}
    inputs = {}
    for i, filename in enumerate([EXTRA_FILE, RESUME_FILE, JOB_FILE]):
        input_type = [key.value for key in InputType][i]
        inputs[input_type] = preprocess(filename, job_file=JOB_FILE, max_lines=300)
        feature_vectors[input_type] = create_feature_vectors(inputs[input_type], input_type)
    eval_sizes = [100 * i for i in range(1, 11)]
    accuracies_by_k = compute_all_accuracies(feature_vectors, inputs, eval_sizes, split_by_type=True)
