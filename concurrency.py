import threading
from admin_functions import add_floor, add_room_to_floor, register_new_organization, register_new_user
from user_functions import book_room
from datetime import datetime
# Initialize some test data
print('===============================Add floors and rooms======================================')

print(add_floor(1))
print(add_room_to_floor(1, "DemoRoom", 10))

print('===============================Register an organization and users======================================')

print(register_new_organization("DemoOrg", "contact@demo.org"))
print(register_new_user("DemoOrg", "User1", "user1@demo.org", "Employee", ["book"]))
print(register_new_user("DemoOrg", "User2", "user2@demo.org", "Employee", ["book"]))

print('===============================Booking rooms concurrently======================================')
# Function to book a room (to be called from multiple threads)
def demo_book_room(user_email):
    result = book_room(user_email, "DemoOrg", "DemoRoom", 1, 
                       datetime.strptime("2023-09-02 10:00", "%Y-%m-%d %H:%M"), 
                       datetime.strptime("2023-09-02 11:00", "%Y-%m-%d %H:%M"))
    print(f"{user_email}: {result}")

# Create threads to book a room
thread1 = threading.Thread(target=demo_book_room, args=("user1@demo.org",))
thread2 = threading.Thread(target=demo_book_room, args=("user2@demo.org",))

# Start the threads
thread1.start()
thread2.start()

# Wait for both threads to finish
thread1.join()
thread2.join()

print("Concurrency demo completed.")
