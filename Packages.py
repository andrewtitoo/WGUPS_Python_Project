import csv
import datetime

class Package:
    def __init__(self, ID, street, city, state, zip_code, deadline, weight, notes, address_update_time=None, new_address=None):
        self.ID = ID
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = "At the hub"
        self.departure_time = None
        self.delivery_time = None
        self.status_history = [(datetime.datetime.now(), "At the hub")]
        self.address_update_time = address_update_time
        self.new_address = new_address
        self.original_address = street  # Store the original address

    def update_address_if_needed(self, current_time):
        if self.address_update_time and current_time >= self.address_update_time:
            print(f"Updating address for Package {self.ID} to {self.new_address}")
            self.street = self.new_address
            self.address_update_time = None  # Prevent further updates

    def __str__(self):
        """Return a string representation of the package with its current status."""
        current_status = self.get_status_at_time(datetime.datetime.now())
        return (f"ID: {self.ID}, Street: {self.street}, City: {self.city}, State: {self.state}, "
                f"Zip Code: {self.zip_code}, Deadline: {self.deadline}, Weight: {self.weight}, "
                f"Notes: {self.notes}, Status: {current_status}, Departure Time: {self.departure_time}, "
                f"Delivery Time: {self.delivery_time}")

    def update_status(self, new_status, time):
        """Update the package's status and append the change to the status history."""
        self.status = new_status
        if new_status == "En route":
            self.departure_time = time
        elif new_status == "Delivered":
            self.delivery_time = time
        self.status_history.append((time, new_status))

    def get_status_at_time(self, query_time):
        """Return the status and potentially updated address of the package at a specific query time."""
        last_known_status = "At the hub"  # Start with default assumption
        current_address = self.original_address  # Default to the original address

        # Go through each status change recorded
        for time, status in self.status_history:
            if time <= query_time:
                last_known_status = status
                # Update the address if the address change time was before the query time
                if self.address_update_time and query_time >= self.address_update_time:
                    current_address = self.new_address

        return last_known_status, current_address


def load_package_data(filename, package_data):
        """Load package data from a CSV file into a hash table."""
        with open(filename) as packages:
            reader = csv.reader(packages, delimiter=',')
            next(reader)  # Skip the header row.
            for row in reader:
                package = Package(int(row[0]), row[1], row[2], row[3], row[4], row[5], row[6], row[7])
                package_data.insert(package.ID, package)