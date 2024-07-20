import pydicom
import matplotlib.pyplot as plt
import os
from glob import glob

folder = input("Zadejte cestu k souborům: ")

text_file_path = os.path.join(folder, 'vysledky.txt')
with open(text_file_path, 'w+') as file:
    file.write('Vysledky mereni mrtve doby:\n')
    file.write('Typ_Datum_kamera    Hlava_okno  Pocet_akum_impulsu  Acq_time  Count_rate\n')

# Define file pattern to find DICOM files
dead_time = glob(os.path.join(folder, 'MD_*.dcm'))[0]
pozadi = glob(os.path.join(folder, 'Pozadi_*.dcm'))[0]

data_paths = [dead_time, pozadi]

# Load the DICOM file
dt_data = pydicom.dcmread(dead_time)
pozadi_data = pydicom.dcmread(pozadi)

data = [dt_data, pozadi_data]

for dicom_data, path in zip(data, data_paths):
    # Get the base filename without extension
    base_filename = os.path.basename(path)
    filename_without_extension = os.path.splitext(base_filename)[0]

    # Access the custom group containing Dataset Names and print them
    if (0x0011, 0x1012) in dicom_data:
        dataset_names = dicom_data[0x0011, 0x1012].value
        dataset_acq_time = dicom_data[0x0018, 0x1242].value*0.001

        # Extract the pixel array from the DICOM data
        if 'PixelData' in dicom_data:
            pixel_array = dicom_data.pixel_array

            # Check if the pixel array has the expected number of slices
            num_slices = pixel_array.shape[0]
            if num_slices != len(dataset_names):
                print("Warning: Number of slices does not match the number of dataset names.")

            # Create a figure and a 2x3 grid of subplots
            fig, axes = plt.subplots(2, 3, figsize=(15, 10), dpi = 200)
            
            # Flatten the axes array for easy iteration
            axes = axes.flatten()

            # Separate the indices of "Head1" and "Head2" datasets
            head1_indices = [i for i, name in enumerate(dataset_names) if "Head1" in name]
            head2_indices = [i for i, name in enumerate(dataset_names) if "Head2" in name]

            # Loop through each "Head1" slice and plot it in the first row
            for idx, head1_idx in enumerate(head1_indices):
                ax = axes[idx]
                ax.imshow(pixel_array[head1_idx], cmap='gray')
                ax.set_title(dataset_names[head1_idx])
                ax.axis('off')  # Hide the axes ticks

                # Calculate and print the sum of pixel values
                pixel_sum = pixel_array[head1_idx].sum()
                count_rate = pixel_sum / dataset_acq_time
                with open(text_file_path, 'a+') as file:
                    file.write(f"{filename_without_extension}   {dataset_names[head1_idx]}  {pixel_sum} {dataset_acq_time} {round(count_rate,2)}\n")

            # Loop through each "Head2" slice and plot it in the second row
            for idx, head2_idx in enumerate(head2_indices):
                ax = axes[idx + 3]
                ax.imshow(pixel_array[head2_idx], cmap='gray')
                ax.set_title(dataset_names[head2_idx])
                ax.axis('off')  # Hide the axes ticks

                # Calculate and print the sum of pixel values
                pixel_sum = pixel_array[head2_idx].sum()
                count_rate = pixel_sum / dataset_acq_time
                with open(text_file_path, 'a+') as file:
                    file.write(f"{filename_without_extension}   {dataset_names[head2_idx]} {pixel_sum} {dataset_acq_time} {round(count_rate,2)}\n")
                    file.close()

            # Adjust layout to avoid overlap
            fig.savefig(os.path.join(folder, f'{filename_without_extension}.jpg'), bbox_inches='tight')

        else:
            print("No image data found in the DICOM file.")
    else:
        print("The DICOM file does not contain the expected custom group with dataset names.")
