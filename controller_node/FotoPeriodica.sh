#!/bin/bash

trap 'exit 0' SIGINT

while true

do
        DATE=$(date +"%Y-%m-%d_%H%M%S")

        raspistill -vf -hf -o /home/pi/camera/$DATE.jpg
done