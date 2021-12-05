Use of Singularity
==================

`Singularity <https://sylabs.io/guides/3.9/user-guide/>`_ is the tool
we use for containerization in this project. Containers allow us to
build an environment which is stable, reproducible and portable --
radio astronomy software does not need to be installed on the target
host so long as it can run Singularity and accept a copy of a
Singularity image built elsewhere. A Singularity image contains a copy
of the operating system, all the dependencies and the target software
itself, and so can be run anywhere.

Full user and admin documentation are available on the Singularity web
site. Here we give a very brief outline of how to use and build a
singularity image, with an example of building a working image
containing `CASA <https://casa.nrao.edu/>`_.

.. _before:

Before starting
---------------

On most systems you will need to ensure that the ``singularity``
command is accessible. On the Cambridge and Hertfordshire systems you
can do this with

	.. code-block:: console

		(host) $ module load singularity

.. _basicuse:

Basic use
----------

If a Singularity or Docker image is available for download then you
can access it with ``singularity pull`` which will create a ``.sif`` file.

.. code-block:: console

		[mjh@lofar-server mjh]$ singularity pull library://lolcow
		INFO:    Using cached image
		[mjh@lofar-server mjh]$ ls -l lolcow_latest.sif 
		-rwxr-xr-x 1 mjh lofar 81454622 Dec  5 16:24 lolcow_latest.sif

You can then run this image, which executes a pre-defined run script
in the singularity environment:

.. code-block:: console

		[mjh@lofar-server mjh]$ singularity run lolcow_latest.sif
		_____________________________
		< Sun Dec 5 16:28:53 GMT 2021 >
		-----------------------------
		\   ^__^
		\  (oo)\_______
		   (__)\       )\/\
		       ||----w |
                       ||     ||
		[mjh@lofar-server mjh]$ 

Or you can run a shell inside it:

.. code-block:: console

		[mjh@lofar-server mjh]$ singularity shell lolcow_latest.sif
		Singularity> cat /etc/os-release 
		NAME="Ubuntu"
		VERSION="20.04 LTS (Focal Fossa)"
		ID=ubuntu
		ID_LIKE=debian
		PRETTY_NAME="Ubuntu 20.04 LTS"
		VERSION_ID="20.04"
		HOME_URL="https://www.ubuntu.com/"
		SUPPORT_URL="https://help.ubuntu.com/"
		BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
		PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
		VERSION_CODENAME=focal
		UBUNTU_CODENAME=focal
		Singularity> 

Or you can run a single command in the singularity environment and
then exit:

.. code-block:: console

		[mjh@lofar-server mjh]$ singularity exec lolcow_latest.sif cowsay moo
		 _____
		 < moo >
		 -----
		 \   ^__^
		 \  (oo)\_______
		    (__)\       )\/\
                        ||----w |
			||     ||

All of these three methods of interacting with an image can also be
run on a Singularity library or Docker image, in which case the image
will be downloaded and deleted after it is no longer needed. However
for HPC work it is probably better to have a local, static version of
the image file.

Binding file systems
--------------------

By default your home directory, the current working directory and /tmp on the host you are running on are accessible inside the Singularity. If you want other areas to be visible you can bind them with the ``-B`` option:

.. code-block:: console
		
		[mjh@lofar-server mjh]$ singularity shell -B/beegfs lolcow_latest.sif
		Singularity> ls /beegfs/
		backup	cair  car  general  lms  lofar	lost+found  temp  usage

Often it is useful to bind a file system or a part of the file system outside the singularity to a different name inside it, e.g. if running a script that needs to have a working directory with a specific name. You can specify this with a colon after the original name.

.. code-block:: console
		
		[mjh@lofar-server mjh]$ singularity shell -B/beegfs/lofar/mjh:/data lolcow_latest.sif

Finally you may want to prevent the image from accessing your home directory. To give it minimal access to the file system use the ``-c`` or ``--contain`` option. This will cause an empty home directory to be presented inside the singularity. Combined with ``-B`` you can use this to give access only to selected parts of the file system.

		
Building an image
-----------------

To build a new singularity image we use a definition file. In this case we will base our image on Scientific Linux 7 (a Red Hat clone) because we want to use CASA, which expects a Red Hat environment:

.. code:: singularity

	  BootStrap: docker
	  From: scientificlinux/sl
	  
	  %post
	  yum -y update
	  yum -y install wget perl less
	  cd /usr/local
	  wget https://casa.nrao.edu/download/distro/casa/release/rhel/casa-6.4.0-16-py3.8.tar.xz
	  tar xf casa-6.4.0-16-py3.8.tar.xz
	  rm casa-6.4.0-16-py3.8.tar.xz

	  %environment
	  export LC_ALL=C
	  export PATH=/usr/local/casa-6.4.0-16/bin:$PATH

	  %runscript
	  casa --nologger --log2term

	  %labels
	  Author IRIS-Radioastronomy
    
The ``%post`` part of the code here installs any security updates and
a few dependencies, then downloads and unpacks CASA. The
``%environment`` part makes sure that the ``casa`` command is on the system PATH and we define a runscript which means that running the singularity image will drop us into a CASA environment.

To build this we run the command:

.. code-block:: console

		[mjh@lofar-server mjh]$ singularity build --fakeroot casa.sif casa.def

The ``--fakeroot`` option here allows us to build the image as a normal user. If running on a machine where you have root access, you should use ``sudo`` instead. 

Running this command you will see the generation of the image,
including the download from Docker and the effects of running the
commands in the ``%post`` script. At the end of the process the ``.sif`` file will be written and can be run:

.. code-block:: console
		
		[mjh@lofar-server mjh]$ singularity run -B/beegfs/car/mjh/jvla:/data casa.sif

		optional configuration file config.py not found, continuing CASA startup without it

		IPython 7.15.0 -- An enhanced Interactive Python.

		Using matplotlib backend: agg
		Telemetry initialized. Telemetry will send anonymized usage statistics to NRAO.
		You can disable telemetry by adding the following line to the config.py file in your rcdir (e.g. ~/.casa/config.py):
		telemetry_enabled = False
		--> CrashReporter initialized.
		CASA 6.4.0.16 -- Common Astronomy Software Applications [6.4.0.16]
		2021-12-05 18:27:46	INFO	::casa	optional configuration file config.py not found, continuing CASA startup without it
		[...]
		
		CASA <1>:

If you have created an account on the `Singularity cloud library <https://cloud.sylabs.io>`_ then you can upload the image there and other users will be able to ``singularity pull`` it:

.. code-block:: console

		[mjh@lofar-server mjh]$ singularity sign casa.sif
		Signing image: casa.sif
		[...]
		Signature created and applied to casa.sif
		[mjh@lofar-server mjh]$ singularity push casa.sif library://mhardcastle/default/casa
		1.3GiB / 1.3GiB [==============================================================================] 100 % 15.3 MiB/s 0s

		Library storage: using 4.14 GiB out of 11.00 GiB quota (37.6% used)
		Container URL: https://cloud.sylabs.io/library/mhardcastle/default/casa

Note that for a singularity pull to work you must apply a tag to the uploaded file!

