from calendar import month_abbr

from constants import (
    DATE_MONTH_INDEX,
    DATE_YEAR_INDEX,
    FILE_NAME_FORMAT,
    MONTH_FIRST_INDEX,
    MONTH_LAST_INDEX,
)


def _extract_date_parts(target_period):
    """Extracts the year and optional month from the period string."""
    date_parts = target_period.split("/")
    target_year = date_parts[DATE_YEAR_INDEX]

    if len(date_parts) <= DATE_MONTH_INDEX:
        return target_year, None

    return target_year, date_parts[DATE_MONTH_INDEX]


def _get_month_abbreviation(month_string, full_target_period):
    """Validates the month and converts it to its calendar abbreviation."""
    try:
        month_num = int(month_string)
    except ValueError:
        print(f"Error: Invalid month format in '{full_target_period}'.")

        return None

    if not MONTH_FIRST_INDEX <= month_num <= MONTH_LAST_INDEX:
        print(
            f"Error: Invalid month '{month_num}'. Please use a value between 1 and 12."
        )

        return None

    return month_abbr[month_num]


def generate_file_pattern(target_period):
    """Generates the glob search pattern from the user's target period string."""
    target_year, target_month = _extract_date_parts(target_period)

    if not target_month:
        return FILE_NAME_FORMAT.format(year=target_year, month="*")

    month_abbreviation = _get_month_abbreviation(target_month, target_period)

    if not month_abbreviation:
        return None

    return FILE_NAME_FORMAT.format(year=target_year, month=month_abbreviation)
