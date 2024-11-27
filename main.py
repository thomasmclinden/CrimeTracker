import matplotlib.pyplot as plt
import pandas as pd

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

# Function to sort neighborhoods by a specific crime rate
def sort_by_crime_rate(criterion):
    sorted_df = df.sort_values(by=criterion, ascending=True)
    print(f"\nNeighborhoods sorted by {criterion}:")
    print(sorted_df)

# Main menu and program loop
while True:
    print("\n--- Crime Data Options ---")
    print("1. View Crime Data for a ZIP code")
    print("2. View Crime Data Chart for a ZIP code")
    print("3. Sort neighborhoods by Violent Crime Rate")
    print("4. Sort neighborhoods by Property Crime Rate")
    print("5. Sort neighborhoods by Drug Crime Rate")
    print("0. Quit")

    choice = int(input("Enter your choice: "))

    if choice == 1:
        zip_code = int(input("Enter ZIP code: "))
        for neighborhood, zip_code_mapping in neighborhood_zip_mapping.items():
            if zip_code == zip_code_mapping:
                crime_rates = crime_data.get(neighborhood, None)
                if crime_rates:
                    print(f"\nCrime Data for {neighborhood} (ZIP: {zip_code}):")
                    print(f"Violent Crime Rate: {crime_rates[0]} per 1,000 residents")
                    print(f"Property Crime Rate: {crime_rates[1]} per 1,000 residents")
                    print(f"Drug Crime Rate: {crime_rates[2]} per 1,000 residents")
                break
        else:
            print("No neighborhood found for that ZIP code.")

    elif choice == 2:
        zip_code = int(input("Enter ZIP code to view chart: "))
        for neighborhood, zip_code_mapping in neighborhood_zip_mapping.items():
            if zip_code == zip_code_mapping:
                crime_rates = crime_data.get(neighborhood, None)
                if crime_rates:
                    plt.bar(['Violent Crime', 'Property Crime', 'Drug Crime'], crime_rates)
                    plt.title(f"Crime Rates for {neighborhood} (ZIP: {zip_code})")
                    plt.ylabel("Crimes per 1,000 residents")
                    plt.show()
                break
        else:
            print("No neighborhood found for that ZIP code.")
    elif choice == 3:
        sort_by_crime_rate('Violent Crime Rate')
    elif choice == 4:
        sort_by_crime_rate('Property Crime Rate')
    elif choice == 5:
        sort_by_crime_rate('Drug Crime Rate')
    elif choice == 0:
        print("Exiting the program.")
        break
    else:
        print("Invalid choice, please try again.")