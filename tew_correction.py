import numpy as np
import matplotlib.pyplot as plt
import pydicom

def tew_correction(em_image, sc1_image, sc2_image):
    # Calculate scatter estimate as the average of the two scatter windows
    scatter_estimate = (sc1_image/(413*0.06) + sc2_image/(318*0.06)) * ((0.2)/2)

    # Subtract scatter estimate from the EM image
    corrected_image = em_image - scatter_estimate

    # Ensure no negative values
    corrected_image = np.clip(corrected_image, 0, None)

    return corrected_image


# def separate_dicom_file(dicom_path):
#     # Read the DICOM file
#     ds = pydicom.dcmread(dicom_path)

#     # Extract the image data (assuming it is in the PixelData field)
#     num_images = 6
#     img_shape = (ds.Rows, ds.Columns)
#     pixel_array = ds.pixel_array.reshape((num_images, *img_shape))
    
#     # Separate images based on their naming convention
#     images = {
#         'Head1_EM': None,
#         'Head1_SC1': None,
#         'Head1_SC2': None,
#         'Head2_EM': None,
#         'Head2_SC1': None,
#         'Head2_SC2': None,
#         'Acq_time' : None,
#         'Acq_date' : None
#     }
    
#     images['Acq_time'] = ds[0x0018, 0x1242].value*0.001
#     images['Acq_date'] = ds[0x0008, 0x0022].value

#     # Assuming the order in the pixel_array is known and consistent
#     images['Head1_EM'] = pixel_array[0]
#     images['Head2_EM'] = pixel_array[1]
#     images['Head1_SC1'] = pixel_array[2]
#     images['Head2_SC1'] = pixel_array[3]
#     images['Head1_SC2'] = pixel_array[4]
#     images['Head2_SC2'] = pixel_array[5]

#     return images

# def tew_correction(em_image, sc1_image, sc2_image):
#     # Calculate scatter estimate as the average of the two scatter windows
#     scatter_estimate = (sc1_image/(413*0.06) + sc2_image/(318*0.06)) * ((364*0.2)/2)

#     # Subtract scatter estimate from the EM image
#     corrected_image = em_image - scatter_estimate

#     # Ensure no negative values
#     corrected_image = np.clip(corrected_image, 0, None)

#     return corrected_image, scatter_estimate

# data_path = "Discovery\MD_20240709\MD_20240709_Discovery.dcm"
# print(pydicom.read_file(data_path).EnergyWindowInformationSequence)

# images = separate_dicom_file(data_path)

# corrected_image, scatter_estimate = tew_correction(images['Head1_EM'], images['Head1_SC1'], images['Head1_SC2'])

# fig, ax = plt.subplots(2, 2, figsize=(20, 10))
# im = ax[0, 0].imshow(images['Head1_EM'], cmap='magma')
# ax[0, 0].set_title('EM image')
# fig.colorbar(im, ax=ax[0, 0])
# im = ax[0, 1].imshow(scatter_estimate, cmap='magma')
# ax[0, 1].set_title('Scatter estimate')
# fig.colorbar(im, ax=ax[0, 1])
# im = ax[1, 0].imshow(corrected_image, cmap='magma')
# ax[1, 0].set_title('Image after TEW correction')
# fig.colorbar(im, ax=ax[1, 0])
# im = ax[1, 1].imshow(images['Head1_EM'] - corrected_image, cmap='magma')
# ax[1, 1].set_title('Substracion of EM image and TEW corrected image')
# fig.colorbar(im, ax=ax[1, 1])
# plt.show()
