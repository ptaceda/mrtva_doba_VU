import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

def vyber_dat_pro_lin_fit(aktivity, count_rate):
    aktivity_fit = [a for a in aktivity if a < 100]  # Filter elements manually
    delka = len(aktivity_fit)
    count_rate_fit = count_rate[:-delka]

    return aktivity_fit, count_rate_fit
