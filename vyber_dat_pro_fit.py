import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

akt = [10,15,20,130,150]
crt = [10.1, 15.1, 20.1, 130.1, 150.2]

def vyber_dat_pro_lin_fit(aktivity, count_rate):
    aktivity_fit = [a for a in aktivity if a < 100]  # Filter elements manually
    delka = len(aktivity_fit)
    count_rate_fit = count_rate[:delka]

    return aktivity_fit, count_rate_fit

print(vyber_dat_pro_lin_fit(akt, crt))
