#### planarni kalibrace Optima


from dicom_file_separator import separate_dicom_file
from tew_correction import tew_correction
from codes.custom_library import region_growing
from geom_prumer import geom_prumer
import numpy as np
from glob import glob
import matplotlib.pyplot as plt
import os

from matplotlib.widgets import PolygonSelector
from matplotlib.path import Path

class ROI_drawer_manual:
    def __init__(self, image):
        self.image = image
        
        # Create figure and axes
        self.fig, self.ax = plt.subplots(figsize=(13, 13))
        self.ax.imshow(self.image, cmap='gray')
        
        # Initialize ROI points, mask, and PolygonSelector
        self.roi_points = []
        self.mask = None
        self.selector = PolygonSelector(self.ax, self.on_select, useblit=True)
        
        # Set the color to a brighter red and linewidth for each artist
        bright_blue = (0.0, 0.5, 1.0)  # RGB values for a bright blue color
        for artist in self.selector.artists:
            artist.set_color(bright_blue)
            artist.set_linewidth(2)
        
        # Connect the event for showing pixel values
        self.fig.canvas.mpl_connect('motion_notify_event', self.show_pixel_value)
        
        # Create a text box for displaying pixel values
        self.text = self.ax.text(0.05, 0.95, '', transform=self.ax.transAxes, color='yellow', fontsize=12,
                                 bbox=dict(facecolor='black', alpha=0.5))

        # Store the contour object for the ROI
        self.contour = None

    def show(self):
        # Display the figure and allow for manual ROI selection
        plt.show()

    def on_select(self, verts):
        # Store the vertices of the manually drawn polygon
        self.roi_points = verts
        self.create_mask()
        self.display_results()

    def create_mask(self):
        # Create a mask for the polygon
        poly_path = Path(self.roi_points)
        y, x = np.mgrid[:self.image.shape[0], :self.image.shape[1]]
        points = np.vstack((x.ravel(), y.ravel())).T
        self.mask = poly_path.contains_points(points).reshape(self.image.shape)
        

    def display_results(self):
        # Clear previous contour if it exists
        if self.contour is not None:
            for coll in self.contour.collections:
                coll.remove()

        # Display the results of the manually drawn ROI
        self.ax.imshow(self.image, cmap='gray')
        if self.mask is not None:
            # Draw the new contour and update the contour attribute
            self.contour = self.ax.contour(self.mask, colors='r', linewidths=2)
        plt.draw()

    def show_pixel_value(self, event):
        # Show the pixel value under the cursor
        if event.inaxes == self.ax:
            x, y = int(event.xdata), int(event.ydata)
            if 0 <= x < self.image.shape[1] and 0 <= y < self.image.shape[0]:
                pixel_value = self.image[y, x]
                self.text.set_text(f'Pixel Value: {pixel_value:.2f}')
                plt.draw()

def polynom_x_stupne_fce(x, a, b, c, d):
    return  a*x**b + c*x**d + 1

kalibrace_folder = "KALIBRACE_20240815/Kalibrace_plan_20240815_Optima"
kalibrace_mds = sorted(glob(os.path.join(kalibrace_folder, 'Kalibrace*')))

aktivity = {
    "20240708" : 700.589,
    "20240709" : 640.979,
    "20240710" : 586.294,
    "20240711" : 537.692,
    "20240712" : 495.958,
    "20240714" : 404.370,
    "20240715" : 379.365,
    "20240717" : 324.319,
    "20240719" : 266.596,
    "20240721" : 226.576,
    "20240723" : 190.942,
    "20240725" : 158.536,
    "20240726" : 152.496,
    "20240729" : 115.038,
    "20240731" : 93.633,
    "20240805" : 62.613,
    "20240808" : 49.233,
    "20240812" : 34.167,
    "20240815" : 26.602,
    "20240819" : 18.401,
    "20240822" : 14.270,
    "20240826" : 10.122,
    "20240903" : 5.069,
    "20240912" : 2.363
}

'''
Type        View            par_a           par_b           par_c           par_d
MD_fak      Anterior        1.95257784e-22  1.48292063e+01  3.00220526e-03  1.59866475e+00
MD_fak_err  Anterior        1.11429727e-21  1.70490377e+00  8.03446102e-04  9.39528531e-02
MD_fak      Anterior_TEW    3.59607553e-11  9.24320666e+00  1.76202032e-02  1.30683100e+00
MD_fak_err  Anterior_TEW    2.29040107e-10  2.43361357e+00  1.09114666e-02  3.27368893e-01
MD_fak      Posterior       1.31409092e-05  3.31323839e+00  1.89360776e-02  8.26102922e-01
MD_fak_err  Posterior       4.52595005e-05  1.11629489e+00  3.65812380e-03  1.53824935e-01
MD_fak      Posterior_TEW   2.00976644e-06  6.10012513e+00  5.13316934e-02  9.03443333e-01
MD_fak_err  Posterior_TEW   9.04267323e-06  2.31794885e+00  6.86036148e-03  1.43276013e-01
MD_fak      Geom_mean       8.47126449e-10  6.39721308e+00  9.96660641e-03  1.20396570e+00
MD_fak_err  Geom_mean       2.32391080e-09  8.65229461e-01  1.72257278e-03  7.96932465e-02
MD_fak      Geom_mean_TEW   4.04182440e-09  8.28032752e+00  3.08865279e-02  1.21697028e+00
MD_fak_err  Geom_mean_TEW   1.30195030e-08  1.42043568e+00  4.94307658e-03  1.08490485e-01
'''



####
#### NA ZÁKLADĚ ODHADU REL. NEJISTOTY ČETNOSTI Z POČTU MĚŘENÍ
####
hlava_1_kal_faktory = []
hlava_1_tew_kal_faktory = []
hlava_2_kal_faktory = []
hlava_2_tew_kal_faktory = []
hlavy_gm = []
hlavy_gm_tew = []

hlava_1_kal_cetnosti = []
hlava_1_tew_kal_cetnosti = []
hlava_2_kal_cetnosti = []
hlava_2_tew_kal_cetnosti = []
hlavy_gm_kal_cetnosti = []
hlavy_gm_tew_kal_cetnosti = []

for md, k in zip(kalibrace_mds, range(len(kalibrace_mds))):
    print(k)
    image = separate_dicom_file(md)

    acq_time = image["Acq_time"]
    acq_date = image["Acq_date"]

    # prenasobeni mrtvou dobou
    hlava_1 = image["Head1_EM"]
    hlava_1 = hlava_1*polynom_x_stupne_fce(np.sum(hlava_1)/acq_time *0.001, 1.95257784e-22, 1.48292063e+01, 3.00220526e-03, 1.59866475e+00)
    hlava_1_tew = tew_correction(image["Head1_EM"], image["Head1_SC1"], image["Head1_SC2"])
    hlava_1_tew = hlava_1_tew*polynom_x_stupne_fce(np.sum(hlava_1_tew)/acq_time *0.001, 3.59607553e-11, 9.24320666e+00, 1.76202032e-02, 1.30683100e+00)
    hlava_2 = image["Head2_EM"]
    hlava_2 = hlava_2*polynom_x_stupne_fce(np.sum(hlava_2)/acq_time *0.001, 1.31409092e-05, 3.31323839e+00, 1.89360776e-02, 8.26102922e-01)
    hlava_2_tew = tew_correction(image["Head2_EM"], image["Head2_SC1"], image["Head2_SC2"])
    hlava_2_tew = hlava_2_tew*polynom_x_stupne_fce(np.sum(hlava_2_tew)/acq_time *0.001, 2.00976644e-06, 6.10012513e+00, 5.13316934e-02, 9.03443333e-01)

    if k == 0:
        maska_1 = ROI_drawer_manual(hlava_1)
        maska_1.show()
        maska_1_tew = ROI_drawer_manual(hlava_1_tew)
        maska_1_tew.show()
        maska_2 = ROI_drawer_manual(hlava_2)
        maska_2.show()
        maska_2_tew = ROI_drawer_manual(hlava_2_tew)
        maska_2_tew.show()

    #maska_1 = region_growing(hlava_1, prah*(np.max(hlava_1) - np.mean(hlava_1[148:163, 105:155])))
    #maska_1_tew = region_growing(hlava_1_tew, prah*(np.max(hlava_1_tew) - np.mean(hlava_1_tew[148:163, 105:155])))
    #maska_2 = region_growing(hlava_2, prah*(np.max(hlava_2) - np.mean(hlava_2[148:163, 105:155])))
    #maska_2_tew = region_growing(hlava_2_tew, prah*(np.max(hlava_2_tew) - np.mean(hlava_2_tew[148:163, 105:155])))


    kal_cetnost_1 = (np.sum(hlava_1*maska_1.mask) / acq_time) 
    kal_cetnost_1_tew = (np.sum(hlava_1_tew*maska_1_tew.mask) / acq_time) 
    kal_cetnost_2 = (np.sum(hlava_2*maska_2.mask) / acq_time) 
    kal_cetnost_2_tew = (np.sum(hlava_2_tew*maska_2_tew.mask) / acq_time) 
    kal_cetnost_gm = geom_prumer(kal_cetnost_1, kal_cetnost_2)
    kal_cetnost_gm_tew = geom_prumer(kal_cetnost_1_tew, kal_cetnost_2_tew)

    hlava_1_kal_cetnosti.append(kal_cetnost_1)
    hlava_1_tew_kal_cetnosti.append(kal_cetnost_1_tew)
    hlava_2_kal_cetnosti.append(kal_cetnost_2)
    hlava_2_tew_kal_cetnosti.append(kal_cetnost_2_tew)
    hlavy_gm_kal_cetnosti.append(kal_cetnost_gm)
    hlavy_gm_tew_kal_cetnosti.append(kal_cetnost_gm_tew)

### výpočet relativního odhadu počtu impulsů zakreslením ROI 
rel_odhad_impulsu_hlava_1 = np.std(hlava_1_kal_cetnosti, ddof=1)/np.mean(hlava_1_kal_cetnosti)
rel_odhad_impulsu_hlava_1_tew = np.std(hlava_1_tew_kal_cetnosti, ddof=1)/np.mean(hlava_1_tew_kal_cetnosti)
rel_odhad_impulsu_hlava_2 = np.std(hlava_2_kal_cetnosti, ddof=1)/np.mean(hlava_2_kal_cetnosti)
rel_odhad_impulsu_hlava_2_tew = np.std(hlava_2_tew_kal_cetnosti, ddof=1)/np.mean(hlava_2_tew_kal_cetnosti)
rel_odhad_impulsu_hlavy_gm = np.std(hlavy_gm_kal_cetnosti, ddof=1)/np.mean(hlavy_gm_kal_cetnosti)
rel_odhad_impulsu_hlavy_gm_tew = np.std(hlavy_gm_tew_kal_cetnosti, ddof=1)/np.mean(hlavy_gm_tew_kal_cetnosti)


### výpočet jednotlivých kalibračních koeficientů se svými nejistotami
hlava_1_kal_faktory = np.array(hlava_1_kal_cetnosti)/aktivity["20240815"]
hlava_1_kal_faktory_err = hlava_1_kal_faktory * np.sqrt(rel_odhad_impulsu_hlava_1**2 + 0.042**2)

hlava_1_tew_kal_faktory = np.array(hlava_1_tew_kal_cetnosti)/aktivity["20240815"]
hlava_1_tew_kal_faktory_err = hlava_1_tew_kal_faktory * np.sqrt(rel_odhad_impulsu_hlava_1_tew**2 + 0.042**2)

hlava_2_kal_faktory = np.array(hlava_2_kal_cetnosti)/aktivity["20240815"]
hlava_2_kal_faktory_err = hlava_2_kal_faktory * np.sqrt(rel_odhad_impulsu_hlava_2**2 + 0.042**2)

hlava_2_tew_kal_faktory = np.array(hlava_2_tew_kal_cetnosti)/aktivity["20240815"]
hlava_2_tew_kal_faktory_err = hlava_2_tew_kal_faktory * np.sqrt(rel_odhad_impulsu_hlava_2_tew**2 + 0.042**2)

hlavy_gm = np.array(hlavy_gm_kal_cetnosti)/aktivity["20240815"]
hlavy_gm_err = hlavy_gm * np.sqrt(rel_odhad_impulsu_hlavy_gm**2 + 0.042**2)

hlavy_gm_tew = np.array(hlavy_gm_tew_kal_cetnosti)/aktivity["20240815"]
hlavy_gm_tew_err = hlavy_gm_tew * np.sqrt(rel_odhad_impulsu_hlavy_gm_tew**2 + 0.042**2)


### vyprintění jednotlivých průměrných kalibračních koeficientů se svými nejistotami
print("Na základě odhadu rel. nejistoty četnosti impulsů a za pomoci nejistoty aktivity")
print(f"Anterior: {np.mean(hlava_1_kal_faktory)} +- {np.sum(hlava_1_kal_faktory_err**2)/len(hlava_1_kal_faktory_err)}")
print(f"Anterior TEW: {np.mean(hlava_1_tew_kal_faktory)} +- {np.sum(hlava_1_tew_kal_faktory_err**2)/len(hlava_1_tew_kal_faktory_err)}")
print(f"Posterior: {np.mean(hlava_2_kal_faktory)} +- {np.sum(hlava_2_kal_faktory_err**2)/len(hlava_2_kal_faktory_err)}")
print(f"Posterior TEW: {np.mean(hlava_2_tew_kal_faktory)} +- {np.sum(hlava_2_tew_kal_faktory_err**2)/len(hlava_2_tew_kal_faktory_err)}")
print(f"Geom. Mean: {np.mean(hlavy_gm)} +- {np.sum(hlavy_gm_err**2)/len(hlavy_gm_err)}")
print(f"Geom. Mean TEW: {np.mean(hlavy_gm_tew)} +- {np.sum(hlavy_gm_tew_err**2)/len(hlavy_gm_tew_err)}")
print("------")






'''
####
#### NA ZÁKLADĚ VÝBĚROVÉ SMĚRODATNÉ ODCHYLKY PRŮMĚRU
####
hlava_1_kal_faktory = []
hlava_1_tew_kal_faktory = []
hlava_2_kal_faktory = []
hlava_2_tew_kal_faktory = []
hlavy_gm = []
hlavy_gm_tew = []

for md in kalibrace_mds:
    image = separate_dicom_file(md)

    acq_time = image["Acq_time"]
    acq_date = image["Acq_date"]

    hlava_1 = image["Head1_EM"]
    hlava_1_tew = tew_correction(image["Head1_EM"], image["Head1_SC1"], image["Head1_SC2"])
    hlava_2 = image["Head2_EM"]
    hlava_2_tew = tew_correction(image["Head2_EM"], image["Head2_SC1"], image["Head2_SC2"])

    maska_1 = region_growing(hlava_1, prah*np.max(hlava_1))
    maska_1_tew = region_growing(hlava_1_tew, prah*np.max(hlava_1_tew))
    maska_2 = region_growing(hlava_2, prah*np.max(hlava_2))
    maska_2_tew = region_growing(hlava_2_tew, prah*np.max(hlava_2_tew))


    kal_faktor_1 = (np.sum(hlava_1*maska_1) / acq_time) / aktivity[acq_date]
    kal_faktor_1_tew = (np.sum(hlava_1_tew*maska_1_tew) / acq_time) / aktivity[acq_date]
    kal_faktor_2 = (np.sum(hlava_2*maska_2) / acq_time) / aktivity[acq_date]
    kal_faktor_2_tew = (np.sum(hlava_2_tew*maska_2_tew) / acq_time) / aktivity[acq_date]
    kal_faktor_gm = (geom_prumer(np.sum(hlava_1*maska_1), np.sum(hlava_2*maska_2)) / acq_time) / aktivity[acq_date]
    kal_faktor_gm_tew = (geom_prumer(np.sum(hlava_1_tew*maska_1_tew), np.sum(hlava_2_tew*maska_2_tew)) / acq_time) / aktivity[acq_date]


    hlava_1_kal_faktory.append(kal_faktor_1)
    hlava_1_tew_kal_faktory.append(kal_faktor_1_tew)
    hlava_2_kal_faktory.append(kal_faktor_2)
    hlava_2_tew_kal_faktory.append(kal_faktor_2_tew)
    hlavy_gm.append(kal_faktor_gm)
    hlavy_gm_tew.append(kal_faktor_gm_tew)


print("Na základě odhadu pomocí výběrové směrodatné odchylky průměru")
print(f"Anterior: {np.mean(hlava_1_kal_faktory)} +- {np.std(hlava_1_kal_faktory, ddof=1)/np.sqrt(len(hlava_1_kal_faktory))}")
print(f"Anterior TEW: {np.mean(hlava_1_tew_kal_faktory)} +- {np.std(hlava_1_tew_kal_faktory, ddof=1)/np.sqrt(len(hlava_1_tew_kal_faktory))}")
print(f"Posterior: {np.mean(hlava_2_kal_faktory)} +- {np.std(hlava_2_kal_faktory, ddof=1)/np.sqrt(len(hlava_2_kal_faktory))}")
print(f"Posterior TEW: {np.mean(hlava_2_tew_kal_faktory)} +- {np.std(hlava_2_tew_kal_faktory, ddof=1)/np.sqrt(len(hlava_2_tew_kal_faktory))}")
print(f"Geom. Mean: {np.mean(hlavy_gm)} +- {np.std(hlavy_gm, ddof=1)/np.sqrt(len(hlavy_gm))}")
print(f"Geom. Mean TEW: {np.mean(hlavy_gm_tew)} +- {np.std(hlavy_gm_tew, ddof=1)/np.sqrt(len(hlavy_gm_tew))}")
'''