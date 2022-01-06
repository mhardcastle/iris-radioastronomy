vis = '3c391_ctm_mosaic_10s_spw0.ms'
smoothed_vis = '3c391_ctm_mosaic_10s_spw0-smoothed.ms'
primary_calibrator = '0'
phase_calibrator = '1'
target_fields = '2~8'
refant = 'ea21'

flagdata(vis=vis, flagbackup=True, mode='manual', antenna='ea13,ea15')

listobs(vis=vis, verbose=True, listfile='3C391.listobs')

flagdata(vis=vis, flagbackup=True, mode='manual', scan='1')

flagdata(vis=vis, flagbackup=True, mode='quack', quackinterval=10.0, quackmode='beg')

hanningsmooth(vis=vis, outputvis=smoothed_vis, datacolumn='data')

flagdata(vis=smoothed_vis, mode='tfcrop', datacolumn='data', timecutoff=3.0, freqcutoff=3.0)

gencal(vis=smoothed_vis, caltable='3c391_ctm_mosaic_10s_spw0-smoothed.antpos', caltype='antpos')

gaincal(vis=smoothed_vis, caltable='3c391_ctm_mosaic_10s_spw0-smoothed.G0', gaintype='G', calmode='p', solint='int', field=primary_calibrator, refant=refant, minsnr=5.0, spw='0:27~36', gaintable=['3c391_ctm_mosaic_10s_spw0-smoothed.antpos'])

gaincal(vis=smoothed_vis, caltable='3c391_ctm_mosaic_10s_spw0-smoothed.K0', gaintype='K', solint='inf', field=primary_calibrator, refant=refant, minsnr=5.0, spw='0:5~58', combine='scan', gaintable=['3c391_ctm_mosaic_10s_spw0-smoothed.antpos','3c391_ctm_mosaic_10s_spw0-smoothed.G0'])

bandpass(vis=smoothed_vis, caltable='3c391_ctm_mosaic_10s_spw0-smoothed.B0', solint='inf', field=primary_calibrator, refant=refant, spw='', combine='scan', gaintable=['3c391_ctm_mosaic_10s_spw0-smoothed.antpos','3c391_ctm_mosaic_10s_spw0-smoothed.G0','3c391_ctm_mosaic_10s_spw0-smoothed.K0'])

applycal(vis=smoothed_vis, calwt=False, gaintable=['3c391_ctm_mosaic_10s_spw0-smoothed.antpos','3c391_ctm_mosaic_10s_spw0-smoothed.G0','3c391_ctm_mosaic_10s_spw0-smoothed.K0','3c391_ctm_mosaic_10s_spw0-smoothed.B0'])

flagdata(vis=smoothed_vis, mode='rflag', datacolumn='corrected', timedevscale=5.0, freqdevscale=5.0, flagbackup=True)

clearcal(vis=smoothed_vis)

setjy(vis=smoothed_vis, field=primary_calibrator, model='3C286_C.im', standard='Perley-Butler 2017')

gaincal(vis=smoothed_vis, caltable='3c391_ctm_mosaic_10s_spw0-smoothed.G1', gaintype='G', calmode='p', solint='int', field=primary_calibrator, refant=refant, spw='0:27~36', minsnr=5.0, gaintable=['3c391_ctm_mosaic_10s_spw0-smoothed.antpos'])

gaincal(vis=smoothed_vis, caltable='3c391_ctm_mosaic_10s_spw0-smoothed.K1', gaintype='K', solint='inf', field=primary_calibrator, refant=refant, spw='0:5~58', combine='scan', minsnr=5.0, gaintable=['3c391_ctm_mosaic_10s_spw0-smoothed.antpos','3c391_ctm_mosaic_10s_spw0-smoothed.G1'])

bandpass(vis=smoothed_vis, caltable='3c391_ctm_mosaic_10s_spw0-smoothed.B1', solint='inf', field=primary_calibrator, refant=refant, spw='', combine='scan', gaintable=['3c391_ctm_mosaic_10s_spw0-smoothed.antpos','3c391_ctm_mosaic_10s_spw0-smoothed.G1','3c391_ctm_mosaic_10s_spw0-smoothed.K1'])

gaincal(vis=smoothed_vis, caltable='3c391_ctm_mosaic_10s_spw0-smoothed.G2', gaintype='G', calmode='ap', solint='inf', field='0,1', refant=refant, spw='0:5~58', gaintable=['3c391_ctm_mosaic_10s_spw0-smoothed.antpos','3c391_ctm_mosaic_10s_spw0-smoothed.K1','3c391_ctm_mosaic_10s_spw0-smoothed.B1'])

fluxscale(vis=smoothed_vis, caltable='3c391_ctm_mosaic_10s_spw0-smoothed.G2', fluxtable='3c391_ctm_mosaic_10s_spw0-smoothed.fluxscale2', reference=primary_calibrator, transfer=[phase_calibrator], incremental=False)

applycal(vis=smoothed_vis, field=primary_calibrator, gaintable=['3c391_ctm_mosaic_10s_spw0-smoothed.antpos','3c391_ctm_mosaic_10s_spw0-smoothed.fluxscale2','3c391_ctm_mosaic_10s_spw0-smoothed.K1','3c391_ctm_mosaic_10s_spw0-smoothed.B1'], gainfield=['',primary_calibrator,'',''], interp=['','nearest','',''], calwt=False)

applycal(vis=smoothed_vis, field=phase_calibrator, gaintable=['3c391_ctm_mosaic_10s_spw0-smoothed.antpos','3c391_ctm_mosaic_10s_spw0-smoothed.fluxscale2','3c391_ctm_mosaic_10s_spw0-smoothed.K1','3c391_ctm_mosaic_10s_spw0-smoothed.B1'], gainfield=['',phase_calibrator,'',''], interp=['','nearest','',''], calwt=False)

applycal(vis=smoothed_vis, field=target_fields, gaintable=['3c391_ctm_mosaic_10s_spw0-smoothed.antpos','3c391_ctm_mosaic_10s_spw0-smoothed.fluxscale2','3c391_ctm_mosaic_10s_spw0-smoothed.K1','3c391_ctm_mosaic_10s_spw0-smoothed.B1'], gainfield=['',phase_calibrator,'',''], interp=['','linear','',''], calwt=False)

statwt(vis=smoothed_vis, datacolumn='data')

tclean(vis=smoothed_vis, field=target_fields, imagename='3C391_Dirty', cell=['2.5arcsec','2.5arcsec'], imsize=[480,480], niter=0, stokes='I', gridder='mosaic')

exportfits(imagename='3C391_Dirty.image', fitsimage='3C391_Dirty.fits', dropstokes=True, dropdeg=True)

stats = imstat(imagename='3C391_Dirty.image')

rms = stats['rms'][0]

tclean(vis=smoothed_vis, field=target_fields, imagename='3C391_Clean', cell=['2.5arcsec','2.5arcsec'], imsize=[480,480], niter=20000, threshold=str(rms*5)+'Jy', stokes='I', gridder='mosaic', deconvolver='multiscale', scales=[0, 5, 15, 45], smallscalebias=0.9, weighting='briggs', robust=0.5, pbcor=True)

exportfits(imagename='3C391_Clean.image', fitsimage='3C391_Clean.fits', dropstokes=True, dropdeg=True)
