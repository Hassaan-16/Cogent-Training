from dataclasses import dataclass


@dataclass
class WeatherReading:
    """data structure for holding each weather reading."""

    date: str | None
    max_temp: float | None
    min_temp: float | None
    max_humidity: float | None
    mean_humidity: float | None


@dataclass
class AverageResults:
    """data structure for holding the average calculations results"""

    average_max_temp: float | None
    average_min_temp: float | None
    average_humidity: float | None


@dataclass
class ExtremeResults:
    """results for yearly extreme values"""

    max_temp: float | None
    min_temp: float | None
    max_humidity: float | None


@dataclass
class DailyTemperature:
    """holds the chart for a single day"""

    day: int
    max_temp: float | None
    min_temp: float | None


@dataclass
class ChartResults:
    """holds the chart data for the month"""

    month_name: str
    year: str
    DailyTemperature: list[DailyTemperature]
