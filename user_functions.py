from data_models import building_lock, building, organizations, organizations_lock, Booking
from datetime import datetime, timedelta

def list_conference_rooms():
    """List all available conference rooms in the building."""
    room_list = []
    with building_lock:
        for floor_number, floor in building.items():
            with floor.lock:
                for room_name, room in floor.rooms.items():
                    room_list.append({
                        "Room Name": room_name,
                        "Floor Number": floor_number,
                        "Capacity": room.capacity,
                        "Additional Details": room.additional_details
                    })
    return room_list

def find_suitable_rooms(capacity, start_time, end_time, additional_details=None):
    """Find suitable rooms based on user requirements."""
    suitable_rooms = []
    with building_lock:
        for floor_number, floor in building.items():
            with floor.lock:
                for room_name, room in floor.rooms.items():
                    with room.lock:
                        # Check room capacity
                        if room.capacity < capacity:
                            continue
                        # Check additional details
                        if additional_details:
                            if not all(item in room.additional_details.items() for item in additional_details.items()):
                                continue
                        # Check availability
                        if any(booking.start_time < end_time and booking.end_time > start_time for booking in room.bookings):
                            continue
                        suitable_rooms.append({
                            "Room Name": room_name,
                            "Floor Number": floor_number,
                            "Capacity": room.capacity,
                            "Additional Details": room.additional_details
                        })
    return suitable_rooms

def book_room(user_email, organization_name, room_name, floor_number, start_time, end_time):
    """Book a room for a specific time slot."""
    with organizations_lock:
        organization = next((org for org in organizations if org.name == organization_name), None)
    
    if not organization:
        return f"Organization {organization_name} does not exist."
    
    with organization.lock:
        user = organization.users.get(user_email)
    
    if not user:
        return f"User {user_email} does not exist in Organization {organization_name}."
    
    with building_lock:
        floor = building.get(floor_number)
    
    if not floor:
        return f"Floor {floor_number} does not exist."
    
    with floor.lock:
        room = floor.rooms.get(room_name)
    
    if not room:
        return f"Room {room_name} does not exist on Floor {floor_number}."
    
    with room.lock:
        # Check availability
        if any(booking.start_time < end_time and booking.end_time > start_time for booking in room.bookings):
            return "Room is not available for the requested time slot."
        
        # Check organization's monthly booking limit
        booking_hours = (end_time - start_time).seconds // 3600
        if organization.total_booking_hours + booking_hours > 30:
            return "Organization has exceeded its monthly booking limit."
        
        # Create a new booking
        new_booking = Booking(user, room, start_time, end_time)
        room.bookings.append(new_booking)
        user.bookings.append(new_booking)
        organization.total_booking_hours += booking_hours
    
    return f"Successfully booked Room {room_name} from {start_time} to {end_time}."

def cancel_booking(user_email, organization_name, room_name, floor_number, start_time):
    """Cancel an existing booking."""
    with organizations_lock:
        organization = next((org for org in organizations if org.name == organization_name), None)
    
    if not organization:
        return f"Organization {organization_name} does not exist."
    
    with organization.lock:
        user = organization.users.get(user_email)
    
    if not user:
        return f"User {user_email} does not exist in Organization {organization_name}."
    
    with building_lock:
        floor = building.get(floor_number)
    
    if not floor:
        return f"Floor {floor_number} does not exist."
    
    with floor.lock:
        room = floor.rooms.get(room_name)
    
    if not room:
        return f"Room {room_name} does not exist on Floor {floor_number}."
    
    with room.lock:
        # Find the booking to cancel
        booking_to_cancel = next((booking for booking in room.bookings if booking.start_time == start_time and booking.user.email == user_email), None)
        
        if not booking_to_cancel:
            return "No such booking exists."
        
        # Check if it's too late to cancel
        if datetime.now() + timedelta(minutes=15) > booking_to_cancel.start_time:
            return "Too late to cancel. Cancellations must be made at least 15 minutes before the booking starts."
        
        # Remove the booking
        room.bookings.remove(booking_to_cancel)
        user.bookings.remove(booking_to_cancel)
        organization.total_booking_hours -= (booking_to_cancel.end_time - booking_to_cancel.start_time).seconds // 3600
    
    return f"Successfully cancelled the booking for Room {room_name} from {start_time}."

def list_user_organization_bookings(user_email, organization_name, start_date, end_date):
    """List all bookings made by a user or by any/all users of that organization within a given date range."""
    with organizations_lock:
        organization = next((org for org in organizations if org.name == organization_name), None)
    
    if not organization:
        return f"Organization {organization_name} does not exist."
    
    booking_list = []
    
    with organization.lock:
        user = organization.users.get(user_email)
    
    if not user:
        return f"User {user_email} does not exist in Organization {organization_name}."
    
    for booking in user.bookings:
        if booking.start_time >= start_date and booking.end_time <= end_date:
            booking_list.append({
                "Room Name": booking.room.name,
                "Floor Number": booking.room.floor_number,
                "Start Time": booking.start_time,
                "End Time": booking.end_time
            })
            
    return booking_list