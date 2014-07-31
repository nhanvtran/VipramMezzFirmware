#!/bin/bash

rm logfile100MHz2Run.log
echo "Starting test:"

rowaddr=0
while [ $rowaddr -lt 128 ];
do
timestamp=$(date +%T)
echo $timestamp
echo $timestamp >> logfile100MHz2Run.log
echo "----Testing Row $rowaddr"
python RandomNumberTest_FullRow.py $rowaddr --go | grep 'match\|Testing Row\|shift\|Loaded\|number of hits'| tee -a logfile100MHz2Run.log
rowaddr=$[$rowaddr+4]
sleep 1s 
done
