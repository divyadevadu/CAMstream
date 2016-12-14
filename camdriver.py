from executor import execute
import signal
import sys
from datetime import datetime

def signal_handler(signal, frame):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S:")
    print(timestamp +' '+'INFO : Exiting Server')
    sys.exit(0)
        
signal.signal(signal.SIGINT, signal_handler)
execute("ffmpeg -f video4linux2 -i /dev/video0 -r 30 -s 640x480 -f mjpeg -qscale 5 - 2>/dev/null | ./streameye")
