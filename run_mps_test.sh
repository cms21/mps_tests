#!/bin/bash -l

APP="/eagle/IRIBeta/fusion/bin/ionorb_stl_boris2d ./ionorb_stl2d_boris.config"
#APP="/eagle/IRIBeta/fusion/bin/ionorb_stl_boris2d"

NRUN=$1
export CUDA_MPS_ACTIVE_THREAD_PERCENTAGE=$(( 100/$NRUN ))
echo "NRUN=${NRUN}"
echo "CUDA_MPS_ACTIVE_THREAD_PERCENTAGE=${CUDA_MPS_ACTIVE_THREAD_PERCENTAGE}"
echo $APP
#./enable_mps_polaris.sh
SECONDS=0
declare -a PIDS=()
NLOOP=$(( $NRUN - 1 ))
for i in $(seq 0 $NLOOP);
do
    # Different slices
    #path_iter=$(( 100 + $i * 20 ))

    # Same slice repeated
    path_iter="100_"$i

    config_path="/eagle/IRIBeta/csimpson/mps_ionorb_test/test/"$path_iter"/"
    cd $config_path
    echo $config_path
    time CUDA_VISIBLE_DEVICES=0 $APP > "./ionorb_"$i".out" 2>&1 &
    
    pid=$!
    PIDS[$i]=$pid
done

for pid in ${PIDS[@]};
do
    wait $pid 
done
echo "TOTAL RUN TIME for "$NRUN" runs is "$SECONDS" seconds"
#/eagle/IRIBeta/csimpson/mps_ionorb_test/disable_mps_polaris.sh



