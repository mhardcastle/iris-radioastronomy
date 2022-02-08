from sys import argv

params = argv[1].split()
vis = params[0]
config = params[1]
band = params[2]

smoothed_vis = vis[:-3]+'-smoothed.ms'
primary_calibrator = '1'
phase_calibrator = '2'
target_field='3'
refant = 'ea21'

caltable_antpos = smoothed_vis[:-3]+".antpos"

listobs(vis=vis, verbose=True, listfile=vis[:-3]+'.listobs')

flagdata(vis=vis, flagbackup=True, mode='manual', field='0,4,5')

flagdata(vis=vis, flagbackup=True, mode='quack', field='', quackinterval=5.0, quackmode='beg')

hanningsmooth(vis=vis, outputvis=smoothed_vis, datacolumn='data')

flagdata(vis=smoothed_vis, mode='tfcrop', datacolumn='data', timecutoff=3.0, freqcutoff=3.0)

gencal(vis=smoothed_vis, caltable=caltable_antpos, caltype='antpos')

gaincal(vis=smoothed_vis, caltable=smoothed_vis[:-3]+'.G0', gaintype='G', calmode='p', solint='int', field=primary_calibrator, refant=refant, minsnr=5.0, spw='0:27~36', gaintable=[caltable_antpos])

gaincal(vis=smoothed_vis, caltable=smoothed_vis[:-3]+'.K0', gaintype='K', solint='inf', field=primary_calibrator, refant=refant, minsnr=5.0, spw='0:5~58', combine='scan', gaintable=[caltable_antpos,smoothed_vis[:-3]+'.G0'])

bandpass(vis=smoothed_vis, caltable=smoothed_vis[:-3]+'.B0', solint='inf', field=primary_calibrator, refant=refant, spw='', combine='scan', gaintable=[caltable_antpos,smoothed_vis[:-3]+'.G0',smoothed_vis[:-3]+'.K0'])

applycal(vis=smoothed_vis, calwt=False, gaintable=[caltable_antpos,smoothed_vis[:-3]+'.G0',smoothed_vis[:-3]+'.K0',smoothed_vis[:-3]+'.B0'])

flagdata(vis=smoothed_vis, mode='rflag', datacolumn='corrected', timedevscale=5.0, freqdevscale=5.0, flagbackup=True)

clearcal(vis=smoothed_vis)

setjy(vis=smoothed_vis, field=primary_calibrator, model='3C48_'+band+'.im', standard='Perley=Butler 2017')

gaincal(vis=smoothed_vis, caltable=smoothed_vis[:-3]+'.G1', gaintype='G', calmode='p', solint='int', field=primary_calibrator, refant=refant, spw='0:27~36', minsnr=5.0, gaintable=[caltable_antpos])

gaincal(vis=smoothed_vis, caltable=smoothed_vis[:-3]+'.K1', gaintype='K', solint='inf', field=primary_calibrator, refant=refant, spw='0:5~58', combine='scan', minsnr=5.0, gaintable=[caltable_antpos,smoothed_vis[:-3]+'.G1'])

bandpass(vis=smoothed_vis, caltable=smoothed_vis[:-3]+'.B1', solint='inf', field=primary_calibrator, refant=refant, spw='', combine='scan', gaintable=[caltable_antpos,smoothed_vis[:-3]+'.G1',smoothed_vis[:-3]+'.K1'])

gaincal(vis=smoothed_vis, caltable=smoothed_vis[:-3]+'.G2', gaintype='G', calmode='ap', solint='inf', field=primary_calibrator+','+phase_calibrator, refant=refant, spw='0:5~58', gaintable=[caltable_antpos,smoothed_vis[:-3]+'.K1',smoothed_vis[:-3]+'.B1'])

fluxscale(vis=smoothed_vis, caltable=smoothed_vis[:-3]+'.G2',fluxtable=smoothed_vis[:-3]+'.fluxscale2', reference=primary_calibrator, transfer=[phase_calibrator], incremental=False)

applycal(vis=smoothed_vis, field=primary_calibrator, gaintable=[caltable_antpos,smoothed_vis[:-3]+'.fluxscale2',smoothed_vis[:-3]+'.K1',smoothed_vis[:-3]+'.B1'], gainfield=['',primary_calibrator,'',''], interp=['','nearest','',''], calwt=False)

applycal(vis=smoothed_vis, field=phase_calibrator, gaintable=[caltable_antpos,smoothed_vis[:-3]+'.fluxscale2',smoothed_vis[:-3]+'.K1',smoothed_vis[:-3]+'.B1'], gainfield=['',phase_calibrator,'',''], interp=['','nearest','',''], calwt=False)

applycal(vis=smoothed_vis, field=target_field, gaintable=[caltable_antpos,smoothed_vis[:-3]+'.fluxscale2',smoothed_vis[:-3]+'.K1',smoothed_vis[:-3]+'.B1'], gainfield=['',phase_calibrator,'',''], interp=['','linear','',''], calwt=False)

statwt(vis=smoothed_vis, datacolumn='data')

#Set cleaning scales to 0, 2*beam, 5*beam (in pixels)
if config=='A':
	cell=['0.25arcsec','0.25arcsec']
	imsize=[11250,11250]
	scales=[0,10,26]
elif config=='B':
	cell=['1arcsec','1arcsec']
	imsize=[3072,3072]
	scales=[0,9,22]
elif config=='C':
	cell=['3arcsec','3arcsec']
	imsize=[1024,1024]
	scales=[0,9,23]
elif config=='D':
	cell=['10arcsec','10arcsec']
	imsize=[320,320]
	scales=[0,9,23]

tclean(vis=smoothed_vis, field=target_field, imagename=smoothed_vis[:-3]+'-Dirty', cell=cell, imsize=imsize, niter=0, stokes='I') 

exportfits(imagename=smoothed_vis[:-3]+'-Dirty.image', fitsimage=smoothed_vis[:-3]+'-Dirty.fits', dropstokes=True, dropdeg=True)

stats = imstat(imagename=smoothed_vis[:-3]+'-Dirty.image')

rms = stats['rms'][0]

tclean(vis=smoothed_vis, field=target_field, imagename=smoothed_vis[:-3]+'-Clean', cell=cell, imsize=imsize, niter=20000, threshold=str(rms*5)+'Jy', stokes='I', deconvolver='multiscale', scales=scales, smallscalebias=0.9, weighting='briggs', robust=0.5, pbcor=True)

exportfits(imagename=smoothed_vis[:-3]+'-Clean.image', fitsimage=smoothed_vis[:-3]+'-Clean.fits', dropstokes=True, dropdeg=True)
