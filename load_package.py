import csv
from package import Package

# Utility functions to load data from CSV files
def load_package_data(filename, hash_table):
    """Loads package data from a CSV file into the provided hash table."""
    with open('packages.csv') as package_file:
        package_data = csv.reader(package_file, delimiter=',')
        next(package_data) # Skip header
        for row in package_data:
            p_id = int(row[0])
            p_address = row[1]
            p_city = row[2]
            p_state = row[3]
            p_zip = row[4]
            p_deadline = row[5]
            p_weight = row[6]
            # Handle potentially missing notes field
            p_notes = row[7] if len(row) > 7 else ""
            p_status = "At Hub"

            package = Package(p_id, p_address, p_city, p_state, p_zip, p_deadline, p_weight, p_status, p_notes)
            hash_table.insert(p_id, package)

def load_distance_data(filename):
    """Loads the distance matrix from the provided CSV file."""
    distances = []
    with open('distance_table.csv') as distance_file:
        distance_data = csv.reader(distance_file, delimiter=',')
        for row in distance_data:
            distances.append(row)
    return distances

def load_address_data(filename):
    """Loads address data from the CSV file."""
    addresses = []
    with open('addresses.csv') as address_file:
        address_data = csv.reader(address_file, delimiter=',')
        for row in address_data:
            # [cite_start]The full address is in the second column [cite: 1, 2, 3, 4]
            addresses.append(row[1])
    return addresses

# Helper functions for distance and time calculations
def get_address_id(address, address_list):
    """Finds the index (ID) for a given address string."""
    for i, addr in enumerate(address_list):
        if address in addr:
            return i
    return -1

def get_distance_between(address1_id, address2_id, distances):
    """Returns the distance between two locations using their IDs from the distance table."""
    try:
        distance = distances[address1_id][address2_id]
        if distance == '':
            distance = distances[address2_id][address1_id]
        return float(distance)
    except (IndexError, ValueError):
        return float('inf')
