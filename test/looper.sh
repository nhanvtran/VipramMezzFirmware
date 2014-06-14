#!/bin/bash

rm logfile.log
timestamp=$(date +%T)
echo $timestamp
echo "Loading full chip with Zeros..."
python loadAllZeros.py --go | grep 'match'

echo "Starting test:"

for rowaddr in `seq 0 3`;
do
for coladdr in `seq 0 3`;
do
echo "Testing $rowaddr, $coladdr"
python singleRoadTest_constantShift_looper100MHz.py $rowaddr $coladdr --go | grep 'match\|Testing Row\|shift'| tee -a logfile.log
echo $timestamp >> logfile.log
sleep 1
done 
done
