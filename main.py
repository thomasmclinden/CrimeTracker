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
    "Eastwick": 19153,
    "Elmwood": 19142,
    "Fairhill": 19133,
    "Fairmount-Spring Garden": 19130,
    "Fishtown": 19125,
    "Fox Chase": 19111,
    "Frankford": 19124,
    "Germantown": 19144,
    "Girard Estates": 19146,
    "Grays Ferry": 19146,
    "Haddington-Carroll Park": 19139,
    "Harrowgate": 19124,
    "Hartranft": 19133,
    "Holmesburry-Torresdale": 19136,
    "Hunting Park": 19140,
    "Juniata Park-Feltonville": 19135,
    "Kensington": 19134,
    "Logan-Fern Rock": 19141,
    "Manayunk": 19127,
    "Marconi Plaza-Packer Park": 19145,
    "Mayfield": 19152,
    "Morris Park": 19111,
    "Mount Airy": 19119,
    "North Central": 19121,
    "Oak Lane": 19126,
    "Olney": 19120,
    "Oxford Circle": 19149,
    "Pennsport-Whitman-Queen": 19148,
    "Point Breeze": 19145,
    "Poplar-Ludlow-Yorktowne": 19104,
    "Rhawnhurst": 19152,
    "Richmond": 19134,
    "Riverfront": 19123,
    "Roxborough": 19128,
    "Schuylkill Southwest": 19146,
    "Somerton": 19116,
    "South Philadelphia": 19147,
    "Strawberry Mansion": 19132,
    "Summerdale": 19124,
    "Tioga-Nicetown": 19140,
    "Torresdale": 19114,
    "Wharton-Hawthorne-Bella Vista": 19145,
    "Wissanoning": 19136,
    "Wynnefield": 19131
}

# Crime data for neighborhoods
# Source: https://data.philly.com/philly/crime/
crime_data = {
    "Alleghany West": (1.82, 4.52, 0.00),
    "Bella Vista/Southwark": (0.50, 2.48, 0.00),
    "Bridesburg": (0.32, 1.27, 0.00),
    "Brewerytown": (0.14, 3.20, 0.00),
    "Bustleton": (0.17, 2.33, 0.00),
    "Byberry": (0.05, 1.50, 0.00),
    "Cedar Brook": (0.21, 1.91, 0.06),
    "Chestnut Hill": (0.28, 3.88, 0.09),
    "City Center East": (1.23, 8.72, 0.05),
    "City Center West": (1.23, 7.88, 0.06),
    "Cobbs Creek": (0.93, 1.65, 0.00),
    "East Falls": (0.41, 3.45, 0.00),
    "Eastwick": (0.59, 2.56, 0.07),
    "Elmwood": (1.45, 2.60, 0.00),
    "Fairhill": (1.58, 1.88, 0.94),
    "Fairmount-Spring Garden": (0.54, 5.57, 0.04),
    "Fishtown": (0.36, 15.80, 0.09),
    "Fox Chase": (0.14, 2.24, 0.00),
    "Frankford": (1.03, 3.91, 0.22),
    "Germantown": (0.75, 4.81, 0.05),
    "Girard Estates": (0.12, 2.21, 0.00),
    "Grays Ferry": (0.61, 3.81, 0.00),
    "Haddington-Carroll Park": (0.70, 2.55, 0.00),
    "Harrowgate": (0.50, 3.00, 0.00),
    "Hartranft": (0.89, 2.50, 0.10),
    "Holmesburry-Torresdale": (0.46, 4.86, 0.07),
    "Hunting Park": (1.53, 2.99, 0.31),
    "Juniata Park-Feltonville": (1.00, 3.04, 0.08),
    "Kensington": (0.98, 2.65, 1.73),
    "Logan-Fern Rock": (0.77, 2.00, 0.15),
    "Manayunk": (0.25, 3.58, 0.00),
    "Marconi Plaza-Packer Park": (0.12, 2.12, 0.00),
    "Mayfield": (0.56, 4.92, 0.16),
    "Morris Park": (0.39, 2.12, 0.00),
    "Mount Airy": (0.14, 1.64, 0.00),
    "North Central": (1.00, 3.50, 0.20),
    "Oak Lane": (0.28, 2.09, 0.00),
    "Olney": (0.56, 2.11, 0.05),
    "Oxford Circle": (0.34, 3.15, 0.00),
    "Pennsport-Whitman-Queen": (0.22, 3.08, 0.00),
    "Point Breeze": (0.35, 3.43, 0.04),
    "Poplar-Ludlow-Yorktowne": (0.12, 2.29, 0.00),
    "Rhawnhurst": (0.29, 5.93, 0.03),
    "Richmond": (0.50, 3.60, 0.05),
    "Riverfront": (0.12, 1.50, 0.00),
    "Roxborough": (0.11, 3.82, 0.00),
    "Schuylkill Southwest": (0.08, 3.26, 0.00),
    "Somerton": (0.16, 2.73, 0.00),
    "South Philadelphia": (0.65, 1.98, 0.00),
    "Strawberry Mansion": (1.45, 5.50, 0.30),
    "Summerdale": (0.35, 3.20, 0.05),
    "Tioga-Nicetown": (1.75, 4.74, 0.06),
    "Torresdale": (0.04, 1.47, 0.00),
    "Wharton-Hawthorne-Bella Vista": (0.50, 3.22, 0.08),
    "Wissanoning": (0.60, 2.98, 0.03),
    "Wynnefield": (0.93, 3.14, 0.00)
}

# Convert crime data to a pandas DataFrame for easier manipulation
df = pd.DataFrame.from_dict(crime_data, orient='index',
                            columns=['Violent Crime Rate', 'Property Crime Rate', 'Drug Crime Rate'])
df.index.name = 'Neighborhood'

# Set pandas options to display the full DataFrame without truncating
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.width', None)  # Prevent wrapping of lines
pd.set_option('display.max_rows', None)  # Show all rows (if the data is small enough)

# Create sorted ZIP codes list for binary search
def create_sorted_zip_mapping():
    zip_to_neighborhood = {}
    for neighborhood, zip_code in neighborhood_zip_mapping.items():
        if zip_code not in zip_to_neighborhood:
            zip_to_neighborhood[zip_code] = []
        zip_to_neighborhood[zip_code].append(neighborhood)
    return (sorted(zip_to_neighborhood.keys()), zip_to_neighborhood)

# Binary search zips
def binary_search_zip(zip_codes, target):
    # Binary search implementation for ZIP codes
    left, right = 0, len(zip_codes) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if zip_codes[mid] == target:
            return mid
        elif zip_codes[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_welcome():
    print("=" * 40)
    print("     Philadelphia Crime Data Analyzer")
    print("  Analyze Crime Statistics Across Neighborhoods")

def display_menu():
    print("\nMenu Options:")
    print("1. View Crime Data for a ZIP code")
    print("2. View Crime Data Chart for a ZIP code")
    print("3. Sort neighborhoods by Violent Crime Rate")
    print("4. Sort neighborhoods by Property Crime Rate")
    print("5. Sort neighborhoods by Drug Crime Rate")
    print("6. View Interactive Crime Rate Map")
    print("0. Exit Program")
    print("=" * 40)

def display_crime_data(neighborhood, zip_code, crime_rates):
    print(f"\nCrime Data for {neighborhood} (ZIP: {zip_code})")
    print("-" * 40)
    print(f"Violent Crime Rate: {crime_rates[0]:.2f} per 1,000 residents")
    print(f"Property Crime Rate: {crime_rates[1]:.2f} per 1,000 residents")
    print(f"Drug Crime Rate: {crime_rates[2]:.2f} per 1,000 residents")
    print("-" * 40)

def merge_sort_neighborhoods(criterion):
    print(f"\nSorting neighborhoods by {criterion} using Merge Sort...")
    print("-" * 40)
    
    def merge(left, right):
        result = []
        left_idx, right_idx = 0, 0
        
        # Compare elements from both arrays and merge them in sorted order
        while left_idx < len(left) and right_idx < len(right):
            if left[left_idx][0] <= right[right_idx][0]:
                result.append(left[left_idx])
                left_idx += 1
            else:
                result.append(right[right_idx])
                right_idx += 1
        
        # Add remaining elements
        result.extend(left[left_idx:])
        result.extend(right[right_idx:])
        return result
    
    def merge_sort(arr):
        # Base case: arrays of length 0 or 1 are already sorted
        if len(arr) <= 1:
            return arr
            
        # Split array in half
        mid = len(arr) // 2
        left = merge_sort(arr[:mid])
        right = merge_sort(arr[mid:])
        
        # Merge the sorted halves
        return merge(left, right)
    
    # Prepare data for sorting
    data_to_sort = []
    for neighborhood, rates in crime_data.items():
        if criterion == 'Violent Crime Rate':
            rate = rates[0]
        elif criterion == 'Property Crime Rate':
            rate = rates[1]
        else:  # Drug Crime Rate
            rate = rates[2]
        data_to_sort.append((rate, neighborhood))
    
    # Sort and display results
    sorted_results = merge_sort(data_to_sort)
    
    print(f"\nNeighborhoods sorted by {criterion} (ascending order):")
    print("-" * 40)
    for rate, neighborhood in sorted_results:
        print(f"{neighborhood}: {rate:.2f}")
    return sorted_results

def display_zip_search_results(zip_code, neighborhood, crime_rates):
    # Display formatted search results
    print(f"\nFound data for ZIP code {zip_code}:")
    print("-" * 40)
    if isinstance(neighborhood, list):
        print(f"Neighborhoods in this ZIP code:")
        for n in neighborhood:
            print(f"\n{n}:")
            print(f"Violent Crime Rate: {crime_data[n][0]:.2f} per 1,000 residents")
            print(f"Property Crime Rate: {crime_data[n][1]:.2f} per 1,000 residents")
            print(f"Drug Crime Rate: {crime_data[n][2]:.2f} per 1,000 residents")
    else:
        print(f"Neighborhood: {neighborhood}")
        print(f"Violent Crime Rate: {crime_rates[0]:.2f} per 1,000 residents")
        print(f"Property Crime Rate: {crime_rates[1]:.2f} per 1,000 residents")
        print(f"Drug Crime Rate: {crime_rates[2]:.2f} per 1,000 residents")
    print("=" * 40)

def search_zip_code():
    # Handle ZIP code search with error checking
    try:
        zip_code = int(input("\nEnter ZIP code: "))
        print("\nSearching...")
        
        # Print available ZIP codes if search fails
        if zip_code not in neighborhood_zip_mapping.values():
            print("\nZIP code not found. Available ZIP codes are:")
            available_zips = sorted(set(neighborhood_zip_mapping.values()))
            for zip_code in available_zips:
                neighborhoods = [n for n, z in neighborhood_zip_mapping.items() if z == zip_code]
                print(f"ZIP {zip_code}: {', '.join(neighborhoods)}")
            return None
        
        # Find neighborhoods in this ZIP code
        neighborhoods = [n for n, z in neighborhood_zip_mapping.items() if z == zip_code]
        if neighborhoods:
            for neighborhood in neighborhoods:
                crime_rates = crime_data[neighborhood]
                display_zip_search_results(zip_code, neighborhood, crime_rates)
            return neighborhoods
        
        return None
            
    except ValueError:
        print("\nPlease enter a valid ZIP code")
        return None

def create_philly_crime_map():
    # Create an interactive map of Philadelphia crime rates
    print("\nGenerating interactive map...")
    
    # Initialize the map centered on Philadelphia
    philly_map = folium.Map(
        location=[39.9526, -75.1652],  # Philadelphia coordinates
        zoom_start=11,
        tiles='OpenStreetMap'
    )
    
    # Initialize geocoder
    geolocator = Nominatim(user_agent="crime_tracker")
    
    # Create feature groups for different crime types
    violent_crime_layer = folium.FeatureGroup(name='Violent Crime Rate')
    property_crime_layer = folium.FeatureGroup(name='Property Crime Rate')
    drug_crime_layer = folium.FeatureGroup(name='Drug Crime Rate')
    
    # Process each neighborhood
    for neighborhood, zip_code in neighborhood_zip_mapping.items():
        try:
            # Get coordinates for the ZIP code
            location = geolocator.geocode(f"{zip_code}, Philadelphia, PA")
            if location:
                # Get crime rates
                violent_rate, property_rate, drug_rate = crime_data[neighborhood]
                
                # Create popup content
                popup_content = f"""
                    <div style="font-family: Arial; width: 200px;">
                        <h4>{neighborhood}</h4>
                        <b>ZIP Code:</b> {zip_code}<br>
                        <b>Violent Crime Rate:</b> {violent_rate:.2f}<br>
                        <b>Property Crime Rate:</b> {property_rate:.2f}<br>
                        <b>Drug Crime Rate:</b> {drug_rate:.2f}<br>
                    </div>
                """
                
                # Add markers to different layers based on crime type
                # Violent Crime (red)
                violent_crime_layer.add_child(
                    folium.CircleMarker(
                        location=[location.latitude, location.longitude],
                        radius=violent_rate * 5,  # Size based on rate
                        popup=popup_content,
                        color='red',
                        fill=True,
                        fill_opacity=0.7
                    )
                )
                
                # Property Crime (blue)
                property_crime_layer.add_child(
                    folium.CircleMarker(
                        location=[location.latitude, location.longitude],
                        radius=property_rate * 2,  # Size based on rate
                        popup=popup_content,
                        color='blue',
                        fill=True,
                        fill_opacity=0.7
                    )
                )
                
                # Drug Crime (green)
                drug_crime_layer.add_child(
                    folium.CircleMarker(
                        location=[location.latitude, location.longitude],
                        radius=drug_rate * 10,  # Size based on rate
                        popup=popup_content,
                        color='green',
                        fill=True,
                        fill_opacity=0.7
                    )
                )
                
        except Exception as e:
            print(f"Error processing {neighborhood}: {str(e)}")
    
    # Add layers to map
    philly_map.add_child(violent_crime_layer)
    philly_map.add_child(property_crime_layer)
    philly_map.add_child(drug_crime_layer)
    
    # Add layer control
    folium.LayerControl().add_to(philly_map)
    
    # Add title
    title_html = '''
        <div style="position: fixed; 
                    top: 10px; left: 50px; width: 300px; height: 90px; 
                    z-index:9999; font-size:14px;
                    background-color: white;
                    border-radius: 10px;
                    padding: 10px;
                    box-shadow: 0 0 15px rgba(0,0,0,0.2);">
            <h4>Philadelphia Crime Rates by Neighborhood</h4>
            <p>Click layers to toggle different crime types.<br>
               Click markers for detailed information.</p>
        </div>
    '''
    philly_map.get_root().html.add_child(folium.Element(title_html))
    
    # Save and display the map
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.html')
    philly_map.save(temp_file.name)
    webbrowser.open('file://' + temp_file.name)
    
    return temp_file.name

def display_crime_map():
    # Handle the map visualization option
    try:
        print("\nCreating interactive map of Philadelphia crime rates...")
        map_file = create_philly_crime_map()
        
        print("\nMap has been opened in your web browser.")
        print("You can toggle different crime rates using the layer control.")
        print("Click on markers to see detailed information.")
        
        input("\nPress Enter to continue...")
        
        # Clean up the temporary file
        try:
            os.unlink(map_file)
        except:
            pass
            
    except Exception as e:
        print(f"\nError creating map: {str(e)}")
        input("\nPress Enter to continue...")

def main():
    try:
        while True:
            clear_screen()
            display_welcome()
            display_menu()
            
            try:
                choice = input("\nEnter your choice: ")
                choice = int(choice)
                
                if choice == 1:
                    search_result = search_zip_code()
                    if not search_result:
                        print("\nNo data found for that ZIP code.")
                    input("\nPress Enter to continue...")  # Wait for user input

                elif choice == 2:
                    try:
                        zip_code = int(input("\nEnter ZIP code to view chart: "))
                        print("\nSearching...")
                        
                        # Get sorted ZIP codes and mapping
                        sorted_zips, zip_to_neighborhood = create_sorted_zip_mapping()
                        
                        # Use binary search to find ZIP code
                        index = binary_search_zip(sorted_zips, zip_code)
                        
                        if index != -1:
                            # Find neighborhood(s) for this ZIP code
                            neighborhoods = [n for n, z in neighborhood_zip_mapping.items() if z == zip_code]
                            for neighborhood in neighborhoods:
                                crime_rates = crime_data.get(neighborhood, None)
                                if crime_rates:
                                    plt.figure(figsize=(10, 6))
                                    bars = plt.bar(['Violent Crime', 'Property Crime', 'Drug Crime'], 
                                                 crime_rates,
                                                 color=['#FF9999', '#66B2FF', '#99FF99'])
                                    
                                    # Add value labels on top of bars
                                    for bar in bars:
                                        height = bar.get_height()
                                        plt.text(bar.get_x() + bar.get_width()/2., height,
                                               f'{height:.2f}',
                                               ha='center', va='bottom')
                                    
                                    plt.title(f"Crime Rates for {neighborhood} (ZIP: {zip_code})")
                                    plt.ylabel("Crimes per 1,000 residents")
                                    plt.show()
                        else:
                            print("\nZIP code not found. Available ZIP codes are:")
                            available_zips = sorted(set(neighborhood_zip_mapping.values()))
                            for z in available_zips:
                                neighborhoods = [n for n, z in neighborhood_zip_mapping.items() if z == zip_code]
                                print(f"ZIP {z}: {', '.join(neighborhoods)}")
                            
                    except ValueError:
                        print("\nPlease enter a valid ZIP code")
                    input("\nPress Enter to continue...")  # Wait for user input

                elif choice in [3, 4, 5]:
                    criteria = {
                        3: 'Violent Crime Rate',
                        4: 'Property Crime Rate',
                        5: 'Drug Crime Rate'
                    }
                    merge_sort_neighborhoods(criteria[choice])
                    input("\nPress Enter to continue...")  # Wait for user input

                elif choice == 6:
                    display_crime_map()
                    input("\nPress Enter to continue...")  # Wait for user input

                elif choice == 0:
                    print("\nThank you for using the Crime Data Analyzer!")
                    break

                else:
                    print("\nInvalid choice. Please try again.")
                    input("\nPress Enter to continue...")  # Wait for user input

            except ValueError:
                print("\nPlease enter a valid number.")
                input("\nPress Enter to continue...")  # Wait for user input

    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        input("\nPress Enter to continue...")  # Wait for user input


if __name__ == "__main__":
    main()