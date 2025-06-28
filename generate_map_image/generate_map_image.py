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
geohashes = [
    "dpm9m", "dpm9q", "dpm9r", "dpm9t", "dpm9v", "dpm9w", "dpm9x", "dpm9y", "dpm9z",
    "dpmc2", "dpmc3", "dpmc6", "dpmc7", "dpmc8", "dpmc9", "dpmcb", "dpmcc", "dpmcd",
    "dpmce", "dpmcf", "dpmcg", "dpmck", "dpmcm", "dpmcq", "dpmcr", "dpmcs", "dpmct",
    "dpmcu", "dpmcv", "dpmcw", "dpmcx", "dpmcy", "dpmcz", "dpmdj", "dpmdm", "dpmdn",
    "dpmdp", "dpmdq", "dpmdr", "dpmdt", "dpmdv", "dpmdw", "dpmdx", "dpmdy", "dpmdz",
    "dpmej", "dpmem", "dpmen", "dpmep", "dpmeq", "dpmer", "dpmet", "dpmev", "dpmew",
    "dpmex", "dpmey", "dpmez", "dpmf0", "dpmf1", "dpmf2", "dpmf3", "dpmf4", "dpmf5",
    "dpmf6", "dpmf7", "dpmf8", "dpmf9", "dpmfb", "dpmfc", "dpmfd", "dpmfe", "dpmff",
    "dpmfg", "dpmfh", "dpmfj", "dpmfk", "dpmfm", "dpmfn", "dpmfp", "dpmfq", "dpmfr",
    "dpmfs", "dpmft", "dpmfu", "dpmfv", "dpmfw", "dpmfx", "dpmfy", "dpmfz", "dpmg0",
    "dpmg1", "dpmg2", "dpmg3", "dpmg4", "dpmg5", "dpmg6", "dpmg7", "dpmg8", "dpmg9",
    "dpmgb", "dpmgc", "dpmgd", "dpmge", "dpmgf", "dpmgg", "dpmgh", "dpmgj", "dpmgk",
    "dpmgm", "dpmgn", "dpmgp", "dpmgq", "dpmgr", "dpmgs", "dpmgt", "dpmgu", "dpmgv",
    "dpmgw", "dpmgx", "dpmgy", "dpmgz", "dpmsj", "dpmsm", "dpmsn", "dpmsp", "dpmsq",
    "dpmsr", "dpmst", "dpmsv", "dpmsw", "dpmsx", "dpmsy", "dpmsz", "dpmtj", "dpmtm",
    "dpmtn", "dpmtp", "dpmtq", "dpmtr", "dpmtt", "dpmtw", "dpmtx", "dpmu0", "dpmu1",
    "dpmu2", "dpmu3", "dpmu4", "dpmu5", "dpmu6", "dpmu7", "dpmu8", "dpmu9", "dpmub",
    "dpmuc", "dpmud", "dpmue", "dpmuf", "dpmug", "dpmuh", "dpmuj", "dpmuk", "dpmum",
    "dpmun", "dpmup", "dpmuq", "dpmur", "dpmus", "dpmut", "dpmuu", "dpmuv", "dpmuw",
    "dpmux", "dpmuy", "dpmuz", "dpmv0", "dpmv1", "dpmv2", "dpmv3", "dpmv4", "dpmv5",
    "dpmv6", "dpmv7", "dpmv8", "dpmv9", "dpmvd", "dpmve", "dpmvh", "dpmvj", "dpmvk",
    "dpmvm", "dpmvn", "dpmvp", "dpmvq", "dpmvr", "dpmvs", "dpmvt", "dpmvw", "dpmvx",
    "dpq12", "dpq13", "dpq16", "dpq17", "dpq18", "dpq19", "dpq1b", "dpq1c", "dpq1d",
    "dpq1e", "dpq1f", "dpq1g", "dpq1k", "dpq1m", "dpq1q", "dpq1r", "dpq1s", "dpq1t",
    "dpq1u", "dpq1v", "dpq1w", "dpq1x", "dpq1y", "dpq1z", "dpq40", "dpq41", "dpq42",
    "dpq43", "dpq44", "dpq45", "dpq46", "dpq47", "dpq48", "dpq49", "dpq4b", "dpq4c",
    "dpq4d", "dpq4e", "dpq4f", "dpq4g", "dpq4h", "dpq4j", "dpq4k", "dpq4m", "dpq4n",
    "dpq4p", "dpq4q", "dpq4r", "dpq4s", "dpq4t", "dpq4u", "dpq4v", "dpq4w", "dpq4x",
    "dpq4y", "dpq4z", "dpq50", "dpq51", "dpq52", "dpq53", "dpq54", "dpq55", "dpq56",
    "dpq57", "dpq58", "dpq59", "dpq5b", "dpq5c", "dpq5d", "dpq5e", "dpq5f", "dpq5g",
    "dpq5h", "dpq5j", "dpq5k", "dpq5m", "dpq5n", "dpq5p", "dpq5q", "dpq5r", "dpq5s",
    "dpq5t", "dpq5u", "dpq5v", "dpq5w", "dpq5x", "dpq5y", "dpq5z", "dpqh0", "dpqh1",
    "dpqh2", "dpqh3", "dpqh4", "dpqh5", "dpqh6", "dpqh7", "dpqh8", "dpqh9", "dpqhb",
    "dpqhc", "dpqhd", "dpqhe", "dpqhf", "dpqhg", "dpqhh", "dpqhj", "dpqhk", "dpqhm",
    "dpqhn", "dpqhp", "dpqhq", "dpqhr", "dpqhs", "dpqht", "dpqhu", "dpqhv", "dpqhw",
    "dpqhx", "dpqhy", "dpqhz", "dpqj0", "dpqj1", "dpqj2", "dpqj3", "dpqj4", "dpqj5",
    "dpqj6", "dpqj7", "dpqj8", "dpqj9", "dpqjd", "dpqje", "dpqjh", "dpqjj", "dpqjk",
    "dpqjm", "dpqjn", "dpqjp", "dpqjq", "dpqjr", "dpqjs", "dpqjt", "dpqjw", "dpqjx"
]

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
        color="green",
        fill=True,
        fill_opacity=0.3,
        popup=f"Geohash: {geohash}"
    ).add_to(m)

    # Add a circle marker at the center of the geohash
    folium.CircleMarker(
        location=[lat, lon],
        radius=1,
        color='black',
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

