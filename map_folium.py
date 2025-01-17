import folium
import geopandas as gpd
import rasterio
import numpy as np
from rasterio.enums import Resampling
from rasterio.warp import transform_bounds
import matplotlib.pyplot as plt

# Filepaths
tif_file = "/Users/supriyarai/Code/ge-o_map/Over_gb/GBOverview.tif"
gml_file = "/Users/supriyarai/Code/ge-o_map/bdline_gml3_gb/Data/INSPIRE_AdministrativeUnit.gml"


# Function to downsample raster data
def downsample_raster(src, scale_factor=4):
    """Downsample the raster by a scale factor."""
    data = src.read(
        out_shape=(
            src.count,
            int(src.height / scale_factor),
            int(src.width / scale_factor)
        ),
        resampling=Resampling.average
    )
    transform = src.transform * src.transform.scale(
        (src.width / data.shape[-1]),
        (src.height / data.shape[-2])
    )
    return data, transform


# Function to add raster to Folium map as an image overlay
def add_raster_to_map(m, tif_file, scale_factor=4):
    """Adds a downsampled raster file as an image overlay on a Folium map."""
    with rasterio.open(tif_file) as src:
        # Downsample the raster
        data, transform = downsample_raster(src, scale_factor=scale_factor)

        # Normalize raster data for visualization
        image = data[0]  # Use the first band
        image = np.interp(image, (image.min(), image.max()), (0, 255)).astype(np.uint8)

        # Save the normalized image as a PNG
        plt.imsave("temp_overlay.png", image, cmap="gray")

        # Get raster bounds and transform them to WGS84
        bounds = transform_bounds(src.crs, "EPSG:4326", *src.bounds)

        # Add the image overlay to the Folium map
        folium.raster_layers.ImageOverlay(
            image="temp_overlay.png",
            bounds=[[bounds[1], bounds[0]], [bounds[3], bounds[2]]],  # South-West, North-East
            opacity=0.6,
            interactive=True,
            name="Raster Overlay"
        ).add_to(m)


# Function to add GML data to Folium map
def add_gml_to_map(m, gml_file, simplify_tolerance=0.01):
    """Adds vector data from a GML file to a Folium map with simplification."""
    gml_data = gpd.read_file(gml_file)

    # Simplify the geometries for better performance
    gml_data["geometry"] = gml_data["geometry"].simplify(simplify_tolerance)

    # Add GML data as a GeoJSON layer
    folium.GeoJson(
        gml_data,
        name="Constituency Boundaries",
        style_function=lambda x: {
            "color": "red",
            "weight": 1,
            "fillOpacity": 0
        }
    ).add_to(m)


# Create a Folium map centered around Great Britain
m = folium.Map(location=[55.3781, -3.4360], zoom_start=6, tiles="OpenStreetMap")

# Add raster and GML data to the map
add_raster_to_map(m, tif_file, scale_factor=4)  # Downsample by a factor of 4
add_gml_to_map(m, gml_file, simplify_tolerance=0.01)  # Simplify geometries

# Add layer control for toggling overlays
folium.LayerControl().add_to(m)

# Save the map to an HTML file
output_map = "great_britain_map.html"
m.save(output_map)

print(f"Map has been saved to {output_map}. Open it in your browser to view the interactive map.")
