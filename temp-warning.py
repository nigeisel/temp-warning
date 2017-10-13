import subprocess
import re
import time
import os
import argparse

CURSOR_UP = '\x1b[1A'
ERASE_LINE = '\x1b[2K'

parser = argparse.ArgumentParser(description='Alarm if temp is too high.')
parser.add_argument('-t', dest='CRITICAL_TEMP', metavar='temperature', type=int, help='temperature that is considered critical in °C', default=92)
parser.add_argument('-i', dest='INTERVAL', metavar='interval', type=int, help='interval to check temp in s', default=5)
parser.add_argument('-b', dest='BEEP', action='store_const', const=True, default=False, help='activate beep on crit temp (default: no beep)')
parser.add_argument('-l', dest='LOG', action='store_const', const=False, default=True, help='deprecated')

args = parser.parse_args()
BEEP, CRITICAL_TEMP, INTERVAL, LOG = args.BEEP, args.CRITICAL_TEMP, args.INTERVAL, args.LOG

if CRITICAL_TEMP < 80 or CRITICAL_TEMP > 110:
    print("Check critical temperature setting. Should be between 80°C and 110°C")
if INTERVAL < 2:
    print("INTERVAL set to 2 as this in minimum")
    INTERVAL = 2

GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'

def colored_text(text, color):
    ENDCOLOR = '\033[0m'
    return color + text + ENDCOLOR

def delete_last():
    print(CURSOR_UP + ERASE_LINE + CURSOR_UP)

def beep():
    duration = 0.1  # second
    freq = 1000  # Hz
    os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (duration, freq))

FIRST = True
while True:
    #sensors_result = subprocess.run(['sensors'], stdout=subprocess.PIPE).stdout.decode("utf-8")
    #found = re.search('id 0:  \+(.+?)°', sensors_result)
    #tempString = found.group(1)

    with open('/sys/class/thermal/thermal_zone0/temp', 'r') as temp_file:
        tempString = temp_file.read()

    try:
        temp = float(tempString) / 1000.0

        if not FIRST:
            delete_last()

        if temp > CRITICAL_TEMP:
            print("Temperature: ", colored_text(str(temp), RED), "°C", colored_text("CRITICAL!", RED))
            if BEEP:
                beep()
        elif temp > CRITICAL_TEMP - 5:
            print("Temperature: ", colored_text(str(temp), YELLOW), "°C")
        else: #elif LOG:
            print("Temperature: ", colored_text(str(temp), GREEN), "°C")

    except ValueError:
        print("ERROR: couldnt convert parsed temperature")

    time.sleep(INTERVAL)
    FIRST = False
