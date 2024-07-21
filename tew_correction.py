import pydicom
import numpy as np
import matplotlib.pyplot as plt

def tew_correction(dicom_path):
    # Read the DICOM file
    ds = pydicom.dcmread(dicom_path)

    # Extract the image data (assuming it is in the PixelData field)
    num_images = 6
    img_shape = (ds.Rows, ds.Columns)
    pixel_array = ds.pixel_array.reshape((num_images, *img_shape))
    
    # Separate images based on their naming convention
    images = {
        'Head1_EM': None,
        'Head1_SC1': None,
        'Head1_SC2': None,
        'Head2_EM': None,
        'Head2_SC1': None,
        'Head2_SC2': None
    }
    
    # Assuming the order in the pixel_array is known and consistent
    images['Head1_EM'] = pixel_array[0]
    images['Head2_EM'] = pixel_array[1]
    images['Head1_SC1'] = pixel_array[2]
    images['Head2_SC1'] = pixel_array[3]
    images['Head1_SC2'] = pixel_array[4]
    images['Head2_SC2'] = pixel_array[5]
    
    def perform_tew_correction(em_image, sc1_image, sc2_image):
        # Calculate scatter estimate as the average of the two scatter windows
        # scatter_estimate = (sc1_image/(413*0.06) + sc2_image/(318*0.06)) * ((364*0.2)/2)
        scatter_estimate = (sc1_image + sc2_image)/2
        print(np.sum(scatter_estimate))
        plt.imshow(scatter_estimate, cmap='gray')
        # Subtract scatter estimate from the EM image
        corrected_image = em_image - scatter_estimate
        # Ensure no negative values
        corrected_image = np.clip(corrected_image, 0, None)
        return corrected_image

    # Perform TEW correction for each head
    corrected_images = {}
    corrected_images['Head1'] = perform_tew_correction(images['Head1_EM'], images['Head1_SC1'], images['Head1_SC2'])
    corrected_images['Head2'] = perform_tew_correction(images['Head2_EM'], images['Head2_SC1'], images['Head2_SC2'])

    return corrected_images

# Example usage
dicom_path = "Discovery/MD_08072024_povedene/MD_08072024_Discovery.dcm"
corrected_images = tew_correction(dicom_path)

# Plotting the corrected images
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.title("Corrected Image - Head 1")
plt.imshow(corrected_images['Head1'], cmap='gray')
plt.subplot(1, 2, 2)
plt.title("Corrected Image - Head 2")
plt.imshow(corrected_images['Head2'], cmap='gray')
plt.show()