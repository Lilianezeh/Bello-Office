STAFF_REGISTER = [
    {"username": "mrs_okafor", "password": "library2024", "position": "Chief Librarian"},
    {"username": "bello_jr", "password": "windowboy", "position": "Member"},
    {"username": "amina_s", "password": "books4life", "position": "Member"},
    {"username": "tunde_reads", "password": "password123", "position": "Member"},
    {"username": "chichi_o", "password": "novels!", "position": "Member"},
    {"username": "baba_musa", "password": "retired55", "position": "Member"},
]
 
MAX_ATTEMPTS = 3
 
 
def find_staff(username):
    """Look up a staff member by username. Returns None if not found."""
    for staff in STAFF_REGISTER:
        if staff["username"] == username:
            return staff
    return None
 
 
def sign_in():
    """Prompt for username/password up to MAX_ATTEMPTS times.
    Returns a small user dict on success, or None if the grille closes."""
    attempts = 0
 
    while attempts < MAX_ATTEMPTS:
        username = input("Username: ")
        password = input("Password: ")
 
        staff = find_staff(username)
 
        if staff is not None and staff["password"] == password:
            return {"username": staff["username"], "position": staff["position"]}
 
        attempts += 1
        remaining = MAX_ATTEMPTS - attempts
        if remaining > 0:
            print(f"That did not match. {remaining} attempt(s) left.")
        else:
            print("Three wrong attempts. The grille is now closed.")
 
    return None
 
 
def can_perform(user, action):
    """Only the Chief Librarian may DELETE. Everyone signed in may do the rest."""
    if action == "DELETE":
        return user["position"] == "Chief Librarian"
    return True
 
