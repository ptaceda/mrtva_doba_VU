import pydicom

# Path to your DICOM file
dicom_file_path = 'KALIBRACE_20240815/Kalibrace_tomo_20240815_Optima/rekonstruovane_obrazy/Optima_0_PW_SPECT_iter_2_subsets_2.dcm'

# Read the DICOM file
try:
    dataset = pydicom.dcmread(dicom_file_path, force=True)
    print(dataset)
    
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
