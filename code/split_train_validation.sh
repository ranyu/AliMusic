#!/bin/bash
for q in `ls ../play_number/`
do
    echo $q
    head -n 154 ../play_number/$q > ../local_train/train_$q 
    tail -n 30 ../play_number/$q > ../local_vali/vali_$q
done
