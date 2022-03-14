.. _CASA-Toolkit-baselines:

Baselines.py
============

Use this script to produce a plot similar to the one below which shows the baselines used throughout an observation.

	.. figure:: images/baselines.png
		:width: 600

		An example output from the baselines.py script 

Python Code
-----------

The script can be downloaded :download:`here <scripts/vla/baselines.py>` and contains the following code:

	.. code-block:: python

		import matplotlib.pyplot as plt

		# Read the data from the measurement set
		tb.open(vis)
		uvw = tb.getcol("UVW")
		tb.close()

		# Split out u, v and w
		uu,vv,ww = uvw

		# Make the plot
		fig, ax = plt.subplots(nrows=1, figsize=(7.0,7.0))
		ax.scatter(uu, vv, s=1.5, rasterized=True, linewidths=0.0, c="k")
		ax.set_xlabel(r"$u$ [m]")
		ax.set_ylabel(r"$v$ [m]")
		plt.savefig("baselines.png:)

