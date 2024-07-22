import pydicom

def separate_dicom_file(dicom_path):
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
        'Head2_SC2': None,
        'Acq_time' : None
    }
    
    images['Acq_time'] = ds[0x0018, 0x1242].value*0.001

    # Assuming the order in the pixel_array is known and consistent
    images['Head1_EM'] = pixel_array[0]
    images['Head2_EM'] = pixel_array[1]
    images['Head1_SC1'] = pixel_array[2]
    images['Head2_SC1'] = pixel_array[3]
    images['Head1_SC2'] = pixel_array[4]
    images['Head2_SC2'] = pixel_array[5]

    return images