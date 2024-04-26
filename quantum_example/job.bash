#!/bin/bash

#SBATCH --job-name=quantum_example_job
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH --output=/data/YOUR_USERNAME_HERE/quantum_example/logs/%A_%a.out
#SBATCH --time=00-01:00:00
#SBATCH --array=1-10

srun apptainer run \
    --bind /data/YOUR_USERNAME_HERE/quantum_example:/root/results \
    /data/YOUR_USERNAME_HERE/quantum_example/image.sif $SLURM_ARRAY_TASK_ID
