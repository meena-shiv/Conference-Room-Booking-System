from datetime import datetime, timedelta
import random
from data_models import building, Booking, organizations

# Function to generate suggestions 
def generate_suggestions(user_email, organization_name, room_name, current_time):
    # Retrieve the user, organization, and room objects
    user = None
    organization = None
    room = None
    for org in organizations:
        if org.name == organization_name:
            organization = org
            if user_email in org.users:
                user = org.users[user_email]
                break
    if not organization or not user:
        return []

    for floor in building.values():
        if room_name in floor.rooms:
            room = floor.rooms[room_name]
            break
    if not room:
        return []

    # Analyze historical data to generate suggestions
    suggestions = []
    for _ in range(3):  # Generate up to 3 suggestions
        available_times = []
        for i in range(8, 17):  # Consider hours from 8 AM to 5 PM
            start_time = datetime(2023, 9, 1, i, 0)
            end_time = start_time + timedelta(hours=1)
            # Check availability based on historical data
            if all(booking.end_time <= start_time or booking.start_time >= end_time for booking in room.bookings):
                # Check organization's monthly limit
                requested_hours = (end_time - start_time).total_seconds() / 3600
                if organization.total_booking_hours + requested_hours <= 30:
                    available_times.append((start_time, end_time))
        if available_times:
            random_time = random.choice(available_times)
            suggestions.append(random_time)
            # Block the chosen time slot to avoid duplicate suggestions
            booking = Booking(user, room, random_time[0], random_time[1])
            organization.total_booking_hours += (random_time[1] - random_time[0]).total_seconds() / 3600
            room.bookings.append(booking)

    return suggestions