def get_all_books(books):
    return 200, books


def get_borrowed_books(books):
    borrowed = []
    for b in books:
        if b["status"] == "borrowed":
            borrowed.append(b)
    return 200, borrowed


def get_one_book(books, number):
    for b in books:
        if b["number"] == number:
            return 200, b
    return 404, f"Book number {number} could not be found on the shelf"


def _lowest_free_number(books):
    """Find the smallest positive number not currently in use.
    This means a deleted book's number can be reused later,
    instead of numbers only ever climbing upward."""
    taken = set(b["number"] for b in books)
    candidate = 1
    while candidate in taken:
        candidate += 1
    return candidate


def add_book(books, title, author):
    new_number = _lowest_free_number(books)
    new_book = {
        "number": new_number,
        "title": title,
        "author": author,
        "status": "on shelf",
    }
    books.append(new_book)
    return 201, new_book


def update_book(books, number, title, author, status):
    for b in books:
        if b["number"] == number:
            b["title"] = title
            b["author"] = author
            b["status"] = status
            return 200, b
    return 404, f"Book number {number} could not be found on the shelf"


def delete_book(books, number):
    for i, b in enumerate(books):
        if b["number"] == number:
            removed = books.pop(i)
            return 200, removed
    return 404, f"Book number {number} could not be found on the shelf"