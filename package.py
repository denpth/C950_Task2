import datetime

# Represents a package with all its attributes
class Package:
    """
    Represents a package with all its delivery information.
    Includes methods to update status based on time.
    """
    def __init__(self, id, address, city, state, zip_code, deadline, weight, status, notes):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline_str = deadline
        self.deadline_time = self._convert_deadline(deadline)
        self.weight = weight
        self.status = status
        self.notes = notes
        self.departure_time = None
        self.delivery_time = None

    def __str__(self):
        return (f"ID: {self.id}, Address: {self.address}, {self.city}, {self.zip_code}, "
                f"Deadline: {self.deadline_str}, Weight: {self.weight} kg, "
                f"Delivery Time: {self.delivery_time}, Status: {self.status}")

    def _convert_deadline(self, deadline_str):
        """Converts a deadline string (e.g., '10:30 AM') to a timedelta object."""
        if deadline_str == 'EOD':
            return datetime.timedelta(hours=23, minutes=59)
        time_part, am_pm = deadline_str.split()
        h, m = map(int, time_part.split(':'))
        if am_pm == 'PM' and h != 12:
            h += 12
        return datetime.timedelta(hours=h, minutes=m)

    def update_status(self, current_time):
        """Updates the package status based on the current time."""
        if self.departure_time is None or current_time < self.departure_time:
             self.status = "At Hub"
        elif self.delivery_time is None or current_time < self.delivery_time:
            self.status = "En Route"
        else:
            self.status = "Delivered"
