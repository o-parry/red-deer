#!/bin/bash

#SBATCH --array=1-10
#SBATCH --chdir=/data/YOUR_USERNAME_HERE/quantum_example
#SBATCH --cpus-per-task=1
#SBATCH --job-name=quantum_example_job
#SBATCH --mem=1G
#SBATCH --ntasks=1
#SBATCH --output=logs/%A_%a.out
#SBATCH --time=1:00:00

srun apptainer run image.sif $SLURM_ARRAY_TASK_ID
