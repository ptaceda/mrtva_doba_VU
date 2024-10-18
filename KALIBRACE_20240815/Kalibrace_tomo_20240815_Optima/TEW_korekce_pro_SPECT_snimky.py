import pydicom
import numpy as np
import matplotlib.pyplot as plt
import pydicom
import numpy as np
import os

def save_corrected_images_to_dicom(original_dicom_path, corrected_images, output_dicom_path):
    # Read the original DICOM file
    original_ds = pydicom.dcmread(original_dicom_path)

    # Make a copy of the original DICOM dataset
    new_ds = original_ds.copy()

    # Ensure that corrected_images has the correct dtype and shape for TEW-corrected 120 images
    corrected_images = corrected_images.astype(np.int16)  # Convert to 16-bit integers for DICOM

    # Assuming corrected_images is a 3D array (num_images, rows, cols)
    num_images, rows, cols = corrected_images.shape

    # Update DICOM attributes to reflect 120 images
    if hasattr(new_ds, 'NumberOfFrames'):
        new_ds.NumberOfFrames = num_images  # Set to 120 frames (TEW-corrected)

    new_ds.Rows, new_ds.Columns = rows, cols  # Update rows and columns based on the corrected images

    # Flatten the corrected images array for PixelData
    corrected_images = corrected_images.reshape(-1)

    # Update PixelData with the corrected images
    new_ds.PixelData = corrected_images.tobytes()

    # Modify (0054, 0090) Angular View Vector to have 120 elements
    if '00540090' in new_ds:
        angular_view_vector = new_ds[0x0054, 0x0090].value
        if len(angular_view_vector) == 360:
            new_ds[0x0054, 0x0090].value = angular_view_vector[:120]  # Keep only the first 120 elements

    # Modify (0054, 0020) Detector Vector to have 120 elements
    if '00540020' in new_ds:
        detector_vector = new_ds[0x0054, 0x0020].value
        if len(detector_vector) == 360:
            new_ds[0x0054, 0x0020].value = detector_vector[:120]  # Keep only the first 120 elements

    # Overwrite attributes that are tied to multi-energy window images
    if hasattr(new_ds, 'EnergyWindowInformationSequence'):
        del new_ds.EnergyWindowInformationSequence  # Remove, as TEW-corrected images don't have energy windows

    if hasattr(new_ds, 'EnergyWindowRangeSequence'):
        del new_ds.EnergyWindowRangeSequence  # Remove this as well, if present

    if hasattr(new_ds, 'EnergyWindowNumber'):
        del new_ds.EnergyWindowNumber  # Clear any reference to specific energy windows

    # Optionally, update other DICOM tags (e.g., SeriesDescription, StudyDate, etc.)
    new_ds.SeriesDescription = "120 TEW Corrected Images"

    # Save the new DICOM file
    new_ds.save_as(output_dicom_path)
    print(f"New DICOM file saved at: {output_dicom_path}")



def tew_correction(em_image, sc1_image, sc2_image):
    # Calculate scatter estimate as the average of the two scatter windows
    scatter_estimate = (sc1_image/(413*0.06) + sc2_image/(318*0.06)) * ((364*0.2)/2)
    
    # Subtract scatter estimate from the EM image
    corrected_image = em_image - scatter_estimate

    # Ensure corrected_image is not less than 0
    corrected_image[corrected_image < 0] = 0

    return corrected_image

def separate_dicom_file_tomo(dicom_path):
    # Read the DICOM file
    ds = pydicom.dcmread(dicom_path)
    print(ds)

    # Extract the image data (assuming it is in the PixelData field)
    num_images = 360  # Ensure this matches your data
    img_shape = (ds.Rows, ds.Columns)
    
    # Handle cases where the number of images might differ
    pixel_array = ds.pixel_array.reshape((num_images, *img_shape))
    
    # Separate images into 3 arrays (assuming they are ordered this way)
    images = {
        'PW': pixel_array[:120],
        'USC': pixel_array[120:240],
        'LSC': pixel_array[240:]
    }
    
    return images

# Load and process the DICOM file
ds = separate_dicom_file_tomo(r"KALIBRACE_20240815\Kalibrace_tomo_20240815_Optima\Kalibrace_tomo_3_20240815_Optima.dcm")
#new_ds = pydicom.dcmread(r"KALIBRACE_20240815\Kalibrace_tomo_20240815_Optima\Kalibrace_zkouska_Optima_2_tomo.dcm")
#print(new_ds)
#plt.imshow(new_ds.pixel_array[0], cmap='gray')
#plt.show()

# Initialize corrected_images with the correct dtype
corrected_images = np.empty((120, ds['PW'].shape[1], ds['PW'].shape[2]), dtype=np.float32)

# Perform TEW correction for each image
for i in range(120):
    corrected_image = tew_correction(ds['PW'][i], ds['USC'][i], ds['LSC'][i])
    corrected_images[i, :, :] = corrected_image

# Save the corrected images to DICOM
output_dicom_path = r"KALIBRACE_20240815\Kalibrace_tomo_20240815_Optima\Kalibrace_zkouska_Optima_3_tomo.dcm"
save_corrected_images_to_dicom(r"KALIBRACE_20240815\Kalibrace_tomo_20240815_Optima\Kalibrace_tomo_3_20240815_Optima.dcm", corrected_images, output_dicom_path)


