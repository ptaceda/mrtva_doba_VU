import numpy as np
from lmfit import Model

def linearni_fce(x, a, b):
    return a * x + b

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

def exp_md_fce(x, tau):
    return x * np.exp(-x * tau)

def lomenna_md_fce(x, tau):
    return x / (1 - x*tau)

def exp_md_fit(x_a_y_data):
    teor_cps = np.array(x_a_y_data[0])
    mer_cps = np.array(x_a_y_data[1])
    model = Model(exp_md_fce)
    params = model.make_params(tau=0.01)
    result = model.fit(mer_cps, params, x=teor_cps)

    # Extracting the best-fit values and their errors
    tau = result.params['tau'].value
    tau_err = result.params['tau'].stderr
    
    # Return as a numpy array
    return np.array([tau, tau_err])

def lomeny_md_fit(x_a_y_data):
    mer_cps = np.array(x_a_y_data[0])
    teor_cps = np.array(x_a_y_data[1])
    model = Model(lomenna_md_fce)
    params = model.make_params(tau=0.01)
    result = model.fit(teor_cps, params, x=mer_cps)

    # Extracting the best-fit values and their errors
    tau = result.params['tau'].value
    tau_err = result.params['tau'].stderr
    
    # Return as a numpy array
    return np.array([tau, tau_err])