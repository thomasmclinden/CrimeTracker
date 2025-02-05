# Crime Analysis & Visualization in Philadelphia

## Overview

This Python project utilizes several libraries to analyze and visualize crime data in Philadelphia. It includes functionality for plotting crime data on maps, visualizing crime statistics, and generating reports.

### Libraries Used:

- **Matplotlib**: For plotting graphs.
- **Pandas**: For data manipulation and analysis.
- **Folium**: For mapping and visualization.
- **Geopy**: For geolocation services.
- **Heapq**: For efficient priority queue operations.

---

## Features

### 1. Crime Data Visualization on Maps
This tool allows users to visualize crime data on an interactive map of Philadelphia using Folium. The map displays markers for specific crimes that have been reported, and it can be zoomed and panned to explore different areas.

### 2. Crime Frequency Analysis
Crime data is processed and visualized using bar charts, pie charts, and time-series graphs. This helps to easily understand crime frequency trends, such as:
- Crime types over time.
- Crime types by neighborhood.

### 3. Neighborhood Analysis
The program allows you to explore the crime rate in specific Philadelphia neighborhoods. Users can:
- Query data by ZIP code.
- Analyze crime data for specific neighborhoods.
- Generate statistics for individual neighborhoods and identify patterns in criminal activity.

---

## Code Walkthrough

### Main Sections of the Code

1. **Libraries and Setup**:
   - The code uses `matplotlib`, `folium`, `geopy`, and other necessary libraries to handle crime data and generate visualizations.
   - A geolocation function uses `geopy` to transform neighborhood names into geographical coordinates.

2. **Crime Data Visualization**:
   - Crime data is represented on maps using Folium, placing markers for each crime in a neighborhood.
   - Different visualizations, such as heat maps, are generated using `folium.plugins`.

3. **Data Processing**:
   - The crime data is processed and visualized using pandas and matplotlib.
   - Crime frequency over time is plotted, along with a breakdown of types of crime and their frequency across neighborhoods.

---

## Example Code

```python
import matplotlib.pyplot as plt
from heapq import heappush, heappop
import pandas as pd
import time
import os
import folium
from folium import plugins
from geopy.geocoders import Nominatim
import webbrowser
import tempfile

# Given mapping of neighborhoods to ZIP codes and crime data
neighborhood_zip_mapping = {
    "Alleghany West": 19140,
    "Bella Vista/Southwark": 19147,
    "Bridesburg": 19137,
    "Brewerytown": 19121,
    "Bustleton": 19115,
    "Byberry": 19116,
    "Cedar Brook": 19150,
    "Chestnut Hill": 19118,
    "City Center East": 19102,
    "City Center West": 19107,
    "Cobbs Creek": 19143,
    "East Falls": 19129,
    "Fishtown": 19125,
    "Germantown": 19144,
    "Harrowgate": 19124,
    "Logan": 19141,
    "Manayunk": 19127,
    "Olney": 19120,
    "Overbrook": 19151,
    "Powelton": 19104,
    "Roxborough": 19128,
    "South Philadelphia": 19148,
    "Southwest Philadelphia": 19142,
    "Spring Garden": 19130,
    "West Philadelphia": 19139,
    "West Oak Lane": 19126
}

# Initialize geolocator
geolocator = Nominatim(user_agent="crime_analysis")

def get_coordinates(address):
    location = geolocator.geocode(address)
    if location:
        return (location.latitude, location.longitude)
    return None

def create_crime_map(neighborhood, crimes):
    m = folium.Map(location=get_coordinates(neighborhood), zoom_start=12)
    
    for crime in crimes:
        lat, lon = get_coordinates(crime['location'])
        folium.Marker([lat, lon], popup=crime['type']).add_to(m)

    # Saving the map to an HTML file
    map_file = tempfile.NamedTemporaryFile(delete=False, suffix='.html')
    m.save(map_file.name)
    map_file.close()

    # Opening the map in the browser
    webbrowser.open(map_file.name)

def plot_crime_statistics(crime_data):
    # Crime counts by type
    crime_types = [crime['type'] for crime in crime_data]
    crime_counts = pd.Series(crime_types).value_counts()

    # Bar chart of crime counts
    crime_counts.plot(kind='bar', figsize=(10, 6))
    plt.title('Crime Counts by Type')
    plt.xlabel('Crime Type')
    plt.ylabel('Count')
    plt.show()

def plot_crime_by_neighborhood(crime_data, neighborhood_zip_mapping):
    # Crime counts by neighborhood
    neighborhood_crimes = {neighborhood: 0 for neighborhood in neighborhood_zip_mapping}
    for crime in crime_data:
        neighborhood = crime['neighborhood']
        if neighborhood in neighborhood_crimes:
            neighborhood_crimes[neighborhood] += 1

    # Bar chart of crime counts by neighborhood
    pd.Series(neighborhood_crimes).plot(kind='bar', figsize=(10, 6))
    plt.title('Crime Counts by Neighborhood')
    plt.xlabel('Neighborhood')
    plt.ylabel('Crime Count')
    plt.show()

# Sample crime data
crime_data = [
    {'type': 'Robbery', 'neighborhood': 'City Center East', 'location': 'Philadelphia, PA'},
    {'type': 'Burglary', 'neighborhood': 'West Philadelphia', 'location': 'Philadelphia, PA'},
    {'type': 'Assault', 'neighborhood': 'South Philadelphia', 'location': 'Philadelphia, PA'}
]

# Generate map for a neighborhood
create_crime_map('City Center East', crime_data)

# Generate crime statistics
plot_crime_statistics(crime_data)

# Generate neighborhood analysis
plot_crime_by_neighborhood(crime_data, neighborhood_zip_mapping)
```
## Installation

1. Install the required libraries using pip:

    ```bash
    pip install matplotlib pandas folium geopy
    ```

2. Clone or download the repository, then run the Python script for analysis.

---

## Usage

1. **Crime Map**:  
    - Enter the name of the neighborhood for which you want to visualize the crime data on the map.
    - The map will be generated and opened in your default browser.

2. **Crime Statistics**:  
    - The program will generate various crime statistics like crime counts by type and neighborhood.
    - Visualizations like bar charts will be displayed using Matplotlib.

---

## Future Enhancements

- Integrate real-time crime data using APIs.
- Provide detailed filtering options by date, crime type, and neighborhood.
- Enhance map with heatmaps showing crime intensity in different areas.

---

## License

This project is licensed under the MIT License.
