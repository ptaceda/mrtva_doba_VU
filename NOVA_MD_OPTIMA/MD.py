import pydicom
import matplotlib.pyplot as plt
from glob import glob
import numpy as np
import cv2
from potrebne_funkce import ROI_drawer_manual, align_images



MD_folders = r"Optima"


pw_1 = {}
lsc_1 = {}
usc_1 = {}
pw_2 = {}
lsc_2 = {}
usc_2 = {}

datum = {}
cas = {}
trvani_akvizice = {}

i=0

folders = sorted(glob(MD_folders + "/MD_*"))
for folder in folders:
    print(sorted(glob(folder + "/*.dcm")))
    kapsle_path, pozadi_path = sorted(glob(folder + "/*.dcm"))

    pozadi = pydicom.dcmread(pozadi_path)
    kapsle = pydicom.dcmread(kapsle_path)

    datum_akvizice_kapsle = kapsle.get_item((0x0008, 0x0022)).value
    time_akvizice_kapsle = kapsle.get_item((0x0008, 0x0032)).value

    cas_akvizice_pozadi = float(pozadi.get_item((0x0018, 0x1242)).value)/1000 # v sekundach
    cas_akvizice_kapsle = float(kapsle.get_item((0x0018, 0x1242)).value)/1000 # v sekundach
    
    pozadi_data = pozadi.pixel_array
    kapsle_data = kapsle.pixel_array


    ### rozrazeni na jednotliva okna
    pozadi_PW_1, pozadi_USC_1, pozadi_LSC_1 = pozadi_data[0], pozadi_data[2], pozadi_data[4]
    pozadi_PW_2, pozadi_USC_2, pozadi_LSC_2 = pozadi_data[1], pozadi_data[3], pozadi_data[5]

    kapsle_PW_1, kapsle_USC_1, kapsle_LSC_1 = kapsle_data[0], kapsle_data[2], kapsle_data[4]
    kapsle_PW_2, kapsle_USC_2, kapsle_LSC_2 = kapsle_data[1], kapsle_data[3], kapsle_data[5]



    ### odecteni pozadi od jednotlivych oken v kapsli s prislusnym casovym faktorem
    kapsle_PW_1 = kapsle_PW_1 - (cas_akvizice_kapsle/cas_akvizice_pozadi)*pozadi_PW_1
    kapsle_LSC_1 = kapsle_LSC_1 - (cas_akvizice_kapsle/cas_akvizice_pozadi)*pozadi_LSC_1
    kapsle_USC_1 = kapsle_USC_1 - (cas_akvizice_kapsle/cas_akvizice_pozadi)*pozadi_USC_1

    kapsle_PW_2 = kapsle_PW_2 - (cas_akvizice_kapsle/cas_akvizice_pozadi)*pozadi_PW_2
    kapsle_LSC_2 = kapsle_LSC_2 - (cas_akvizice_kapsle/cas_akvizice_pozadi)*pozadi_LSC_2
    kapsle_USC_2 = kapsle_USC_2 - (cas_akvizice_kapsle/cas_akvizice_pozadi)*pozadi_USC_2

    ### naleznuti ROI - masky
    # if i == 0:
    #     predmaska_1 = ROI_drawer_manual(kapsle_PW_1)
    #     predmaska_1.show()
    #     predmaska_2 = ROI_drawer_manual(kapsle_PW_2)
    #     predmaska_2.show()

    #     maska_1 = predmaska_1.mask
    #     maska_2 = predmaska_2.mask

    #     reference_PW_1 = kapsle_PW_1
    #     reference_LSC_1 = kapsle_LSC_1
    #     reference_USC_1 = kapsle_USC_1

    #     reference_PW_2 = kapsle_PW_2
    #     reference_LSC_2 = kapsle_LSC_2
    #     reference_USC_2 = kapsle_USC_2
    # else:
    #     kapsle_PW_1 = align_images(reference_PW_1, kapsle_PW_1)
    #     kapsle_LSC_1 = align_images(reference_LSC_1, kapsle_LSC_1)
    #     kapsle_USC_1 = align_images(reference_USC_1, kapsle_USC_1)

    #     kapsle_PW_2 = align_images(reference_PW_2, kapsle_PW_2)
    #     kapsle_LSC_2 = align_images(reference_LSC_2, kapsle_LSC_2)
    #     kapsle_USC_2 = align_images(reference_USC_2, kapsle_USC_2)

    # ### Aplikace masky na jednotlive snimky
    # kapsle_PW_1_prikon_impulsu = np.sum(maska_1 * kapsle_PW_1)/cas_akvizice_kapsle
    # kapsle_LSC_1_prikon_impulsu = np.sum(maska_1 * kapsle_LSC_1)/cas_akvizice_kapsle
    # kapsle_USC_1_prikon_impulsu = np.sum(maska_1 * kapsle_USC_1)/cas_akvizice_kapsle

    # plt.imshow(maska_1 * kapsle_PW_1)
    # plt.show()
    # plt.imshow(maska_1 * kapsle_LSC_1)
    # plt.show()

    # kapsle_PW_2_prikon_impulsu = np.sum(maska_2 * kapsle_PW_2)/cas_akvizice_kapsle
    # kapsle_LSC_2_prikon_impulsu = np.sum(maska_2 * kapsle_LSC_2)/cas_akvizice_kapsle
    # kapsle_USC_2_prikon_impulsu = np.sum(maska_2 * kapsle_USC_2)/cas_akvizice_kapsle

    ### Aplikace masky na jednotlive snimky
    kapsle_PW_1_prikon_impulsu = np.sum(kapsle_PW_1)/cas_akvizice_kapsle
    kapsle_LSC_1_prikon_impulsu = np.sum(kapsle_LSC_1)/cas_akvizice_kapsle
    kapsle_USC_1_prikon_impulsu = np.sum(kapsle_USC_1)/cas_akvizice_kapsle

    kapsle_PW_2_prikon_impulsu = np.sum(kapsle_PW_2)/cas_akvizice_kapsle
    kapsle_LSC_2_prikon_impulsu = np.sum(kapsle_LSC_2)/cas_akvizice_kapsle
    kapsle_USC_2_prikon_impulsu = np.sum(kapsle_USC_2)/cas_akvizice_kapsle

    pw_1[i] = kapsle_PW_1_prikon_impulsu
    lsc_1[i] = kapsle_LSC_1_prikon_impulsu
    usc_1[i] = kapsle_USC_1_prikon_impulsu

    pw_2[i] = kapsle_PW_2_prikon_impulsu
    lsc_2[i] = kapsle_LSC_2_prikon_impulsu
    usc_2[i] = kapsle_USC_2_prikon_impulsu

    datum[i] = datum_akvizice_kapsle
    cas[i] = time_akvizice_kapsle
    trvani_akvizice[i] = cas_akvizice_kapsle

    i+=1


print("pw_1 = ")
print(pw_1)
print("\nlsc_1 = ")
print(lsc_1)
print("\nusc_1 =")
print(usc_1)

print("\npw_2")
print(pw_2)
print("\nlsc_2")
print(lsc_2)
print("\nusc_2")
print(usc_2)

print("\ndatum_akvizice")
print(datum)
print("\ncas_akvizice")
print(cas)
print("\ntrvani_akvizice")
print(trvani_akvizice)


