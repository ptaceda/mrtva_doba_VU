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
    new_ds.NumberOfFrames = num_images  # Set to 120 frames (TEW-corrected)

    new_ds.Rows, new_ds.Columns = rows, cols  # Update rows and columns based on the corrected images

    # Flatten the corrected images array for PixelData
    corrected_images = corrected_images.reshape(-1)

    # Update PixelData with the corrected images
    new_ds.PixelData = corrected_images.tobytes()

    # Modify (0054, 0090) Angular View Vector to have 120 elements
    new_ds[0x0054, 0x0090].value = new_ds[0x0054, 0x0090].value[:120]  # Keep only the first 120 elements

    # Modify (0054, 0020) Detector Vector to have 120 elements
    new_ds[0x0054, 0x0020].value = new_ds[0x0054, 0x0020].value[:120]  # Keep only the first 120 elements

    # Modify (0054, 0050) Rotation Vector to have 120 elements
    new_ds[(0x0054, 0x0050)].value = new_ds[(0x0054, 0x0050)].value[:120]  # Keep only the first 120 elements

    if (0x0013, 0x101e) in new_ds:
        new_ds[(0x0013, 0x101e)].value = new_ds[(0x0013, 0x101e)].value[:120]  # Keep only the first 120 elements
    else:
        new_ds.add_new((0x0013, 0x101e), 'FD', [0.0] * 120)  # Create a new FD tag with 120 elements of 0.0




    # Optionally, update other DICOM tags (e.g., SeriesDescription, StudyDate, etc.)
    new_ds[0x0008, 0x103e].value = "TEW Corrected Images"

    new_ds[0x0009, 0x1026].value = 1
    new_ds[0x0009, 0x1045].value = '**' # predtim ve tvaru '**\\**\\**'

    new_ds[0x0011, 0x1011].value = original_ds[0x0011, 0x1011].value[0]
    new_ds[0x0011, 0x1012].value = ['TEW Corrected EM']
    new_ds[0x0011, 0x1015].value = original_ds[0x0011, 0x1015].value[0]
    new_ds[0x0011, 0x1016].value = original_ds[0x0011, 0x1016].value[0]
    new_ds[0x0011, 0x1017].value = original_ds[0x0011, 0x1017].value[0]
    new_ds[0x0011, 0x1018].value = original_ds[0x0011, 0x1018].value[0]
    new_ds[0x0011, 0x1019].value = original_ds[0x0011, 0x1019].value[0]
    new_ds[0x0011, 0x101a].value = original_ds[0x0011, 0x101a].value[0]
    new_ds[0x0011, 0x101f].value = original_ds[0x0011, 0x101f].value[0]
    new_ds[0x0011, 0x1026].value = original_ds[0x0011, 0x1026].value[0]
    new_ds[0x0011, 0x1027].value = original_ds[0x0011, 0x1027].value[0:2]
    new_ds[0x0011, 0x1028].value = original_ds[0x0011, 0x1028].value[0:2]
    new_ds[0x0011, 0x102c].value = original_ds[0x0011, 0x102c].value[0]
    new_ds[0x0011, 0x102d].value = original_ds[0x0011, 0x102d].value[0]
    new_ds[0x0011, 0x102e].value = original_ds[0x0011, 0x102e].value[0]
    new_ds[0x0011, 0x102f].value = original_ds[0x0011, 0x102f].value[0]
    new_ds[0x0011, 0x1030].value = ['TEW Corrected EM']
    new_ds[0x0011, 0x1031].value = original_ds[0x0011, 0x1031].value[0]
    new_ds[0x0011, 0x1032].value = original_ds[0x0011, 0x1032].value[0]
    new_ds[0x0011, 0x1033].value = original_ds[0x0011, 0x1033].value[0]
    new_ds[0x0011, 0x1034].value = original_ds[0x0011, 0x1034].value[0]
    new_ds[0x0011, 0x1035].value = original_ds[0x0011, 0x1035].value[0]
    new_ds[0x0011, 0x1036].value = original_ds[0x0011, 0x1036].value[0]
    new_ds[0x0011, 0x1037].value = '**'  # Previously in the format '**\\**\\**'
    new_ds[0x0011, 0x1038].value = original_ds[0x0011, 0x1038].value[0]
    new_ds[0x0011, 0x1039].value = original_ds[0x0011, 0x1039].value[0]
    new_ds[0x0011, 0x103a].value = original_ds[0x0011, 0x103a].value[0]
    new_ds[0x0011, 0x103b].value = original_ds[0x0011, 0x103b].value[0]
    new_ds[0x0011, 0x103c].value = original_ds[0x0011, 0x103c].value[0]
    new_ds[0x0011, 0x103f].value = original_ds[0x0011, 0x103f].value[0]
    new_ds[0x0011, 0x1040].value = original_ds[0x0011, 0x1040].value[0]
    new_ds[0x0011, 0x1041].value = original_ds[0x0011, 0x1041].value[0]
    new_ds[0x0011, 0x1042].value = original_ds[0x0011, 0x1042].value[0]
    new_ds[0x0011, 0x1043].value = original_ds[0x0011, 0x1043].value[0]
    new_ds[0x0011, 0x1044].value = original_ds[0x0011, 0x1044].value[0]
    new_ds[0x0011, 0x1045].value = original_ds[0x0011, 0x1045].value[0]
    new_ds[0x0011, 0x1046].value = original_ds[0x0011, 0x1046].value[0]
    new_ds[0x0011, 0x1050].value = ['TEW Corrected EM']
    new_ds[0x0011, 0x1055].value = original_ds[0x0011, 0x1055].value[0]
    new_ds[0x0011, 0x1056].value = original_ds[0x0011, 0x1056].value[0]
    new_ds[0x0011, 0x1057].value = original_ds[0x0011, 0x1057].value[0:2]

    new_ds[0x0013, 0x1012].value = original_ds[0x0013, 0x1012].value[0]
    new_ds[0x0013, 0x1015].value = original_ds[0x0013, 0x1015].value[0]

    new_ds[0x0033, 0x1107].value = original_ds[0x0033, 0x1107].value[0]


    # Update Energy Window Vector (0054,0010) to have 120 elements
    new_ds[(0x0054, 0x0010)].value = original_ds[(0x0054, 0x0010)].value[0:120]  # Update with the desired array of 120 elements

    # Update the Number of Energy Windows (0054,0011) to 1
    new_ds[(0x0054, 0x0011)].value = 1

    # Update the Energy Window Information Sequence (0054,0012)
    # Keep only the first item in the sequence and modify it
    energy_window_info_seq = new_ds[(0x0054, 0x0012)].value
    energy_window_info_seq[:] = [energy_window_info_seq[0]]  # Retain only the first sequence item

    # Modify the retained item
    first_window_range_seq = energy_window_info_seq[0][(0x0054, 0x0013)].value
    first_window_range_seq[:] = [first_window_range_seq[0]]  # Retain only the first range sequence

    # Update the Energy Window Lower Limit and Upper Limit
    energy_window_info_seq[0][(0x0054, 0x0013)].value[0][(0x0054, 0x0014)].value = '327.6'
    energy_window_info_seq[0][(0x0054, 0x0013)].value[0][(0x0054, 0x0015)].value = '400.4'

    # Update the Energy Window Name
    energy_window_info_seq[0][(0x0054, 0x0018)].value = 'I131_EM_TEW_corrected'


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

    # Extract the image data (assuming it is in the PixelData field)
    # num_images = 360  # Ensure this matches your data
    img_shape = (ds.Rows, ds.Columns)
    
    # Handle cases where the number of images might differ
    pixel_array = ds.pixel_array.reshape((num_images, *img_shape))
    
    # Separate images into 3 arrays (assuming they are ordered this way)
    if num_images == 360:
        images = {
            'PW': pixel_array[:120],
            'USC': pixel_array[120:240],
            'LSC': pixel_array[240:]
        }
    else:
        images = {
            'PW': pixel_array[:60],
            'USC': pixel_array[60:120],
            'LSC': pixel_array[120:]
        }
    
    return images

num_images = 360

# Load and process the DICOM file
path = r"/Users/danielptacek/Desktop/mrtva_doba_VU/KALIBRACE_20240815/Kalibrace_tomo_20240815_Optima/Kalibrace_tomo_2_20240815_Optima.dcm"
ds = separate_dicom_file_tomo(path)
#new_ds = pydicom.dcmread(r"KALIBRACE_20240815\Kalibrace_tomo_20240815_Optima\Kalibrace_zkouska_Optima_2_tomo.dcm")
#print(new_ds)
#plt.imshow(new_ds.pixel_array[0], cmap='gray')
#plt.show()

if num_images == 360:
    # Initialize corrected_images with the correct dtype
    corrected_images = np.empty((120, ds['PW'].shape[1], ds['PW'].shape[2]), dtype=np.float32)

    # Perform TEW correction for each image
    for i in range(120):
        corrected_image = tew_correction(ds['PW'][i], ds['USC'][i], ds['LSC'][i])
        corrected_images[i, :, :] = corrected_image
else:
    # Initialize corrected_images with the correct dtype
    corrected_images = np.empty((60, ds['PW'].shape[1], ds['PW'].shape[2]), dtype=np.float32)

    # Perform TEW correction for each image
    for i in range(60):
        corrected_image = tew_correction(ds['PW'][i], ds['USC'][i], ds['LSC'][i])
        corrected_images[i, :, :] = corrected_image

# Save the corrected images to DICOM
output_dicom_path = r"/Users/danielptacek/Desktop/mrtva_doba_VU/KALIBRACE_20240815/Kalibrace_tomo_20240815_Optima/Kalibrace_TEW_Optima_2_tomo.dcm"
save_corrected_images_to_dicom(path, corrected_images, output_dicom_path)


