#!/bin/bash

# I have a directory of pickle files in it. 
# I want to loop over each file and run a python script on each file in the directory.
# The python script is draw_fig1_cv4vr.py
# and use parallel

for file in /data2/fparodi/human/cv4vr/high_anxiety/*pkl
do
    echo $file
    python draw_fig1_cv4vr.py --pkl=$file
done