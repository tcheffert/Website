from datetime import datetime, date
from enum import Enum
from decimal import Decimal


class MoonPhase(Enum):
    NEW_MOON = 0
    WAXING_CRESCENT = 1
    FIRST_QUARTER = 2
    WAXING_GIBBOUS = 3
    FULL_MOON = 4
    WANING_GIBBOUS = 5
    LAST_QUARTER = 6
    WANING_CRESCENT = 7


def age(date_time: datetime) -> Decimal:
    """Calculates the age of the moon for a given date."""

    # Convert the datetime to date
    date = date_time.date()
    year = date.year
    month = date.month
    day = date.day

    if month < 3:
        year -= 1
        month += 12

    # Calculate Julian day
    a = year // 100
    b = 2 - a + a // 4
    jd = int(365.25 * (year + 4716)) + \
        int(30.6001 * (month + 1)) + day + b - 1524.5

    # Calculate days since the new moon
    days_since_new_moon = jd - 2451550.1

    return Decimal(days_since_new_moon % 29.530588853)


def phase(age: Decimal) -> MoonPhase:
    """Determines the moon phase for a given age."""
    if age < 1.84566 or age > 27.68493:
        return MoonPhase.NEW_MOON
    elif age < 5.53699:
        return MoonPhase.WAXING_CRESCENT
    elif age < 9.22831:
        return MoonPhase.FIRST_QUARTER
    elif age < 12.91963:
        return MoonPhase.WAXING_GIBBOUS
    elif age < 16.61096:
        return MoonPhase.FULL_MOON
    elif age < 20.30228:
        return MoonPhase.WANING_GIBBOUS
    elif age < 23.99361:
        return MoonPhase.LAST_QUARTER
    elif age < 27.68493:
        return MoonPhase.WANING_CRESCENT
