import re
from typing import Tuple

## -- Task 3 (IN3110 optional, IN4110 required) -- ##

# create array with all names of months
month_names = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]

# Creating dictionary with month names as keys and month numbers as values
# for easier substitution later
month_numbers = {name: f"{i + 1:02}" for i, name in enumerate(month_names)}


def get_date_patterns() -> Tuple[str, str, str]:
    """Return strings containing regex pattern for year, month, day
    arguments:
        None
    return:
        year, month, day (tuple): Containing regular expression patterns for each field
    """

    # Regex to capture days, months and years with numbers
    # year should accept a 4-digit number between at least 1000-2029
    year = r"(?P<year>[1-2]\d{3})"  # Will find any 4-digit number within 1000-2999

    # month should accept month names or month numbers
    all_months_string = ""
    for key, item in month_numbers.items():
        all_months_string += (
            rf"{key}|{item}|"  # Making pattern for "January|01|February|02|..."
        )
    all_months_string = all_months_string[:-1]  # Remove last | character
    month = rf"(?P<month>{all_months_string})"

    # day should be a number, which may or may not be zero-padded
    day = r"(?P<day>[0-3]?[0-9])"  # Must match days that go from 1 or 01 to 31

    return year, month, day


def convert_month(s: str) -> str:
    """Converts a string month to number (e.g. 'September' -> '09'.

    arguments:
        s (str) : month name
    returns:
        month_number (str) : month number as zero-padded string
    """
    # If already digit do nothing
    if s.isdigit():
        return s
    else:
        month_number = month_numbers[s]
    # Convert to number as string
    return month_number


def zero_pad(n: str) -> str:
    """zero-pad a number string if it is single digit
    arguments:
        n (str): String number to zero pad
    returns:
        padded_string (str) : zero padded string if it is single digit,
                              else it is returned unchanged.

    example:
        turns '2' into '02'

    """
    if len(n) == 1 and n.isdigit():
        padded_string = f"0{n}"
        return padded_string
    else:
        return n


def find_dates(text: str, output: str = None) -> list:
    """Finds all dates in a text using reg ex

    arguments:
        text (str): A string containing html text from a website.
        output (str, optional): Name of output file to save dates to.
    return:
        dates (list): A list with all the dates found
    """
    year, month, day = get_date_patterns()

    # Date on format YYYY/MM/DD - ISO
    ISO = rf"(?P<date>{year}-{month}-{day})"

    # Date on format DD/MM/YYYY
    DMY = rf"(?P<date>{day},?\s{month},?\s{year})"

    # Date on format MM/DD/YYYY
    MDY = rf"(?P<date>{month},?\s{day},?\s{year})"

    # Date on format YYYY/MM/DD
    YMD = rf"(?P<date>{year},?\s{month},?\s{day})"

    # list with all supported format pattens
    formats = [
        ISO,
        DMY,
        MDY,
        YMD,
    ]
    dates = []

    # find all dates in any format in text
    for date_pattern in formats:
        # find all dates matching current formate
        date_list = re.findall(date_pattern, text)

        if len(date_list) > 0:
            # iterating through all found dates and formate them correctly
            for date in date_list:
                # Get month from current date, convert to month number and zero pad it
                month_in_date = re.search(date_pattern, date[0]).group("month")
                month_in_date = convert_month(month_in_date)
                month_in_date = zero_pad(month_in_date)

                # Get year from current date
                year_in_date = re.search(date_pattern, date[0]).group("year")

                # Get day from current date and zero pad it
                day_in_date = re.search(date_pattern, date[0]).group("day")
                day_in_date = zero_pad(day_in_date)

                # Formatting to correct date formate
                mapping = rf"{year_in_date}/{month_in_date}/{day_in_date}"

                # Save found date with correct formate to list
                dates.append(mapping)
        else:
            continue

    # Write to file if wanted
    if output:
        with open(output, "w") as outfile:
            for date in dates:
                outfile.write(date + "\n")

    return dates
