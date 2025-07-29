from time import sleep
import sys

def is_temperature_ok(temp):
    return 95 <= temp <= 102

def is_pulse_ok(pulse):
    return 60 <= pulse <= 100

def is_spo2_ok(spo2):
    return spo2 >= 90

def vitals_check(temperature, pulseRate, spo2):
    return {
        "temperature": is_temperature_ok(temperature),
        "pulse": is_pulse_ok(pulseRate),
        "spo2": is_spo2_ok(spo2)
    }

def blink_alert(duration=6):
    for _ in range(duration):
        print('\r* ', end='')
        sys.stdout.flush()
        sleep(1)
        print('\r *', end='')
        sys.stdout.flush()
        sleep(1)

def alert_if_critical(vitals_status):
    alerts = {
        "temperature": "Temperature critical!",
        "pulse": "Pulse Rate is out of range!",
        "spo2": "Oxygen Saturation out of range!"
    }
    any_alert = False
    for vital, alert_msg in alerts.items():
        if not vitals_status[vital]:
            print(alert_msg)
            blink_alert()
            any_alert = True
    return not any_alert

def vitals_ok(temperature, pulseRate, spo2):
    vitals_status = vitals_check(temperature, pulseRate, spo2)
    return alert_if_critical(vitals_status)
