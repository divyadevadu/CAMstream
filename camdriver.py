from executor import execute
import signal
import sys
from datetime import datetime
import re

VIDEO_DEV = None

def signal_handler(signal, frame):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S:')
    print('%s INFO : Exiting Server'%timestamp)
    sys.exit(0)

def find_available():
    global VIDEO_DEV
    cmd_out = execute('ls -ltrh /dev/video*', capture=True)
    pattern = re.compile('/dev/video(.+?)')
    all_devices = pattern.findall(cmd_out)
    while True:
        for device in all_devices:
            print('Press ( %s ) : dev/video%s'%(device,device))
        VIDEO_DEV = raw_input('Enter the choice from above : ')
        if VIDEO_DEV in all_devices:
            break
        else:
            print('Invalid choice %s'%VIDEO_DEV)
    
signal.signal(signal.SIGINT, signal_handler) #First bind CTRL+C event
find_available()
command = 'ffmpeg -f video4linux2 -i /dev/video%s \
            -r 30 -s 640x480 -f mjpeg -qscale 5 - \
            2>/dev/null | ./streameye'%VIDEO_DEV

execute(command)
