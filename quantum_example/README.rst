###############
Quantum Example
###############

Here is an example of an experiment that is ready to run on Red Deer. It simulates randomly generated quantum circuits. You do not need to know anything about quantum computing to understand the example.

********
Contents
********

``image/``
==========

This directory contains files to be copied into the image.

``image/args.csv``
------------------

This CSV file contains the arguments associated with each array task.

``image/requirements.txt``
--------------------------

These are the Python packages required by ``image/simulate.py``. They are specified with exact versions for reproducibility (this can sometimes cause issues if a specific version of a package is removed from  `PyPI <https://pypi.org/>`_).

``image/simulate.py``
---------------------

This Python script performs the quantum circuit simulation. It takes a single argument, the array task ID.

``image.def``
=============

This is the Apptainer Definition File for the image.

``job.bash``
============

This is the SLURM script that launches the job. It is an array job consisting of 10 array tasks.

*****
Usage
*****

Follow these steps exactly to setup and launch the example:

#. **On your own machine**, clone the repository: ``git clone git@github.com:o-parry/red-deer.git``.
#. Change directories to the repository: ``cd red-deer``.
#. Open ``quantum_example/job.bash`` in a text editor and replace ``YOUR_USERNAME_HERE`` with your own username.
#. Zip the example: ``zip -r quantum_example.zip quantum_example``.
#. Transfer ``quantum_example.zip`` to ``/data/$USER`` using the Navigator tab in the web interface.
#. **On Red Deer**, unzip the example: ``unzip /data/$USER/quantum_example.zip -d /data/$USER/``.
#. Change directories to the quantum example directory: ``cd /data/$USER/quantum_example``.
#. Build the image: ``apptainer build image.sif image.def``.
#. Launch the job: ``sbatch job.bash``. If all is well, you will see the following output: ``Submitted batch job JOB_ID``, where ``JOB_ID`` is a number.
#. Check the job is running (or waiting in the queue) using the Slurm tab (or you can use the ``squeue`` command).
#. Once you are happy that everything is working, you can cancel the job using ``scancel JOB_ID``, or wait for the job to finish naturally (it shouldn't take more than a few minutes).
