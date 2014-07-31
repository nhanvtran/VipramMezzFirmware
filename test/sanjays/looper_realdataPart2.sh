#!/bin/bash

freq=90
i=4
rm logfile${freq}MHzRealDataIO${i}Run.log

startnum=1
while [ $startnum -lt 4097 ];
do
timestamp=$(date +%T)
echo $timestamp
echo $timestamp >> logfile${freq}MHzRealDataIO${i}Run.log
python RunFile2.py "Rearranged10kPatterns_sec27_0DC_lowPT_0DC.txt" $startnum "ChosenBits.txt" --go | grep 'Loaded\|match\|Testing\|There\|Output\|Comparison' | tee -a logfile${freq}MHzRealDataIO${i}Run.log
startnum=$[$startnum+1024]
sleep 1s
done
