from datetime import datetime

DIARY_FILE = "desk_diary.txt"


def log_event(username, slip, code, message):
    """Append one line to the diary. Never overwrites, only adds."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{timestamp} | {username} | slip: {slip} | reply: {code} {message}\n"
    with open(DIARY_FILE, "a") as f:
        f.write(line)