import pydicom
import numpy as np
import os
import argparse


def substract_SPECT_images(image_SC, image_no_SC):
    ds1 = pydicom.dcmread(image_SC)
    ds2 = pydicom.dcmread(image_no_SC)

    img_SC = ds1.pixel_array
    img_no_SC = ds2.pixel_array
    
    print("Minimum v SC - no_SC: ", np.min(img_SC - img_no_SC))
    print("Maximum v SC - no_SC: ", np.max(img_SC - img_no_SC))
    print("Mean v SC - no_SC: ", np.mean(img_SC - img_no_SC))
    print("STD v SC - no_SC: ", np.std(img_SC - img_no_SC))
    return None


if __name__ == "__main__":
    # Create the argument parser
    parser = argparse.ArgumentParser(description="Extract photopeak window from DICOM files.")
    
    # Add arguments for input and output directories
    parser.add_argument("image_SC", type=str, help="Path to the dicom image with scatter correction.")
    parser.add_argument("Image_no_SC", type=str, help="Path to the dicom image with NO scatter correction.")
    
    # Parse the command-line arguments
    args = parser.parse_args()
    
    # Call the function with the parsed arguments
    substract_SPECT_images(args.image_SC, args.image_no_SC)
