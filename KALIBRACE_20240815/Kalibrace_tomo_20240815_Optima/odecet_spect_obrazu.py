import pydicom
import numpy as np


img_SC = "KALIBRACE_20240815/Kalibrace_tomo_20240815_Optima/Optima_AC.SC.RR_1.dcm"
img_no_SC = "KALIBRACE_20240815/Kalibrace_tomo_20240815_Optima/Optima_AC.RR_1.dcm"

def load_dicom_files(file1, file2):
    ds1 = pydicom.dcmread(file1)
    ds2 = pydicom.dcmread(file2)

    img1 = ds1.pixel_array
    img2 = ds2.pixel_array
    
    return img1, img2


image_SC, image_no_SC = load_dicom_files(img_SC, img_no_SC)

print("Maximum v SC - no_SC: ", np.max(image_no_SC - image_SC))