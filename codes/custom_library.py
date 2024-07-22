'''
Načítá se takhle:
import importlib.util
import sys

sys.path.insert(0, '/Users/danielptacek/Desktop/WORKSPACE/Knihovny_a_postupy')

my_lib = importlib.util.module_from_spec(importlib.util.spec_from_file_location('custom_library', '/Users/danielptacek/Desktop/WORKSPACE/Knihovny_a_postupy/custom_library.py'))
importlib.util.spec_from_file_location('custom_library', '/Users/danielptacek/Desktop/WORKSPACE/Knihovny_a_postupy/custom_library.py').loader.exec_module(moje_knihovna)
sys.modules['custom_library'] = my_lib

'''

import locale
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
from queue import Queue
import time
import pydicom as pdic



def carka(cislo_s_teckou, zaokr_index):
    cislo = round(cislo_s_teckou, zaokr_index)
    cislo_s_carkou = str(cislo).replace('.', ',')
    return cislo_s_carkou

def carka_for_funkce(cislo_s_teckou, zaokr_index):
    cislo = round(cislo_s_teckou, zaokr_index)
    cislo_s_carkou = str(cislo).replace('.', '{,}')
    return cislo_s_carkou

def zaokrouhleni(cislo, nejistota, pripadne_plus):
    char = str(nejistota)

    if nejistota >= 1:
        num = int(nejistota)
        num_str = str(num)
        index = (-len(num_str)+1) + pripadne_plus
    
    elif nejistota <= -1:
        num = -int(nejistota)
        num_str = str(num)
        index = (-len(num_str)+1) + pripadne_plus
    
    elif ('e' in char or 'E' in char) and nejistota > 0:
        helper = char.index('-')
        substring = char[helper+1:]
        index = int(substring) + pripadne_plus
    
    elif ('e' in char or 'E' in char) and nejistota < 0:
        reversed_char = char[::-1]
        helper = reversed_char.index('-')
        substring = char[len(char) - helper:]
        index = int(substring) + pripadne_plus

    elif -1 < nejistota < 0:  
        index = 1 + pripadne_plus
        for i in range(3,len(char[1:])):
            if char[i] == '0':
                index += 1
            else:
                break

    elif 0 < nejistota < 1:
        index = 1 + pripadne_plus
        for i in range(2,len(char)):
            if char[i] == '0':
                index += 1
            else:
                break

    else:
        index = 0 + pripadne_plus
    
    zaokr_cislo_s_nejistotou = np.array([round(cislo, index), round(nejistota, index)])
    return zaokr_cislo_s_nejistotou

class Graf_1:
    def __init__(self, fontsize, title, xlabel, ylabel, figsize, legend_fontsize=None) -> None:
        # nastavi v grafech carky misto tecek
        locale.setlocale(locale.LC_NUMERIC, "de_DE")
        plt.rcdefaults()
        plt.rcParams['axes.formatter.use_locale'] = True
        plt.rcParams['font.size'] = fontsize
        plt.rcParams['xtick.labelsize'] = fontsize
        plt.rcParams['ytick.labelsize'] = fontsize

        self.Figure, self.fig = plt.subplots(figsize = figsize, dpi = 250) 
        self.title = title
        self.ylabel = ylabel
        self.xlabel = xlabel
        self.legend_fontsize = legend_fontsize if legend_fontsize is not None else fontsize - 4

        self.fig.set_xlabel(self.xlabel)
        self.fig.set_ylabel(self.ylabel)
        self.fig.set_title(self.title)
        self.fig.grid(color='black', ls='-.', lw=0.25)

    def plot(self, x, y, marker, label_data, color, markeredgewidth, markersize):
        self.fig.plot(x, y, marker, label=label_data, color=color, markeredgewidth=markeredgewidth, markersize=markersize)
        self.fig.legend(loc='best', edgecolor='black', fontsize=self.legend_fontsize)
    
    def errorbar(self, x, y, yerr, marker, label_data, color, markersize, sirka_nejistot, sirka_primky_nejistot):
        self.fig.errorbar(x=x, y=y, yerr=yerr, fmt=' ', marker=marker, markersize=markersize, ecolor='black', zorder=2, elinewidth=sirka_primky_nejistot, label=label_data, capsize=sirka_nejistot, color=color)
        self.fig.legend(loc='best', edgecolor='black', fontsize=self.legend_fontsize)

class Graf_1_2:
    def __init__(self, fontsize, suptitle, title_1, xlabel_1, ylabel_1, title_2, xlabel_2, ylabel_2, figsize) -> None:
        # nastavi v grafech carky misto tecek
        locale.setlocale(locale.LC_NUMERIC, "de_DE")
        plt.rcdefaults()
        plt.rcParams['axes.formatter.use_locale'] = True
        plt.rcParams['font.size'] = fontsize
        plt.rcParams['xtick.labelsize'] = fontsize
        plt.rcParams['ytick.labelsize'] = fontsize

        self.Figure, self.fig = plt.subplots(1,2, figsize = figsize, dpi = 250) 
        self.suptitle = suptitle

        self.title_1 = title_1
        self.ylabel_1 = ylabel_1
        self.xlabel_1 = xlabel_1

        self.title_2 = title_2
        self.ylabel_2 = ylabel_2
        self.xlabel_2 = xlabel_2

        plt.suptitle(self.suptitle, fontweight="bold")
        
        self.fig[0].set_xlabel(self.xlabel_1)
        self.fig[0].set_ylabel(self.ylabel_1)
        self.fig[0].set_title(self.title_1, fontweight="bold")
        self.fig[0].grid(color='black', ls = '-.', lw = 0.35)

        self.fig[1].set_xlabel(self.xlabel_2)
        self.fig[1].set_ylabel(self.ylabel_2)
        self.fig[1].set_title(self.title_2, fontweight="bold")
        self.fig[1].grid(color='black', ls = '-.', lw = 0.35)

    def plot(self, x, y, i, marker, label_data, color, markeredgewidth, markersize):
        self.fig[i].plot(x=x, y=y, marker = marker, label = label_data, color = color, markeredgewidth = markeredgewidth, markersize = markersize)
        self.fig[i].legend(loc = 'best', edgecolor = 'black', fontsize = 11)
    
    def errorbar(self, x, y, i, yerr, marker, label_data, color, ecolor, markersize, sirka_nejistot, sirka_primky_nejistot):
        self.fig[i].errorbar(x=x, y=y, yerr= yerr, fmt=' ', marker = marker, markersize = markersize, ecolor = ecolor, zorder = 2, elinewidth=sirka_primky_nejistot, label = label_data, capsize=sirka_nejistot, color = color)
        self.fig[i].legend(loc = 'best', edgecolor = 'black', fontsize = 11)

class Graf_2_1:
    def __init__(self, fontsize, suptitle, title_1, xlabel_1, ylabel_1, title_2, xlabel_2, ylabel_2, figsize) -> None:
        # nastavi v grafech carky misto tecek
        locale.setlocale(locale.LC_NUMERIC, "de_DE")
        plt.rcdefaults()
        plt.rcParams['axes.formatter.use_locale'] = True
        plt.rcParams['font.size'] = fontsize
        plt.rcParams['xtick.labelsize'] = fontsize
        plt.rcParams['ytick.labelsize'] = fontsize

        self.Figure, self.fig = plt.subplots(2,1, figsize = figsize, dpi = 250) 
        self.suptitle = suptitle

        self.title_1 = title_1
        self.ylabel_1 = ylabel_1
        self.xlabel_1 = xlabel_1

        self.title_2 = title_2
        self.ylabel_2 = ylabel_2
        self.xlabel_2 = xlabel_2

        plt.suptitle(self.suptitle)
        
        self.fig[0].set_xlabel(self.xlabel_1)
        self.fig[0].set_ylabel(self.ylabel_1)
        self.fig[0].set_title(self.title_1, fontweight="bold")
        self.fig[0].grid(color='black', ls = '-.', lw = 0.2)

        self.fig[1].set_xlabel(self.xlabel_2)
        self.fig[1].set_ylabel(self.ylabel_2)
        self.fig[1].set_title(self.title_2, fontweight="bold")
        self.fig[1].grid(color='black', ls = '-.', lw = 0.2)

    def plot(self, x, y, i, marker, label_data, color, markeredgewidth, markersize):
        self.fig[i].plot(x=x, y=y, marker = marker, label = label_data, color = color, markeredgewidth = markeredgewidth, markersize = markersize)
        # self.fig[i].legend(loc = 'best', edgecolor = 'black', fontsize = 12)
    
    def errorbar(self, x, y, i, yerr, marker, label_data, color, ecolor, markersize, sirka_nejistot, sirka_primky_nejistot):
        self.fig[i].errorbar(x=x, y=y, yerr= yerr, fmt=' ', marker = marker, markersize = markersize, ecolor = ecolor, zorder = 2, elinewidth=sirka_primky_nejistot, label = label_data, capsize=sirka_nejistot, color = color)
        # self.fig[i].legend(loc = 'best', edgecolor = 'black', fontsize = 12)



def region_growing(image, threshold):
    zacatek = time.time()
    # Find the maximum pixel value in the image
    seed = np.unravel_index(np.argmax(image), image.shape)
    
    # Create a binary mask with the same shape as the image
    mask = np.zeros_like(image, dtype=bool)
    
    # Create a queue and add the seed pixel to it
    q = Queue()
    q.put(seed)
    # Loop until the queue is empty
    while not q.empty():
        # Get the next pixel from the queue
        pixel = q.get()
        
        # Check if the pixel is greater than the threshold
        if image[tuple(map(int, pixel))] > threshold:
            # Mark the pixel in the mask
            mask[tuple(pixel)] = True
            # print(f'Pixel {pixel} has been put into mask. It should not be put in the queue to be examined.')
            
            # Get the neighbors of the pixel
            neighbors = np.array([
                [pixel[0] - 1, pixel[1]],
                [pixel[0] + 1, pixel[1]],
                [pixel[0], pixel[1] - 1],
                [pixel[0], pixel[1] + 1]
            ])
            
            # Check each neighbor and add it to the queue if it meets the criteria
            for neighbor in neighbors:
                if (
                    0 <= neighbor[0] < image.shape[0] and
                    0 <= neighbor[1] < image.shape[1] and
                    not mask[tuple(neighbor)] and
                    image[tuple(map(int, neighbor))] > threshold
                ):
                    mask[tuple(neighbor)] = True
                    q.put(tuple(neighbor))
                    # print(f'Pixel {tuple(neighbor)} was put in the queue.')
    
    # Return the binary mask
    konec = time.time()
    cas = konec - zacatek
    # print(f"maska hotova za {cas:.5f} seconds")
    return mask

def region_growing3D(image, threshold):
    zacatek = time.time()
    # Find the maximum pixel value in the image
    seed = np.unravel_index(np.argmax(image), image.shape)
    # Create a binary mask with the same shape as the image
    mask = np.zeros_like(image, dtype=bool)
    
    # Create a queue and add the seed pixel to it
    q = Queue()
    q.put(seed)
    # Loop until the queue is empty
    while not q.empty():
        # Get the next pixel from the queue
        pixel = q.get()
        
        # Check if the pixel is greater than the threshold
        if image[tuple(map(int, pixel))] > threshold:
            # Mark the pixel in the mask
            mask[tuple(pixel)] = True
            # print(f'Pixel {pixel} has been put into mask. It should not be put in the queue to be examined.')
            
            # Get the neighbors of the pixel
            neighbors = np.array([
                [pixel[0] - 1, pixel[1], pixel[2]],
                [pixel[0] + 1, pixel[1], pixel[2]],
                [pixel[0], pixel[1] - 1, pixel[2]],
                [pixel[0], pixel[1] + 1, pixel[2]],
                [pixel[0], pixel[1], pixel[2] - 1],
                [pixel[0], pixel[1], pixel[2] + 1]
            ])
            
            # Check each neighbor and add it to the queue if it meets the criteria
            for neighbor in neighbors:
                if (
                    0 <= neighbor[0] < image.shape[0] and
                    0 <= neighbor[1] < image.shape[1] and
                    0 <= neighbor[2] < image.shape[2] and
                    not mask[tuple(neighbor)] and
                    image[tuple(map(int, neighbor))] > threshold
                ):
                    mask[tuple(neighbor)] = True
                    q.put(tuple(neighbor))
                    # print(f'Pixel {tuple(neighbor)} was put in the queue.')
    
    # Return the binary mask
    konec = time.time()
    cas = konec - zacatek
    # print(f"maska hotova za {cas:.5f} seconds")
    return mask

def region_growing3D_for_nema(image, threshold, starting_point):
    zacatek = time.time()
    # Find the maximum pixel value in the image
    seed = starting_point
    # Create a binary mask with the same shape as the image
    mask = np.zeros_like(image, dtype=bool)
    
    # Create a queue and add the seed pixel to it
    q = Queue()
    q.put(seed)
    # Loop until the queue is empty
    while not q.empty():
        # Get the next pixel from the queue
        pixel = q.get()
        
        # Check if the pixel is greater than the threshold
        if image[tuple(map(int, pixel))] > threshold:
            # Mark the pixel in the mask
            mask[tuple(pixel)] = True
            # print(f'Pixel {pixel} has been put into mask. It should not be put in the queue to be examined.')
            
            # Get the neighbors of the pixel
            neighbors = np.array([
                [pixel[0] - 1, pixel[1], pixel[2]],
                [pixel[0] + 1, pixel[1], pixel[2]],
                [pixel[0], pixel[1] - 1, pixel[2]],
                [pixel[0], pixel[1] + 1, pixel[2]],
                [pixel[0], pixel[1], pixel[2] - 1],
                [pixel[0], pixel[1], pixel[2] + 1]
            ])
            
            # Check each neighbor and add it to the queue if it meets the criteria
            for neighbor in neighbors:
                if (
                    0 <= neighbor[0] < image.shape[0] and
                    0 <= neighbor[1] < image.shape[1] and
                    0 <= neighbor[2] < image.shape[2] and
                    not mask[tuple(neighbor)] and
                    image[tuple(map(int, neighbor))] > threshold
                ):
                    mask[tuple(neighbor)] = True
                    q.put(tuple(neighbor))
                    # print(f'Pixel {tuple(neighbor)} was put in the queue.')
    
    # Return the binary mask
    konec = time.time()
    cas = konec - zacatek
    # print(f"maska hotova za {cas:.5f} seconds")
    return mask

def flip_matrix(matrix):
    flipped_matrix = [[[not value for value in row] for row in plane] for plane in matrix]
    return flipped_matrix

def funkce_valec(path_to_file, sdd_nebo_V, t, aktivita, objem_nebo_vzalenost, threshold_v_procent):    
    nejistoty_RG = {0.03: 0.02289437722894377,
                    0.05: 0.019765532182542452,
                    0.1: 0.015985499564608336,
                    0.15: 0.017686623527730715,
                    0.2: 0.037546836876960615,
                    0.25: 0.047207383382619476,
                    0.3: 0.05222274769449042,
                    0.35: 0.0866598622874901,
                    0.4: 0.3362928221859707,
                    0.45: 0.33304481960750704,
                    0.5: 0.5015684051398337,
                    0.55: 0.7004978062774215}

    dicom_image = pdic.dcmread(path_to_file)

    image = dicom_image.pixel_array
    image_bg = image[145:171, 210:241]


    figure, ax = plt.subplots(1,2, figsize = (12,12), dpi = 200)

    rozdil = image.max() - image_bg.mean()

    maska = region_growing(image, (threshold_v_procent/100)*rozdil)

    ax[0].imshow(image, cmap='gray')
    if objem_nebo_vzalenost == 'vzdalenost':
        ax[0].set_title('Vzdálenost ' + sdd_nebo_V +' cm')
    else:
        ax[0].set_title('Objem ' + sdd_nebo_V +' ml')
    ax[1].imshow(maska)
    ax[1].set_title('ROIka pomocí region growingu, thresh = '+ str(threshold_v_procent) +' %')

    celkem_count = np.sum(image)
    roi_count = np.sum(image * maska)
    sigma_roi_count = np.sqrt(roi_count)
    nejistota_RG = nejistoty_RG[round(0.01*threshold_v_procent,2)]*roi_count
    celkova_nejistota_roi_count = np.sqrt(sigma_roi_count**2 + nejistota_RG**2)

    cps = roi_count/t    
    cps_err = celkova_nejistota_roi_count/t

    citlivost = cps/aktivita
    citlivost_err = citlivost * np.sqrt( (cps_err / cps)**2 + (0.03)**2 )
    
    a = zaokrouhleni(citlivost, citlivost_err, 1)
    ax[0].text(23,40,f'Počet impulsů v obraze = {celkem_count}\nPočet impulsů v roice = {roi_count}\nCitlivost = ({carka(a[0], 2)} +- {carka(a[1], 2)}) cps/MBq', color = 'white')
    if objem_nebo_vzalenost == 'vzdalenost':
        figure.savefig('/Users/danielptacek/Library/CloudStorage/OneDrive-ČeskévysokéučenítechnickévPraze/dokumenty_BP/bachelor_data/obrazky/RG_threshold_'+ str(threshold_v_procent) +'/valec_plan_5ml_vzdalenost/valec_plan_5ml_'+ sdd_nebo_V +'cm.jpg', bbox_inches = 'tight')
    else:
        figure.savefig('/Users/danielptacek/Library/CloudStorage/OneDrive-ČeskévysokéučenítechnickévPraze/dokumenty_BP/bachelor_data/obrazky/RG_threshold_'+ str(threshold_v_procent) +'/valec_plan_objem_10cm/valec_plan_'+ sdd_nebo_V +'ml_10cm.jpg', bbox_inches = 'tight')

    plt.close()
    return citlivost, citlivost_err


def funkce_antrop(path_to_file,sdd, objem, t, pred_A, po_A, threshold_v_procent):
    # nacteni dat
    dicom_image = pdic.dcmread(path_to_file)

    rel_nejistoty_RG = {0.03: 0.02289437722894377,
                        0.05: 0.019765532182542452,
                        0.1: 0.015985499564608336,
                        0.15: 0.017686623527730715,
                        0.2: 0.037546836876960615,
                        0.25: 0.047207383382619476,
                        0.3: 0.05222274769449042,
                        0.35: 0.0866598622874901,
                        0.4: 0.3362928221859707,
                        0.45: 0.33304481960750704,
                        0.5: 0.5015684051398337,
                        0.55: 0.7004978062774215}

    # Berou se snímky jen z horní kamery
    image = dicom_image.pixel_array[0]
    image_bg = image[145:181, 205:241]
    # if objem == 'v1' and sdd == '5':
    #     print(np.mean(image_bg))

    figure, ax = plt.subplots(1,2, figsize = (12,12), dpi = 200)

    rozdil = image.max() - image_bg.mean()

    maska = region_growing(image, (threshold_v_procent/100)*rozdil)

    ax[0].imshow(image, cmap='gray')
    ax[0].set_title('Vzdálenost - ' + sdd +' cm, Objem - '+ objem)
    ax[1].imshow(maska)
    ax[1].set_title('ROIka pomocí region growingu, thresh = '+ str(threshold_v_procent) +' %')

    celkem_count = np.sum(image)
    roi_count = np.sum(image * maska)
    sigma_roi_count = np.sqrt(roi_count)
    nejistota_RG = rel_nejistoty_RG[round(0.01*threshold_v_procent,2)]*roi_count

    celkova_nejistota_roi_count = np.sqrt(sigma_roi_count**2 + nejistota_RG**2)

    cps = roi_count/t    
    cps_err = celkova_nejistota_roi_count/t

    aktivita = pred_A - po_A
    aktivita_err = np.sqrt((0.03*pred_A)**2 + (0.03*po_A)**2)

    citlivost = cps/aktivita
    citlivost_err = citlivost * np.sqrt((cps_err/cps)**2 + (aktivita_err/aktivita)**2)

    a = zaokrouhleni(citlivost, citlivost_err, 1)
    ax[0].text(23,40,f'Počet impulsů v obraze = {celkem_count}\nPočet impulsů v roice = {roi_count}\nCitlivost = ({carka(a[0],2)} +- {carka(a[1], 2)}) cps/MBq', color = 'white')
    figure.savefig('/Users/danielptacek/Library/CloudStorage/OneDrive-ČeskévysokéučenítechnickévPraze/dokumenty_BP/bachelor_data/obrazky/RG_threshold_'+ str(threshold_v_procent) +'/antrop_plan_'+ objem +'_vzdalenost/antrop_plan_'+ objem +'_'+ sdd +'cm.jpg', bbox_inches = 'tight')
    
    plt.close()
    return citlivost, citlivost_err

