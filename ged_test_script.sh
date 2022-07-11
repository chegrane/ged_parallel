#!/bin/bash
# a bash script to test ged algorithm

# set_1 = 2, 4, 1, 1
# set_2 = 2, 4, 1, 2
# set_3 = 6, 2, 3, 1
setting=$2   # input the setting number as s1, s2, s3


# check setting
if [ $setting == "s1" ]; then
    c_node_sub=2
    c_node_del_ins=4
    c_edge_sub=1
    c_edge_del_ins=1
elif [ $setting == "s2" ]; then
    c_node_sub=2
    c_node_del_ins=4
    c_edge_sub=1
    c_edge_del_ins=2
elif [ $setting == "s3" ]; then
    c_node_sub=6
    c_node_del_ins=2
    c_edge_sub=3
    c_edge_del_ins=1
else
    echo "setting not found"
    exit 1
fi

exe_jar_file="Exact_GED_BB_DF_high_level_with_load_balancing.jar"
amount_RunTime_Seconds=$3  # this is not important, because it is hard coded for now dirctly in java
NB_threads=20


# get dataset name
dataset_name=$1

dir_path="/home/ichegrane/GED_datasets/TUDataset/$dataset_name/gxl"
root_directory_output="Result_TUDataset_GED_parallel_t120_sh/"${dataset_name}
path_output=$root_directory_output/"test_${dataset_name}_${setting}.csv"


# read all files in given directory path and store them in an array
files=($(ls $dir_path))

# loop through all files in the directory, 
# and run ged algorithm on each file with next file as the reference
for (( i=0; i<${#files[@]}-1; i++ )); do
    g1="$dir_path/${files[$i]}"
    g2="$dir_path/${files[$i+1]}"
    echo $g1 $g2 
    java -jar $exe_jar_file $c_node_sub $c_node_del_ins $c_edge_sub $c_edge_del_ins $g1 $g2 $path_output "TUDataset" $amount_RunTime_Seconds $NB_threads
done

echo "finished : setting $setting"

