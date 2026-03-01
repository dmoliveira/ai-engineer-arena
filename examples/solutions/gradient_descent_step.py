def solve(weights, gradients, learning_rate):
    updated = [w - learning_rate * g for w, g in zip(weights, gradients)]
    return [round(value, 6) for value in updated]
