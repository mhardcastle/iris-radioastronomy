.. _VLA-using-casa-plotms:

Using Casa's Plotms
===================

``plotms`` is a GUI tool supplied with casa for plotting visibility and calibration data. The HPC services offered by, for example, the `Cambridge CSD3 system
<https://docs.hpc.cam.ac.uk/hpc/index.html>`_, are intended to be used with batch submission scripts where GUI tools cannot be used. Fortunately, ``plotms`` can be called from the command line and used to save plots without using the GUI functionality. This tutorial describes how to use ``plotms`` as part of a batch submission script without using its GUI functionality. This allows users to exploit the full functionality of ``plotms``.

.. _VLA-using-casa-plotms-buiding-the-singularity-container:

Building the Singularity Container
----------------------------------

#. The basic casa singularity described in :ref:`use-of-singularity` must be modified in order to allow access to ``plotms`` from within a submission script. The following script, named :download:`casa_plotms.def <scripts/vla/casa_plotms.def>`, can be used to create a singularity container capable of running ``plotms`` as part of a batch submission script:

	.. code-block:: bash

		Bootstrap: docker
		From: scientificlinux/sl

		%post
		yum -y update
		yum -y upgrade
		yum -y install xorg-x11-server-Xvfb
		yum -y install wget perl less

		#Install casa dependencies
		yum -y install fontconfig freetype freetype-devel fontconfig-devel libstdc++

		#Install casa
		cd /usr/local
		wget https://casa.nrao.edu/download/distro/casa/release/rhel/casa-6.4.3-27-py3.8.tar.xz
		tar xf casa-6.4.3-27-py3.8.tar.xz
		rm casa-6.4.3-27-py3.8.tar.xz

		#The above casa installation contains three AppImage files
		#AppImages only work within singularity containers if they are unpacked
		#The following replaces the three packed AppImages with unpacked versions
		cd /usr/local/casa-6.4.3-27/lib/py/lib/python3.8/site-packages/casaplotms/__bin__/
		./casaplotms-x86_64.AppImage --appimage-extract
		chmod -R 755 /usr/local/casa-6.4.3-27/lib/py/lib/python3.8/site-packages/casaplotms/__bin__/squashfs-root/
		rm ./casaplotms-x86_64.AppImage
		ln -s ./squashfs-root/AppRun ./casaplotms-x86_64.AppImage

		cd /usr/local/casa-6.4.3-27/lib/py/lib/python3.8/site-packages/casaplotserver/__bin__/
		./casaplotserver-x86_64.AppImage --appimage-extract
		chmod -R 755 /usr/local/casa-6.4.3-27/lib/py/lib/python3.8/site-packages/casaplotserver/__bin__/squashfs-root/
		rm ./casaplotserver-x86_64.AppImage
		ln -s ./squashfs-root/AppRun ./casaplotserver-x86_64.AppImage

		cd /usr/local/casa-6.4.3-27/lib/py/lib/python3.8/site-packages/casaviewer/__bin__/
		./casaviewer-x86_64.AppImage --appimage-extract
		chmod -R 755 /usr/local/casa-6.4.3-27/lib/py/lib/python3.8/site-packages/casaviewer/__bin__/squashfs-root
		rm ./casaviewer-x86_64.AppImage
		ln -s ./squashfs-root/AppRun ./casaviewer-x86_64.AppImage

		%environment
		export LC_ALL=C
		export PATH=/usr/local/casa-6.4.3-27/bin:$PATH

		%runscript
		xvfb-run casa --nologger --log2term --nogui

		%labels
		Author IRIS-Radioastronomy

	Note the following points about the definition script:

		* The ``xorg-x11-server-Xvfb`` (X Virtual Frame Buffer) is an X server package that allows software that would normally require an X display to be run on machines with no display hardware. Rather than interacting with a monitor ``plotms`` interacts with this package.
		* When casa is installed, it also installs three AppImage files one of which, ``casaplotms-x86_64.AppImage``, is used to run ``plotms``. AppImage's require access to FUSE in order to run. However, using FUSE to mount a filesystem inside a container may undermine the security features offered by singularity. This script therefore adopts an alternative, safer, solution and unpacks/extracts the AppImage before redirecting any calls to the original AppImage to the unpacked version. Whilst strictly only the ``casaplotms`` AppImage is needed to run ``plotms`` this script unpacks all three AppImages for completeness.
		* The runscript command ``xvfb-run casa ...`` uses Xvfb to launch casa so that all calls to the display are redirected to Xvfb.

#. Using this script a singularity container, in this case named ``casa_plotms.sif``, can be built by entering the following command:

.. code-block:: console

	(host) $ singularity build --fakeroot casa_plotms.sif casa_plotms.def


.. _VLA-using-casa-plotms-create-the-slurm-script:

Create the slurm script
-----------------------

#. The slurm script used in this tutorial is called :download:`casa_plotms.slurm <scripts/vla/casa_plotms.slurm>` and contains the following lines of code:

	.. code-block:: bash

		#!/bin/bash
		#SBATCH -J Casa-Plotms
		#SBATCH -A DIRAC-TP001-CPU
		#SBATCH -p icelake
		#SBATCH --nodes=1
		#SBATCH --ntasks=1
		#SBATCH --time=00:45:00
		#SBATCH --mail-type=ALL
		#SBATCH --no-requeue

		#! Enter the script to run here
		. /etc/profile.d/modules.sh
		module load rhel8/default-icl
		module load singularity
		singularity exec casa_plotms.sif xvfb-run casa -c 3C391_script.py

This script is nearly identical to the one described in :ref:`VLA-basic-imaging`. The important difference is in the last line which executes a command within the singularity container ``casa_plotms.sif``. The execute command does not trigger the run script within the singularity and so the command ``xvfb-run casa ...`` is needed to use Xvfb to launch casa which in turn calls the casa script named 3C391_script.py. 

.. _VLA-using-casa-plotms-create-the-casa-script:

Create the CASA script
----------------------

#. The casa script used in this tutorial is named :download:`3C391_script.py <scripts/vla/3C391_script.py>`. This script follows the `VLA Continuum Tutorial 3C 391 <https://casaguides.nrao.edu/index.php?title=VLA_Continuum_Tutorial_3C391-CASA6.2.0>`_ to generate an image of the supernova remnant 3C 391. The measurement set used in this tutorial can be downloaded from the VLA tutorial website. Shown below are two of the calls made to ``plotms`` within the script:

	.. code-block:: python

		...

		plotms(vis=vis,selectdata=True,correlation='RR,LL',averagedata=True,avgchannel='64',coloraxis='field',showgui=False,plotfile='plotms_3c391-Time.png',highres=True)

		...

		plotms(vis='3c391_ctm_mosaic_10s_spw0.G0all',xaxis='time',yaxis='phase',coloraxis='corr',iteraxis='antenna',exprange='all',plotrange=[-1,-1,-180,180],showgui=False,plotfile='plotms_3c391-G0all-phase.png',highres=True)	

		...


	Note the following points about the casa script
		* Every call to ``plotms`` sets the argument ``showgui=False``. This is necessary in order for the script to work.
		* Every call to ``plotms`` sets the argument ``highres=True``. Setting this variable to False causes it to save the images using the screen resolution which fails causing it to revert to saving in high resolution. Setting the ``highres`` argument to True causes it to go straight to saving in high resolution saving time
		* If using the ``iteraxis`` variable, ``exprange`` must not be null. In the above example we have set ``exprange='all'`` which causes ``plotms`` to save one image for every ``iteraxis`` page.

.. _VLA-using-casa-plotms-running-the scripts:

Running the scripts
-------------------

#. Log on to the `Cambridge CSD3 system <https://docs.hpc.cam.ac.uk/hpc/index.html>`_ as described in :ref:`cambridgehpc-login`.

#. If necessary install the plotms-enabled singularity container described in :ref:`VLA-using-casa-plotms-buiding-the-singularity-container`

#. Run the slurm script by entering

	.. code-block:: console

		(host) $ sbatch casa_plotms.slurm

#. Check the casa `.log` and `runtask.log` files for any errors. An exit value of `1` in the `runtask.log` file indicates a terminal error occurred and the process was terminated prematurely.

Generating Single Plots
-----------------------

When generating a small number of images, rather than running a batch script it may be more efficient to generate images using command line prompts. To do this:

#. Log on to the `Cambridge CSD3 system <https://docs.hpc.cam.ac.uk/hpc/index.html>`_ as described in :ref:`cambridgehpc-login`.

#. If necessary install the plotms-enabled singularity container described in :ref:`VLA-using-casa-plotms-buiding-the-singularity-container`

#. Run the plotms-enabled singularity container by entering

	.. code-block:: console
	
		(host) $ run singularity casa_plotms.sif

#. This will load the singularity and start casa automatically returning the casa command prompt. In order to generate an image enter a ``plotms`` command making sure to set ``showgui=False`` and setting the argument ``plotfile`` to the name of the file you wish to create. If using the ``iteraxis`` argument it is advisable to also set the ``exprange`` argument to tell plotms which of the iteraxis pages you wish to be saved. For example:

	.. code-block:: console

		(CASA) $ plotms(vis='3c391_ctm_mosaic_10s_spw0.G0',xaxis='time',yaxis='phase',coloraxis='corr',field='J1331+3030',iteraxis='antenna',exprange='all',plotrange=[-1,-1,-180,180],timerange='08:02:00~08:17:00',showgui=False,plotfile='plotms_3c391-G0-phase.png',highres=True)
