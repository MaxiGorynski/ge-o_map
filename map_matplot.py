import rasterio
from rasterio.plot import show
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider

# Filepaths
tif_file = "GBOverview.tif"
gml_file = "/Users/supriyarai/Code/ge-o_map/bdline_gml3_gb/Data/INSPIRE_AdministrativeUnit.gml"

# Initialize zoom level
zoom_level = 1.0

def update_zoom(ax, zoom_factor):
    """Update the zoom level of the map."""
    global zoom_level
    zoom_level *= zoom_factor
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    ax.set_xlim([x / zoom_factor for x in xlim])
    ax.set_ylim([y / zoom_factor for y in ylim])
    zoom_slider.set_val(zoom_level * 100)  # Update slider value
    plt.draw()

def zoom_in(event):
    """Zoom in on the map."""
    update_zoom(ax, 1.2)

def zoom_out(event):
    """Zoom out of the map."""
    update_zoom(ax, 0.8)

# Open the .tif file
with rasterio.open(tif_file) as dataset:
    # Set up the figure and axes
    fig, ax = plt.subplots(figsize=(12, 10))
    plt.subplots_adjust(right=0.85)  # Leave space for buttons

    # Plot the raster map
    show(dataset, ax=ax, title="Great Britain Map with Constituency Boundaries (Zoomable)")

    # Load the GML file with Geopandas
    gml_data = gpd.read_file(gml_file)
    gml_data.plot(ax=ax, edgecolor='red', facecolor='none', linewidth=0.5)

    # Add zoom buttons
    ax_zoom_in = plt.axes([0.87, 0.5, 0.1, 0.05])  # x, y, width, height
    ax_zoom_out = plt.axes([0.87, 0.4, 0.1, 0.05])
    button_zoom_in = Button(ax_zoom_in, 'Zoom In')
    button_zoom_out = Button(ax_zoom_out, 'Zoom Out')
    button_zoom_in.on_clicked(zoom_in)
    button_zoom_out.on_clicked(zoom_out)

    # Add zoom level slider
    ax_zoom_slider = plt.axes([0.87, 0.3, 0.1, 0.03])
    zoom_slider = Slider(ax_zoom_slider, 'Zoom %', 10, 500, valinit=100, valstep=10)

    # Function to adjust zoom level from the slider
    def update_from_slider(val):
        global zoom_level
        new_zoom = val / 100  # Convert slider value back to zoom level
        if new_zoom != zoom_level:
            update_zoom(ax, new_zoom / zoom_level)

    zoom_slider.on_changed(update_from_slider)

    # Display the interactive plot
    plt.show()
