
import math


def verify_isbn10_format(isbn_str):
    # Validate input type
    if not isinstance(isbn_str, str):
        return None

    # Remove hyphens and surrounding spaces
    cleaned = isbn_str.replace('-', '').strip()

    # ISBN-10 must contain exactly 10 characters
    if len(cleaned) != 10:
        return None

    # First nine characters must be digits
    if not cleaned[:9].isdigit():
        return None

    # Last character must be a digit or X
    check_char = cleaned[9].upper()
    if not (check_char.isdigit() or check_char == 'X'):
        return None

    first_digit = int(cleaned[0])
    group_code = cleaned[1:4]

    return f"Group {group_code}: Starts {first_digit}, Checksum {check_char}"


def calculate_depreciation_factor(book_age_str):
    # Validate input type
    if not isinstance(book_age_str, str):
        return None

    try:
        parts = book_age_str.split('/')

        # Exactly two values are required
        if len(parts) != 2:
            return None

        age = float(parts[0])
        life = float(parts[1])

        # Reject NaN and infinite values
        if not math.isfinite(age) or not math.isfinite(life):
            return None

        # Age cannot be negative and lifespan must be positive
        if age < 0 or life <= 0:
            return None

        depreciation = 1.0 - (age / life)

        return round(max(0.1, depreciation), 2)

    except (ValueError, OverflowError):
        return None


def lookup_condition_multiplier(condition_code):
    # Validate input type
    if not isinstance(condition_code, str):
        return None

    grade = condition_code.strip().upper()

    multipliers = {
        "MINT": 1.25,
        "LIKE_NEW": 1.00,
        "VERY_GOOD": 0.80,
        "GOOD": 0.60,
        "POOR": 0.30
    }

    # Safely handle unknown conditions
    return multipliers.get(grade)


def main():
    print("==== Running verify_isbn10_format ====")
    isbn_in = input("Enter ISBN-10 (e.g. 0-306-40615-2): ")
    print(verify_isbn10_format(isbn_in))

    print("\n==== Running calculate_depreciation_factor ====")
    age_in = input("Enter age/lifespan in years (e.g. 3/10): ")
    print("Depreciation Factor:", calculate_depreciation_factor(age_in))

    print("\n==== Running lookup_condition_multiplier ====")
    cond_in = input("Enter condition (e.g. MINT, GOOD, POOR): ")
    print("Multiplier:", lookup_condition_multiplier(cond_in))


if __name__ == "__main__":
    main()
