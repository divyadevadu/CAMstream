from executor import execute
execute("ffmpeg -f video4linux2 -i /dev/video0 -r 30 -s 640x480 -f mjpeg -qscale 5 - 2>/dev/null | ./streameye")
