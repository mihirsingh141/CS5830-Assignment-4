import numpy as np
import pandas as pd
from sklearn.metrics import r2_score
import sys
import json

def main():
    # Retrieve input and output file paths from command line arguments
    in_path = sys.argv[1]
    out_path = sys.argv[2]

    groundTruth = pd.read_csv(in_path).values
    predictedTruth = pd.read_csv(out_path).values

    n = min(len(groundTruth),len(predictedTruth))

    groundTruth = groundTruth[:n]
    predictedTruth = predictedTruth[:n]

    # Calculate R2 scores for each column (ignoring the first column, often an index)
    scores = []
    for i in range(1,groundTruth.shape[1]):
        scores.append(r2_score(groundTruth[:,i],predictedTruth[:,i]))

    # Write the R2 scores to a text file
    with open('data/R2_score.txt','w') as f:
        for score in scores:
            f.write(str(score)+' ')

    # Write the R2 scores to a JSON file 
    with open('data/metrics.json','w') as f:
        for score in scores:
            json.dump({'r2_score': score}, f)

if __name__ == '__main__':
    main()