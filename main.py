from admin_functions import *
from suggetions import generate_suggestions
from user_functions import *

# Test the admin functions

print('===============================Add floors======================================')

print(add_floor(1))
print(add_floor(2))
print(add_floor(1))  # Should return that the floor already exists

print('===============================Add rooms to floors======================================')

print(add_room_to_floor(1, "Room101", 10))
print(add_room_to_floor(1, "Room102", 12, {"Projector": "Available"}))
print(add_room_to_floor(2, "Room201", 8))
print(add_room_to_floor(3, "Room301", 10))  # Should return that the floor does not exist
print(add_room_to_floor(1, "Room101", 10))  # Should return that the room already exists

print('===============================Register organizations======================================')

print(register_new_organization("Org1", "contact@org1.com"))
print(register_new_organization("Org2", "contact@org2.com", {"Address": "123 Main St"}))
print(register_new_organization("Org1", "contact@org1.com"))  # Should return that the organization already exists

print('===============================Register users within organizations======================================')

print(register_new_user("Org1", "Alice", "alice@org1.com", "Manager", ["book", "cancel"]))
print(register_new_user("Org1", "Bob", "bob@org1.com", "Employee", ["book"]))
print(register_new_user("Org3", "Charlie", "charlie@org3.com", "Manager", ["book", "cancel"]))  # Should return that the organization does not exist
print(register_new_user("Org1", "Alice", "alice@org1.com", "Manager", ["book", "cancel"]))  # Should return that the user already exists

print('===============================generate suggetions======================================')

user_email = "alice@org1.com"
organization_name = "Org1"
room_name = "Room101"
current_time = datetime.now()  # Current time for suggestions
suggestions = generate_suggestions(user_email, organization_name, room_name, current_time)

# Display suggestions to the user
if suggestions:
    print("Suggestions for user: ", user_email)
    print("Room : ", room_name)
    for i, suggestion in enumerate(suggestions, start=1):
        print(f"Suggestion {i}: {suggestion[0].strftime('%Y-%m-%d %H:%M')} - {suggestion[1].strftime('%H:%M')}")
else:
    print("No suggestions available.")

# Test the user features

print('===============================List conference rooms======================================')

print("List of Conference Rooms:")
print(list_conference_rooms())

print('===============================Find suitable rooms======================================')

print("\nSuitable Rooms for capacity=10, time=2023-09-01 10:00 to 2023-09-01 12:00:")
print(find_suitable_rooms(10, datetime.strptime("2023-09-01 10:00", "%Y-%m-%d %H:%M"), datetime.strptime("2023-09-01 12:00", "%Y-%m-%d %H:%M")))

print('===============================Book a room======================================')

print("\nBooking Room101 on Floor 1:")
print(book_room("alice@org1.com", "Org1", "Room101", 1, datetime.strptime("2023-09-01 10:00", "%Y-%m-%d %H:%M"), datetime.strptime("2023-09-01 12:00", "%Y-%m-%d %H:%M")))

print('===============================Find suitable rooms again to check if Room101 is now unavailable======================================')

print("\nSuitable Rooms for capacity=10, time=2023-09-01 10:00 to 2023-09-01 12:00:")
print(find_suitable_rooms(10, datetime.strptime("2023-09-01 10:00", "%Y-%m-%d %H:%M"), datetime.strptime("2023-09-01 12:00", "%Y-%m-%d %H:%M")))

print('===============================Book a room for testing cancellation======================================')

print(book_room("alice@org1.com", "Org1", "Room102", 1, datetime.strptime("2023-09-01 14:00", "%Y-%m-%d %H:%M"), datetime.strptime("2023-09-01 16:00", "%Y-%m-%d %H:%M")))

print('=============================== Cancel a booking======================================')

print("\nCancel Booking for Room102 on Floor 1:")
print(cancel_booking("alice@org1.com", "Org1", "Room102", 1, datetime.strptime("2023-09-01 14:00", "%Y-%m-%d %H:%M")))

print('===============================List user/organization bookings======================================')

print("\nList of User Bookings for Alice from Org1 between 2023-09-01 and 2023-09-02:")
print(list_user_organization_bookings("alice@org1.com", "Org1", datetime.strptime("2023-09-01", "%Y-%m-%d"), datetime.strptime("2023-09-02", "%Y-%m-%d")))