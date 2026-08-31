# The Bello Office — A Library Backend Simulator

Mr. Bello is retiring from the council library on Adeniran Street, and this program takes over his job at the window. A visitor writes a request ("a slip"), the program does whatever the slip asks for, and hands back a reply. Every reply always starts with a numeric code, the same way a real web API answers with a status code before its message — this project is really a tiny API, dressed up as a library counter.

## How It's Organised

```
bello-office-project/
├── main.py            — the window itself: reads a slip, prints a reply, nothing more
└── bello_office/
    ├── __init__.py    — marks this folder as an importable package
    ├── shelf.py       — the only file that reads/writes book_shelf.json
    ├── auth.py        — staff register, sign-in loop, lockout, role checks
    ├── logbook.py      — GET/POST/PUT/DELETE logic; the only file that edits book data
    └── record.py       — writes one line per slip to desk_diary.txt
```

Each file has a single responsibility, and `main.py` never touches the book list, the staff register, or a file directly — it only parses input and calls the right function.

## Requirements

- Python 3 (no external packages — only the standard library: `json`, `os`, `datetime`)

## Running It

```
py main.py
```

You'll be prompted for a username and password before anything else. Three wrong attempts closes the session with a `401`. Once signed in, type a slip at the `Slip:` prompt. Type `QUIT` to leave.

## The Four Verbs

| Verb | Meaning | Example |
|---|---|---|
| `GET` | Look something up | `GET books`, `GET book 3`, `GET books borrowed` |
| `POST` | Register a new book | `POST book` — you'll be asked for a title and author |
| `PUT` | Correct an existing book's details | `PUT book 3` — asks for new title, author, status |
| `DELETE` | Remove a book for good | `DELETE book 3` — Chief Librarian only |

Anything else — a made-up verb, missing arguments, letters where a book number should be — is treated as an unreadable slip, not a crash.

## Reply Codes

| Code | Meaning | Fires when |
|---|---|---|
| 200 | Request succeeded | A GET, PUT, or DELETE completes |
| 201 | Something new was created | A POST adds a book |
| 400 | Slip could not be understood | Unknown verb, missing parts, or a non-numeric book number |
| 401 | Not signed in | Sign-in failed after three attempts |
| 403 | Signed in, but not allowed | A Member sends a DELETE |
| 404 | No matching book | A well-formed but nonexistent book number |

Every function in `logbook.py` returns `(code, message)` as a pair — nothing is printed until `main.py` receives that pair, so "every reply starts with a code" is guaranteed by how the code is shaped, not by remembering to add it in every branch.

## Staff Register

```
mrs_okafor    — Chief Librarian
bello_jr      — Member
amina_s       — Member
tunde_reads   — Member
chichi_o      — Member
baba_musa     — Member
```

Only the Chief Librarian's DELETE requests are honoured. A Member attempting DELETE gets a firm `403`.

## Persistence

Books live in `book_shelf.json`, created next to `main.py` the first time the program runs.

- **No file yet** → the program seeds itself with the ten starting books and writes them out.
- **Every successful add / edit / delete** → the updated list is saved immediately, so nothing is lost between sessions.
- **A damaged file** → if `book_shelf.json` can't be parsed as JSON, the program notices, prints a short notice, and falls back to the ten starting books instead of crashing.

Book numbers are reused once freed: deleting book 3 and later adding a new book gives that new book number 3 again, rather than always climbing upward. This is handled by `_lowest_free_number()` in `logbook.py`, which scans for the smallest number not currently in use.

## The Desk Diary (Bonus)

`record.py` appends one line per slip to `desk_diary.txt` — who sent it, what it said, what code came back, and when. The file is opened in append mode only, so old sessions are never erased.

## Design Notes

- **Permission checking is separate from the action itself.** `logbook.py`'s `delete_book()` has no idea who's asking — `main.py` calls `auth.can_perform()` first and only proceeds if that returns `True`. This means the DELETE rule could change tomorrow without editing `logbook.py` at all.
- **Validation happens before any room is called.** `main.py` checks that book numbers are actually digits before dispatching, so something like `PUT book cat` never reaches `logbook.py` in the first place.
- **Nothing prints except `main.py`.** Every other file returns data; only the window itself displays anything, which keeps "what happened" and "what the user sees" cleanly separated.

## Testing Checklist

- [x] Restart test — add or delete a book, close the program, reopen it, confirm the change is still there
- [x] First-run test — with no `book_shelf.json` present, the program starts calmly with the original ten books
- [x] Damaged-file test — corrupting `book_shelf.json` triggers a graceful reset instead of a crash
- [x] Nonsense test — unknown verbs, non-numeric book numbers, and empty slips all return 400, never a crash
- [x] Permission test — a Member's DELETE is refused with 403; the Chief Librarian's succeeds
- [x] Diary test — every slip sent in a session is appended to `desk_diary.txt` with its result