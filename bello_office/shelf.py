import json
import os
 
BOOK_FILE = "book_shelf.json"
 
STARTER_BOOKS = [
    {"number": 1, "title": "Things Fall Apart", "author": "Chinua Achebe", "status": "on shelf"},
    {"number": 2, "title": "Purple Hibiscus", "author": "Chimamanda Adichie", "status": "borrowed"},
    {"number": 3, "title": "The Famished Road", "author": "Ben Okri", "status": "on shelf"},
    {"number": 4, "title": "Sozaboy", "author": "Ken Saro-Wiwa", "status": "on shelf"},
    {"number": 5, "title": "Jagua Nana", "author": "Cyprian Ekwensi", "status": "borrowed"},
    {"number": 6, "title": "The Joys of Motherhood", "author": "Buchi Emecheta", "status": "on shelf"},
    {"number": 7, "title": "Arrow of God", "author": "Chinua Achebe", "status": "on shelf"},
    {"number": 8, "title": "Stay With Me", "author": "Ayobami Adebayo", "status": "borrowed"},
    {"number": 9, "title": "The Fishermen", "author": "Chigozie Obioma", "status": "on shelf"},
    {"number": 10, "title": "Half of a Yellow Sun", "author": "Chimamanda Adichie", "status": "on shelf"},
]
 
 
def load_books():
    """Load the shelf from disk. Handles first run and a damaged file."""
    if not os.path.exists(BOOK_FILE):
        # First-day case: no file yet, seed it and write it out
        save_books(STARTER_BOOKS)
        return list(STARTER_BOOKS)
 
    try:
        with open(BOOK_FILE, "r") as f:
            data = json.load(f)
        if not isinstance(data, list):
            raise ValueError("shelf file did not contain a list of books")
        return data
    except (json.JSONDecodeError, ValueError):
        # Vandal case: file exists but is broken. Notice, say so, recover.
        print("The shelf file looks damaged. Starting over with the original ten books.")
        save_books(STARTER_BOOKS)
        return list(STARTER_BOOKS)
 
 
def save_books(books):
    """Write the current list of books back to disk."""
    with open(BOOK_FILE, "w") as f:
        json.dump(books, f, indent=4)
 
