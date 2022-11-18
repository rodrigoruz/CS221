# CS221

## Final Project

- The input for our system would be user profile (for example user uploads CV to app). We would parse this user profile with some featurizer.
- We have scrapped 2 datasets (OYA, Amazon job listings) and use a Kaggle dataset that can be found here https://www.kaggle.com/datasets/gauravduttakiit/resume-dataset?resource=download
- We use cosine similarity as a metric between two "documents"

## Notes on Usage.

1. Be sure that you have already installed the selenium package
2. Download chromedriver.exe from https://chromedriver.storage.googleapis.com/index.html?path=73.0.3683.20/
   and insert it in your code (be sure that is unzipped).
3. Also, replace "/" with "\\".
4. Install the proper Chrome driver (eg. 73+) so to be combined with chromedriver version (eg. 73+ too)
5. Change Driver Path Variable: DRIVER_PATH
6. Change the URL you are scrapping

## Installation Requirements

Create a new environment, then download SpaCY and the Wikipedia 2014 Glove dataset:
https://spacy.io/usage
https://github.com/stanfordnlp/GloVe
