"""
User:
    - id | int
    - username | string
    - password | string -- hashed
    - email | string
    - social_profile | relationship
    - authentications | relationship
    - password_changes | relationship
    - last_active | timestamp

    - updated_at | datetime
    - created_at | datetime
"""

"""
Profile:
    - id | int
    - user_id | int
    - email | string
    - phone | string
    - snap | string
    - insta | string
    - spotify | string
    - linkedin | string
    - facebook | string
    - first_name | string
    - last_name | string
    
    - updated_at | datetime
    - created_at | datetime
"""

"""
Authentications:
    - id | int
    - username | string
    - password | string
    - user_id | relationship
    - successful | bool
    - ip_address | string
    
    - updated_at | datetime
    - created_at | datetime
"""

"""
Password Changes:
    - id
    - old_hash
    - new_hash
    - user_id
    
    - updated_at | datetime
    - created_at | datetime
"""
