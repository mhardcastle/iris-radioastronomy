cell='2.5arcsec'
imsize=480
outim='3c391_ctm_spw0_multiscale_dirty'
field='2~8'
phasecenter = ['J2000','18:49:24.411','-00d55m43.08']

# Create the dirty image
im.open(vis)
im.defineimage(cellx=cell, celly=cell, nx=imsize, ny=imsize, phasecenter=phasecenter, stokes='I')
im.selectvis(field=field)
im.makeimage(type='corrected', image=outim+".image")
im.close()

# Export the results to a fits file
exportfits(imagename=outim+".image", fitsimage=outim+".fits")
