import sys
from time import sleep

def blink_alert(duration=6):
    for _ in range(duration):
        print('\r* ', end='')
        sys.stdout.flush()
        sleep(1)
        print('\r *', end='')
        sys.stdout.flush()
        sleep(1)
