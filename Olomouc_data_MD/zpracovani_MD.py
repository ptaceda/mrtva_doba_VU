import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Function for decay law (you may want to use this later)
def premenovy_zakon(a_0, polocas, start_date, end_date):
    days_diff = (end_date - start_date).days
    return a_0 * np.exp(-np.log(2) / polocas * days_diff)

# Parameters for iodine
polocas_jod = 8.04  # Half-life in days
pocatecni_a = 5010  # Initial activity in MBq
ref_datum = pd.to_datetime("2019-10-17")

# Load the data from file
file_path = "Olomouc_data_MD/data.txt"  # Update this if the file is located elsewhere
df = pd.read_csv(file_path, sep="\t")

# Convert date column to datetime format
df['acq. date'] = pd.to_datetime(df['acq. date'], format='%Y%m%d')

# Separate the data for each detector (D1 = anterior, D2 = posterior)
anterior_pozadi = df[df['image'].str.contains('D1')]
anterior_data = df[df['image'].str.contains('1_EM')]
posterior_pozadi = df[df['image'].str.contains('D2')]
posterior_data = df[df['image'].str.contains('2_EM')]

pozadi_ant_cr = np.array(anterior_pozadi['pixelValues'])/(np.array(anterior_pozadi['ActualFrameDuration']) / 1000)
pozadi_pos_cr = np.array(posterior_pozadi['pixelValues'])/(np.array(posterior_pozadi['ActualFrameDuration']) / 1000)
data_ant_cr = np.array(anterior_data['pixelValues'])/(np.array(anterior_data['ActualFrameDuration']) / 1000)
data_pos_cr = np.array(posterior_data['pixelValues'])/(np.array(posterior_data['ActualFrameDuration']) / 1000)

count_rate_pos = data_pos_cr - pozadi_pos_cr
count_rate_ant = data_ant_cr - pozadi_ant_cr
geom_prum = np.sqrt(count_rate_ant * count_rate_pos)

aktivity = anterior_data['acq. date'].apply(lambda end_date: premenovy_zakon(pocatecni_a, polocas_jod, ref_datum, end_date)).to_numpy()

# Filter data where aktivity < 100
mask = aktivity < 100
aktivity_filtered = aktivity[mask]
count_rate_ant_filtered = count_rate_ant[mask] / 1000

# Perform the linear fit for anterior data (where aktivity < 100)
slope, intercept = np.polyfit(aktivity_filtered, count_rate_ant_filtered, 1)  # Linear fit (1st degree polynomial)



# Plot the data and the fitted line
plt.subplots(1,1, figsize=(8, 5))

plt.plot(aktivity, count_rate_ant/1000, 'o', label='Anterior', color='red')
plt.plot(aktivity, geom_prum/1000, 'd', label='Geom. průměr', color='green')
plt.plot(aktivity, count_rate_pos/1000, '+', label='Posterior', color='blue')

# Plot the linear fit for anterior data where aktivity < 100
plt.plot(aktivity, slope * aktivity + intercept, '--', label=f'Linear Fit (Anterior)', color='red')

plt.xlabel('Aktivita [MBq]')
plt.ylabel(r'Count rate [kcps]')
plt.title('Count rate z PW', fontweight='bold')
plt.ylim(0, None)
plt.xlim(0, None)
plt.legend(loc='best', edgecolor='black', fontsize=11)
plt.grid(color='black', ls='-.', lw=0.35)

plt.show()

# Print the slope and intercept of the fitted line
print(f"Slope (m): {slope}")
print(f"Intercept (c): {intercept}")
