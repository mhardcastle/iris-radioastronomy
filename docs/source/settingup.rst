Signing up for Dirac/HPC Resources
==================================

`DiRAC <https://dirac.ac.uk>`_ is funded by the STFC and provides High Performance Computing (HPC) facilities. At present DiRAC HPC facilities are hosted at Cambridge, Durham, Edinburgh and Leicester Universities.

This document describes how to register to use the DiRAC HPC facility hosted at the University of Cambridge. The Cambridge HPC is described in detail `here <https://www.hpc.cam.ac.uk>`_. In order to use the Cambridge HPC facility users must first register on SAFE before applying for a DiRAC account.


.. _registerSAFE:

Registering on SAFE
-------------------

.. This follows <https://dirac-safe.readthedocs.io/en/latest/safe-guide-users.html#safe-registering-logging-in-passwords>_

#. Go to the SAFE `New User Signup Form <https://safe.epcc.ed.ac.uk/dirac/signup.jsp>`_

	.. _fig-SAFERegistration
	.. figure:: images/SAFERegistration.png
		:width: 600
	
		The SAFE registration screen

#. Fill in your details
#. Click "Register" and (assuming you wish to continue) accept the terms and conditions
#. You will then be emailed a link allowing you to complete registration for SAFE and choose a password

After registering, should you need to change any of your details, go to `SAFE <https://safe.epcc.ed.ac.uk/dirac/>`_ and sign in using your email address and password.


.. _registerDIRAC:

Registering on DiRAC
--------------------

In order to register on DiRAC you must first have a SAFE account as described in :ref:`Registering on SAFE<registerSAFE>`. Registering for the Cambridge HPC will grant access to both Central Processing Unit (CPU) and Graphics Processing Unit (GPU) architectures. The CPU is designed to run quickly and handle a wide range of tasks but has limited concurrency whereas the GPU is designed to optimise rendering of images and can perform multiple parallel operations.

#. If not already logged in, log in to your SAFE account `here <https://safe.epcc.ed.ac.uk/dirac/>`__
#. Go to the `Request login account page <https://safe.epcc.ed.ac.uk/dirac/TransitionServlet/User//-/Transition=Choose%20Project>`_
#. Enter the project code ``tp001`` and click "Next"
#. Select ``Cambridge_HPC`` and click "Next"

	.. figure:: images/CambridgeDiracAccountRequest.png
		:width: 600

		The DiRAC account request screen

#. The next screen displays the username that will be assigned to you, make a note of this and click "Request".
#. You will receive an email once your request has been approved


Logging on to Cambridge HPC
---------------------------

#. In order to log on to the HPC for the first time find your password for the Cambridge HPC by logging in to your SAFE account `here <https://safe.epcc.ed.ac.uk/dirac/>`__ (if not already logged in)
#. Under the "Login Accounts" heading select "(username)@Cambridge_HPC" where username should be replaced with the name supplied during the DiRAC registration process. Click the button labelled "View Login Account Password" and make a note of the password displayed
#. Open a terminal command prompt and, replacing username with the name supplied during the DiRAC registration process, enter the following to access the CPU:

	.. code-block:: console

		(host) $ ssh (username)@login.hpc.cam.ac.uk

	or enter the following to access the GPU

	.. code-block:: console

		(host) $ ssh (username)@login-gpu.hpc.cam.ac.uk

#. When logging in to the CPU, if asked to accept one of the following fingerprints, type ``yes``

	* \MD5:eb:e3:a1:f0:64:68:cf:9c:63:da:84:db:2e:ee:15:83
	* \SHA256:nFVSXK+VRGCaUupQEdhXz06kp01m2fzzmbgPr0sc2so

	or when logging in to the GPU, if asked to accept one of the following fingerprints, type ``yes``

	* \MD5:fd:5c:6b:7d:49:95:2f:da:7f:5c:50:9a:bb:ef:3f:24
	* \SHA256:2rl+MXd9rsrDzFZwEItmhhiHTlLTIqN0d3TSGLTgjTI

	After accepting the fingerprint your computer will remember it when logging on in the future.

#. After logging in the first time you will be asked to choose a new password. This password will then be used for logging in to both CPU and GPU. Your password will *not* be visible in your SAFE account.

Your account has a storage allocation of 40GB in your home directory. Snapshots of your home directory are taken hourly/daily/weekly. If you delete a file by accident go to /home/.zfs/snapshot and browse the appropriate snapshot for the file which can then be copied back to your home directory.



