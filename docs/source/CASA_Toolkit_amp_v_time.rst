.. _CASA-Toolkit-amp-v-time:

Amp_v_time.py
=============

Use this script to produce a plot similar to the one below which shows the visibility amplitudes plotted as a function of time and colorised by field.

	.. figure:: images/amp_v_time.png
		:width: 600

		An example output from the amp_v_time.py script

Python Code
-----------

The script can be downloaded :download:`here <scripts/vla/amp_v_time.py>` and contains the following code:

	.. code-block:: python

		from matplotlib import pyplot as plt, dates as mdates, colors as colors
		import datetime as dt
		import numpy as np

		# Each stokes type is defined by a number as defined by the Stokes class enumeration
		# RR is defined as 5
		# RL is defined as 6
		# LR is defined as 7
		# LL is defined as 8

		# Read the data from the measurement set
		tb.open(vis+"/POLARIZATION")
		corr_type = tb.getcol("CORR_TYPE")
		tb.close()

		# Get the index numbers for the RR and LL polarizations
		RR_index = np.asarray(corr_type==5).nonzero()[0][0]
		LL_index = np.asarray(corr_type==8).nonzero()[0][0]

		tb.open(vis)
		#weight=tb.getcol("WEIGHT") #array of float64 with shape [npol, nvis]
		flag = tb.getcol("FLAG") #array of bool with shape [npol, nchan, nvis]
		time = tb.getcol("TIME") #array of float64 with length nvis
		field = tb.getcol("FIELD_ID") #array of int with length nvis
		data = tb.getcol("DATA") #array of complex128 with shape [npol, nchan, nvis]
		tb.close()

		# Choose only the LL and RR polarizations
		data = data[[RR_index, LL_index], :] #array of complex128 with shape [2, nchan, nvis]
		#weight = weight[[RR_index, LL_index], :] #array of float64 with shape [2, nvis]
		flag = flag[[RR_index, LL_index], :] #array of bool with shape [2, nchan, nvis]

		# Use a masked array to make sure we exclude flagged values
		data_masked = np.ma.array(data, mask=flag)

		# Weight the data
		#data_masked = data_masked*weight[:, np.newaxis, :]

		# Average the channels
		data_masked = np.average(data_masked, axis=1) #array af complex128 with shape [2, nvis]

		#average the polarizations
		#data = np.sum(data * weight[:, np.newaxis, :], axis=0) / np.sum(weight, axis=0) #array of complex128 with shape [nchan, nvis]

		# Calculate the visibility amplitude
		amp = np.abs(data_masked)

		# Extract the unflagged data only
		amp_good = amp.data[~amp.mask]

		# Get the corresponding times and fields
		time_good = np.concatenate((time[~amp.mask[0]],time[~amp.mask[1]]), axis=None) 
		field_good = np.concatenate((field[~amp.mask[0]],field[~amp.mask[1]]), axis=None)

		# Casa uses the modified julian date (MJD)  epoch of 17-Nov-1858
		# This is different to the datetime default
		# Calculate the offset and convert floats to dates
		offset = dt.datetime(1858,11,17) - dt.datetime.fromtimestamp(0)
		dates_good = [dt.datetime.fromtimestamp(t+offset.total_seconds()) for t in time_good]

		# Plot the data
		fig,ax = plt.subplots(nrows=1,figsize=(7.0,7.0))
		#cmap = colors.ListedColormap(['black','yellow','green','red','orange','lime','blue','purple','cyan','brown','silver','pink'])
		ax.scatter(dates_good,amp_good,s=1.5,rasterized=True,linewidths=0.0,c=field_good,cmap="gnuplot")
		ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
		ax.set_xlabel(r"$Time$ [hh:mm:ss]")
		ax.set_ylabel(r"$Amplitude$ [Jy]")
		plt.savefig("amp_v_time_python.png")
		plt.close()

