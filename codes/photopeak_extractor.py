import pydicom
import numpy as np
import os
import argparse

def process_dicom_directory(input_dir, output_dir):
    # Get all DICOM files in the input directory and sort them alphabetically
    dicom_files = sorted([f for f in os.listdir(input_dir) if f.lower().endswith('.dcm')])

    if not dicom_files:
        print("No DICOM files found in the directory.")
        return

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Process each DICOM file in the directory
    for dicom_file in dicom_files:
        dicom_path = os.path.join(input_dir, dicom_file)
        try:
            extract_photopeak_anterior(dicom_path, output_dir)
        except Exception as e:
            print(f"Error processing {dicom_file}: {e}")
    
    print(f"Processing complete. Files saved in {output_dir}")

def extract_photopeak_anterior(dicom_path, output_dir):
    ds = pydicom.dcmread(dicom_path)

    object_names = ds.get((0x0011, 0x1050)).value

    try:
        photopeak_index = object_names.index('Head1_EM')
    except ValueError:
        raise ValueError("Photopeak window 'Head1_EM' not found in object names.")

    pixel_array = ds.pixel_array
    photopeak_image = pixel_array[photopeak_index, :, :]

    new_ds = ds.copy()
    new_ds.PixelData = photopeak_image.tobytes()
    new_ds.NumberOfFrames = 1
    new_ds[0x0011, 0x1050].value = ['Head1_EM']

    original_filename = os.path.basename(dicom_path)
    filename_no_ext, file_ext = os.path.splitext(original_filename)
    new_filename = f"{filename_no_ext}_PW{file_ext}"

    output_file = os.path.join(output_dir, new_filename)
    new_ds.save_as(output_file)
    print(f"Photopeak DICOM saved as {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process DICOM files to extract photopeak window.")
    parser.add_argument("input_dir", type=str, help="Directory containing DICOM files")
    parser.add_argument("output_dir", type=str, help="Directory to save processed DICOM files")

    args = parser.parse_args()

    process_dicom_directory(args.input_dir, args.output_dir)
