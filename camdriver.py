from executor import execute
import signal
import sys
from datetime import datetime
import re

MAX_FPS = 30
RESOLUTION_AVAILABLE = ['640x480',]
VIDEO_DEV = None
FPS = None
RESOLUTION = None

def signal_handler(signal, frame):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S:')
    print('%s INFO : Exiting Server'%timestamp)
    sys.exit(0)

def select_video_device():
    global VIDEO_DEV
    cmd_out = execute('ls -ltrh /dev/video*', capture=True)
    pattern = re.compile('/dev/video(.+?)')
    all_devices = pattern.findall(cmd_out)
    while True:
        for device in all_devices:
            print('Press ( %s ) : dev/video%s'%(device,device))
        VIDEO_DEV = raw_input('Access the device from above : ')
        if VIDEO_DEV in all_devices:
            break
        else:
            print('Invalid selection %s'%VIDEO_DEV)


def select_fps():
    global MAX_FPS, FPS
    print('Select FPS between(0-%d)'%MAX_FPS)
    while True:
        try:
            FPS = int(raw_input('Enter the FPS from required : '))
            if FPS > MAX_FPS:
                print('FPS %d is over the limited %d FPS'%(FPS, MAX_FPS))
            else:
                break
        except ValueError as e:
            if FPS is None:
                print 'Invalid selection None'
            else:
                print 'Invalid selection %s'%str(FPS)

def select_resolution():
    global RESOLUTION_AVAILABLE, RESOLUTION
    while True:
        try:
            for id_,resolution in enumerate(RESOLUTION_AVAILABLE):
                print('Press( %d ): resolution %s'%(id_,resolution))
                try:
                    index = int(raw_input('Enter the required resolution'))
                    RESOLUTION = RESOLUTION_AVAILABLE[index]
                    if RESOLUTION in RESOLUTION_AVAILABLE:
                        return
                    else:
                        print('Invalid selection %d'%RESOLUTION)
                except IndexError:
                    print('Invalid selection %d'%index)
        except ValueError:
            if RESOLUTION is None:
                print 'Invalid selection None'
            else:
                print 'Invalid selection %s'%str(RESOLUTION)

    
            
signal.signal(signal.SIGINT, signal_handler) #First bind CTRL+C event
select_video_device()
select_fps()
select_resolution()
command = 'ffmpeg -f video4linux2 -i /dev/video%s \
            -r %d -s %s -f mjpeg -qscale 5 - \
            2>/dev/null | ./streameye'%(VIDEO_DEV,FPS,RESOLUTION)

execute(command)
