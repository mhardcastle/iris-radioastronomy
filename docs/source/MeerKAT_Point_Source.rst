.. _MeerKAT_Point_Source:

MeerKAT Point Source Catalog
=================

This guide is both an example of how to create containers which can be used to process survey data and a guide on using IRIS resources to process the MeerKAT point source catalog and spectral index fitting.

.. _MeerKAT-Point-Source-getting-started:

Building the Singularity Container
---------------

The basics of creating a Singularity container are covered in :ref:'use-of-sunglarity', however the example given focuses on create a CASA container. We want to create a container that uses a specific python version, python packages, and custom python programs and collects them in a container so anyone can reproduce the same results when processing MeerKAT data.

Load the singularity module by entering:

	.. code-block:: console

		(host) $ module load singularity

The MeerKAT singularity container takes a command line input to run one of several data-reduction python programs.

Creating Python Scripts to Run Slurm
-----------

The MeerKAT processing python programs are designed to run on induvidual data cubes. This is due to several of the programs taking 1-4 hours to processes a cube due to the large number of point sources.

The code below is an example of how to write a python script which will submit a number of jobs to slurm. You will need both a python program submitting the jobs as well as a slurm file providing the proper. Note, this file is NOT within the container. It is an outside program so that we can run the container multiple times.
	
	.. code-block:: console

		File Edit Options Buffers Tools Python Help                                                                                                                                                                  
		#!/usr/bin/env python3                                                                                                                                                                                       
		# -*- coding: utf-8 -*-                                                                                                                                                                                      

		import os
		import subprocess

		# =============================================================================                                                                                                                              
		# Top layer python script to set multiple jobs going on the cluster.                                                                                                                                         
		# =============================================================================                                                                                                                              

		filepath = '/rds/project/rds-bRdYdViqoGA/bsmart/MeerKAT/Mosaic_Planes/'
                                                                                                                                                         
		f=os.listdir (filepath)

		for filename in f:

        		folder=filepath+filename+'/'
        		sbatch_command = """sbatch --export=folder='{0}' /rds/project/rds-bRdYdViqoGA/bsmart/MeerKAT/Singularity/run_bane.sh""".format(folder)
        		print(sbatch_command)
        		print(folder)
        		print('Submitting job')
        		exit_status = subprocess.call(sbatch_command, shell=True)

        		if exit_status is 1:
                		print('Job failed to submit')

				print('Done submitting jobs!')
	
The above program imports both os and suprocess so that we can use console commands to submit multiple slurm. It takes a filepath to a folder containing all the meerkat cubes and sends each cube as an input to a Singularity container. I will break down induvidual lines for clarity.

	.. code-block:: console
		filepath = '/rds/project/rds-bRdYdViqoGA/bsmart/MeerKAT/Mosaic_Planes/'
		f=os.listdir (filepath)

Filepath is the path containing all of the cube folders that will be processed. In each of the MeerKAT scripts it stays the same, and os.listdir then reads in each of the folder names into variable f.

	.. code-block:: console
		for filename in f:

        		folder=filepath+filename+'/'
        		sbatch_command = """sbatch --export=folder='{0}' /rds/project/rds-bRdYdViqoGA/bsmart/MeerKAT/Singularity/run_bane.sh""".format(folder)
        		print(sbatch_command)
        		print(folder)
        		print('Submitting job')
        		exit_status = subprocess.call(sbatch_command, shell=True)

        		if exit_status is 1:
                		print('Job failed to submit')

				print('Done submitting jobs!')
				
The aboce code takes the filepath and adds to it each of the folder names within Mosaic_Planes. I then create the sbatch_command using the new folder variable within the format and write the sbatch command. In this case, {0} tells the command to read the first variable in .format(). If I had included two variables .format(var1,var2) and wanted to access var2, I would use {1} and so forth.
	
Creating Slurm Job Submission file
-----------	
	
The bellow code will be an example of a slurm job submission file which will be 
	
	.. code-block:: console

		#!/bin/bash                                                                                                                                                                                              
		#SBATCH -A DIRAC-TP001-CPU                                                                                                                                                                               
		#SBATCH -p skylake                                                                                                                                                                                       
		#SBATCH --ntasks 32                                                                                                                                                                                      
		#SBATCH --time=36:00:00                                                                                                                                                                                  
		#SBATCH --output=banetest_%j.log                                                                                                                                                                         
		#SBATCH --mail-type=ALL                                                                                                                                                                                  
		#I) tasks will there be in total? (<= nodes*32)                                                                                                                                                          

		#! The skylake/skylake-himem nodes have 32 CPUs (cores) each.                                                                                                                                            

		#! Number of nodes and tasks per node allocated by SLURM (do not change):                                                                                                                                

		numnodes=$SLURM_JOB_NUM_NODES
		numtasks=$SLURM_NTASKS
		mpi_tasks_per_node=$(echo "$SLURM_TASKS_PER_NODE" | sed -e  's/^\([0-9][0-9]*\).*$/\1/')

		#! Optionally modify the environment seen by the application                                                                                                                                             

		#! (note that SLURM reproduces the environment at submission irrespective of ~/.bashrc):                                                                                                                \           
		. /etc/profile.d/modules.sh                # Leave this line (enables the module command)  
		module purge                               # Removes all modules still loaded 
		module load rhel7/default-peta4            # REQUIRED- loads the basic environment 
		module load singularity
		pwd; hostname; date
		FILENAME=${folder}
		#! Full path to application executable:                                                                                                                                                                  
		application="singularity run -B/rds/project/rds-bRdYdViqoGA/bsmart/MeerKAT meerkat_test.sif"
		
		#! Run options for the application:                                                                                                                                                                      
		options="python3 /usr/local/MeerKAT/python_programs/auto_bane_cluster.py --input_folder=${FILENAME}"

		#! Work directory (i.e. where the job will run):                                                                                                                                                         
		workdir="/rds/project/rds-bRdYdViqoGA/bsmart/MeerKAT/Singularity/"  # The value of SLURM_SUBMIT_DIR sets workdir to the directory                                                                        

                             # in which sbatch is run.                                                                                                                                                   
		#! Are you using OpenMP (NB this is unrelated to OpenMPI)? If so increase this             

This particular job requires a path to the data be provided. The previous folder variable that was in the python program is avalaible to the slurm script.

To run singularity using slurm, we need to load the singularity module within the slurm script. In the above script, this is done with the following lines.

	.. code-block:: console
		. /etc/profile.d/modules.sh                # Leave this line (enables the module command)  
		module purge                               # Removes all modules still loaded 
		module load rhel7/default-peta4            # REQUIRED- loads the basic environment 
		module load singularity
		
After singularity is loaded in the slurm script, any number of processes in the singularity container can be run. In this example, we are giving slurm the singularity command as an application. The singularity command loads in the desired container, and options then passes the commands to the container so that we can run the desired applications within the container. In this example, we are asking the container to run the program auto_bane_cluster.py in python3 with an input variable "input_folder". In this example, ${FILENAME} is a variable which was passed from the original python3 script outside the container and into this script so multiple jobs can be run on different files. 

	.. code-block:: console
		#! Full path to application executable:  
		application="singularity run -B/rds/project/rds-bRdYdViqoGA/bsmart/MeerKAT meerkat_test.sif
		
		#! Run options for the application:  
		options="python3 /usr/local/MeerKAT/python_programs/auto_bane_cluster.py --input_folder=${FILENAME}"


Best Practice Notes
-----------

There are several things you want to keep in mind when creating a container or writing a script to submit multiple jobs:

- You want to keep your container as small as possible. The idea is you are creating a purpose built containerised environment that can process your data the way you want, and nothing else. This also means your data should not be within the container. It will be passed in outside of the container, and the results will be processed outside the container.
- Make sure all of the programs inside your container have generalized paths. It is better to pass in a path to your data rather than have it coded in. This allows more flexibility.
- Make sure all of the programs inside your container have generalized paths. It is better to pass in a path to your data rather than have it coded in. This allows more flexibility.
- In the following examples, a job may take anywhere from 20 minutes to 2-3 hours. While an induvidual job does not tie up resources for long, the number of jobs means your job may end up in the queue. If you do not recieve an email telling you the job is processing immediatly, first check the queue to see if it has been assigned yet or if it is waiting. Be careful not to accidentally resubmit, otherwise the job will end up inthe queue twice.


Running MeerKAT Data Processing
-----------
Processing the MeerKAT data from the cubes is split up into several different programs and is dependant on three file locations. For this example, I have a master folder called MeerKAT which contains all of the data needed to create the spectral index catalog.
 
File Setup
-----------
To processes the MeerKAT data, you need a folder which contains the following files:
	- Aegean_Test_Catalogue_Full
	- Mom0_comp_catalogs
	- Mosaic_Planes
	- Singularity
	- python_scripts

The first three folders are required as they contain all of the relevant MeerKAT data that has been processed. The Aegean_Test_Catalogue_Full contains the folders:
	- Mom0_comp_catalogs  
	- Mom0_comp_ds9_regions  
	- Mom0_isle_catalogs  
	- Mom0_isle_ds9_regions

and can be found by accessing PATH_HERE

The Mom0_comp_catalogs folder contains all of the moment zero maps of the cubes. These are used to process the average background used.
	- Mom0_comp_catalogs  
	- Mom0_comp_ds9_regions  
	- Mom0_isle_catalogs  
	- Mom0_isle_ds9_regions

Process Background
-----------
 
 The first step to processing the MeerKAT data cubes is to create the backgrounds for the 0th moment maps. The induvidual backgrounds for each plane have been seperately processed, and the combined zeroth moment is needed to background subtract. The background is processed with the BANE program, part of the Aegean processing package used to make the full point source catalog created by Mubela Mutale and found on the MeerKAT survey repository. All commands assume you are starting in the MeerKAT folder.
 
 	.. code-block:: console
	
		cd python_programs
		python3 jobSubmitter_Bane.py

This job submitter is the same one used in the example above, and sends each induvidual cube file path to a singularity container submitted to slurm to process the background. The output files are written to the Mosaic_Plane folder for each cube.

Process Photometric Catalog
-----------
Once the backgrounds have been processed, run the following program.

 	.. code-block:: console
	
		python3 jobSubmitter_Phot.py

This program submits induvidual cubes to slurm, where it reads in the Aegean point source catalog and uses the Bane backgrounds and catalog to measure the photometry for each wavelength in the cube using astropy photometry. These are written to indivudial photometry files for each layer within a given cubes Mosaic_Plane folder, and use the background files to calculate the noise in each anulus.

Process Spectral Indices and Clean Up Catalog
-----------

Now that the photometry at each wavelength has been calculated, we can put together a spectral index catalog for each of the induvidual points. The following programs throw out points which are not bright enough and ones which do not have enough measurements in each wavelength.

First, the tables need to be properly organized with the correct observation frequencies. To do this

 	.. code-block:: console
	
		python3 jobSubmitter_Freq.py

 

Merging Catalogs
-----------
After all the data has been processed and the catalog columns have been organized and cleaned, this program takes all of the different induvidual cube catalogs and merges them into one large catalog, giving each source a designated reference number in the process.

 	.. code-block:: console
		python3 jobSubmitter_Combi.py

The combined point source catalog is written to the MeerKAT folder. Once the catalogs have been combined, the last step is to assign an ID to all of the sources. To do this, run the following program. This will likely be combined with jobSubmitter_Combi.py in the future.

	.. code-block:: console
		python3 jobSubmitter_ID.py
		














