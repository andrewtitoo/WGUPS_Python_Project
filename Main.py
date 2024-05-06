# Name: Andrew Titoian
# Class: Data Structures and Algorithms II - C950
# Student ID: 011646949
import os
import datetime
from Packages import load_package_data
from Truck import Truck
from Truck import load_address_and_distance_data
from HashTable import HashTableWChains

# Function to display the status of all packages at specific times
def display_package_status_at_times(trucks, times):
    for time_str in times:
        query_time = datetime.datetime.combine(datetime.date.today(), datetime.datetime.strptime(time_str, "%H:%M").time())
        print(f"\nStatus of all packages at {time_str}:")
        for truck in trucks:
            print(f"\nTruck {truck.truck_id}:")
            for package_id in truck.packages:
                package = truck.package_data.search(package_id)
                if package:
                    status, address = package.get_status_at_time(query_time)
                    time_info = f"at {package.delivery_time.strftime('%H:%M')}" if package.delivery_time else "N/A"
                    print(f"Package {package_id}: {status} at {address} {time_info}")

# Main function to initialize data and provide user interface for tracking
def main():
    # Initialize the hash table to store package data
    package_data = HashTableWChains()
    # Load package data from a CSV file into the hash table
    load_package_data('Data/packageCSV (2).csv', package_data)
    # Manually set the update details for package #9
    package_9 = package_data.search(9)
    if package_9:
        package_9.address_update_time = datetime.datetime.combine(datetime.date.today(), datetime.time(10, 20))
        package_9.new_address = "410 S State St"

    # Paths to address and distance data CSV files
    address_file = 'Data/addresses (1).csv'
    distance_file = 'Data/distanceCSV (2).csv'

    # Check if both CSV files exist before attempting to load data
    if os.path.exists(address_file) and os.path.exists(distance_file):
        address_data, distance_data = load_address_and_distance_data(address_file, distance_file)
        print("Addresses loaded from CSV files:")
        print(address_data)
        print("\nDistances loaded from CSV files:")
        print(distance_data)
    else:
        print("Error: One or both of the CSV files are missing.")
        return

    # Initialize trucks with specified start times and assigned packages
    start_time = datetime.datetime.combine(datetime.date.today(), datetime.time(8, 0))
    truck1 = Truck(18, 0, "4001 South 700 East", start_time, [1, 13, 14, 15, 16, 19, 20, 26, 30, 31, 34, 35, 37, 40],
                   package_data, 1)
    truck2 = Truck(18, 0, "4001 South 700 East", start_time, [2, 3, 4, 5, 12, 18, 22, 24, 27, 29, 33, 36, 38],
                   package_data, 2)
    truck3_start_time = start_time + datetime.timedelta(minutes=65)  # Truck 3 departs at 9:05 AM
    truck3 = Truck(18, 0, "4001 South 700 East", truck3_start_time, [6, 7, 8, 9, 10, 11, 17, 21, 23, 25, 28, 32, 39],
                   package_data, 3)

    # Create a list of trucks
    trucks = [truck1, truck2, truck3]

    # Deliver packages
    for truck in trucks:
        truck.deliver_packages()

    # User interface for tracking packages and viewing mileage
    time_ranges = {
        "1": ["8:35", "9:25"],
        "2": ["9:35", "10:25"],
        "3": ["12:03", "13:12"]
    }

    while True:
        print("\n----- Package Tracking System -----")
        print("1. Check the status of a package")
        print("2. View the total mileage of the trucks")
        print("3. View package status for specific time ranges")
        print("4. Check the status of a package at a specific time")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            package_id = int(input("Please enter package ID: "))
            package = package_data.search(package_id)
            if package:
                print("\nPackage information:")
                print(package)
            else:
                print("\nPackage ID not found.")
        elif choice == '2':
            total_mileage = 0
            print("\nMileage Information:")
            for truck in trucks:
                print(f"Truck {truck.truck_id} traveled {truck.miles} miles.")
                total_mileage += truck.miles
            print(f"The total mileage traveled by all trucks is {total_mileage} miles.")
        elif choice == '3':
            for key, times in time_ranges.items():
                display_package_status_at_times(trucks, times)
        elif choice == '4':
            package_id = int(input("Please enter package ID: "))
            time_input = input("Enter the time (HH:MM format): ")
            try:
                query_time = datetime.datetime.combine(datetime.date.today(),
                                                       datetime.datetime.strptime(time_input, "%H:%M").time())
                package = package_data.search(package_id)
                if package:
                    status, address = package.get_status_at_time(query_time)
                    print(f"\nStatus of Package {package_id} at {time_input}: {status}")
                    print(f"Delivery address: {address}")  # Display the potentially updated address
                    print(f"Delivery deadline: {package.deadline}")
                    print(f"City: {package.city}")
                    print(f"Zip code: {package.zip_code}")
                    print(f"Weight: {package.weight}")
                    print(f"Notes: {package.notes}")
                else:
                    print("\nPackage ID not found.")
            except ValueError:
                print("Invalid time format. Please enter the time in HH:MM format.")
        elif choice == '5':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, or 5.")

if __name__ == "__main__":
    main()