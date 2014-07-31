#!/bin/bash

freq=10
N=50

#while [ $N -lt 101 ];
#do

B=''

#iter=0
#while [ $B -lt 6 ];
#do

rm logfile${freq}MHzNewStressB${B}N${N}.log

rm NewStressInfoFile.txt

rownum=0
while [ $rownum -lt 128 ];
do
timestamp=$(date +%T)
echo $timestamp
echo $timestamp >> logfile${freq}MHzNewStressB${B}N${N}.log
python RunFile.py $rownum $N $freq --go | grep "Loaded" | tee -a logfile${freq}MHzNewStressB${B}N${N}.log
rownum=$[$rownum+4]
sleep 1s
done

echo "RUN MODE"
rownum=0
while [ $rownum -lt 128 ];
do
timestamp=$(date +%T)
echo $timestamp
echo $timestamp >> logfile${freq}MHzNewStressB${B}N${N}.log
python RunFile3.py $rownum $N $freq --go | grep "Loaded\|checkData\|There\|Output" | tee -a logfile${freq}MHzNewStressB${B}N${N}.log
rownum=$[$rownum+16]
sleep 1s
done

#B=$[$B+1]
#done
#iter=$[$iter+1]
#done

#N=$[$N+20]
#done
