###############
Quantum Example
###############

Here is an example of an experiment that is ready to be executed on Red Deer. It simulates randomly generated quantum circuits, but you do not need to know anything about quantum computing to understand the example.

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

``logs/``
=========

Here is where the output logs from each array task will be stored.

``results/``
============

This directory becomes a bind, to which the results of the experiment will be stored.

``job.bash``
============

This is the SLURM script that launches the job. It is an array job consisting of 10 array tasks.

*****
Usage
*****

Follow these steps exactly to setup and launch the example:

#. Clone the repository: ``git clone git@github.com:o-parry/red-deer.git``.
#. Change directories to the repository: ``cd red-deer``.
#. Open ``quantum_example/image.def`` and ``quantum_example/job.bash`` in a text editor and replace all occurrences of ``YOUR_USERNAME_HERE`` with your own username.
#. Zip the example: ``zip -r quantum_example.zip quantum_example``.
#. Transfer ``quantum_example.zip`` to ``/data/$USER`` (``$USER`` refers to your own username, e.g., ``owain``) using the Navigator tab in the web interface.
#. Unzip the example using the Terminal tab: ``unzip /data/$USER/quantum_example.zip -d /data/$USER/``.
#. Build the image: ``apptainer build /data/$USER/quantum_example/image.sif /data/$USER/quantum_example/image.def``.
#. Launch the job: ``sbatch /data/$USER/quantum_example/job.bash``. If all is well, you will see the following output: ``Submitted batch job JOB_ID``, where ``JOB_ID`` is a number.
#. Check the job is running (or waiting in the queue) using the Slurm tab (or you can use the ``squeue`` command).
#. Once you are happy that everything is working, you can cancel the job using ``scancel JOB_ID``, or wait for the job to finish naturally (it shouldn't take more than a few minutes).
