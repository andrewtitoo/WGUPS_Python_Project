import datetime
import csv

def load_address_and_distance_data(address_file, distance_file):
    """ Load address and distance data from CSV files, returning dictionaries with the parsed data. """
    global AddressCSV, DistanceCSV
    address_data = {}
    distance_data = {}
    try:
        # Open and read address file.
        with open(address_file) as addr_file:
            address_reader = csv.reader(addr_file)
            AddressCSV = list(address_reader)
            for row in AddressCSV:
                address_data[row[2]] = int(row[0])

        # Open and read distance file.
        with open(distance_file) as dist_file:
            distance_reader = csv.reader(dist_file)
            DistanceCSV = list(distance_reader)
            for row in DistanceCSV:
                distances = {addr: float(dist) if dist else 0.0 for addr, dist in zip(address_data.keys(), row[1:])}
                distance_data[row[0]] = distances

        # Add base location distance mapping if missing.
        if '4001 South 700 East' not in distance_data:
            distance_data['4001 South 700 East'] = {addr: 0.0 for addr in address_data.keys()}

    except Exception as e:
        print("Error:", e)
        import traceback
        traceback.print_exc()

    return address_data, distance_data
class Truck:
    """ Represents a truck responsible for delivering packages. """
    def __init__(self, speed, miles, current_location, depart_time, package_ids, package_data, truck_id):
        self.speed = speed
        self.miles = miles
        self.current_location = current_location
        self.time = depart_time  # this should be datetime.datetime now
        self.depart_time = depart_time
        self.packages = package_ids  # List of package IDs the truck is responsible for
        self.package_data = package_data
        self.truck_id = truck_id  # Identifier for the truck

    def __str__(self):
        return f"Truck {self.truck_id}: Speed: {self.speed}, Miles: {self.miles}, Current Location: {self.current_location}, Time: {self.time}, Departure Time: {self.depart_time}, Package IDs: {self.packages}"

    def address(self, address_name):
        """ Returns the ID associated with the given address, with added debugging. """
        for row in AddressCSV:
            if address_name == row[2]:  # Ensure exact match
                return int(row[0])
        print(f"Address not found: {address_name}")  # Debugging line
        return None

    def betweenst(self, address1, address2):
        """ Calculates the distance between two addresses. """
        distance = DistanceCSV[address1][address2]
        if distance == '':
            distance = DistanceCSV[address2][address1]
        return float(distance)

    def deliver_packages(self):
        """ Simulates the process of delivering packages with error handling. """
        print(f"Routes for Truck {self.truck_id}:")
        enroute = [self.package_data.search(package_id) for package_id in self.packages]
        for package in enroute:
            package.update_status('En route', self.time)
        while enroute:
            nextAddress = float('inf')
            nextPackage = None
            for package in enroute:
                address1_index = self.address(self.current_location)
                address2_index = self.address(package.street)
                if address1_index is None or address2_index is None:
                    print(f"Invalid address lookup for package {package.ID}")
                    continue  # Skip this package or handle error as needed
                distance = self.betweenst(address1_index, address2_index)
                if distance < nextAddress:
                    nextAddress = distance
                    nextPackage = package
            if nextPackage is None:
                print("No valid next package found; ending delivery loop.")
                break
            self.miles += nextAddress
            self.current_location = nextPackage.street
            travel_time = datetime.timedelta(hours=nextAddress / self.speed)
            self.time += travel_time
            nextPackage.update_status('Delivered', self.time)
            enroute.remove(nextPackage)
