from threading import Lock

class Floor:
    def __init__(self, floor_number):
        self.floor_number = floor_number
        self.rooms = {}  # Dictionary to hold room_name: Room object pairs
        self.lock = Lock()  # Lock for handling concurrency

class Room:
    def __init__(self, name, floor_number, capacity, additional_details=None):
        self.name = name
        self.floor_number = floor_number
        self.capacity = capacity
        self.additional_details = additional_details if additional_details else {}
        self.bookings = []  # List to hold Booking objects
        self.lock = Lock()  # Lock for handling concurrency

class Organization:
    def __init__(self, name, contact_info, additional_details=None):
        self.name = name
        self.contact_info = contact_info
        self.additional_details = additional_details if additional_details else {}
        self.users = {}  # Dictionary to hold email: User object pairs
        self.total_booking_hours = 0  # For monthly limit tracking
        self.lock = Lock()  # Lock for handling concurrency

class User:
    def __init__(self, name, email, role, permissions, organization):
        self.name = name
        self.email = email
        self.role = role
        self.permissions = permissions
        self.organization = organization  # Reference to the Organization object
        self.bookings = []  # List to hold Booking objects
        self.lock = Lock()  # Lock for handling concurrency

class Booking:
    def __init__(self, user, room, start_time, end_time):
        self.user = user  # Reference to the User object
        self.room = room  # Reference to the Room object
        self.start_time = start_time  # datetime object
        self.end_time = end_time  # datetime object
        self.lock = Lock()  # Lock for handling concurrency

# Initialize an empty building (dictionary to hold floor_number: Floor object pairs)
building = {}
building_lock = Lock()  # Lock for handling concurrency

# Initialize an empty list of organizations
organizations = []
organizations_lock = Lock()  # Lock for handling concurrency

print("Data models have been successfully created!")

