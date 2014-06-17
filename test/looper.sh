#!/bin/bash

rm logfile.log
echo "Starting test:"

for rowaddr in `seq 0 5`;
do
for coladdr in `seq 0 5`;
do
timestamp=$(date +%T)
echo $timestamp
echo $timestamp >> logfile.log
echo "Testing $rowaddr, $coladdr"
python RandomNumberTest.py $rowaddr $coladdr --go | grep 'match\|Testing Row\|shift\|Loaded'| tee -a logfile.log
sleep 1s
done 
done
