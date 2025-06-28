import folium
import pygeohash as pgh
import webbrowser
import os


def geohash_bounds(geohash):
    """
    Calculate the bounding box (south, west, north, east) for a given geohash.
    """
    lat, lon, lat_err, lon_err = pgh.decode_exactly(geohash)
    south = lat - lat_err
    north = lat + lat_err
    west = lon - lon_err
    east = lon + lon_err
    return (south, west, north, east)


# List of geohashes
geohashes = ["dpm9m", "dpm9q", "dpm9r", "dpm9t", "dpm9v", "dpm9w", "dpm9x", "dpm9y", "dpm9z"]

# Decode geohashes into (latitude, longitude) pairs
locations = [pgh.decode(geohash) for geohash in geohashes]

# Calculate the center of the map based on the average of geohash locations
avg_lat = sum(lat for lat, lon in locations) / len(locations)
avg_lon = sum(lon for lat, lon in locations) / len(locations)

# Create the folium map centered at the average location
m = folium.Map(location=[avg_lat, avg_lon], zoom_start=11)


# Add each geohash as a colored rectangle, marker, and label
for geohash in geohashes:
    lat, lon = pgh.decode(geohash)             # Get center point of geohash
    south, west, north, east = geohash_bounds(geohash)  # Get bounding box

    # Draw the rectangle representing the geohash boundary
    folium.Rectangle(
        bounds=[(south, west), (north, east)],
        color="red",
        fill=True,
        fill_opacity=0.3,
        popup=f"Geohash: {geohash}"
    ).add_to(m)

    # Add a circle marker at the center of the geohash
    folium.CircleMarker(
        location=[lat, lon],
        radius=5,
        color='blue',
        fill=True,
        fill_opacity=0.7
    ).add_to(m)

    # Add geohash label as text on the map
    folium.map.Marker(
        [lat, lon],
        icon=folium.DivIcon(
            icon_size=(170, 36),
            icon_anchor=(20, -10),
            html=f'<div style="font-size: 10pt; color: black;">{geohash}</div>',
        )
    ).add_to(m)


# Save the map to an HTML file
map_file = "geohashes_map.html"
m.save(map_file)

# Open the map automatically in the default web browser
webbrowser.open('file://' + os.path.realpath(map_file))

