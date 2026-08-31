from bello_office import auth, shelf, logbook, record


def print_reply(code, message):
    print(f"{code} {message}")


def handle_slip(slip, books, user):
    parts = slip.split()

    if not parts:
        return 400, "I cannot read this slip"

    verb = parts[0].upper()

    if verb == "GET":
        if len(parts) == 2 and parts[1] == "books":
            return logbook.get_all_books(books)

        if len(parts) == 3 and parts[1] == "books" and parts[2] == "borrowed":
            return logbook.get_borrowed_books(books)

        if len(parts) == 3 and parts[1] == "book":
            if not parts[2].isdigit():
                return 400, "I cannot read this slip"
            return logbook.get_one_book(books, int(parts[2]))

        return 400, "I cannot read this slip"

    if verb == "POST":
        if len(parts) == 2 and parts[1] == "book":
            title = input("Title: ")
            author = input("Author: ")
            code, result = logbook.add_book(books, title, author)
            if code == 201:
                shelf.save_books(books)
            return code, result

        return 400, "I cannot read this slip"

    if verb == "PUT":
        if len(parts) == 3 and parts[1] == "book":
            if not parts[2].isdigit():
                return 400, "I cannot read this slip"
            number = int(parts[2])
            title = input("New title: ")
            author = input("New author: ")
            status = input("New status (on shelf/borrowed): ")
            code, result = logbook.update_book(books, number, title, author, status)
            if code == 200:
                shelf.save_books(books)
            return code, result

        return 400, "I cannot read this slip"

    if verb == "DELETE":
        if len(parts) == 3 and parts[1] == "book":
            if not parts[2].isdigit():
                return 400, "I cannot read this slip"
            number = int(parts[2])

            if not auth.can_perform(user, "DELETE"):
                return 403, "I know who you are, and you are not allowed to do this"

            code, result = logbook.delete_book(books, number)
            if code == 200:
                shelf.save_books(books)
            return code, result

        return 400, "I cannot read this slip"

    return 400, "I cannot read this slip"


def main():
    user = auth.sign_in()

    if user is None:
        print_reply(401, "Who are you? Sign in first.")
        return

    books = shelf.load_books()

    print("The desk is open. Type a slip, or QUIT to leave.")

    while True:
        slip = input("\nSlip: ")

        if slip.upper() == "QUIT":
            print("The desk is now closed.")
            break

        code, message = handle_slip(slip, books, user)
        print_reply(code, message)
        record.log_event(user["username"], slip, code, message)


if __name__ == "__main__":
    main()