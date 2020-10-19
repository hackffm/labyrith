#!/bin/bash
#export LD_LIBRARY_PATH=~/git/mjpg-streamer/mjpg-streamer-experimental/
#~/git/mjpg-streamer/mjpg-streamer-experimental/mjpg_streamer -o "output_http.so -w ./www" -i "input_raspicam.so -rot 180" &
~/git/FPVCar/webserver_tornado/mjpg-streamer/mjpg_streamer -o "/home/pi/git/FPVCar/webserver_tornado/mjpg-streamer/output_http.so -w ./www" -i "/home/pi/git/FPVCar/webserver_tornado/mjpg-streamer/input_raspicam.so -rot 180 -x 640 -y 480 -fps 5 -quality 5" &
echo $!
