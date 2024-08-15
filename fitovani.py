import numpy as np
from lmfit import Model

def linearni_fce(x, a, b):
    return a * x + b

bbb = ([93.633, 62.613, 49.233, 34.167], [7.341499151033462, 5.003963281821333, 3.953806390115188, 2.840609184442201])

def linearni_fit(x_a_y_data):
    aktivity = np.array(x_a_y_data[0])
    count_rate = np.array(x_a_y_data[1])
    model = Model(linearni_fce)
    params = model.make_params(a=1, b=0)
    result = model.fit(count_rate, params, x=aktivity)
    
    # Extracting the best-fit values and their errors
    a = result.params['a'].value
    b = result.params['b'].value
    a_err = result.params['a'].stderr
    b_err = result.params['b'].stderr
    
    # Return as a numpy array
    return np.array([a, b, a_err, b_err])

print(linearni_fit(bbb))