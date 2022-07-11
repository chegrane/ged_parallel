#!/bin/bash
#SBATCH --job-name=ged_parallel_test # Job name
#SBATCH --output=%x__%j.log                            # Standard output and error log
#SBATCH --mail-type=BEGIN,END,FAIL                           # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=ibrahim.chegrane@usherbrooke.ca    # Where to send mail
#SBATCH --nodes=1                                      # Run all processes on a single node	
#SBATCH --ntasks=1                                     # Run a single task
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=20                             # Number of CPU cores per task
#SBATCH --array=0-6
#SBATCH --time=20:00:00                              # Time limit hrs:min:sec
#SBATCH --partition=crocoib                           # Partition to submit to

###    srun python test_parallel_one_node.py

ldn=(benzene MUTAG AIDS aspirin TRIANGLES MSRC_21) # list_dataset_name
exe_jar_file=$1
setting=$2
srun --exclusive --nodes 1 --ntasks 1 python3 test_GED_script.py ${ldn[${SLURM_ARRAY_TASK_ID}]} 3600 $exe_jar_file $setting > log_${exe_jar_file}_${setting}_${ldn[${SLURM_ARRAY_TASK_ID}]}_t3600

