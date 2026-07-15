from calendar import month_abbr
from constants import (
    DATE_YEAR_INDEX,
    DATE_MONTH_INDEX,
    MONTH_FIRST_INDEX,
    MONTH_LAST_INDEX,
    FILE_NAME_FORMAT,
)


def generate_file_pattern(target_period):
    """Generates the glob search pattern from the user's target period string."""
    date_parts = target_period.split("/")
    target_year = date_parts[DATE_YEAR_INDEX]

    if len(date_parts) <= DATE_MONTH_INDEX:
        file_pattern = FILE_NAME_FORMAT.format(year=target_year, month="*")
    else:
        try:
            month_num = int(date_parts[DATE_MONTH_INDEX])

            if not MONTH_FIRST_INDEX <= month_num <= MONTH_LAST_INDEX:
                print(
                    f"Error: Invalid month '{month_num}'. Please use a value between 1 and 12."
                )

                return None

            month_abbreviation = month_abbr[month_num]
            file_pattern = FILE_NAME_FORMAT.format(
                year=target_year, month=month_abbreviation
            )

        except ValueError:
            print(f"Error: Invalid month format in '{target_period}'.")

            return None

    return file_pattern
