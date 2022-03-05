LOFAR processing with ddf-pipeline
==================================

ddf-pipeline <https://github.com/mhardcastle/ddf-pipeline> is the
LOFAR Surveys Key Science Project standard reduction pipeline for
Dutch-baseline data. It is designed for reduction of data which has
already been processed through prefactor
<https://git.astron.nl/eosc/prefactor3-cwl>. It also contains a number
of utility routines for working with the archived LoTSS data.

Setup
-----

ddf-pipeline comes with a singularity recipe. You can build the
singularity image from the recipe
<https://github.com/mhardcastle/ddf-pipeline/blob/master/ddf-py3.singularity>
or pull from the singularity repository:

       .. code-block:: console
		       
		       (host) $ singularity pull library://mhardcastle/default/ddf-pipeline

Interactive use
---------------

Use ``singularity shell`` to have access to a shell in which you can
run commands in the ddf-pipeline environment.

      .. code-block:: console

		      (host) $ singularity shell ddf-pipeline_latest.sif

For example here you can run data preparation commands such as
``download_field.py`` and ``make_mslist.py``.
		      
Use in jobs
-----------

The following is a basic Slurm script to run ddf-pipeline itself from
the singularity environment. You'll need to adjust the working
directory and other environment variables.

.. code-block:: console

		#!/bin/bash

		#! Call with --export FIELD=Pxxx+xx

		#SBATCH -J ddf-pipeline
		#SBATCH --nodes=1
		#SBATCH --ntasks=32
		#SBATCH --time=36:00:00
		#SBATCH --mail-type=ALL
		#SBATCH --no-requeue
		#SBATCH -p skylake-himem

		. /etc/profile.d/modules.sh
		module purge               
		module load rhel7/default-peta4 
		module load singularity
		
		application="singularity run ddf-pipeline-latest.sif"
		options="pipeline.py tier1-config.cfg"
		workdir="/rds/project/rds-bRdYdViqoGA/mjh/$FIELD"
		
		export OMP_NUM_THREADS=1
		
		export DDF_PIPELINE_CATALOGS=/rds/project/rds-bRdYdViqoGA/mjh/bootstrap
		export DDF_PIPELINE_DATABASE=True
		export DDF_PIPELINE_CLUSTER=Cambridge

		CMD="$application $options"

		cd $workdir

		JOBID=$SLURM_JOB_ID

		echo -e "JobID: $JOBID\n======"
		echo "Time: `date`"
		echo "Running on master node: `hostname`"
		echo "Current directory: `pwd`"

		echo -e "\nExecuting command:\n==================\n$CMD\n"

		eval $CMD 

The script illustrates the use of an environment variable to determine
what field will be processed. Call with


      .. code-block:: console

		      (host) $ sbatch --export FIELD=P123+45 ddf-pipeline.sh

Note that ideally ddf-pipeline requires a week's walltime, so you
should be prepared for several restarts if the local system does not
allow this. You can use the ``--dependency=afterany:JOBID`` option to
``sbatch`` to stack up a set of dependent jobs that will give the
required walltime.
		      

Self-calibration
----------------

This section describes how to use the self-calibration scripts to
improve the calibration of public or private LoTSS data. [TBD]
