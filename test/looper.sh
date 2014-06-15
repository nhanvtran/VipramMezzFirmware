#!/bin/bash

rm logfile.log
echo "Starting test:"

for rowaddr in `seq 0 127`;
do
for coladdr in `seq 0 31`;
do
timestamp=$(date +%T)
echo $timestamp
echo $timestamp >> logfile.log
echo "Testing $rowaddr, $coladdr"
python singleRoadTest_constantShift_looper100MHz.py $rowaddr $coladdr --go | grep 'match\|Testing Row\|shift'| tee -a logfile.log
sleep 1s
done 
done
