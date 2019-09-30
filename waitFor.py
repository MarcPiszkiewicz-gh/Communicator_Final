
import os
import subprocess
import time
import csv
import re
import json

progress = [ '|\r', '/\r', '-\r', '\\\r' ]
i = 0

def waitForDevice(): #Wait for device
    i = 0
    device = ''
    print("Waiting for connection...")
    while device == '':
        time.sleep(0.1)
        device = os.popen("adb devices").read().split('\n', 1)[1].split("device")[0].strip()
        print(progress[i], end = '')
        if i < 3:
            i += 1
        else:
            i = 0
    print ("\nDevice is ready.")


def waitForBoot(): #Wait for boot
    i = 0
    boot_completed = ''
    print("Waiting for boot to complete...")
    while boot_completed != '1':
        time.sleep(0.1)
        boot_completed = os.popen("adb shell getprop sys.boot_completed").read().split('\n', 1)[0]
        print(progress[i], end = '')
        if i < 3:
            i += 1
        else:
            i = 0
    print ("\nDevice is ready.")

