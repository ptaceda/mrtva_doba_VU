import numpy as np
from lmfit import Model

def linearni_fce(x, a, b):
    return a * x + b

def linearni_fit(aktivity, count_rate):
    model = Model(linearni_fce)
    params = model.make_params(a=1, b=0)
    result = model.fit(count_rate, params, aktivity=aktivity)
    return result