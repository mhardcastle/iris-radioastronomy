Parallel Processing
===================

This tutorial describes how to set up a slurm script to simultaneously process multiple VLA images. This tutorial processes two images taken of the wide angle tail 3C 465. One image was taken in A configuration and the other was taken in B configuration. Both images were taken in the L-band. The data used in this tutorial can be downloaded from the `VLA archive <https://science.nrao.edu/facilities/vla/archive/index>`_ by entering the project code ``12A-195`` and choosing the B-configuration data taken in the 28th May 2012 and the A-configuration data taken on the 31st October 2012.

This script makes use of the ``parallel`` module to manage resources and enable parallel processing. The parallel module utilises all available processors, so that several processes can be run in parallel with each other. If there are more processes called than there are available processors, the parallel module will wait for a process to complete before starting the next process. For example, if there are three tasks (A, B and C) and only two processors parallel will initially execute tasks A and B. It will then only start running task C once either task A or B has completed.


.. _Parallel-Processing-getting-started:

Getting Started
---------------

#. After downloading the data untar it using the command

	.. code-block:: console

		(host) $ tar -xvf 12A-195.sb12378614.eb13812032.56231.2797265625.ms.tar
		(host) $ tar -xvf 12A-195.sb7351094.eb10491731.56075.655723206015.ms.tar

   This will unpack the two measurement sets:

	* 12A-195.sb12378614.eb13812032.56231.2797265625.ms
	
	* 12A-195.sb7351094.eb10491731.56075.655723206015.ms

   Both observations contain the following fields:

	+-----+----------+------------------------------------------+
	|Field|Field Name|Comments                                  |
	+=====+==========+==========================================+
	|0    |3C48      |Setup scan                                |
	+-----+----------+------------------------------------------+
	|1    |3C48      |Primary Calibrator                        |
	+-----+----------+------------------------------------------+
	|2    |J2340+2641|Phase Calibrator                          |
	+-----+----------+------------------------------------------+
	|3    |3C 465    |Target	                            |
	+-----+----------+------------------------------------------+
	|4    |J0313+4120|Phase Calibrator (unused in this tutorial)|
	+-----+----------+------------------------------------------+
	|5    |3C83.1B   |Target (unused in this tutorial)          |
	+-----+----------+------------------------------------------+

	
#. The A configuration observation was taken on the 31st October 2012 between 06:45 and 09:15. The B configuration image was taken on the 28th May 2012 between 15:44 and 18:13. The operators log for both observations can be downloaded from `here <http://www.vla.nrao.edu/cgi-bin/oplogs.cgi>`_.

#. Load the singularity module by entering:

	.. code-block:: console

		(host) $ module load singularity

#. Download the singularity image created in :ref:`use-of-singularity`. The following command downloads the most up to date image which is 1.3 GB and so this may take some time!

	.. code-block:: console

		(host) $ singularity pull library://mhardcastle/default/casa

Create the slurm script
-----------------------

#. The slurm script used in this tutorial is called :download:`VLA_Parallel_Processing.slurm <scripts/vla/VLA_Parallel_Processing.slurm>` and contains the following lines of code:

	.. code-block:: console

		#!/bin/bash
		#SBATCH -J VLA-Parallel-Processing
		#SBATCH -A DIRAC-TP001-CPU
		#SBATCH -p icelake
		#SBATCH --nodes=1
		#SBATCH --ntasks=2
		#SBATCH --time=03:00:00
		#SBATCH --mail-type=ALL
		#SBATCH --no-requeue

		#! Enter the script to run here
		. /etc/profile.d/modules.sh
		module load rhe18/default-icl
		module load singularity
		module load parallel

		# Describe the measurement sets to be processed
		INPUTS=("12A-195.sb12378614.eb13812032.56231.2797265625.ms A L" "12A-195.sb7351094.eb10491731.56075.655723206015.ms B L")

		# Set up the srun command
		# The -N1 -n1 options allocate a single core to each task
		srun="srun --exclusive -N1 -n1"

		# Set up the parallel command
		# The delay of 0.2 prevents overloading the controlling node
		# -j is the number of tasks to run simultaneously
		# --joblog and --resume combine to create a task log that can be used to monitor progress
		parallel="parallel --delay 0.2 -j $SLURM_NTASKS --joblog runtask.log --resume"
		
		# Run the command
		$parallel "$srun singularity exec casa_latest.sif casa -c VLA_Process_3C465_Images.py {1} ::: "${INPUTS[@]}"

Note the following points about the slurm script:

	* The command ``#SBATCH -J VLA-Parallel-Processing`` names the job VLA-Processing-Multiple-Images
	* The command ``#SBATCH -A DIRAC-TP001-CPU`` is the name of the project under which time has been allocated
	* The command ``#SBATCH -p icelake`` ensures we are using the icelake cluster
	* By default slurm allocates one cpu per task and so the commands ``#SBATCH --nodes=1``  and ``#SBATCH --ntasks=2`` combine to ask for two CPUs on a single node. On icelake each node has 76 CPUs with all CPUs on the same node sharing memory resources. Changing the nodes variable to 2 would have the effect of asking for two CPUs on different machines. Since the CPUs would no longer be sharing memory each task will run slightly quicker however the job is likely to take longer to schedule and is an inefficient use of resources.
	* The command ``#SBATCH --time=03:00:00`` is requesting 3 (wall-clock) hours of processing time.
	* The command ``#SBATCH --mail-type=ALL`` means email messages will be sent at the start and end of the job or (if applicable) when an error occurs. To disable this set the option to ``NONE``.
	* The command ``#SBATCH --no-requeue`` means that if this job is interrupted by a node failure/system downtime it will `not` be automatically rescheduled.
	* The command ``. /etc/profile.d/modules.sh`` enables the module command
	* The command ``module load rhe18/default-icl`` loads the basic environment needed by icelake
	* The two module load commands load the singularity and parallel modules
	* The `INPUTS` command defines a list of parameters that will be passed to the casa script. In this example the list is typed directly into the script but this could be altered to read the parameters from a file.
	* The ``srun --exclusive -n1 -N1`` allocates exclusive use of a single core to each task
	* The ``parallel --delay 0.2 -f $SLURM_NTASKS`` tells the parallel process that we are running ``ntasks`` parallel processes. In this case ntasks=2, so we are running two parallel processes.
	* The ``$parallel...`` command iterates through the ``INPUTS`` list calling the ``srun`` command for each element in the list. For each call of ``srun``, parallel replaces the placeholder `{1}` with the list element. The command ``srun`` uses the casa_latest.sif singularity to call the VLA_Process_3C465_Images.py script within casa, sending it the parameters within the `{1}` placeholder.

.. _Parallel-Processing-Create-the-casa-script:

Create the CASA script
----------------------

#. The casa script used in this tutorial is called :download:`VLA_Process_3C465_Images.py <scripts/vla/VLA_Process_3C465_Images.py>` and is based on the code used in the :ref:`VLA-basic-imaging-getting-started` tutorial. The download file contains the full script with a summarised version given below:

	.. code-block:: console

		from sys import argv

		params = argv[1].split()
		vis = params[0]
		config = params[1]
		band = params[2]

		smoothed_vis = vis[:-3]+'-smoothed.ms'
		primary_calibrator = '1'
		phase_calibrator = '2'
		target_field='3'
		refant = 'ea21'

		caltable_antpos = smoothed_vis[:-3]+".antpos"

		listobs(vis=vis, verbose=True, listfile=vis[:-3]+'.listobs')

		# Standard casa data flagging and calibration commands go here

		# Set up the variables used in imaging. The values depend upon the configuration
		if config=='A':
			cell=['0.25arcsec','0.25arcsec']
			imsize=[11250,11250]
			scales=[0,10,26]
		elif config=='B':
			cell=['1arcsec','1arcsec']
			imsize=[3072,3072]
			scales=[0,9,22]
		elif config=='C':
			cell=['3arcsec','3arcsec']
			imsize=[1024,1024]
			scales=[0,9,23]
		elif config=='D':
			cell=['10arcsec','10arcsec']
			imsize=[320,320]
			scales=[0,9,23]

		# Extract data used for imaging from the measurement set
		rms = stats['rms'][0]

		tclean(vis=smoothed_vis, field=target_field, imagename=smoothed_vis[:-3]+'-Clean', cell=cell, imsize=imsize, niter=20000, threshold=str(rms*5)+'Jy', stokes='I', deconvolver='multiscale', scales=scales, smallscalebias=0.9, weighting='briggs', robust=0.5, pbcor=True)

Note the following points about the casa script:

	* The ``params = argv[1].split()`` command imports the parameter string that was supplied by the call to parallel in the slurm script and splits it into its components. The next few lines populate the variables used throughout the script. In this example the name of the measurement set as well as the VLA configuration and band of the measurement set are all supplied. This could be expanded to include any additional information desired.
	* The ``listobs`` and ``tclean`` commands give a simple example of how the variables can be used within the script
	* The nested ``if`` block is an example of how to use the data to set up the variables used during imaging. This script only uses the ``config`` variable but this could easily be expanded to include additional variables such as ``band``.

Running the scripts
-------------------

#. Log on to the `Cambridge CSD3 system <https://docs.hpc.cam.ac.uk/hpc/index.html>`_ as described in :ref:`cambridgehpc-login`. 

#. If necessary download the casa singularity as described in :ref:`VLA-basic-imaging-getting-started`.

#. Run the slurm script by entering

	.. code-block:: console

		(host) $ sbatch VLA_Parallel_Processing.slurm

#. Check the casa `.log` and `runtask.log` files for any errors. An exit value of `1` in the `runtask.log` file indicates a terminal error occurred and the process was terminated prematurely.












