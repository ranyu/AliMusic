#!/bin/bash
for q in `ls ../vali_result/`
do
    echo $q
    python ./validation_submit.py ./vali_result ../vali_result/$q
    python ./Fscore.py ./vali_result ../local_vali/vali_$q >> SCORE
    rm vali_result
done
    python sum_score.py SCORE 
    rm SCORE
