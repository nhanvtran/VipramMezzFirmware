#!/bin/bash

rm logfile.log
echo "Starting test:"

for rowaddr in `seq 0 127`;
do
timestamp=$(date +%T)
echo $timestamp
echo $timestamp >> logfile.log
echo "----Testing Row $rowaddr"
python RandomNumberTest_FullRow.py $rowaddr --go | grep 'match\|Testing Row\|shift\|Loaded\|number of hits'| tee -a logfile.log
sleep 1s 
done
