import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import PolygonSelector
from matplotlib.path import Path
from scipy.signal import fftconvolve
import locale


def tew_correction(pw_okno, lsc_okno, usc_okno):
    scatter_estimate = (usc_okno/0.06 + lsc_okno/0.06) * (0.2/2)
    return pw_okno - scatter_estimate

def align_images(reference_image, moving_image):
    """
    Align two images using convolution and FFT.

    Parameters
    ----------
    reference_image : numpy.ndarray
        Reference image
    moving_image : numpy.ndarray
        Image to be aligned

    Returns
    -------
    aligned_moving_image : numpy.ndarray
        Aligned image
    """
    # Perform convolution using fftconvolve
    convolution_result = fftconvolve(reference_image, moving_image[::-1, ::-1], mode='same')

    # Find the location of the maximum value in the convolution result
    y_max, x_max = np.unravel_index(np.argmax(convolution_result), convolution_result.shape)

    # Calculate the shift in x and y directions
    shift_y = y_max - reference_image.shape[0] // 2
    shift_x = x_max - reference_image.shape[1] // 2

    # Shift the moving image to align with the reference image
    aligned_moving_image = np.roll(moving_image, shift=(shift_y, shift_x), axis=(0, 1))

    return aligned_moving_image

class ROI_drawer_manual:
    def __init__(self, image):
        self.image = image
        
        # Create figure and axes
        self.fig, self.ax = plt.subplots(figsize=(13, 13))
        self.ax.imshow(self.image, cmap='gray')
        
        # Initialize ROI points, mask, and PolygonSelector
        self.roi_points = []
        self.mask = None
        self.selector = PolygonSelector(self.ax, self.on_select, useblit=True)
        
        # Set the color to a brighter red and linewidth for each artist
        bright_blue = (0.0, 0.5, 1.0)  # RGB values for a bright blue color
        for artist in self.selector.artists:
            artist.set_color(bright_blue)
            artist.set_linewidth(2)
        
        # Connect the event for showing pixel values
        self.fig.canvas.mpl_connect('motion_notify_event', self.show_pixel_value)
        
        # Create a text box for displaying pixel values
        self.text = self.ax.text(0.05, 0.95, '', transform=self.ax.transAxes, color='yellow', fontsize=12,
                                 bbox=dict(facecolor='black', alpha=0.5))

        # Store the contour object for the ROI
        self.contour = None

    def show(self):
        # Display the figure and allow for manual ROI selection
        plt.show()

    def on_select(self, verts):
        # Store the vertices of the manually drawn polygon
        self.roi_points = verts
        self.create_mask()
        self.display_results()

    def create_mask(self):
        # Create a mask for the polygon
        poly_path = Path(self.roi_points)
        y, x = np.mgrid[:self.image.shape[0], :self.image.shape[1]]
        points = np.vstack((x.ravel(), y.ravel())).T
        self.mask = poly_path.contains_points(points).reshape(self.image.shape)
        

    def display_results(self):
        # Clear previous contour if it exists
        if self.contour is not None:
            for coll in self.contour.collections:
                coll.remove()

        # Display the results of the manually drawn ROI
        self.ax.imshow(self.image, cmap='gray')
        if self.mask is not None:
            # Draw the new contour and update the contour attribute
            self.contour = self.ax.contour(self.mask, colors='r', linewidths=2)
        plt.draw()

    def show_pixel_value(self, event):
        # Show the pixel value under the cursor
        if event.inaxes == self.ax:
            x, y = int(event.xdata), int(event.ydata)
            if 0 <= x < self.image.shape[1] and 0 <= y < self.image.shape[0]:
                pixel_value = self.image[y, x]
                self.text.set_text(f'Pixel Value: {pixel_value:.2f}')
                plt.draw()


class Graf_1:
    def __init__(self, fontsize, title, xlabel, ylabel, figsize, legend_fontsize=None) -> None:
        # Set locale for numeric formatting to Czech (if locale is installed)
        try:
            locale.setlocale(locale.LC_NUMERIC, "cs_CZ.UTF-8")
        except locale.Error:
            print("Czech locale 'cs_CZ.UTF-8' not available. Using default locale.")

        plt.rcdefaults()
        plt.rcParams['axes.formatter.use_locale'] = True
        plt.rcParams['font.size'] = fontsize
        plt.rcParams['xtick.labelsize'] = fontsize
        plt.rcParams['ytick.labelsize'] = fontsize

        # Create figure and axis
        self.Figure, self.fig = plt.subplots(figsize=figsize, dpi=250)
        self.title = title
        self.ylabel = ylabel
        self.xlabel = xlabel
        self.legend_fontsize = legend_fontsize if legend_fontsize is not None else fontsize - 4

        self.fig.set_xlabel(self.xlabel)
        self.fig.set_ylabel(self.ylabel)
        self.fig.set_title(self.title)
        self.fig.grid(color='black', ls='-.', lw=0.25)

        # Custom formatter for x and y axes
        #self.fig.xaxis.set_major_formatter(FuncFormatter(self.czech_formatter))
        #self.fig.yaxis.set_major_formatter(FuncFormatter(self.czech_formatter))

    # Formatter function to convert numbers to Czech format
    #@staticmethod
    def czech_formatter(x, pos):
        return f"{x:,.1f}".replace(",", "\u2009").replace(".", ",")

    def plot(self, x, y, marker, label_data, color, markeredgewidth, markersize):
        self.fig.plot(x, y, marker, label=label_data, color=color, markeredgewidth=markeredgewidth, markersize=markersize)
        self.fig.legend(loc='best', edgecolor='black', fontsize=self.legend_fontsize)

    def errorbar(self, x, y, yerr, marker, label_data, color, markersize, sirka_nejistot, sirka_primky_nejistot):
        self.fig.errorbar(
            x=x, y=y, yerr=yerr, fmt=' ', marker=marker, markersize=markersize,
            ecolor='black', zorder=2, elinewidth=sirka_primky_nejistot, label=label_data,
            capsize=sirka_nejistot, color=color
        )
        self.fig.legend(loc='best', edgecolor='black', fontsize=self.legend_fontsize)

class Graf_1_2:
    def __init__(self, fontsize, suptitle, title_1, xlabel_1, ylabel_1, title_2, xlabel_2, ylabel_2, figsize) -> None:
        # Set locale for numeric formatting to Czech (if locale is installed)
        try:
            locale.setlocale(locale.LC_NUMERIC, "cs_CZ.UTF-8")
        except locale.Error:
            print("Czech locale 'cs_CZ.UTF-8' not available. Using default locale.")

        plt.rcdefaults()
        plt.rcParams['axes.formatter.use_locale'] = True
        plt.rcParams['font.size'] = fontsize
        plt.rcParams['xtick.labelsize'] = fontsize
        plt.rcParams['ytick.labelsize'] = fontsize

        self.Figure, self.fig = plt.subplots(1, 2, figsize=figsize, dpi=250)
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
        self.fig[0].grid(color='black', ls='-.', lw=0.35)

        self.fig[1].set_xlabel(self.xlabel_2)
        self.fig[1].set_ylabel(self.ylabel_2)
        self.fig[1].set_title(self.title_2, fontweight="bold")
        self.fig[1].grid(color='black', ls='-.', lw=0.35)

    def plot(self, x, y, i, marker, label_data, color, markeredgewidth, markersize):
        # Ensure x and y are passed as positional arguments
        self.fig[i].plot(x, y, marker=marker, label=label_data, color=color, markeredgewidth=markeredgewidth, markersize=markersize)
        self.fig[i].legend(loc='best', edgecolor='black', fontsize=11)
    
    def errorbar(self, x, y, i, yerr, marker, label_data, color, ecolor, markersize, sirka_nejistot, sirka_primky_nejistot):
        self.fig[i].errorbar(x, y, yerr=yerr, fmt=' ', marker=marker, markersize=markersize, ecolor=ecolor, zorder=2, elinewidth=sirka_primky_nejistot, label=label_data, capsize=sirka_nejistot, color=color)
        self.fig[i].legend(loc='best', edgecolor='black', fontsize=11)
