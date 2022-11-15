# CS221

## Final Project

- The input for our system would be user profile (for example user uploads CV to app). We would parse this user profile with some featurizer.
- Right now we can start working with job descriptions only, because getting profile dataset (actual people that are working the jobs) is difficult.
- We have 2 datasets (OYA, Amazon job listings) and we updated the brainstorm doc a bit so it's more clearer.
- We need to think about a similarity metric between two "documents", so if you have time and you are aligned on the direction of the project, please look into it. I will as well.

We want to meet again sometime later today. I will be online for next ~5hrs so if you have a timeslot you prefer there, then let's meet. Currently with Rodrigo we are working on "productionalizing" our scrappers, so we can start working with real datasets

## Notes on Usage.

1. Be sure that you have already installed the selenium package
2. Download chromedriver.exe from https://chromedriver.storage.googleapis.com/index.html?path=73.0.3683.20/
   and insert it in your code (be sure that is unzipped).
3. Also, replace "/" with "\\".
4. Install the proper Chrome driver (eg. 73+) so to be combined with chromedriver version (eg. 73+ too)
5. Change Driver Path Variable: DRIVER_PATH
6. Change the URL you are scrapping
