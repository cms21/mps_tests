#!/bin/bash -l

/eagle/IRIBeta/csimpson/mps_ionorb_test/enable_mps_polaris.sh
for i in 1 4 8 16 32 48;
do
    ./run_mps_test.sh $i &> test_$i.out
done
/eagle/IRIBeta/csimpson/mps_ionorb_test/disable_mps_polaris.sh





