import pandas as pd
import numpy as np

def compute_lift_warning_value(da):
    x = da['percent_persons_contacted'].values
    y = da['percent_patients_found'].values

    index = np.argmin(np.abs(1 - (np.diff(y) / np.diff(x))))
    return x[index]