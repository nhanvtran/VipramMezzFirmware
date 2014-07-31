#!/bin/bash

freq=77
N=60
A=1
filename="logfile${freq}MHzLocationStressA${A}N${N}.log"

rm $filename
rm "LocationStressInfoFile.txt"

rownum=0
while [ $rownum -lt 128 ];
do
timestamp=$(date +%T)
echo $timestamp
echo $timestamp >> $filename
python RunFile.py $rownum $N $freq --go | grep "Loaded" | tee -a $filename

rownum=$[$rownum+4]
sleep 1s
done

rownum=0
echo "RUN MODE"
echo "RUN MODE" >> $filename
while [ $rownum -lt 128 ];
do
colnum=0
while [ $colnum -lt 32 ];
do
timestamp=$(date +%T)
echo $timestamp
echo $timestamp >> $filename
python RunFile3.py $rownum $N $freq $colnum --go | grep "Loaded\|Output\|matches\|checkData" | tee -a $filename
colnum=$[$colnum+16]
done
rownum=$[$rownum+1]
done
