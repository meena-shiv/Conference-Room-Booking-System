**Conference Room Booking System**

1. **Overview of the System**

The Conference Room Booking System is designed to manage the booking of conference rooms in a building with multiple floors. The system allows administrators to add floors, rooms, and organizations and register users under these organizations. Users can then book rooms, view their bookings, and cancel bookings under certain conditions.

2. **Data Models**

The system uses the following main data models:

- Floor: Represents a floor in the building.
- Room: Represents a conference room on a floor.
- Organization: Represents an organization using the system.
- User: Represents a user within an organization.
- Booking: Represents a room booking made by a user.
3. **Features and Functions**

The system supports the following features and functions:

- Add Floor and Room Details
- Register New Organization
- Register New User
- List Conference Rooms
- Find Suitable Rooms
- Book Room
- Cancel Booking
- List User/Organization Bookings
- Monthly Booking Limit
- Suggestion Functionality
4. **Concurrency Handling**

The system is designed to handle multiple users and organizations booking rooms simultaneously. This is achieved through the use of Python's threading locks at both the global and object levels. This ensures that all operations are thread-safe.

5. **Code Structure**

The code is modular, with separate functions for each feature. Each function uses locks to ensure thread safety. The system uses in-memory data structures like dictionaries and lists to store all the data related to conference rooms, bookings, organizations, and users.

6. **Commands for Demo**

Please run the below commands to test the code.

- Overall demo
  - python main.py
- Concurrency demo

○ python concurrency.py

Please use the main.py or concurrency.py file for custom inputs and testing.
