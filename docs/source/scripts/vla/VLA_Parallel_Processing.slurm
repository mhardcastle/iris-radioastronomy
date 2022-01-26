#!/bin/bash
#!

#!#############################################################
#!#### Modify the options in this section as appropriate ######
#!#############################################################

#! sbatch directives begin here ###############################
#! Name of the job:
#SBATCH -J VLA-Parallel-Processing
#! Which project should be charged:
#SBATCH -A DIRAC-TP001-CPU
#SBATCH -p icelake
#! How many whole nodes should be allocated?
#SBATCH --nodes=2
#! How many (MPI) tasks will there be in total? (<= nodes*76)
#! The Ice Lake (icelake) nodes have 76 CPUs (cores) each and
#! 3380 MiB of memory per CPU.
#SBATCH --ntasks=2
#! How much wallclock time will be required?
#SBATCH --time=03:00:00
#! What types of email messages do you wish to receive?
#SBATCH --mail-type=ALL
#! Uncomment this to prevent the job from being requeued (e.g. if
#! interrupted by node failure or system downtime):
#SBATCH --no-requeue

#! ############################################################
#! Modify the settings below to specify the application's environment, location 
#! and launch method:

#! Optionally modify the environment seen by the application
#! (note that SLURM reproduces the environment at submission irrespective of ~/.bashrc):
. /etc/profile.d/modules.sh                # Leave this line (enables the module command)
##module purge                               # Removes all modules still loaded
module load rhel8/default-icl              # REQUIRED - loads the basic environment
module load singularity
module load parallel

# Describe the measurement sets to be processed
INPUTS=("12A-195.sb12378614.eb13812032.56231.2797265625.ms A L" "12A-195.sb7351094.eb10491731.56075.655723206015.ms B L")

## The -N1 -n1 options allocate a single core to each task
srun="srun --exclusive -N1 -n1"

## The delay of 0.2 prevents overloading the controlling node
## -j is the number of tasks to run simutaneously
## --joblog and --resume combine to create a task log that can be used to monitor progress
parallel="parallel --delay 0.2 -j $SLURM_NTASKS --joblog runtask.log --resume"

## Run the command
$parallel "$srun singularity exec casa_latest.sif casa -c VLA_Process_3C465_Images.py {1}" ::: "${INPUTS[@]}"
