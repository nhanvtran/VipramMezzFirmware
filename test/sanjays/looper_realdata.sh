#!/bin/bash/

freq=90
i=4
rm logfile${freq}MHzRealDataIO${i}.log

python RandomArrangeLines.py "10kPatterns_sec27_0DC_lowPT_0DC.txt"
rm ChosenBits.txt
g++ -o OptimizeNANDChoice OptimizeNANDChoice.cpp
./OptimizeNANDChoice "10kPatterns_sec27_0DC_lowPT_0DC.txt" "ChosenBits.txt" 0
./OptimizeNANDChoice "10kPatterns_sec27_0DC_lowPT_0DC.txt" "ChosenBits.txt" 1
./OptimizeNANDChoice "10kPatterns_sec27_0DC_lowPT_0DC.txt" "ChosenBits.txt" 2
./OptimizeNANDChoice "10kPatterns_sec27_0DC_lowPT_0DC.txt" "ChosenBits.txt" 3

linenum=1
ls
while [ $linenum -lt 4097 ];
do
timestamp=$(date +%T)
echo $timestamp
echo $timestamp >> logfile${freq}MHzRealDataIO${i}.log
python RunFile.py "Rearranged10kPatterns_sec27_0DC_lowPT_0DC.txt" $linenum "ChosenBits.txt" --go | grep 'Loaded\|There\|Output' | tee -a logfile${freq}MHzRealDataIO${i}.log
linenum=$[$linenum+256]
sleep 1s
done

