import os
import sys
import pydicom # type: ignore
import matplotlib.pyplot as plt # type: ignore
import pandas as pd # type: ignore
from glob import glob
from codes.custom_library import Graf_1_2

# Set the working directory to the project directory
device = input("Zadej prosím, na jakém zařízení děláš (mac/doma/prace): ")
if device == "doma":
    project_dir = r"C:/Users/danie/Desktop/mrtva_doba_VU"
    os.chdir(project_dir)
elif device == "mac":
    project_dir = r"/Users/danielptacek/Desktop/mrtva_doba_VU"
    os.chdir(project_dir)
else:
    project_dir = r"U:/Dokumenty/mrtva_doba_VU"
    os.chdir(project_dir)


# Verify the change
print("Current working directory:", os.getcwd()) 

# Ensure the project directory is in sys.path
if project_dir not in sys.path:
    sys.path.append(project_dir)




### ------------------------------------

from dicom_file_separator import separate_dicom_file_tomo
import numpy as np
from glob import glob
from pytomography.io.SPECT import dicom
from pytomography.algorithms import OSEM
from pytomography.projectors.SPECT import SPECTSystemMatrix
from pytomography.likelihoods import PoissonLogLikelihood
import tifffile

kal_obraz_path = "KALIBRACE_20240815/Kalibrace_tomo_20240815_Optima/Kalibrace_tomo_1_20240815_Optima.dcm"
soubor_path_obrazu = glob('KALIBRACE_20240815/Kalibrace_tomo_20240815_Optima/Kalibrace*.dcm')
min_pocet_iter = 2
max_pocet_iter = 8
min_pocet_subset = 2
max_pocet_subset = 16

output_dir = 'KALIBRACE_20240815/Kalibrace_tomo_20240815_Optima/rekonstruovane_obrazy_tiff'
os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist

# Function to save the reconstructed image as a DICOM
# def save_reconstructed_image_as_dicom(reconstructed_image, output_filename):
#     ds = pydicom.Dataset()

#     # Add necessary DICOM metadata
#     ds.PatientName = "Tomograficka^kalibrace^20240815^Optima"
#     ds.PatientID = "20240815"
#     ds.Modality = "NM"  # Nuclear Medicine (SPECT)
#     ds.SeriesInstanceUID = pydicom.uid.generate_uid()
#     ds.SOPInstanceUID = pydicom.uid.generate_uid()
#     ds.StudyInstanceUID = pydicom.uid.generate_uid()
    
#     # Assuming reconstructed_image has shape (slices, height, width)
#     slices, rows, cols = reconstructed_image.shape
    
#     # Metadata for the reconstructed image
#     ds.SamplesPerPixel = 1
#     ds.PhotometricInterpretation = "MONOCHROME2"
#     ds.Rows = rows
#     ds.Columns = cols
#     ds.NumberOfFrames = slices
#     ds.BitsAllocated = 16
#     ds.BitsStored = 16
#     ds.HighBit = 15
#     ds.PixelRepresentation = 0  # Unsigned integer
#     ds.SliceThickness = 0.4416968  # You can adjust based on metadata

#     # For 3D data, PixelData should be a multi-frame DICOM
#     print(np.array(reconstructed_image).shape)
#     ds.PixelData = np.array(reconstructed_image)

#     # Set encoding attributes
#     ds.is_little_endian = True
#     ds.is_implicit_VR = False

#     # Save the DICOM file
#     output_path = os.path.join(output_dir, output_filename)
#     ds.save_as(output_path)
#     print(f"Reconstructed image saved as DICOM: {output_path}")

def save_reconstructed_image_as_tiff(reconstructed_image, output_filename):
    output_path = os.path.join(output_dir, output_filename)
    # Save the 3D image data as a multi-page TIFF
    tifffile.imwrite(output_path, np.array(reconstructed_image), dtype=np.array(reconstructed_image).dtype)
    print(f"Reconstructed image saved as TIFF: {output_filename}")




for path, i in zip(soubor_path_obrazu, range(len(soubor_path_obrazu))):
    for n_iter in np.arange(min_pocet_iter, max_pocet_iter + 1):
        for n_subset in np.arange(min_pocet_subset, max_pocet_subset + 1,2):
            
            ### načtení potřebných metadat
            object_meta, proj_meta = dicom.get_metadata(kal_obraz_path, index_peak=0)

            ### načítání photopeak projekcí
            photopeak = dicom.get_projections(kal_obraz_path, index_peak=0)

            ### načtení scatter estimate
            scatter = dicom.get_energy_window_scatter_estimate(kal_obraz_path, index_peak=0, index_lower=2, index_upper=1)

            ### vytvorení SPECT systémové matice
            system_matrix = SPECTSystemMatrix(
                obj2obj_transforms = [],
                proj2proj_transforms = [],
                object_meta = object_meta,
                proj_meta = proj_meta
            )

            ### vytvorení likelihood založeného na logaritmu Poissonova rozdelení
            likelihood_PW = PoissonLogLikelihood(system_matrix, photopeak)
            likelihood_TEW = PoissonLogLikelihood(system_matrix, photopeak, scatter)

            ### zadefinování rekonstrukčního algoritmu OSEM
            reconstruction_algorithm_PW = OSEM(likelihood_PW)
            reconstruction_algorithm_TEW = OSEM(likelihood_TEW)

            ### provedení rekonstrukce
            reconstructed_object_PW = reconstruction_algorithm_PW(n_iters=n_iter, n_subsets=n_subset)
            reconstructed_object_TEW = reconstruction_algorithm_TEW(n_iters=n_iter, n_subsets=n_subset)

            ### Uložit výsledné objekty jako DICOM soubory
            pw_filename = f'Discovery_{i}_PW_SPECT_iter_{n_iter}_subsets_{n_subset}.tiff'
            tew_filename = f'Discovery_{i}_TEW_SPECT_iter_{n_iter}_subsets_{n_subset}.tiff'

            save_reconstructed_image_as_tiff(reconstructed_object_PW, pw_filename)
            save_reconstructed_image_as_tiff(reconstructed_object_TEW, tew_filename)
            print('-------')
    print(f'Hotova {i}/3 všech souboru')

print('Všechno je hotovo, nyni spustit 3 příkazy:')
print('|git add .| a počkat (bez tech |)')
print('|git commit -am "Dodelani OPTIMA SPECTu ve formatu tiff"| a opět počkat')
print('|git push| a opět počkat, potom by to mělo být vše a vše je odesláno na github')




















# # idx_z = 61
# # slice_pytomography_PW = reconstructed_object_PW.cpu()[:,:,idx_z].T
# # slice_pytomography_PW_SC = reconstructed_object_PW_SC.cpu()[:,:,idx_z].T

# # plt.subplots(1,3)
# # plt.subplot(131)
# # plt.title('PW')
# # plt.pcolormesh(slice_pytomography_PW , cmap='magma')
# # plt.axis('off')
# # plt.colorbar()
# # plt.subplot(132)
# # plt.title('PW a SC')
# # plt.pcolormesh(slice_pytomography_PW_SC, cmap='magma')
# # plt.axis('off')
# # plt.colorbar()
# # plt.subplot(133)
# # plt.title('PW - (PW a SC)')
# # plt.pcolormesh(slice_pytomography_PW - slice_pytomography_PW_SC, cmap='magma')
# # plt.axis('off')
# # plt.colorbar()

# # plt.show()