import pydicom
import matplotlib.pyplot as plt

# Path to your DICOM file
dicom_file_path = r'C:\Users\danie\Desktop\mrtva_doba_VU\KALIBRACE_20240815\Kalibrace_tomo_20240815_Optima\Kalibrace_zkouska_Optima_1_tomo.dcm'

# Read the DICOM file
try:
    dataset = pydicom.dcmread(dicom_file_path, force=True)
    print(dataset)

    # plt.imshow(dataset.pixel_array, cmap='gray')
    # plt.show()

    #print(dataset.pixel_array.shape)
    #plt.subplots(2,3, figsize=(15, 10), dpi = 200)
    #plt.subplot(231)
    #plt.imshow(dataset.pixel_array[0,:,:], cmap='gray')
    #plt.axis('off')
    #plt.subplot(232)
    #plt.imshow(dataset.pixel_array[1,:,:], cmap='gray')
    #plt.axis('off')
    #plt.subplot(233)
    #plt.imshow(dataset.pixel_array[2,:,:], cmap='gray')
    #plt.axis('off')
    #plt.subplot(234)
    #plt.imshow(dataset.pixel_array[3,:,:], cmap='gray')
    #plt.axis('off')
    #plt.subplot(235)
    #plt.imshow(dataset.pixel_array[4,:,:], cmap='gray')
    #plt.axis('off')
    #plt.subplot(236)
    #plt.imshow(dataset.pixel_array[5,:,:], cmap='gray')
    #plt.axis('off')
    #plt.show()
    
    # Check if (0011, 1012) tag exists
    if (0x0011, 0x1012) in dataset:
        dataset_names = dataset[(0x0011, 0x1012)].value
        
        # Iterate over each dataset name and print dicominfo
        for dataset_name in dataset_names:
            print(f"Dataset Name: {dataset_name}")
            
            # Access elements based on your requirement
            for elem in dataset:
                if dataset[elem].tag.is_private:
                    continue
                # Print element name and value
                print(f"{elem.name}: {dataset[elem].value}")
                
            print("\n")  # Separate each dataset info with a newline
            
except Exception as e:
    print(f"Error reading DICOM file: {str(e)}")
