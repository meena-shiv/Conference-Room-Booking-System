from data_models import building_lock, building, organizations, organizations_lock, Organization, User, Floor, Room

def add_floor(floor_number):
    """Add a new floor to the building."""
    with building_lock:
        if floor_number in building:
            return f"Floor {floor_number} already exists."
        building[floor_number] = Floor(floor_number)
    return f"Successfully added Floor {floor_number}."

def add_room_to_floor(floor_number, room_name, capacity, additional_details=None):
    """Add a new room to an existing floor."""
    with building_lock:
        floor = building.get(floor_number)
        if not floor:
            return f"Floor {floor_number} does not exist."
            
    with floor.lock:
        if room_name in floor.rooms:
            return f"Room {room_name} already exists on Floor {floor_number}."
        floor.rooms[room_name] = Room(room_name, floor_number, capacity, additional_details)
    return f"Successfully added Room {room_name} to Floor {floor_number}."

def register_new_organization(name, contact_info, additional_details=None):
    """Register a new organization."""
    with organizations_lock:
        for org in organizations:
            if org.name == name:
                return f"Organization {name} already exists."
        new_org = Organization(name, contact_info, additional_details)
        organizations.append(new_org)
    return f"Successfully registered Organization {name}."

def register_new_user(organization_name, name, email, role, permissions):
    """Register a new user within an organization."""
    with organizations_lock:
        organization = next((org for org in organizations if org.name == organization_name), None)
    
    if not organization:
        return f"Organization {organization_name} does not exist."
    
    with organization.lock:
        if email in organization.users:
            return f"User with email {email} already exists in Organization {organization_name}."
        new_user = User(name, email, role, permissions, organization)
        organization.users[email] = new_user
    return f"Successfully registered User {name} in Organization {organization_name}."