.. _CASA-Toolkit:

Using the CASA Toolkit
======================

The CASA toolkit is a suite of functions that can be called directly via CASA's python interface. The functions within the toolkit are called by CASA itself when executing tasks. 

Users often use the CASA toolkit as it:
	* contains some functionality that is not available in a task
	* allows users to do something differently to how CASA's tasks operate
	* allows users to do only a part of what a task does potentially improving efficiency
	* provides direct access to the measurement set data

There is an introduction to the CASA toolkit published by the NRAO called `Beyond CASA Tasks <https://science.nrao.edu/science/meetings/2017/vla-data-reduction/Myers_CASA_ToolkitAndScripting_Oct2017_win.pdf>`_. A more comprehensive description of the functions available within the toolkit is given in the `CASA toolkit reference manual <https://casa.nrao.edu/docs/casaref/CasaRef.html>`_.

Below are given several examples of how to use the CASA toolkit as part of a slurm script. 

.. _CASA-Toolkit-getting-started:

Getting Started
---------------

In order to run a series of batch commands, the slurm script loads the CASA singularity and passes a python script containing all the commands to run to CASA. For example, in order to call a python script called ``master.py`` the slurm script would execute the command:

	.. code-block:: console

		singularity exec casa_latest.sif xvfb-run casa --nologger --log2term --nogui -c master.py

Examples of how to create a slurm script that passes a python script to CASA are given in :ref:`VLA-basic-imaging-create-the-slurm-script`, :ref:`Parallel-Processing-create-the-slurm-script` and :ref:`VLA-using-casa-plotms-create-the-slurm-script`.

In the above example, the python script, ``master.py``, contains all the calls to the standard CASA tasks such as ``flagdata``, ``gaincal`` and ``bandpass``. Examples of python scripts calling standard CASA commands can be found in :ref:`VLA-basic-imaging-running-as-a-script`, :ref:`Parallel-Processing-Create-the-casa-script` and :ref:`VLA-using-casa-plotms-create-the-casa-script`.

As well as calling tasks, the python script passed to CASA can also contain calls to the toolkit. However, for the sake of clarity and ease of maintenance it is often easier to encapsulate calls to the toolkit within their own python script. These sub-scripts are then called from the main python script. This is the method described here. For example, in order to call the python script called ``baselines.py`` the following line would have to be added into the main python script (``master.py`` in the above example):

	.. code-block:: python

		exec(open("./baselines.py").read())

Note the following points about this call:

	* The string literal contains the path of the script to be called.
	* All variables defined in the master script are available in the sub-script. For example, if the master script defines a variable ``vis=my_measurement_set.ms`` then the variable ``vis`` can be used within the sub-script (``baselines.py`` in the above example).

In all of the following examples it is assumed that the master script defines a variable called ``vis`` that contains the name of the measurement set. All other variables used in calls to the CASA toolkit are hard coded and would likely need to be changed to work similarly to the variable ``vis`` in a real-world application.

**Note on memory**

Some of the CASA toolkit functions are memory intensive. By default, when using the icelake nodes slurm allocates 3,380MB of memory per CPU and when using the icelake-himem nodes 6,760 MB are allocated per CPU. When the amount of memory allocated runs out the slurm script will fail with an out of memory error. If the allocated memory is insufficient more memory can be requested by adding the ``SBATCH --mem=####`` command to the slurm script. For example, in order to request 13,000 MB of memory the following command would be used:

	.. code-block:: console

		#SBATCH --mem=13000

It is worth noting that when using icelake memory is allocated in blocks of 3,380 MB. There is therefore little point in requesting 4,000 MB. Similarly, when using icelake-himem memory is allocated in blocks of 6,760 MB.

:ref:`Amp_v_Time.py <CASA-Toolkit-amp-v-time>`
----------------------------------------------

.. toctree::
	:maxdepth: 0
	:hidden:

	CASA_Toolkit_amp_v_time

Use this script to produce a plot similar to the one below which shows the visibility amplitudes plotted as a function of time and colorised by field.

	.. _fig-CASA-Toolkit-amp-v-time:
	.. figure:: images/amp_v_time.png
		:width: 600

		An example output from the amp_v_time.py script

:ref:`Baselines.py <CASA-Toolkit-baselines>`
--------------------------------------------

.. toctree::
	:maxdepth: 0
	:hidden:
	:titlesonly:

	CASA_Toolkit_baselines

Use this script to produce a plot similar to the one below which shows the baselines used throughout an observation.

	.. _fig-CASA-Toolkit-baselines:
	.. figure:: images/baselines.png
		:width: 600

		An example output from the baselines.py script

:ref:`Dirty_Image.py <CASA-Toolkit-dirty-image>`
------------------------------------------------

.. toctree::
	:maxdepth: 0
	:hidden:
	:titlesonly:

	CASA_Toolkit_dirty_image

Use this script to produce an image similar to the one below which shows the dirty image of an observation.

	.. _fig-CASA-Toolkit-dirty-image:
	.. figure:: images/dirty_image.png
		:width: 600

		An example output from the dirty_image.py script

