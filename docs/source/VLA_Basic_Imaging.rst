.. _VLA-basic-imaging:

VLA Basic Imaging
=================

This tutorial uses the measurement set from the CASA tutorial `VLA Continuum Tutorial 3C 391 <https://casaguides.nrao.edu/index.php?title=VLA_Continuum_Tutorial_3C391-CASA6.2.0>`_ to generate an image of the supernova remnant 3C 391. The data in the measurement set was taken using a bandwidth of 128 MHz centred at 4.6 GHz with the VLA in D-configuration. The data set includes polarisation data that is not used in this tutorial.

.. _VLA-basic-imaging-getting-started:

Getting Started
---------------

#. The data required for this workflow can be downloaded from the CASA tutorial web page `VLA Continuum Tutorial 3C 391 <https://casaguides.nrao.edu/index.php?title=VLA_Continuum_Tutorial_3C391-CASA6.2.0>`_. N.B. This data set has been modified to include only the data necessary to run this tutorial, if desired the full observation can be downloaded fro the `VLA Archive <https://archive.nrao.edu/archive/advquery.jsp>`_ using the archive file id ``TDEM0001_sb1218006_1.55310.33439732639``. If downloading from the VLA archive it is normally easiest to download it as a tar file.

   After downloading the data untar it:

	.. code-block:: console

		(host) $ tar -xzvf 3c391_ctm_mosaic_10s_spw0.ms.tgz

   There are four fields in this observation

	* \field 0 is 3C 286 (also referred to as J1331+3030), the bandpass calibrator
	* \field 1 is J1822-0938, the phase calibrator
	* \fields 2-8 inclusive are the mosaicked fields that make up 3C 391, the target
	* \field 9 is 3C 84 (also referred to as J0319+4130), the polarization calibrator. This field is unused in this workflow
	
#. This observation was taken on the 24th April 2010 between 08:02 and 16:00. The operators log can be downloaded from `here <http://www.vla.nrao.edu/cgi-bin/oplogs.cgi>`_.

#. Load the singularity module by entering:

	.. code-block:: console

		(host) $ module load singularity

#. Download the singularity image created in :ref:`use-of-singularity`. The following command downloads the most up to date image which is 1.3 GB and so this may take some time!

	.. code-block:: console

		(host) $ singularity pull library://mhardcastle/default/casa

#. CASA is started automatically when the singularity image is run:

	.. code-block:: console

		(host) $ singularity run casa_latest.sif

   N.B. If the data and singularity are not installed in the users home directory the above command will load CASA but any files saved will be output to the home directory rather than the current working directory. To specify which directory on the server is to be  treated as the home directory within the singularity use the -H command. For example, to change the singularity home directory to */beegfs/lofar/user* start the singularity using:

	.. code-block:: console

		(host) $ singularity run -H /beegfs/lofar/user:/home casa_latest.sif

Flagging
--------

All the following commands are run from the CASA command prompt inside the singularity

#. The operators log states that antenna *ea13* has no receiver and *ea15* has corrupted data. Both antennas are therefore flagged:

	.. code-block:: console

		(CASA) $ flagdata(vis='3c391_ctm_mosaic_10s_spw0.ms', flagbackup=True, mode='manual', antenna='ea13,ea15')


#. Generate a file containing the observation log. The following command will create a file called 3C391.listobs.

	.. code-block:: console

		(CASA) $ listobs(vis='3c391_ctm_mosaic_10s_spw0.ms', verbose=True, listfile='3C391.listobs')

#. From the observation log it can be seen that the first scan of the bandpass calibrator, 3C 286, was extremely short (20 seconds). This was a setup scan which is therefore flagged:

	.. code-block:: console

		(CASA) $ flagdata(vis='3c391_ctm_mosaic_10s_spw0.ms', flagbackup=True, mode='manual', scan='1')

#. At the start of each scan it typically takes a few moments for the VLA antennas to settle into position. As a result it is common practice to remove the first few seconds of data from the start of each scan. In the example below we flag (or `quack`) the first 10 seconds of each scan.

	.. code-block:: console

		(CASA) $ flagdata(vis='3c391_ctm_mosaic_10s_spw0.ms', flagbackup=True, mode='quack', quackinterval=10.0, quackmode='beg')

#. Sharp peaks in RFI may cause Gibbs ringing. This usually occurs for narrow band RFI and is observable as a zig-zag pattern in the neighbouring channels. To prevent this the data can be Hanning smoothed. N.B. Hanning smoothing decreases the spectral resolution by a factor of two and may not be appropriate when performing spectral analysis.

	.. code-block:: console

		(CASA) $ hanningsmooth(vis='3c391_ctm_mosaic_10s_spw0.ms', outputvis='3c391_ctm_mosaic_10s_spw0-smoothed.ms', datacolumn='data')

#. Using *tfcrop* to automatically flag any visibility amplitude outliers. In the code below it flags data more than 3 standard deviations away from both the time and frequency fits.

	.. code-block:: console

		(CASA) $ flagdata(vis='3c391_ctm_mosaic_10s_spw0-smoothed.ms', mode='tfcrop', datacolumn='data', timecutoff=3.0, freqcutoff=3.0)

#. RFI-rich spectral windows may still contain significant amounts of RFI. To improve flagging we increase the contrast between clean and affected data by performing a coarse preliminary bandpass calibration to take out the bandpass shape from the data. 

	.. code-block:: console

		(CASA) $ gencal(vis='3c391_ctm_mosaic_10s_spw0-smoothed.ms', caltable='3c391_ctm_mosaic_10s_spw0-smoothed.antpos', caltype='antpos')

		(CASA) $ gaincal(vis='3c391_ctm_mosaic_10s_spw0-smoothed.ms', caltable='3c391_ctm_mosaic_10s_spw0-smoothed.G0', gaintype='G', calmode='p', solint='int', field='0', refant='ea21', minsnr=5.0, spw='0:27~36', gaintable=['3c391_ctm_mosaic_10s_spw0-smoothed.antpos'])

		(CASA) $ gaincal(vis='3c391_ctm_mosaic_10s_spw0-smoothed.ms', caltable='3c391_ctm_mosaic_10s_spw0-smoothed.K0', gaintype='K', solint='inf', field='0', refant='ea21', minsnr=5.0, spw='0:5~58', combine='scan', gaintable=['3c391_ctm_mosaic_10s_spw0-smoothed.antpos','3c391_ctm_mosaic_10s_spw0-smoothed.G0'])

		(CASA) $ bandpass(vis='3c391_ctm_mosaic_10s_spw0-smoothed.ms', caltable='3c391_ctm_mosaic_10s_spw0-smoothed.B0', solint='inf', field='0', refant='ea21', spw='', combine='scan', gaintable=['3c391_ctm_mosaic_10s_spw0-smoothed.antpos','3c391_ctm_mosaic_10s_spw0-smoothed.G0','3c391_ctm_mosaic_10s_spw0-smoothed.K0'])

		(CASA) $ applycal(vis='3c391_ctm_mosaic_10s_spw0-smoothed.ms', calwt=False, gaintable=['3c391_ctm_mosaic_10s_spw0-smoothed.antpos','3c391_ctm_mosaic_10s_spw0-smoothed.G0','3c391_ctm_mosaic_10s_spw0-smoothed.K0','3c391_ctm_mosaic_10s_spw0-smoothed.B0'])

#. Having done the preliminary bandpass we can now use *rflag* to do some more flagging. In this example we flag RFI that is more than 5 standard deviations away from both the time and frequency-calculated median values.

	.. code-block:: console

		(CASA) $ flagdata(vis='3c391_ctm_mosaic_10s_spw0-smoothed.ms', mode='rflag', datacolumn='corrected', timedevscale=5.0, freqdevscale=5.0, flagbackup=True)

Calibration
-----------

#. Before calculating the final calibration tables we must remove the preliminary calibration that was done in order to run *rflag*

	.. code-block:: console

		(CASA) $ clearcal(vis='3c391_ctm_mosaic_10s_spw0-smoothed.ms')

		(CASA) $ setjy(vis='3c391_ctm_mosaic_10s_spw0-smoothed.ms', field='0', model='3C286_C.im', standard='Perley-Butler 2017')

#. Now that all the RFI is (hopefully) removed, we calculate the final calibration tables for the primary calibrator, which in this example is 3C 286 (field 0).

	.. code-block:: console

		(CASA) $ gaincal(vis='3c391_ctm_mosaic_10s_spw0-smoothed.ms', caltable='3c391_ctm_mosaic_10s_spw0-smoothed.G1', gaintype='G', calmode='p', solint='int', field='0', refant='ea21', spw='0:27~36', minsnr=5.0, gaintable=['3c391_ctm_mosaic_10s_spw0-smoothed.antpos'])

		(CASA) $ gaincal(vis='3c391_ctm_mosaic_10s_spw0-smoothed.ms', caltable='3c391_ctm_mosaic_10s_spw0-smoothed.K1', gaintype='K', solint='inf', field='0', refant='ea21', spw='0:5~58', combine='scan', minsnr=5.0, gaintable=['3c391_ctm_mosaic_10s_spw0-smoothed.antpos','3c391_ctm_mosaic_10s_spw0-smoothed.G1'])

		(CASA) $ bandpass(vis='3c391_ctm_mosaic_10s_spw0-smoothed.ms', caltable='3c391_ctm_mosaic_10s_spw0-smoothed.B1', solint='inf', field='0', refant='ea21', spw='', combine='scan', gaintable=['3c391_ctm_mosaic_10s_spw0-smoothed.antpos','3c391_ctm_mosaic_10s_spw0-smoothed.G1','3c391_ctm_mosaic_10s_spw0-smoothed.K1'])

#. Calculate the gain calibration table for the primary and secondary calibrators simultaneously

	.. code-block:: console

		(CASA) $ gaincal(vis='3c391_ctm_mosaic_10s_spw0-smoothed.ms', caltable='3c391_ctm_mosaic_10s_spw0-smoothed.G2', gaintype='G', calmode='ap', solint='inf', field='0,1', refant='ea21', spw='0:5~58', gaintable=['3c391_ctm_mosaic_10s_spw0-smoothed.antpos','3c391_ctm_mosaic_10s_spw0-smoothed.K1','3c391_ctm_mosaic_10s_spw0-smoothed.B1'])

#. Scale the amplitude gains, N.B. Setting *incremental=False* makes a new output table that replaces the gain calibration table.

	.. code-block:: console

		(CASA) $ fluxscale(vis='3c391_ctm_mosaic_10s_spw0-smoothed.ms', caltable='3c391_ctm_mosaic_10s_spw0-smoothed.G2', fluxtable='3c391_ctm_mosaic_10s_spw0-smoothed.fluxscale2', reference='0', transfer=['1'], incremental=False)

#. Apply the calibration

	.. code-block:: console

		(CASA) $ applycal(vis='3c391_ctm_mosaic_10s_spw0-smoothed.ms', field='0', gaintable=['3c391_ctm_mosaic_10s_spw0-smoothed.antpos','3c391_ctm_mosaic_10s_spw0-smoothed.fluxscale2','3c391_ctm_mosaic_10s_spw0-smoothed.K1','3c391_ctm_mosaic_10s_spw0-smoothed.B1'], gainfield=['','0','',''], interp=['','nearest','',''], calwt=False)

		(CASA) $ applycal(vis='3c391_ctm_mosaic_10s_spw0-smoothed.ms', field='1', gaintable=['3c391_ctm_mosaic_10s_spw0-smoothed.antpos','3c391_ctm_mosaic_10s_spw0-smoothed.fluxscale2','3c391_ctm_mosaic_10s_spw0-smoothed.K1','3c391_ctm_mosaic_10s_spw0-smoothed.B1'], gainfield=['','1','',''], interp=['','nearest','',''], calwt=False)

		(CASA) $ applycal(vis='3c391_ctm_mosaic_10s_spw0-smoothed.ms', field='2~8', gaintable=['3c391_ctm_mosaic_10s_spw0-smoothed.antpos','3c391_ctm_mosaic_10s_spw0-smoothed.fluxscale2','3c391_ctm_mosaic_10s_spw0-smoothed.K1','3c391_ctm_mosaic_10s_spw0-smoothed.B1'], gainfield=['','1','',''], interp=['','linear','',''], calwt=False)

Imaging
-------

#. Before starting to image the data it is recommended to run *statwt* to remove any noise scatter that may have been caused by flagging.

	.. code-block:: console

		(CASA) $ statwt(vis='3c391_ctm_mosaic_10s_spw0-smoothed.ms', datacolumn='data')

#. When cleaning an image, it is recommended that the pixel size is set so that there are at least 4-5 pixels across the beam. The image in this example has a resolution of 12 arcsec and so a pixel size of 2.5 arcsec is chosen.

#. When using the VLA there is significant sensitivity outside of the main lobe of the primary beam. Any sources detected in the sidelobes need cleaning and removing from the dirty beam. This can be done either by using outlier fields or, as in this tutorial, creating very large images that encompass these interfering sources. We therefore create images that are approximately twice the size of the primary beam. In this example this is 20 arcmin.

#. In addition, the CASA algorithm *tclean* is computationally faster when using image sizes of 5\*2 :superscript:`n` \*3 :superscript:`m` pixels where n and m are integer numbers. Therefore, in this workflow we generate images that are 480 pixels both vertically and horizontally

#. Create the dirty image. 

	.. code-block:: console

		(CASA) $ tclean(vis='3c391_ctm_mosaic_10s_spw0-smoothed.ms', field='2~8',imagename='3C391_Dirty', cell=['2.5arcsec','2.5arcsec'], imsize=[480,480], niter=0, stokes='I', gridder='mosaic')

#. Export the dirty image to a fits file

	.. code-block:: console

		(CASA) $ exportfits(imagename='3C391_Dirty.image', fitsimage='3C391_Dirty.fits', dropstokes=True, dropdeg=True)

#. Find the rms across the whole image. N.B. The following command does not exclude the source region, instead it uses the entire image to calculate the RMS in Jy.

	.. code-block:: console

		(CASA) $ stats = imstat(imagename='3C391_Dirty.image')

		(CASA) $ stats['rms']

#. Create the clean image.

	.. code-block:: console

		(CASA) $ tclean(vis='3c391_ctm_mosaic_10s_spw0-smoothed.ms', field='2~8',imagename='3C391_Clean', cell=['2.5arcsec','2.5arcsec'], imsize=[480,480], niter=20000, threshold='1.0mJy', stokes='I', gridder='mosaic', deconvolver='multiscale', scales=[0, 5, 15, 45], smallscalebias=0.9, weighting='briggs', robust=0.5, pbcor=True)

#. Finally, export the image into a fits-format file

	.. code-block:: console

		(CASA) $ exportfits(imagename='3C391_Clean.image', fitsimage='3C391_Clean.fits', dropstokes=True, dropdeg=True)

.. _VLA-basic-imaging-running-as-a-script:

Running as a Script
-------------------

The script used in this example is called VLA_Basic_Imaging_Script.py and can be downloaded :download:`here <scripts/vla/VLA_Basic_Imaging_Script.py>`.

After downloading the measurement set and starting the singularity instance as described in :ref:`VLA-basic-imaging-getting-started`, the above commands can be run as a single script using the following command:

	.. code-block:: console

		(CASA) $ execfile('VLA_Basic_Imaging_Script.py')

Running the script as a Slurm job on Cambridge CSD3
---------------------------------------------------

#. Start by logging on to the `Cambridge CSD3 system <https://docs.hpc.cam.ac.uk/hpc/index.html>`_ as described in :ref:`cambridgehpc-login`. If necessary download the casa singularity as described in :ref:`VLA-basic-imaging-getting-started`.

#. Create the following slurm script. This script used in this exmaple is named :download:`VLA_Basic_Imaging.slurm <scripts/vla/VLA_Basic_Imaging.slurm>`, though it can be given any name. Note, the slurm script calls the same :download:`VLA_Basic_Imaging_Script.py <scripts/vla/VLA_Basic_Imaging_Script.py>` script used in :ref:`VLA-basic-imaging-running-as-a-script`. If necessary, download and install this script into the working directory.

	.. code-block:: console

		#!/bin/bash
		#SBATCH -J VLA-Basic-Imaging
		#SBATCH -A DIRAC-TP001-CPU
		#SBATCH -p icelake
		#SBATCH --nodes=1
		#SBATCH --ntasks=1
		#SBATCH --time=00:45:00
		#SBATCH --mail-type=ALL
		#SBATCH --no-requeue

		#! Enter the script to run here
		. /etc/profile.d/modules.sh
		module load rhe18/default-icl
		module load singularity
		singularity exec casa_latest.sif casa -c VLA_Basic_Imaging_Script.py

#. Note the following points about the slurm script:

	* The command ``#SBATCH -J VLA-Basic-Imaging`` names the job VLA-Basic-Imaging
	* The command ``#SBATCH -A DIRAC-TP001-CPU`` is the name of the project under which time has been allocated
	* The command ``#SBATCH -p icelake`` ensures we are using the icelake cluster
	* The command ``#SBATCH --nodes=1`` states we only require a single node
	* The command ``#SBATCH --ntasks=1`` states we are running a single task/process. By default slurm allocates one task per cpu and so we are effectively asking for a single cpu. On icelake each CPU has a single core and by default each icelake CPU is allocated 3380 MiB of memory.
	* The command ``#SBATCH --time=00:45:00`` is requesting 45 (wall-clock) minutes of processing time.
	* The command ``#SBATCH --mail-type=ALL`` means email messages will be sent at the start and end of the job or (if applicable) when an error occurs. To disable this set the option to ``NONE``.
	* The command ``#SBATCH --no-requeue`` means that if this job is interrupted by a node failure/system downtime it will `not` be automatically rescheduled.
	* The command ``. /etc/profile.d/modules.sh`` enables the module command
	* The command ``module load rhe18/default-icl`` loads the basic environment needed by icelake
	* The command ``module load singularity`` loads the singularity module
	* The command ``singularity exec casa_latest.sif casa -c VLA_Basic_Imaging_Script.py`` executes the command ``casa -c VLA_Basic_Imaging_Script.py`` within the singularity environment. This is the command that runs the casa script.

#. Run the slurm script by entering

	.. code-block:: console

		(host) $ sbatch VLA_Basic_Imaging.slurm












