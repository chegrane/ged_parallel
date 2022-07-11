#!/bin/bash
#SBATCH --job-name=ged_parallel_test # Job name
#SBATCH --output=%x__%j.log                            # Standard output and error log
#SBATCH --nodes=1                                      # Run all processes on a single node	
#SBATCH --ntasks=1                                     # Run a single task
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=16                             # Number of CPU cores per task (20 for node that conatin more than 20)
#SBATCH --time=01:10:00                              # Time limit hrs:min:sec
#SBATCH --reservation=adabah_9
###SBATCH --partition=any*                           # Partition to submit to


exe_jar_file=$1
c_node_sub=$2
c_node_del_ins=$3
c_edge_sub=$4
c_edge_del_ins=$5
file_path_g1=$6
file_path_g2=$7
path_output=$8
test_name=$9    # TUDataset this is to knwo with parser to use to read the graph
amount_RunTime_Seconds=${10}
NB_threads=${11}
dataset_name=${12} # this the name of the datset: AIDS, MUTAG, etc.
setting=${13} # this is the setting number: s1, s2, s3
cd GED_parallel/  # access the GED_parallel folder
srun --nodes 1 --ntasks 1 java -jar $exe_jar_file $c_node_sub $c_node_del_ins $c_edge_sub $c_edge_del_ins $file_path_g1 $file_path_g2 $path_output $test_name $amount_RunTime_Seconds $NB_threads > log_${exe_jar_file}_${setting}_${dataset_name}_t3600

