# Communicator Post-Flash Tests
# Version 1.1
# Marc Piszkiewicz
# Guardhat, Inc.

import os
import subprocess
import datetime
import time
import csv
import waitFor
import glob
import os.path
import re
from os import path

#from adb.client import Client as AdbClient

print()
print("Start adb server.")
subprocess.call(r"adb start-server")

# 1 - Power on Hat

print()
print("Before testing begins:")
print("1. Cover TOF sensor")
print("2. Press power button until blue Status LED blinks and wait for \"Guardhat is now ready.\" voice prompt.")
print()
print("Starting adb server")
subprocess.call(r"adb start-server")

def convert(seconds): 
    min, sec = divmod(seconds, 60) 
    hour, min = divmod(min, 60) 
    return "%dhr %02dmin %02dsec" % (hour, min, sec)

os.chdir(r"c:\Code\GUID")

# Check for valid serial number in .csv file - Return HW MAC from *GUID*.csv  Add code from Reflash program to retrieve MAC 
myfile = open("COMMUNICATOR_GUID.csv", "rt") # Future: pass GUIDS file as a variable
contents = myfile.read()

# Check for valid serial number in .csv file - Return HW MAC from *GUID*.csv  Add code from Reflash program to retrieve MAC 
validSN = -1
guid = ''
while validSN == -1:
    print()
    print("Press CTRL-C to abort test at any time.")
    print()
    serial = input('Enter serial number: ')
    validSN = contents.find(serial)
    if validSN != -1: # add check for valid GUID
        with open('COMMUNICATOR_GUID.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            for row in csv_reader:
                if row["Serial"] == serial:
                    WiFiMAC = str({row["WiFiMAC"]}).strip("{}' ")
                    validMAC = len(WiFiMAC) # valid IP addresses are between 7 and 15 characters long
                    guid = str({row["GUID"]}).strip("{}'") # passed through to log file
                    ModemType = str({row["ModemType"]}).strip("{}'")
                line_count += 1
            #Check GUID here
            if len(guid) != len("3bd68210-2a89-4030-897c-76f43e0bab50"): # check that GUID is correct length.
                print("Cannot find GUID")
                validSN = -1
    if validSN == -1: # add check for valid GUID
        print("Invalid serial number")

# Check for IP address

validIP = False

if validMAC == 17:# check for valid IP addresses
    print("Check Wi-Fi hotspot for IP address corresponding to Physical Address(MAC) = "+ WiFiMAC)
else:
    print("Check Wi-Fi hotspot for IP address.  Physical Address(MAC) not stored.  Device might not be flashed.")

modemInput = -1 # Check for valid modem type
if ( ModemType != 'WP' and ModemType != 'HL' ):
    print('Modem Type not found - please enter')
    while modemInput == -1:
        modemInput = int(input('1 for HLxxxx or  2 for WPxxxx: '))
        if (modemInput == 1):
            ModemType = 'HL'
        elif (modemInput == 2):
            ModemType = 'WP'
        else:
            modemInput = -1
            print('Invalid response.')
        

#Manual IP address entry
IPaddr = ''
cannot = -1
while validIP == False:
    print()
    while IPaddr == '':
        IPaddr = input ("Enter Hat IP address: ")
        if IPaddr == '':
            print("Invalid IP address.")
        
    connectList = [ 'adb connect ', IPaddr, ':5123']
    connectCommand = ''.join(connectList)
    cannot = os.popen(connectCommand).read().find("cannot")
    print(cannot)
    if cannot == -1:
        validIP = True
    else:
        print()
        print("Invalid IP address.")
        validIP = False
        IPaddr = ''
        
disconnectList = [ 'adb disconnect ', IPaddr, ':5123']
disconnectCommand = ''.join(disconnectList)

# Start the clock 
stopwatchStart = time.strftime("%a %b %d %H:%M:%S %Y")    #timestamp for log file
stopwatchStart2 = time.perf_counter()                     #start time for time elapsed


#Battery voltage check
print()
print("Checking battery voltage...")
print()

# No error checking - waits for response:
response = os.popen("adb shell logcat -e voltage: -m 1").read()

# Error checking, allows non-measurement:
#response = os.popen("adb shell logcat -e voltage: -d").read()

responseOK = response.find( "voltage:" )
if responseOK != -1:
    battVoltage = float(response.split( "voltage:" )[1].split('\n')[0].strip()) / 1000
    print("Battery is at " + str(battVoltage) + "V")
    print()
else:
    print( 'Cannot read battery voltage.' )
    battVoltage = 999.999999

#
print()
print ("Cover TOF sensor on the back of the brim.")

# LED Test

print()
print ("LED Test...")
print('Clearing LEDs')
os.popen('adb shell \"echo none > /sys/class/leds/R_2-0030/trigger\"')
os.popen('adb shell \"echo none > /sys/class/leds/G_2-0030/trigger\"')
os.popen('adb shell \"echo none > /sys/class/leds/B_2-0030/trigger\"')
os.popen('adb shell \"echo none > /sys/class/leds/R_2-0031/trigger\"')
os.popen('adb shell \"echo none > /sys/class/leds/G_2-0031/trigger\"')
os.popen('adb shell \"echo none > /sys/class/leds/B_2-0031/trigger\"')
os.popen('adb shell \"echo none > /sys/class/leds/R_2-0032/trigger\"')
os.popen('adb shell \"echo none > /sys/class/leds/G_2-0032/trigger\"')
os.popen('adb shell \"echo none > /sys/class/leds/B_2-0032/trigger\"')
os.popen('adb shell \"echo none > /sys/class/leds/R_2-0033/trigger\"')
os.popen('adb shell \"echo none > /sys/class/leds/G_2-0033/trigger\"')
os.popen('adb shell \"echo none > /sys/class/leds/B_2-0033/trigger\"')
os.popen('adb shell \"echo none > /sys/class/leds/red/trigger\"')
os.popen('adb shell \"echo none > /sys/class/leds/green/trigger\"')
os.popen('adb shell \"echo none > /sys/class/leds/blue/trigger\"')
os.popen('adb shell \"echo 0 > /sys/class/leds/R_2-0030/brightness\"')
os.popen('adb shell \"echo 0 > /sys/class/leds/G_2-0030/brightness\"')
os.popen('adb shell \"echo 0 > /sys/class/leds/B_2-0030/brightness\"')
os.popen('adb shell \"echo 0 > /sys/class/leds/R_2-0031/brightness\"')
os.popen('adb shell \"echo 0 > /sys/class/leds/G_2-0031/brightness\"')
os.popen('adb shell \"echo 0 > /sys/class/leds/B_2-0031/brightness\"')
os.popen('adb shell \"echo 0 > /sys/class/leds/R_2-0032/brightness\"')
os.popen('adb shell \"echo 0 > /sys/class/leds/G_2-0032/brightness\"')
os.popen('adb shell \"echo 0 > /sys/class/leds/B_2-0032/brightness\"')
os.popen('adb shell \"echo 0 > /sys/class/leds/R_2-0033/brightness\"')
os.popen('adb shell \"echo 0 > /sys/class/leds/G_2-0033/brightness\"')
os.popen('adb shell \"echo 0 > /sys/class/leds/B_2-0033/brightness\"')
os.popen('adb shell \"echo 0 > /sys/class/leds/red/brightness\"')
os.popen('adb shell \"echo 0 > /sys/class/leds/green/brightness\"')
os.popen('adb shell \"echo 0 > /sys/class/leds/blue/brightness\"')

print('Blue Membrane LEDs - all four (4) should light in sequence.')

keypress = input('Press ENTER to start the sequence.')

delay = 0.1
i = 0
while i < 10:
    os.popen('adb shell \"echo 200 > /sys/class/leds/B_2-0030/brightness\"')
    os.popen('adb shell \"echo 200 > /sys/class/leds/B_2-0031/brightness\"')
    os.popen('adb shell \"echo 200 > /sys/class/leds/B_2-0032/brightness\"')
    time.sleep(delay)
    os.popen('adb shell \"echo 0 >   /sys/class/leds/B_2-0030/brightness\"')
    os.popen('adb shell \"echo 200 > /sys/class/leds/B_2-0033/brightness\"')
    time.sleep(delay)
    os.popen('adb shell \"echo 0 >   /sys/class/leds/B_2-0031/brightness\"')
    os.popen('adb shell \"echo 200 > /sys/class/leds/B_2-0030/brightness\"')
    time.sleep(delay)
    os.popen('adb shell \"echo 0 >   /sys/class/leds/B_2-0032/brightness\"')
    os.popen('adb shell \"echo 200 > /sys/class/leds/B_2-0031/brightness\"')
    time.sleep(delay)
    os.popen('adb shell \"echo 0 >   /sys/class/leds/B_2-0033/brightness\"')
    os.popen('adb shell \"echo 200 > /sys/class/leds/B_2-0032/brightness\"')
    time.sleep(delay)
    i += 1

os.popen('adb shell \"echo 0 > /sys/class/leds/B_2-0030/brightness\"')
os.popen('adb shell \"echo 0 > /sys/class/leds/B_2-0031/brightness\"')
os.popen('adb shell \"echo 0 > /sys/class/leds/B_2-0032/brightness\"')
os.popen('adb shell \"echo 0 > /sys/class/leds/B_2-0033/brightness\"')

keypress = input('Press ENTER to continue.')

print('Green Membrane LEDs - all four (4) should light.')

os.popen('adb shell \"echo 200 > /sys/class/leds/G_2-0030/brightness\"')
os.popen('adb shell \"echo 200 > /sys/class/leds/G_2-0031/brightness\"')
os.popen('adb shell \"echo 200 > /sys/class/leds/G_2-0032/brightness\"')
os.popen('adb shell \"echo 200 > /sys/class/leds/G_2-0033/brightness\"')

keypress = input('Press ENTER to continue.')

os.popen('adb shell \"echo 0 > /sys/class/leds/G_2-0030/brightness\"')
os.popen('adb shell \"echo 0 > /sys/class/leds/G_2-0031/brightness\"')
os.popen('adb shell \"echo 0 > /sys/class/leds/G_2-0032/brightness\"')
os.popen('adb shell \"echo 0 > /sys/class/leds/G_2-0033/brightness\"')

print('Red Membrane LEDs - all four (4) should light.')

os.popen('adb shell \"echo 200 > /sys/class/leds/R_2-0030/brightness\"')
os.popen('adb shell \"echo 200 > /sys/class/leds/R_2-0031/brightness\"')
os.popen('adb shell \"echo 200 > /sys/class/leds/R_2-0032/brightness\"')
os.popen('adb shell \"echo 200 > /sys/class/leds/R_2-0033/brightness\"')

keypress = input('Press ENTER to continue.')

os.popen('adb shell \"echo 0 > /sys/class/leds/R_2-0030/brightness\"')
os.popen('adb shell \"echo 0 > /sys/class/leds/R_2-0031/brightness\"')
os.popen('adb shell \"echo 0 > /sys/class/leds/R_2-0032/brightness\"')
os.popen('adb shell \"echo 0 > /sys/class/leds/R_2-0033/brightness\"')

os.popen('adb shell \"echo 0 > /sys/class/leds/B_2-0030/brightness\"')
os.popen('adb shell \"echo 0 > /sys/class/leds/B_2-0031/brightness\"')
os.popen('adb shell \"echo 0 > /sys/class/leds/B_2-0032/brightness\"')
os.popen('adb shell \"echo 0 > /sys/class/leds/B_2-0033/brightness\"')
os.popen('adb shell \"echo 0 > /sys/class/leds/G_2-0030/brightness\"')
os.popen('adb shell \"echo 0 > /sys/class/leds/G_2-0031/brightness\"')
os.popen('adb shell \"echo 0 > /sys/class/leds/G_2-0032/brightness\"')
os.popen('adb shell \"echo 0 > /sys/class/leds/G_2-0033/brightness\"')
os.popen('adb shell \"echo 0 > /sys/class/leds/R_2-0030/brightness\"')
os.popen('adb shell \"echo 0 > /sys/class/leds/R_2-0031/brightness\"')
os.popen('adb shell \"echo 0 > /sys/class/leds/R_2-0032/brightness\"')
os.popen('adb shell \"echo 0 > /sys/class/leds/R_2-0033/brightness\"')

print('Violet Neighbor LEDs both should light.')

os.popen('adb shell \"echo 40 > /sys/class/leds/blue/brightness\"')
os.popen('adb shell \"echo 40 > /sys/class/leds/green/brightness\"')
os.popen('adb shell \"echo 40 > /sys/class/leds/red/brightness\"')

keypress = input('Press ENTER to continue.')

print('Clearing LEDs')

os.popen('adb shell \"echo 0 > /sys/class/leds/blue/brightness\"')
os.popen('adb shell \"echo 0 > /sys/class/leds/green/brightness\"')
os.popen('adb shell \"echo 0 > /sys/class/leds/red/brightness\"')

#log result

print()

LEDlog = 'NULL' #this will be logged
LEDtested = False # default to enter while loop
LEDPassFail = -1

while LEDtested == False:  
    
    if LEDPassFail == -1: # prompt
        LEDPassFailIn = input( 'Did all LEDs work? (Y/N)' ).lower().strip()
        if len(LEDPassFailIn) == 1:
            LEDPassFail = ord(LEDPassFailIn[0])
        else:
            LEDPassFail = 0
    
    if LEDPassFail == 121: # 'y' response
        LEDlog = 'P' #P for Pass
        LEDtested = True
        
    elif LEDPassFail == 110: # 'n' response
        LEDlog = 'F' #F for Fail
        LEDtested = True

    else: # any other responses
        print('Invalid response')
        LEDPassFail = -1

#Button Tests
os.popen("adb shell logcat -c")

# logcat -e for the following:
#

buttons = [
    'Volume Down Button',
    'Volume Up Button',
    'Call Button',
    'SOS Button',
    'Status Button',
    'PTT Mic Button',
    'PTT CHP Button',
    'Power Button',
    'Pic Button'
    ]

keyCodes = [
    'keyCode=KEYCODE_VOLUME_DOWN,',
    'keyCode=KEYCODE_VOLUME_UP,',
    'keyCode=KEYCODE_BUTTON_GUARDHAT_CAL,',
    'keyCode=KEYCODE_BUTTON_GUARDHAT_SOS,',
    'keyCode=KEYCODE_BUTTON_GUARDHAT_STATUS,',
    'keyCode=KEYCODE_BUTTON_GUARDHAT_PTT,',
    'keyCode=KEYCODE_BUTTON_GUARDHAT_CHP,',
    'keyCode=KEYCODE_POWER,',
    'keyCode=KEYCODE_BUTTON_GUARDHAT_PIC,',
]

buttonOK = [
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
]
# Press all the buttons!
os.popen("adb shell logcat -c")

buttonRetry = True
firstTime = True

while (buttonRetry == True):
    if firstTime == True:
        print()
        print('Press all buttons on the hat at least once.')
        
    print()    
    keypress = input('Press ENTER to continue.')
    print()
    i = 0
    for button in buttons:
        if buttonOK [ i ] == False:
            response = os.popen("adb shell logcat -e " + keyCodes[ i ] + " -d").read().find( keyCodes[ i ] )
        else:
            response = 1
            
        if response != -1:
            print('Detected.......... ' + buttons[ i ])
            buttonOK [ i ] = True
        else:
            print('Did not detect.... ' + buttons[ i ])
            # Do nothing - do not overwrite previous True
        i += 1 
    
#    print(buttonOK)
    
    buttonFails = 0
    for element in buttonOK:
        if element == False:
            buttonFails += 1
    
#    print('buttonFails =      ' + str(buttonFails))    
    
    if buttonFails == 0:
        buttonLog = 'P'
        buttonRetry = False
    else:
        print()
        print('Did not detect all buttons')
        buttonPassFail = -1
        print()
        buttonRetryIn = input( 'Retry Test? (Y/N)' ).lower().strip()
        if len(buttonRetryIn) == 1:
            buttonPassFail = ord(buttonRetryIn[0])
        else:
            buttonPassFail = 0
            
        if buttonPassFail == 121: # 'y' response
            buttonRetry = True
            # print button that need retest
            print()
            i = 0
            for elem in buttonOK:
                if elem == False:
                    print('Press the', buttons[ i ])
                i += 1
            
        elif buttonPassFail == 110: # 'n' response
            buttonLog = 'F' #F for Fail
            buttonRetry = False
            
        else: # any other responses
            print('Invalid response')
            buttonPassFail = -1
            buttonRetry = True
    
    firstTime = False

# Speaker Tests
SpeakerLog = 'NULL'
SpeakerTested = False
SpeakerPassFail = -1

print()
print("Cover the right speaker next to the Volume Down button with your hand tight against the brim, then press the status button.")
print()
keypress = input('Press ENTER to continue.')
print()
print("Cover the left speaker next to the Power button with your hand tight against the brim, then press the status button.")
print()
keypress = input('Press ENTER to continue.')
print()

while SpeakerTested == False:  
    if SpeakerPassFail == -1: # prompt
        SpeakerPassFailIn = input( 'Did both Speakers work? (Y/N)' ).lower().strip()
        if len(SpeakerPassFailIn) == 1:
            SpeakerPassFail = ord(SpeakerPassFailIn[0])
        else:
            SpeakerPassFail = 0
    
    if SpeakerPassFail == 121: # 'y' response
        SpeakerLog = 'P' #P for Pass
        SpeakerTested = True
        
    elif SpeakerPassFail == 110: # 'n' response
        SpeakerLog = 'F' #F for Fail
        SpeakerTested = True

    else: # any other responses
        print('Invalid response')
        SpeakerPassFail = -1
        
# Camera - Video

# Change Upload parameter

os.chdir(r"c:\Communicator_Final")
os.popen("adb push DeviceConfig.json /data/data/com.guardhat.saturn/")

print()
print('Press and hold Status button [O] until IP address message is read out from the hat.')
print()
keypress = input('Press ENTER after you hear the IP address message.')

# Kill Saturn app
ps = os.popen("adb shell \"ps | grep saturn\"").read().split()[1]
os.popen("adb shell kill " + ps)

stop = False
while stop == False: # check that saturn process is totally dead.
    time.sleep(1)
    ps = os.popen("adb shell \"ps | grep saturn\"").read()
    if len(ps) == 0:
        stop = True
    else:
        stop = False
time.sleep(2)        

# Re-start Saturn app
os.popen("adb shell am start -n com.guardhat.saturn/.TaskControllerActivity")
print()
print('Wait for \"Ready\" prompt.')
print()
keypress = input('Press ENTER to continue.')

os.chdir(r"c:\Communicator_Final")
os.popen("del /q files")

#HTML Template
pageTemplatePhotosBegin =  " \
<!DOCTYPE html> \
<html> \
<body> \
<h2>Images Found on DUT</h2>"

pageTemplateVideosBegin = " \
<!DOCTYPE html> \
<html> \
<body> \
<h2>Videos Found on DUT</h2>"

pageTemplatePhotoFile = "<h2>No images found on DUT</h2>"
pageTemplateVideoFile = "<h2>No videos found on DUT</h2>"

pageTemplateEnd = " \
</body> \
</html> "

#Remove extraneous files on DUT
os.chdir(r"c:\Communicator_Final")
os.popen("adb shell rm -r -f /storage/emulated/0/Android/data/com.guardhat.saturn/files/*")

Tested = False
retry = -1
i = 0

os.chdir(r"c:\Communicator_Final")

DoneFileTest = 0
MP4FileTest = 0
Tested = False
retry = -1
i = 0

while Tested == False:
    print()
    print("Hold the Camera Button until you hear, \"Video recording starting.\"")
    print()
    keypress = input('Press ENTER to continue.')

    print()
    print("Hold the Camera Button until you hear, \"Video recording ending.\"")
    print()
    keypress = input('Press ENTER to continue.')
    
    # Loop up to 10 times while there there is no .mp4 file or no .done file
    while ((i < 10) and (DoneFileTest == 0)):
        time.sleep(1)
        DoneFiles = os.popen("adb shell ls /storage/emulated/0/Android/data/com.guardhat.saturn/files/*.mp4.done").read()
        DoneFileTest = len(DoneFiles)
        i += 1

    if DoneFileTest == 0:
        print('No MP4 files found.')
        retryIn = input('Retry test (Y/N)').lower().strip()
        if len(retryIn) >= 1:
            retry = ord(retryIn[0])
        else:
            retry = 0
        if retry == 121: # 'y' response
            Tested = False
            i = 0 # Reset the inner while loop
            DoneFileTest = 0
        elif retry == 110: # 'n' response
            Tested = True
        else: # any other responses
            print('Invalid response')
            Tested = False
            i = 0 # Reset the inner while loop
            DoneFileTest = 0
    
    else: # any other responses
        print('MP4 files found')
        Tested = True
        os.popen("adb pull /storage/emulated/0/Android/data/com.guardhat.saturn/files/")
        
os.chdir(r"c:\Communicator_Final")
os.popen("adb pull /storage/emulated/0/Android/data/com.guardhat.saturn/files/")
time.sleep(2)

os.chdir(r"c:\Communicator_Final\files")
#os.popen("del /q *done")
#time.sleep(2)

# Generate html file here

f = open("c:\\Communicator_Final\\files\\video.html", "w")
f.write(str(pageTemplateVideosBegin))

# Get .mp4 files
count = 0
for f_name in os.listdir('c:\\Communicator_Final\\files'):
    if f_name.endswith('.mp4'):
        videoFile = str(f_name)
        f.write('<video width=\"500\" height=\"333\" controls>')
        pageTemplateVideoFile = "<source src = \"" + videoFile + "\" type=\"video/mp4\"> </video> <p></p>" 
        f.write(str(pageTemplateVideoFile))
        count += 1
if count < 1:
    f.write(str(pageTemplateVideoFile))
    
f.write(str(pageTemplateEnd))

f.close()

if count > 0:
    
    os.chdir(r"c:\ ")
    os.popen("start chrome.exe file://c:/Communicator_Final/files/video.html")
    
    keypress = input('Check video for image and sound in Chrome Browser window, then close Chrome window.  Press ENTER to continue.')
    print()
    
    VideoLog = 'NULL' #this will be logged
    VideoTested = False # default to enter while loop
    VideoPassFail = -1
    
    while VideoTested == False:
        
        if VideoPassFail == -1: # prompt
            VideoPassFailIn = input( 'Is the video OK? (Y/N)' ).lower().strip()
            if len(VideoPassFailIn) == 1:
                VideoPassFail = ord(VideoPassFailIn[0])
            else:
                VideoPassFail = 0
                    
            if VideoPassFail == 121: # 'y' response
                VideoLog = 'P' #P for Pass
                VideoTested = True
                        
            elif VideoPassFail == 110: # 'n' response
                VideoLog = 'F' #F for Fail
                VideoTested = True
                            
            else: # any other responses
                print('Invalid response')
                VideoPassFail = -1
                                
else:
    VideoLog = 'F' #F for Fail

os.popen("adb shell rm -r -f /storage/emulated/0/Android/data/com.guardhat.saturn/files/*")

os.chdir(r"C:\Code\App")
os.popen("adb push DeviceConfig.json /data/data/com.guardhat.saturn/")

print()
print('Press and hold Status button [O] until IP address message is read out from the hat.')
print()
keypress = input('Press ENTER after you hear the IP address message.')

# Kill Saturn app
ps = os.popen("adb shell \"ps | grep saturn\"").read().split()[1]
os.popen("adb shell kill " + ps)

stop = False
while stop == False: # check that saturn process is totally dead.
    time.sleep(1)
    ps = os.popen("adb shell \"ps | grep saturn\"").read()
    if len(ps) == 0:
        stop = True
    else:
        stop = False
time.sleep(2)

# Re-start Saturn app
os.popen("adb shell am start -n com.guardhat.saturn/.TaskControllerActivity")
print()
print('Wait for \"Ready\" prompt.')
print()
keypress = input('Press ENTER to continue.')


#SD card
os.chdir(r"c:\Communicator_Final")

print("Checking for uSD card")

uSDlog = ''
uSD_present = ''
uSD_present = os.popen("adb shell ls /storage").read().split('\n')[0].strip('emulatedself')
print(uSD_present)
if uSD_present != '':
    print("uSD is present")
    uSDlog = 'P'
    path = "/storage/" + uSD_present + "/"
#    print(path)
    os.popen( "adb push loremImpsum.txt " + path )
    time.sleep(2)
    readCard = os.popen( "adb shell cat " + path + "loremImpsum.txt").read()
    print("Text file uploaded to uSD card:")
    print(readCard, end = '')
    os.popen( "adb shell rm " + path + "loremImpsum.txt" )

else:
    print()
    print("uSD card is missing.")
    print()
    uSDlog = 'F'

print()
print()

#NFC card

#NFCretry = True
#
#while (NFCretry == True):
#    print()
#    print("Hold NFC card against shell side of Call button")
#    print()
#    os.popen("adb shell logcat -c")
#    NFCevent = -1
#    key = input('Press ENTER after you hear a voice prompt, or if there is no response at all.')
#    NFCevent = os.popen("adb shell logcat -e NFCManager -d").read().find("NFCManager")
#    print()
#    if NFCevent != -1:
#        print('NFC swipe detected')
#        NFClog = 'P'
#        NFCretry = False
#    else:
#        print('Did not detect NFC swipe')
#        NFCPassFail = -1
#        NFCretryIn = input( 'Retry Test? (Y/N)' ).lower().strip()
#        if len(NFCretryIn) == 1:
#            NFCPassFail = ord(NFCretryIn[0])
#        else:
#            NFCPassFail = 0
#            
#        if NFCPassFail == 121: # 'y' response
#            NFCretry = True
#            
#        elif NFCPassFail == 110: # 'n' response
#            NFClog = 'F' #F for Fail
#            NFCretry = False
#
#        else: # any other responses
#            print('Invalid response')
#            NFCPassFail = -1
#            NFCretry = True
#    
#
#print("NFC card swipe Test Result: " + NFClog)

#Sensor & Position Board

measParam = [
    "Temperature  : ",
    "Humidity     : ",
    "Pressure     : ",
    "Noise        : ",
    "HatWorn      : ",
    "Acceleration : "
    ]

searchString = [
    "ReceiveMessageSM.*Temperature",
    "ReceiveMessageSM.*Humidity",
    "ReceiveMessageSM.*Pressure",
    "ReceiveMessageSM.*Noise",
    "ReceiveMessageSM.*HatWorn",
    "Calculated.*Acceleration"
    ]

splitString = [
    "(Temperature) : ",
    "(Humidity) : ",
    "(Pressure) : ",
    "(Noise) : ",
    "(HatWorn) : ",
    "Calculated Acceleration:"
    ]

sensorData = [
    999.999999,
    999.999999,
    999.999999,
    999.999999,
    999.999999,
    999.999999
    ]

os.popen("adb shell logcat -c")
#time.sleep(1) # sleep required for logcat to accumulate data
time.sleep(2) # sleep required for logcat to accumulate data

# Loop to check measurements
i = 0
for measure in measParam:
    response = os.popen("adb shell logcat -e " + searchString[ i ] + " -d").read()
    responseOK = response.find( splitString[ i ] )
    if (responseOK != -1):
        sensorData[ i ] = response.split( splitString[ i ] )[1].split('\n')[0].strip()
        print( 'Detected ' + measure + " " + str(sensorData[ i ]))
    else:
        print( 'Did not detect ' + measure )
    i += 1

# Write out measurements
Temperature   = sensorData[ 0 ]
Humidity      = sensorData[ 1 ]
Pressure      = sensorData[ 2 ]
Noise         = sensorData[ 3 ]
HatWornClosed = sensorData[ 4 ]
Acceleration  = sensorData[ 5 ]

# Repeat logcat for HatWorn with sensor covered

print()
print("Remove cover from TOF sensor")
print()
keypress = input('Press ENTER to continue.')
os.popen("adb shell logcat -c")
time.sleep(1) # sleep required for logcat to accumulate data

response = os.popen("adb shell logcat -e " + searchString[ 4 ] + " -d").read()
responseOK = response.find( splitString[ 4 ] )
if responseOK != -1:
    HatWornOpen = response.split( splitString[ 4 ] )[1].split('\n')[0].strip()
    print( 'Detected ' + measParam[ 4 ] + " " + str(sensorData[ 4 ]))
else:
    HatWornOpen = 999.999999
    print( 'Did not detect ' + measParam[ 4 ] )
    

if int(HatWornClosed) == 1 or int(HatWornClosed) == 2:
    HatWornClosedLog = 'P'
else:
    HatWornClosedLog = 'F'

if int(HatWornOpen) == 0:
    HatWornOpenLog = 'P'
else:
    HatWornOpenLog = 'F'
   
# SIM/Modem checks
modemDetect = -1
SIMerror = -1
SIMdetected = -1
networkDetect = -1
i = 0

progress = [ '|\r', '/\r', '-\r', '\\\r' ]

modemDetect = os.popen("adb shell lsusb").read()
if len(modemDetect) == 0:
    print()
    print("Modem not detected.  Verify S1710 is OFF.")
    ModemDetectLog = 'F'
else:
    print()
    print("Modem detected.")
    ModemDetectLog = 'P'

if (ModemType == 'WP' and ModemDetectLog == 'P'): #WP
    os.popen("adb shell su")
    os.popen("adb shell stop ril-daemon-qmi")
    os.popen("adb shell logcat -c")
    os.popen("adb shell start ril-daemon-qmi")
elif ModemDetectLog == 'P': #                 #HL
    os.popen("adb shell su")
    os.popen("adb shell stop ril-daemon-hl")
    os.popen("adb shell logcat -c")
    os.popen("adb shell start ril-daemon-hl")

SIMdetectLog = 'F'
j = 0
while SIMerror == -1 and SIMdetected == -1 and j < 10:
    
    command = "adb shell \"logcat -e CME.*ERROR -d -b radio\""
    SIMerrorMessage = os.popen(command).read()
    SIMerror = SIMerrorMessage.find("ERROR")
        
    command = "adb shell \"logcat -e CIMI -d -b radio\""
    SIMdetectMessage = os.popen(command).read()
    SIMdetected = SIMdetectMessage.find("CIMI")
    
    if SIMdetected != -1:
        print()
        print("SIM card detected.")
        SIMdetectLog = 'P'
    elif ((SIMdetected == -1) and (SIMerror != -1)):
        print()
        print("No SIM card detected.")
        SIMdetectLog = 'F'

    print(progress[i], end = '') #spin the spinner
    if i < 3:
        i += 1
    else:
        i = 0
        
    j += 1
    


# for HL Modem only:
if ModemType == 'HL' and SIMdetectLog == 'P':
    logcatCREG = os.popen("adb shell \"logcat -e CREG: -d -b radio\"").read().splitlines()
    i = -1
    for line in logcatCREG:
        i += 1

    CREGresponse = str(logcatCREG[i]).split("+CREG:")[1].strip()
    print("+CREG: " + CREGresponse)
    if len(CREGresponse) > 4:
        print("Attached to netowrk.")
        NetworkAttachedLog = 'Y'
    else:
        print("Not attached to network.")
        NetworkAttachedLog = 'N'

# For WP Modem Only:
elif ModemType == 'WP' and SIMdetectLog == 'P':
    logcatCOPS = os.popen("adb shell \"logcat -e COPS: -d -b radio\"").read().splitlines()
    i = -1
    for line in logcatCOPS:
        i += 1

    COPSresponse = str(logcatCOPS[i]).split("+COPS:")[1].strip()
    print("+COPS: " + COPSresponse)
    if len(COPSresponse) > 4:
        print("Attached to network.")
        NetworkAttachedLog = 'Y'
    else:
        print("Not attached to network.")
        NetworkAttachedLog = 'N'
else:
    print("Not attached to network.")
    NetworkAttachedLog = 'N'

# Log the following: ModemDetectLog SIMdetectLog NetworkAttachedLog

print()

# Check RTC

time.sleep(1)

# RTC check section

day =   [ '', 'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
month = [ '', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec' ]

carrierTime = os.popen("adb shell hwclock -r").read().strip().split(' ')
lts = time.gmtime()

carrierTimeHHMMSS = str(carrierTime[3])
gmtTimeHHMMSS = str(lts[3]).zfill(2)+':'+str(lts[4]).zfill(2)+':'+str(lts[5]).zfill(2)
gmtTimeSS = str(lts[5]).zfill(2)

# avoid clock rollover problems
#while gmtTimeHHMMSS == '23:59:59' or gmtTimeHHMMSS == '00:00:00'  or gmtTimeHHMMSS == '00:00:01' : # day rollover
while gmtTimeSS == '59' or gmtTimeSS == '00'  or gmtTimeSS == '01' : # minute rollover
    print()
    print("Waiting for clock rollover")
    print()
    time.sleep(5)
    carrierTime = os.popen("adb shell hwclock -r").read().split(' ')
    lts = time.gmtime()
    carrierTimeHHMMSS = str(carrierTime[4])
    gmtTimeHHMMSS = str(lts[3]).zfill(2)+':'+str(lts[4]).zfill(2)+':'+str(lts[5]).zfill(2)

# lts data:
# time.struct_time(tm_year=2019, tm_mon=9, tm_mday=24, tm_hour=21, tm_min=46, tm_sec=55, tm_wday=1, tm_yday=267, tm_isdst=0)
# time.struct_time(tm_year=2019, tm_mon=9, tm_mday=6, tm_hour=18, tm_min=44, tm_sec=41, tm_wday=4, tm_yday=249, tm_isdst=0)
# index               0             1         2          3           4          5          6           7           8

carrierTimeDay    = str(carrierTime[0])
carrierTimeMonth  = str(carrierTime[1])
carrierTimeDate   = str(carrierTime[2]).zfill(2)
carrierTimeHHMMSS = str(carrierTime[3])
carrierTimeHH     = str(carrierTime[3]).split(':')[0]
carrierTimeMM     = str(carrierTime[3]).split(':')[1]
carrierTimeSS     = str(carrierTime[3]).split(':')[2]
carrierTimeYear   = str(carrierTime[4])

gmtTimeWeekday    = day[int(lts[6])]
gmtTimeMonth      = month[int(lts[1])]
gmtTimeDate       = str(lts[2]).zfill(2)
gmtTimeHHMMSS     = str(lts[3]).zfill(2)+':'+str(lts[4]).zfill(2)+':'+str(lts[5]).zfill(2)
gmtTimeHH         = str(lts[3]).zfill(2)
gmtTimeMM         = str(lts[4]).zfill(2)
gmtTimeSS         = str(lts[5]).zfill(2)
gmtTimeYear       = str(lts[0]).zfill(4)
print('{:^10}'.format('--------') + '{:>10}'.format('--------')          + ' | ' + '{:<10}'.format('--------'))
print('{:^10}'.format('Compare')  + '{:>10}'.format('Hat Time')          + ' | ' + '{:<10}'.format('GMT Time'))
print('{:^10}'.format('--------') + '{:>10}'.format('--------')          + ' | ' + '{:<10}'.format('--------'))
print('{:^10}'.format('Month')    + '{:>10}'.format(carrierTimeMonth)    + ' | ' + '{:<10}'.format(gmtTimeMonth))
print('{:^10}'.format('Date')     + '{:>10}'.format(carrierTimeDate)     + ' | ' + '{:<10}'.format(gmtTimeDate))
print('{:^10}'.format('Time')     + '{:>10}'.format(carrierTimeHHMMSS)   + ' | ' + '{:<10}'.format(gmtTimeHHMMSS))
print('{:^10}'.format('TimeHH')   + '{:>10}'.format(carrierTimeHH)       + ' | ' + '{:<10}'.format(gmtTimeHH))
print('{:^10}'.format('TimeMM')   + '{:>10}'.format(carrierTimeMM)       + ' | ' + '{:<10}'.format(gmtTimeMM))
print('{:^10}'.format('TimeSS')   + '{:>10}'.format(carrierTimeSS)       + ' | ' + '{:<10}'.format(gmtTimeSS))
print('{:^10}'.format('Year')     + '{:>10}'.format(carrierTimeYear)     + ' | ' + '{:<10}'.format(gmtTimeYear))
print('{:^10}'.format('--------') + '{:>10}'.format('--------')          + ' | ' + '{:<10}'.format('--------'))

RTCpass = 1

# compare Year
if gmtTimeYear != carrierTimeYear:
    print('Year does not match')
    RTCpass = 0
    
# compare Month
if gmtTimeMonth != carrierTimeMonth:
    print('Month does not match')
    RTCpass = 0

# compare Date
if gmtTimeDate != carrierTimeDate:
    print('Day does not match')
    RTCpass = 0
    
# compare Hour
if gmtTimeHH != carrierTimeHH:
    print('Hour does not match')
    RTCpass = 0

# compare Minute 
if gmtTimeMM != carrierTimeMM:
    print('Mintute does not match')
    RTCpass = 0

# compare Seconds within 1 second
if abs(int(gmtTimeSS) - int(carrierTimeSS)) > 1 : # Fails if difference is more than 1 second.
    print('Seconds is off by more than 1 second')
    RTCpass = 0

if RTCpass == 0:
    print()
    print('RTC clock has failed')
    RTClog = 'F'
else:
    print()
    print('RTC clock is working')
    RTClog = 'P'

# Write log file
os.chdir(r"c:\Communicator_Final")

stopwatchStop2 = time.perf_counter()
timeElapsed = convert(stopwatchStop2 - stopwatchStart2)

#Placeholder values for tests not implemented:

appendRow = [ 
    stopwatchStart, 
    serial,
    IPaddr,
    WiFiMAC, 
    guid, 
    battVoltage,
    LEDlog,
    buttonLog,
    SpeakerLog,
    VideoLog,
    uSDlog,
    Temperature,
    Humidity,
    Pressure,
    Noise,
    HatWornClosedLog,
    Acceleration,
    HatWornOpenLog,
    ModemDetectLog,
    SIMdetectLog,
    NetworkAttachedLog,
    RTClog,
    timeElapsed
    ]
#removed     NFClog,

topRow = [
    'Test Start', 
    'Serial',
    'IPaddr',
    'WiFiMAC', 
    'GUID', 
    'Battery Voltage',
    'LEDs',
    'Buttons',
    'Speakers',
    'Video',
    'uSD',
    'Temperature',
    'Humidity',
    'Pressure',
    'Noise',
    'HatWornClosed',
    'Acceleration',
    'HatWornOpen',
    'ModemDetect',
    'SIMdetect',
    'NetworkAttached',
    'RTC',
    'Test Duration'
    ]

#removed     'NFC',

#print(appendRow)

# for loops for log file .csv
if os.path.isfile('FinalTestLog.csv'):
    with open(r'FinalTestLog.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(appendRow)
else:
    with open(r'FinalTestLog.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(topRow)
        writer.writerow(appendRow)
f.close()

# Display test results
print()
print("Test Results:")
print()
print("---------------------------------------------------------")
print()

i = 0
for measurement in topRow:
    print( '{:^20}'.format(measurement) + ":" + '{:<20}'.format(appendRow[i]))
    i += 1

print()
print("---------------------------------------------------------")
print()

# adb disconnect <IP address of hat:5123>
subprocess.call(disconnectCommand)

print()
print("Press and hold power button until voice prompt says \"Power down initiated.\"")
print("Wait for all LEDs to be turned off.")
print("Test Complete.")

exit()