import numpy as np
import matplotlib.pyplot as plt

def tew_correction(em_image, sc1_image, sc2_image):
    # Calculate scatter estimate as the average of the two scatter windows
    scatter_estimate = (sc1_image/(413*0.06) + sc2_image/(318*0.06)) * ((364*0.2)/2)
    print(np.sum(scatter_estimate))
    # scatter_estimate = (sc1_image + sc2_image)/2
    # plt.imshow(scatter_estimate, cmap='gray')

    # Subtract scatter estimate from the EM image
    corrected_image = em_image - scatter_estimate

    # Ensure no negative values
    corrected_image = np.clip(corrected_image, 0, None)
    # plt.imshow(corrected_image, cmap='gray')

    return corrected_image
