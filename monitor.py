""" Feedback by Mentor

1. Use a single data structure per vital: name, value, min, max
2. Pass a list of such vital dictionaries to vitals_ok()

3. Ensure alert_if_critical handles one key, one object, one structure at a time

4. Keep print logic in a separate printer.py file and inject via arguments

5. Maintain key ordering in messages: name, value, range (for clarity and consistency)

"""
from alerts import blink_alert
from printer import default_printer

def is_value_in_range(vital):
    return vital["min"] <= vital["value"] <= vital["max"]

def alert_if_critical(vitals, printer=default_printer, blinker=blink_alert):
    any_alert = False
    for vital in vitals:
        if not is_value_in_range(vital):
            message = (
                f"{vital['name']} out of range! "
                f"Value: {vital['value']} (Expected: {vital['min']} to {vital['max']})"
            )
            printer(message)
            blinker()
            any_alert = True
    return not any_alert

def vitals_ok(vitals, printer=default_printer, blinker=blink_alert):
    return alert_if_critical(vitals, printer, blinker)


