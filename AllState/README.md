#AllState Claim Severity Challenge
## Challenge Description
How severe is an insurance claim?

When you’ve been devastated by a serious car accident, your focus is on the things that matter the most: family, friends, and other loved ones. Pushing paper with your insurance agent is the last place you want your time or mental energy spent. This is why Allstate, a personal insurer in the United States, is continually seeking fresh ideas to improve their claims service for the over 16 million households they protect.

Allstate is currently developing automated methods of predicting the cost, and hence severity, of claims. In this recruitment challenge, Kagglers are invited to show off their creativity and flex their technical chops by creating an algorithm which accurately predicts claims severity. Aspiring competitors will demonstrate insight into better ways to predict claims severity for the chance to be part of Allstate’s efforts to ensure a worry-free customer experience.

## Solution
There were a total of 3 different models tried out, each of the model can be found in the approached folder. All three python scripts perform an end to end analysis with the final predictions as well. My final submission for this challenge was a weighted average of the 3 solutions.
### File Description

1. Analysis.ipynb: This contains the code for Exploratory Data Analysis (EDA).
2. Approaches Folder:
    * approach.py - The base model, contains treatment for loss function, special objective function for XGBoost, handling of categorical values
    * approach_additional_features.py - Contains additional features than the base model. Features taken from a public kernel
    * approach_additional_features_lightGBM.py - Same as approach_additional_features except LightGBM was used for a faster performance
