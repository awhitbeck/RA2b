#!/bin/bash

index=0
for i in `seq 0 306`;
#for i in `seq 0 122`;
do
    start=$((i*10+1))
    end=$(((i+1)*10))
    args="\"${start} ${end} ${index}\""
    echo $args
    condor_submit TPskim.jdl arguments="${args}"
    index=$((index+1))
done