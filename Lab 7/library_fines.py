"""
Library Fines - hardened version (Lab 7: fuzz testing).

Every public function validates its input and returns None for anything
invalid instead of raising, so no input can crash the program.
"""
import re

LOAN_PERIOD_DAYS = 14      # days a book may be kept without a fine
FINE_PER_DAY = 2           # fine for every day beyond the loan period
MAX_DAYS = 36500           # 100 years; larger values are data-entry errors
MAX_INPUT_LENGTH = 10_000  # reject huge inputs up front (avoids DoS / int() limits)

# [A-Za-z] and [0-9] match ASCII only, unlike str.isdigit()/\d or int(),
# which also accept "1_000", "١٢" (Arabic-Indic digits), " 7", etc.
_MEMBER_ID_RE = re.compile(r"([A-Za-z]{1,10})-([0-9]{1,9})")
_DAYS_RE = re.compile(r"[0-9]{1,6}")


def parse_member_id(member_id):
    """'STU-1023' -> ('STU', 1023). Returns None if the ID is invalid."""
    if not isinstance(member_id, str) or len(member_id) > MAX_INPUT_LENGTH:
        return None
    match = _MEMBER_ID_RE.fullmatch(member_id.strip())
    if match is None:
        return None
    member_type, number = match.groups()
    return member_type.upper(), int(number)


def total_fine(days_csv):
    """'10,20,30' -> 44 (Rs 2 per day beyond 14 days). Returns None if invalid."""
    if not isinstance(days_csv, str) or len(days_csv) > MAX_INPUT_LENGTH:
        return None
    parts = [part.strip() for part in days_csv.split(",")]
    if not all(_DAYS_RE.fullmatch(part) for part in parts):
        return None  # empty entry, negative number, letters, symbols, ...
    days = [int(part) for part in parts]
    if any(d > MAX_DAYS for d in days):
        return None
    return sum((d - LOAN_PERIOD_DAYS) * FINE_PER_DAY for d in days if d > LOAN_PERIOD_DAYS)


def shelf_code(title):
    """'Harry Potter' -> 'HP'. Returns None if the title has fewer than two usable words."""
    if not isinstance(title, str) or len(title) > MAX_INPUT_LENGTH:
        return None
    initials = []
    for word in title.split():
        # first letter/digit of the word, skipping leading punctuation like "(The)"
        first = next((ch for ch in word if ch.isalnum()), None)
        if first is None:
            continue
        upper = first.upper()
        # 'ß'.upper() == 'SS' would make the code 3 characters long; keep it as is
        initials.append(upper if len(upper) == 1 and upper.isalnum() else first)
        if len(initials) == 2:
            return "".join(initials)
    return None


def read_input(prompt):
    """input() that returns '' instead of crashing on EOF (Ctrl+Z / Ctrl+D) or Ctrl+C."""
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        print()
        return ""


def main():
    print("==== Running parse_member_id ====")
    user_input = read_input("Enter a member ID (e.g. STU-1023): ")
    result = parse_member_id(user_input)
    if result is None:
        print("Invalid member ID: expected letters, a hyphen and digits (e.g. STU-1023).")
    else:
        print("Member Type and Number:", result)

    print("\n==== Running total_fine ====")
    user_input = read_input("Enter days kept for each book as CSV (e.g. 10,20,30): ")
    result = total_fine(user_input)
    if result is None:
        print(f"Invalid input: enter whole numbers from 0 to {MAX_DAYS} separated by commas.")
    else:
        print("Total Fine:", result)

    print("\n==== Running shelf_code ====")
    user_input = read_input("Enter a book title with at least two words: ")
    result = shelf_code(user_input)
    if result is None:
        print("Invalid title: it must contain at least two words.")
    else:
        print("Shelf Code:", result)


if __name__ == "__main__":
    main()
