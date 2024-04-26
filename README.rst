########
Red Deer
########

`Click here <https://reddeer.dcs.shef.ac.uk:9090>`_ to access the web interface (you must be connected to the VPN). Your username is your first name in lowercase. Your password is "password". You will be prompted to change your password when you first log in. Here you will find a file browser, a terminal, and several other utilities. Alternatively you could just use SSH.

Each user has two personal directories. The first is located on the ``root`` partition, at ``/home/$USER``. The second is located on the ``data`` partition, at ``/data/$USER``. The root partition is limited to 100 gigabytes and should **not** be used to store large input files or experimental results.

This guide is intended to give an introduction to SLURM and Apptainer (the two main technologies on Red Deer to facilitate the scheduling and execution of jobs). It is not intended to be an exhaustive reference. Please see the external links in the Further Reading sections. For a worked example, please see ``quantum_example``.

*****
SLURM
*****

Red Deer uses SLURM to handle the scheduling of jobs. To schedule a job, you must write a shell script and issue the command: ``sbatch MY_SCRIPT.bash``. The structure of the script should be something like this:
::

	#!/bin/bash
	#SBATCH --arg-1=foo
	#SBATCH --arg-2=bar
	#SBATCH --arg-3=baz
	srun do_stuff

The first line is always required. The following three lines are used to pass arguments to ``sbatch``. Alternatively you could pass arguments on the command line: ``sbatch --arg-1=foo --arg-2=bar --arg-3=baz MY_SCRIPT.bash``. Arguments passed on the command line take precedence over those specified in a script. There are many arguments that can be passed to ``sbatch``, but realistically you should only need the following:

* ``--job-name=JOB_NAME`` sets the name of the job to ``JOB_NAME``. This is required.
* ``--ntasks=N_TASKS`` declares that the job consists of ``N_TASKS`` parallel tasks. By default jobs consist of a single task.
* ``--cpus-per-task=N_CPUS`` requests ``N_CPUS`` per task, such that the total number of CPUs required for the job is ``N_TASKS`` * ``N_CPUS``.
* ``--mem=MEM_LIMIT`` sets the maximum amount of memory available to the job. ``MEM_LIMIT`` should be an integer and the default unit is megabytes. Alternatively you can specify the limit in gigabytes, for example: ``--mem=16G``. The default memory limit is 1000 megabytes. Setting the limit too high could result in longer queuing times. Setting it too low could result in your job being killed.
* ``--output=OUTPUT_FILE`` arranges for the ``STDOUT`` and ``STDERR`` streams to be combined and recorded in ``OUTPUT_FILE``. The default ``OUTPUT_FILE`` is ``/home/$USER/slurm-%j.out``, where ``%j`` is replaced by the job ID.
* ``--time=TIME_LIMIT`` sets a time limit for the job. ``TIME_LIMIT`` should be specified as ``DAYS-HOURS:MINUTES:SECONDS`` (e.g., ``--time=01-10:05:30`` for 1 day, 10 hours, 5 minutes, and 30 seconds). SLURM kills jobs that exceed their time limit. By default there is no time limit, but specifying one may reduce queuing times.

Tasks within a job are launched with the ``srun`` command. For example, a job consisting of three tasks ought to invoke ``srun`` three times. Any commands invoked directly (i.e., not prefaced with ``srun``) should be fast intermediate steps only (e.g., copying files around).

Standard Jobs
=============

Here is an example of a single-task job:
::

	#!/bin/bash
	#SBATCH --job-name=my_job
	#SBATCH --ntasks=1
	#SBATCH --cpus-per-task=4
	#SBATCH --mem=1G
	#SBATCH --output=logs/my_job-%j.out
	#SBATCH --time=1:00:00
	srun do_multi_threaded_stuff

In this case, the job requires 4 CPUs and is limited to 1 gigabyte of memory. Because this job contains a single task, it is up to ``do_multi_threaded_stuff`` to fully utilise the available CPUs.

Here is an alternative approach consisting of four tasks:
::

	#!/bin/bash
	#SBATCH --job-name=my_job
	#SBATCH --ntasks=4
	#SBATCH --cpus-per-task=1
	#SBATCH --mem=1G
	#SBATCH --output=logs/my_job-%j.out
	#SBATCH --time=1:00:00
	srun do_single_threaded_stuff
 	srun do_single_threaded_stuff
	srun do_single_threaded_stuff
	srun do_single_threaded_stuff

This job still requires 4 CPUs (n.b., ``--cpus-per-task=1``) but SLURM will execute ``do_single_threaded_stuff`` four times in parallel.

Array Jobs
==========

Array jobs are a good choice when you need run a series of very similar tasks. Here is an example:
::

	#!/bin/bash
	#SBATCH --job-name=my_array_job
	#SBATCH --ntasks=1
	#SBATCH --cpus-per-task=1
	#SBATCH --mem=1G
	#SBATCH --output=logs/my_array_job-%A_%a.out
	#SBATCH --time=1:00:00
	#SBATCH --array=1-100
	srun do_single_threaded_stuff $SLURM_ARRAY_TASK_ID

SLURM will arrange for ``do_single_threaded_stuff`` to be executed 100 times. In each case, ``$SLURM_ARRAY_TASK_ID`` evaluates to the array task ID, which in this example will be a number between 1 and 100 inclusive (as specified by the ``--array`` argument). The time and resource limits apply to each array task, so each invocation of ``do_single_threaded_stuff`` will have a time limit of 1 hour, will use a single CPU, and will have up to 1 gigabyte of available memory. For array jobs, the default ``OUTPUT_FILE`` is ``slurm-%A_%a.out`` where ``%A`` is replaced by the job ID and ``%a`` with the array task ID.

Please be aware that if ``do_single_threaded_stuff`` is very fast, then SLURM will spend more time managing and queuing tasks than computing them, which is very wasteful of resources. Otherwise, array jobs are the best approach for `embarrassingly parallel <https://en.wikipedia.org/wiki/Embarrassingly_parallel>`_ workloads. You should always use array jobs where possible. They enable SLURM to interleave jobs between different users more effectively.

Further Reading
===============

* https://slurm.schedmd.com/sbatch.html documentation for ``sbatch``. Lists all the possible arguments.
* https://docs.hpc.shef.ac.uk/en/latest documentation for Sheffield HPC. Stanage and Bessemer also use SLURM, so some of the documentation could be relevant to Red Deer.

*********
Apptainer
*********

In the interest of system stability, you do not have sudo privileges on Red Deer. This means that you cannot install packages. Instead, you can create your own Apptainer images that contain all the packages you need, and launch your jobs inside containers.

Building Images
===============

Before you run containers, you must build the image from which to launch them. To do so, you need to create an Apptainer Definition File. Here is a simple example:
::

    Bootstrap: docker
    From: ubuntu:jammy
    Stage: build

    %files
        /host/path/file1 /container/path/file1
        /host/path/file2 /container/path/file2

    %post
    	export DEBIAN_FRONTEND=noninteractive && \
        apt-get update && \
        apt-get install -y package1 package2
        
    %environment
    	export VAR1=foo
        export VAR2=bar
        
    %runscript
        do_stuff $1 $2 $3

When building this image, Apptainer first downloads the base image for a fresh installation of Ubuntu Jammy as a starting point. The ``%files`` section instructs Apptainer to copy two files into the image. The ``%post`` section contains commands to customise the image as needed, in this case installing some packages. The ``%environment`` section defines environment variables to be set within containers launched from the image. Variables defined here are not set for the commands in the ``%post`` section. Finally, the ``%runscript`` section defines the default actions that containers should perform when launched.

To build an image, use the following command:
::

	apptainer build my_image_file.sif my_definition_file.def

This instructs Apptainer to build an image according to ``my_definition_file.def`` and save it as a Singularity Image File ``my_image_file.sif``.

Launching Containers
====================

To launch a container, use the following command:
::

	apptainer run my_image_file.sif ARG1 ARG2 ARG3
    
In the previous example, this will cause ``do_stuff`` to be executed with the three arguments inside a container. By default, the container file system is read-only. Attempting to create or modify files will result in an error. To enable processes within the container to create files that remain after the container has finished, you can specify binds:
::

	apptainer --bind /host/path:/container/path run my_image_file.sif ARG1 ARG2 ARG3
    
In this case, Apptainer will make the file or directory at ``/host/path`` in the Red Deer file system available in the container file system at ``/container/path``. By default, Apptainer binds the current working directory and the home directory (``/home/$USER``). 

You may need to execute programs inside containers that expect to be able to create files in various locations (e.g., for logging or caching purposes). By default, such programs may fail because the container file system is read-only. As a workaround, you can pass the ``--writable-tmpfs`` flag. This enables programs to make changes to the container file system that will be discarded once the container has finished.

Further Reading
===============

* https://apptainer.org/docs/user/main/index.html documentation for Apptainer.
