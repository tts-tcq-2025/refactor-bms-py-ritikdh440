"""
Feedback
1. Single data structure per vital → dictionary with keys:
   - "name": vital name
   - "value": measured value
   - "min": minimum threshold
   - "max": maximum threshold

2. Functions accept a list of such vital dictionaries.

3. alert_if_critical() → processes one vital at a time
   (One key, one object, one structure).

4. Printing logic is not hardcoded; passed in as dependency.
   Default comes from printer.py.

5. Key ordering in messages is fixed (name → value → expected range).
"""

from alerts import blink_alert
from printer import default_printer


def _tolerance(vital):
    """Return tolerance band = 1.5% of max limit."""
    return 0.015 * vital["max"]


def _classify(vital):
    """Classify vital value as OK, WARN_LOW, WARN_HIGH, LOW, HIGH."""
    val, lo, hi = vital["value"], vital["min"], vital["max"]
    tol = _tolerance(vital)

    if val < lo:
        return "LOW"
    if val > hi:
        return "HIGH"
    if lo <= val <= lo + tol:
        return "WARN_LOW"
    if hi - tol <= val <= hi:
        return "WARN_HIGH"
    return "OK"


def _render_message(vital, status):
    """
    Render a message for a vital based on its status.

    NOTE: Ordering of keys is intentional:
          name → value → expected range
    """
    base = (
        f"{vital['name']} "
        f"Value: {vital['value']} "
        f"(Expected: {vital['min']} to {vital['max']})"
    )
    if status == "LOW":
        return base + " → CRITICAL LOW"
    if status == "HIGH":
        return base + " → CRITICAL HIGH"
    if status == "WARN_LOW":
        return base + " → Approaching low"
    if status == "WARN_HIGH":
        return base + " → Approaching high"
    return None


def alert_if_critical(vitals, printer=default_printer, blinker=blink_alert):
    """
    Check all vitals and alert if any are critical.
    - Prints messages via injected printer
    - Blinks if critical
    Returns True if all vitals are OK, False otherwise.
    """
    any_alert = False
    for vital in vitals:
        status = _classify(vital)
        message = _render_message(vital, status)
        if message:
            printer(message)
        if status in ("LOW", "HIGH"):
            blinker()
            any_alert = True
    return not any_alert


def vitals_ok(vitals, printer=default_printer, blinker=blink_alert):
    """
    Entry point: Check if all vitals are OK.
    Uses alert_if_critical under the hood.
    """
    return alert_if_critical(vitals, printer, blinker)
