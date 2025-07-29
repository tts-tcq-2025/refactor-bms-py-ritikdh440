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
    if not vitals_status["temperature"]:
        print("Temperature critical!")
        blink_alert()
    if not vitals_status["pulse"]:
        print("Pulse Rate is out of range!")
        blink_alert()
    if not vitals_status["spo2"]:
        print("Oxygen Saturation out of range!")
        blink_alert()
    return all(vitals_status.values())

def vitals_ok(temperature, pulseRate, spo2):
    vitals_status = vitals_check(temperature, pulseRate, spo2)
    return alert_if_critical(vitals_status)
