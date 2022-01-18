Slurm Cheat Sheet
=================

The Cambridge HPC uses slurm to manage resources and schedule jobs. The following are a list of commands that may prove useful when managing slurm jobs.

For more detailed descriptions of slurm commands there are several available online resources including:

* `https://www.cism.ucl.ac.be/Services/Formations/slurm/2016/slurm.pdf <https://www.cism.ucl.ac.be/Services/Formations/slurm/2016/slurm.pdf>`_
* `https://slurm.schedmd.com/man_index.html <https://slurm.schedmd.com/man_index.html>`_

Additional information about each of the commands described, for example ``sinfo``, can also be obtained using the man command, for example ``man sinfo``.


Account Balance
---------------

Use the following command to get information about the amount of hours available for use on each of the accounts to which you have access:

	.. code-block:: console

		(host) $ mybalance

This will return a list similar to the following:

+------------+------------------------+-------------+-----------------+
|User / Usage|Account / Usage         |Account Limit|Available (hours)|
+============+========================+=============+=================+
|dc-webs1 / 1|DIRAC-TP001-CPU / 12,000|500,000      |488,000          |
+------------+------------------------+-------------+-----------------+
|dc-webs1 / 0|DIRAC-TP001-GPU /0      |2,000        |2,000            |
+------------+------------------------+-------------+-----------------+

* User is the name of the user whose account information is being shown
* Account shows the account names available to the user along with the amount of hours that have already been spent against that account
* Account Limit details the maximum number of hours allocated to each account
* Available lists the amount of hours still available to be spent


Getting Cluster Info
--------------------

To get information about the available nodes and partitions use the following command:

	.. code-block:: console

		(host) $ sinfo

This will return a list similar to the following. Each partition is listed with separate entries for each unique node state.

+---------+-----+----------+-----+-----+--------------------------------------------+
|PARTITION|AVAIL|TIMELIMIT |NODES|STATE|NODELIST                                    |
+=========+=====+==========+=====+=====+============================================+
|icelake  |up   |7-00:00:00|18   |idle |cpu-q-[58,97,99-100,169-176,397-400,411-412]|
+---------+-----+----------+-----+-----+--------------------------------------------+
|icelake  |down |7-00:00:00|1    |down |cpu-q-244                                   |
+---------+-----+----------+-----+-----+--------------------------------------------+

* PARTITION is the partition name
* AVAIL states whether the partition is currently available or not
* TIMELIMIT gives the maximum time limit for any user job in days-hours:minutes:seconds. `infinite` is displayed if there is no time limit
* NODES gives the number of nodes in this state
* STATE gives the current state of the nodes. The most common states are `allocated` if the node has been allocated to a job, `down` if the node is unavailable and `idle` if the node is unallocated
* NODELIST lists the names of every node in this state

Monitoring Jobs
---------------

To see the status of all jobs submitted by an individual user use the following command replacing `username` with your user name:

	.. code-block:: console

		(host) $ squeue -u username

This will return a list similar to the following:

+--------+---------+--------------------+--------+--+----+-----+----------------+
|JOBID   |PARTITION|NAME                |USER    |ST|TIME|NODES|NODELIST(REASON)|
+========+=========+====================+========+==+====+=====+================+
|51610182|icelake  |VLA-Combining-Images|dc-webs1|R |5:12|1    |cpu-q-79        |
+--------+---------+--------------------+--------+--+----+-----+----------------+
|51610183|icelake  |VLA-Basic-Imaging   |dc-webs1|PD|0:00|1    |                |
+--------+---------+--------------------+--------+--+----+-----+----------------+

* JOBID is the id assigned to the job by slurm
* PARTITION describes which partition the job is scheduled to be run on, icelake in the above example.
* NAME gives the name of the script as defined using the ``#SBATCH -J`` command
* USER is the name of the user who submitted the job, dc-webs1 in the above example
* ST is the state of the job. The most common states are `R` if the job is running, `PD` if the job is pending, `F` if the job has failed and `CD` if the job completed successfully
* TIME is the amount of time used by the process
* NODES is the number of nodes allocated to the job
* NODELIST(REASON) lists the names of the nodes allocated to the job

Controlling Jobs
----------------

To cancel a job use the following command replacing `jobid` with the identifier of the job to be cancelled:

	.. code-block:: console

		(host) $ scancel jobid





