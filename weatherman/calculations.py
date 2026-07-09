import data_models
import calendar


def parse_float(x):
    """strips the strings, and returns as float"""
    x = str(x).strip()
    if x == "":
        return None
    try:
        return float(x)
    except ValueError:
        return None


def calculate_average_monthly(data):
    """calculate the average monthly max/min temperature and mean humidity"""
    max_temps = []
    min_temps = []
    mean_humidities = []

    for row in data:
        max_temp = parse_float(row.max_temp)
        if max_temp is not None:
            max_temps.append(max_temp)

        min_temp = parse_float(row.min_temp)
        if min_temp is not None:
            min_temps.append(min_temp)

        mean_humidity = parse_float(row.mean_humidity)
        if mean_humidity is not None:
            mean_humidities.append(mean_humidity)

    average_max_temp = sum(max_temps) / len(max_temps) if max_temps else 0.0
    average_min_temp = sum(min_temps) / len(min_temps) if min_temps else 0.0
    average_humidity = (
        sum(mean_humidities) / len(mean_humidities) if mean_humidities else 0.0
    )

    return data_models.AverageResults(
        average_max_temp, average_min_temp, average_humidity
    )


def calculate_monthly_report(data):
    """gets the monthly max temperatures, min temperatures"""
    highest_temps = []
    lowest_temps = []

    for row in data:
        max_temp = parse_float(row.max_temp)
        min_temp = parse_float(row.min_temp)
        if max_temp is not None:
            highest_temps.append(max_temp)
        if min_temp is not None:
            lowest_temps.append(min_temp)

    return highest_temps, lowest_temps


def calculate_chart_data(data):
    """Parses data into a ChartResults object for bonus mixed charts."""
    daily_temps = []
    year_str = ""
    month_name = ""

    for row in data:
        if not row.date:
            continue

        clean_date = row.date.replace("/", "-")
        parts = clean_date.split("-")

        if not year_str and len(parts) >= 3:
            year_str = parts[0]
            try:
                month_num = int(parts[1])
                month_name = calendar.month_name[month_num]
            except ValueError:
                month_name = "Unknown"

        try:
            day = int(parts[-1])
            max_t = row.max_temp if row.max_temp is not None else 0.0
            min_t = row.min_temp if row.min_temp is not None else 0.0

            daily_temps.append(data_models.DailyTemperature(day, max_t, min_t))
        except (ValueError, IndexError):
            continue

    return data_models.ChartResults(month_name, year_str, daily_temps)


def calculate_extreme_values(data):
    """gets the max temperature, min temperature and max humidity"""

    max_temps = []
    min_temps = []
    max_humidities = []

    for row in data:
        max_temp = parse_float(row.max_temp)
        if max_temp is not None:
            max_temps.append(max_temp)

        min_temp = parse_float(row.min_temp)
        if min_temp is not None:
            min_temps.append(min_temp)

        max_humidity = parse_float(row.max_humidity)
        if max_humidity is not None:
            max_humidities.append(max_humidity)

    highest = max(max_temps) if max_temps else None
    lowest = min(min_temps) if min_temps else None
    highest_humidity = max(max_humidities) if max_humidities else None

    return data_models.ExtremeResults(highest, lowest, highest_humidity)
