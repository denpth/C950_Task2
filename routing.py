import datetime
import csv
from chainingHash import ChainingHashTable
from package import Package
from load_package import load_package_data, load_distance_data, load_address_data, get_address_id, get_distance_between

def format_time_24h(time_delta):
    """Convert timedelta to 24-hour format string (HH:MM)."""
    if time_delta is None:
        return "N/A"
    
    total_seconds = int(time_delta.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    
    # Handle 24+ hour times by wrapping to next day
    hours = hours % 24
    
    return f"{hours:02d}:{minutes:02d}"

class Main:
    """Main class to orchestrate the WGUPS delivery simulation."""

    def __init__(self):
        self.package_hash_table = ChainingHashTable()
        load_package_data('packages.csv', self.package_hash_table)
        self.distances = load_distance_data('distance_table.csv')
        self.addresses = load_address_data('addresses.csv')
        self.correction_time = datetime.timedelta(hours=10, minutes=20)

    def deliver_packages(self, truck, start_time):
        """
        Executes the delivery route for a given truck using a greedy nearest-neighbor algorithm.
        This function now includes logic to handle the wrong address for package #9.
        Time Complexity: O(N^2) where N is the number of packages on the truck.
        """
        undelivered = [self.package_hash_table.search(pkg_id) for pkg_id in truck['packages']]
        truck['current_time'] = start_time
        truck['current_location'] = "4001 South 700 East, Salt Lake City, UT 84107"  # The hub address [cite: 1]

        # Set departure time for all packages on this truck
        for package in undelivered:
            package.departure_time = start_time
            self.package_hash_table.insert(package.id, package)

        while undelivered:
            min_distance = float('inf')
            next_package = None

            # Find the nearest undelivered package
            for package in undelivered:
                # Handle special case for package #9
                if package.id == 9:
                    if truck['current_time'] < self.correction_time:
                        continue  # Skip package 9 if it's before 10:20 AM
                    else:
                        # Update address if time is 10:20 AM or later
                        package.address = "410 S State St"
                        package.zip_code = "84111"
                        self.package_hash_table.insert(9, package)

                current_loc_id = get_address_id(truck['current_location'], self.addresses)
                package_loc_id = get_address_id(package.address, self.addresses)
                distance = get_distance_between(current_loc_id, package_loc_id, self.distances)

                if distance < min_distance:
                    min_distance = distance
                    next_package = package

            # If no valid next package is found (e.g., only #9 remains before 10:20), advance time
            if next_package is None:
                truck['current_time'] = self.correction_time
                continue

            # Travel to the next package's location
            truck['mileage'] += min_distance
            travel_time = datetime.timedelta(hours=min_distance / 18.0)
            truck['current_time'] += travel_time

            # Update the delivered package's info
            next_package.delivery_time = truck['current_time']
            self.package_hash_table.insert(next_package.id, next_package)

            truck['current_location'] = next_package.address
            undelivered.remove(next_package)

        # Return to hub and finalize the truck's finish time
        hub_loc_id = get_address_id("4001 South 700 East", self.addresses)
        final_loc_id = get_address_id(truck['current_location'], self.addresses)
        return_trip_dist = get_distance_between(final_loc_id, hub_loc_id, self.distances)
        truck['mileage'] += return_trip_dist
        truck['finish_time'] = truck['current_time'] + datetime.timedelta(hours=return_trip_dist / 18.0)

    def run(self):
        """
        Sets up the trucks, runs the simulation accounting for driver availability,
        and provides a user interface for status checks.
        """
        # Strategic manual loading of trucks to ensure all constraints are met.
        truck1_array = [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40]
        truck2_array = [3, 6, 18, 25, 27, 28, 32, 33, 35, 36, 38, 39]
        truck3_array = [2, 4, 5, 7, 8, 9, 10, 11, 12, 17, 21, 22, 23, 24, 26]
        truck1_array.sort()
        truck2_array.sort()
        truck3_array.sort()
        truck1 = {'packages': truck1_array, 'mileage': 0.0}
        truck2 = {'packages': truck2_array, 'mileage': 0.0}
        truck3 = {'packages': truck3_array, 'mileage': 0.0}

        # --- Driver & Truck Departure Logic ---
        # Driver 1 and 2 leave at 8:00 AM and 9:05 AM
        self.deliver_packages(truck1, datetime.timedelta(hours=8))
        self.deliver_packages(truck2, datetime.timedelta(hours=9, minutes=5))

        # Determine when the first driver is free
        first_driver_free_time = min(truck1['finish_time'], truck2['finish_time'])

        # Truck 3 must leave after 9:05 AND when a driver is available
        truck3_earliest_departure = datetime.timedelta(hours=9, minutes=5)
        truck3_actual_departure = max(truck3_earliest_departure, first_driver_free_time)

        self.deliver_packages(truck3, truck3_actual_departure)


        print("\n--- Verifying All Delivery Deadlines ---")
        all_met = True
        for i in range(1, 41):
            package = self.package_hash_table.search(i)
            if package.delivery_time is None:
                print(f"❌ FAILED: Package {package.id} was not delivered!")
                all_met = False
            elif package.delivery_time > package.deadline_time:
                print(
                    f"❌ FAILED: Package {package.id} missed deadline! Delivered at {format_time_24h(package.delivery_time)}, Deadline was {package.deadline_str}")
                all_met = False
        if all_met:
            print("✅ Success! All packages were delivered on time.")

        # User interface for package status lookup
        while True:
            try:
                user_time_str = input("\nEnter a time (HH:MM) to check package statuses, or type 'exit' to quit: ")
                if user_time_str.lower() == 'exit':
                    break

                (h, m) = user_time_str.split(':')
                user_time = datetime.timedelta(hours=int(h), minutes=int(m))

                print(f"\n--- Status of all packages at {format_time_24h(user_time)} ---")
                print("\U0001F69A Truck 1")
                self.print_truck(truck1_array, user_time)
                print("\U0001F69A Truck 2")
                self.print_truck(truck2_array, user_time)
                print("\U0001F69A Truck 3")
                self.print_truck(truck3_array, user_time)

            except (ValueError, IndexError):
                print("Invalid time format. Please use HH:MM.")

         # --- Final Results and Verification ---
        total_mileage = truck1['mileage'] + truck2['mileage'] + truck3['mileage']
        print("✅ WGUPS Delivery Simulation Complete.")
        print(f"Total mileage for all trucks: {total_mileage:.2f} miles.")

    def print_truck(self, truck_array, user_time):
        for i in truck_array:
            package = self.package_hash_table.search(i)

            # Temporarily set address for package 9 based on lookup time
            original_address, original_zip = package.address, package.zip_code
            if package.id == 9:
                if user_time < self.correction_time:
                    package.address = "300 State St"  # The wrong address [cite: 6, 8]
                    package.zip_code = "84103"  # The wrong zip code [cite: 6, 8]
                else:
                    package.address = "410 S State St"
                    package.zip_code = "84111"

            package.update_status(user_time)
            # Only show delivery time if package has been delivered at the queried time
            if package.status == "Delivered":
                print("\033[32m", end="")
                delivery_time_display = format_time_24h(package.delivery_time)
            elif package.status == "En Route":
                print("\033[93m", end="")
                delivery_time_display = "N/A"
            elif package.status == "Delayed":
                print("\033[31m", end="")
                delivery_time_display = "Delayed"
            else:    
                print("\033[0m", end="")
                delivery_time_display = "N/A"
            print(f"Package {package.id}: Status: {package.status}. Delivery Address: {package.address}, "
                f"{package.zip_code}. Deadline: {package.deadline_str}. Delivery Time: {delivery_time_display} \033[0m")

            # Revert package 9 address for next loop integrity
            if package.id == 9:
                package.address, package.zip_code = original_address, original_zip