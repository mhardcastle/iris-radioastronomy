Cambridge CSD3 cheat sheet
==========================

The `Cambridge CSD3 system
<https://docs.hpc.cam.ac.uk/hpc/index.html>`_ is documented
extensively on its own web pages. These are internal notes for quick
start for our project.

.. _cambridgehpc-login:

Login
-----

Log in with your username to the CPU system (DIRAC username):

	.. code-block:: console

		(host) $ ssh <username>@login-cpu.hpc.cam.ac.uk

If you have set up an authorized key, you may use this to bypass the
password prompt:

	.. code-block:: console

		(host) $ ssh -i ~/.ssh/dirac_rsa <username>@login.hpc.cam.ac.uk

Work area
---------

The project shared disk space is ``/rds/project/rds-bRdYdViqoGA/``.
Make yourself a working directory there.

Jobs
----

The system uses Slurm (though for those familiar with Torque, ``qsub``
and ``qstat`` commands work more or less as you would expect on the
login nodes).

There are three main types of compute nodes on the cluster, Skylake,
Cascade Lake and Ice Lake (from earlier to later generation). Skylake
nodes are 32-core nodes, Cascade Lake 56 core, and Ice Lake 76 core
nodes. All are Intel-based. These show up as partitions (like Torque
queues) on the cluster, i.e. you are explicitly selecting the type of
machine you will get when you submit to the cluster using the
partitions ``skylake``, ``cclake`` or ``icelake``. There are also
himem (high-memory) version of each partition.

To get a single core for testing purposes on one of these machines do
e.g.

	.. code-block:: console

		(CSD3) $ sintr -p icelake

This drops you in a ``screen`` session on a compute node. You can
specify wall time, numbers of cores etc on the command line.

To run a batch job do e.g.

	.. code-block:: console

		(CSD3) $ sbatch example_slurm_script

You can find template job scripts in
``/usr/local/Cluster-Docs/SLURM``. A useful option in batch mode is
``#SBATCH --mail-type=ALL`` which ensures that you will be e-mailed on
start, end and error. Job output appears in the directory where you
ran the ``sbatch`` command.

To view the queue in native Slurm mode use the ``squeue`` command.

Note that if (and only if) you have a Slurm job running on a compute
node you are allowed to ``ssh`` into it to check on the job, run
``htop`` etc.
		
Modules
-------

Modules work as on the Hertfordshire system, e.g. ``module load
singularity`` gets you access to the singularity command. There are
many more modules available though.
