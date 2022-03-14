import matplotlib.pyplot as plt

# Read the data from the measurement set
tb.open(vis)
uvw=tb.getcol("UVW") #array of float64 with shape [3, nvis]
tb.close()

# Split out u,v and w
uu,vv,ww = uvw

# Make the plot
fig,ax = plt.subplots(nrows=1,figsize=(7.0,7.0))
ax.scatter(uu,vv,s=1.5,rasterized=True,linewidths=0.0,c="k")
ax.set_xlabel(r"$u$ [m]")
ax.set_ylabel(r"$v$ [m]")
plt.savefig("baselines.png")
