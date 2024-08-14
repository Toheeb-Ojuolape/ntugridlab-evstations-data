import numpy as np

def smape(validation, predictions):
    return 100/len(validation) * np.sum(2 * np.abs(predictions - validation) / (np.abs(validation) + np.abs(predictions)))