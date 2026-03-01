def solve(probabilities, threshold):
    return [1 if value >= threshold else 0 for value in probabilities]
