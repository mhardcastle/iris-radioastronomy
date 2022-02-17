vis = '3c391_ctm_mosaic_10s_spw0.ms'
splitvis = '3c391_ctm_mosaic_spw0.ms'

listobs(vis=vis)

plotants(vis=vis, figfile='plotants_3c391_antenna_layout.png')

clearstat()

flagdata(vis=vis,flagbackup=True,mode='manual',scan='1')

flagdata(vis=vis,flagbackup=True,mode='manual',antenna='ea13,ea15')

flagdata(vis=vis,mode='quack',quackinterval=10.0,quackmode='beg')

clearstat()

plotms(vis=vis,selectdata=True,correlation='RR,LL',averagedata=True,avgchannel='64',coloraxis='field',showgui=False,plotfile='plotms_3c391-Time.png',highres=True)

plotms(vis=vis,xaxis='uvdist',yaxis='Amp',selectdata=True,field='8',correlation='RR,LL',avgtime='1e6',showgui=False,plotfile='plotms_3c391-UVDist.png',highres=True)

plotms(vis=vis,field='',correlation='RR,LL',timerange='',antenna='ea01',spw='0:31',xaxis='time',yaxis='antenna2',plotrange=[-1,-1,0,26],coloraxis='field',showgui=False,plotfile='plotms_3c391-Antenna2.png',highres=True)

gencal(vis=vis,caltable='3c391_ctm_mosaic_10s_spw0.antpos',caltype='antpos')

setjy(vis=vis,field='J1331+3030',standard='Perley-Butler 2017',model='3C286_C.im',usescratch=False,scalebychan=True,spw='')

gaincal(vis=vis,caltable='3c391_ctm_mosaic_10s_spw0.G0all',field='0,1,9',refant='ea21',spw='0:27~36',gaintype='G',calmode='p',solint='int',minsnr=5,gaintable=['3c391_ctm_mosaic_10s_spw0.antpos'])

plotms(vis='3c391_ctm_mosaic_10s_spw0.G0all',xaxis='time',yaxis='phase',coloraxis='corr',iteraxis='antenna',exprange='all',plotrange=[-1,-1,-180,180],showgui=False,plotfile='plotms_3c391-G0all-phase.png',highres=True)

flagdata(vis=vis,flagbackup=True,mode='manual',antenna='ea05')

gaincal(vis=vis,caltable='3c391_ctm_mosaic_10s_spw0.G0',field='J1331+3030',refant='ea21',spw='0:27~36',calmode='p',solint='int',minsnr=5,gaintable=['3c391_ctm_mosaic_10s_spw0.antpos'])

plotms(vis='3c391_ctm_mosaic_10s_spw0.G0',xaxis='time',yaxis='phase',coloraxis='corr',field='J1331+3030',iteraxis='antenna',exprange='all',plotrange=[-1,-1,-180,180],timerange='08:02:00~08:17:00',showgui=False,plotfile='plotms_3c391-G0-phase.png',highres=True)

gaincal(vis=vis,caltable='3c391_ctm_mosaic_10s_spw0.K0',field='J1331+3030',refant='ea21',spw='0:5~58',gaintype='K',solint='inf',combine='scan',minsnr=5,gaintable=['3c391_ctm_mosaic_10s_spw0.antpos','3c391_ctm_mosaic_10s_spw0.G0'])

plotms(vis='3c391_ctm_mosaic_10s_spw0.K0',xaxis='antenna1',yaxis='delay',coloraxis='baseline',showgui=False,plotfile='plotms_3c391-K0-delay.png',highres=True)

bandpass(vis=vis,caltable='3c391_ctm_mosaic_10s_spw0.B0',field='J1331+3030',spw='',refant='ea21',combine='scan',solint='inf',bandtype='B',gaintable=['3c391_ctm_mosaic_10s_spw0.antpos','3c391_ctm_mosaic_10s_spw0.G0','3c391_ctm_mosaic_10s_spw0.K0'])

plotms(vis='3c391_ctm_mosaic_10s_spw0.B0',field='J1331+3030',xaxis='chan',yaxis='amp',coloraxis='corr',iteraxis='antenna',exprange='all',gridrows=2,gridcols=2,showgui=False,plotfile='plotms_3c391-B0-amp.png',highres=True)

plotms(vis='3c391_ctm_mosaic_10s_spw0.B0',field='J1331+3030',xaxis='chan',yaxis='phase',coloraxis='corr',plotrange=[-1,-1,-180,180],iteraxis='antenna',exprange='all',gridrows=2,gridcols=2,showgui=False,plotfile='plotms_3c391-B0-phase.png',highres=True)

gaincal(vis=vis,caltable='3c391_ctm_mosaic_10s_spw0.G1',field='J1331+3030',spw='0:5~58',solint='inf',refant='ea21',gaintype='G',calmode='ap',solnorm=False,gaintable=['3c391_ctm_mosaic_10s_spw0.antpos','3c391_ctm_mosaic_10s_spw0.K0','3c391_ctm_mosaic_10s_spw0.B0'],interp=['linear','linear','nearest'])

gaincal(vis=vis,caltable='3c391_ctm_mosaic_10s_spw0.G1',field='J1822-0938',spw='0:5~58',solint='inf',refant='ea21',gaintype='G',calmode='ap',gaintable=['3c391_ctm_mosaic_10s_spw0.antpos','3c391_ctm_mosaic_10s_spw0.K0','3c391_ctm_mosaic_10s_spw0.B0'],append=True)

plotms(vis='3c391_ctm_mosaic_10s_spw0.G1',xaxis='time',yaxis='phase',gridrows=1,gridcols=2,iteraxis='corr',exprange='all',coloraxis='baseline',plotrange=[-1,-1,-180,180],plotfile='plotms_3c391-G1-phase.png',showgui=False,highres=True)

plotms(vis='3c391_ctm_mosaic_10s_spw0.G1',xaxis='time',yaxis='amp',gridrows=1,gridcols=2,iteraxis='corr',exprange='all',coloraxis='baseline',plotfile='plotms_3c391-G1-amp.png',showgui=False,highres=True)

plotms(vis='3c391_ctm_mosaic_10s_spw0.G1',xaxis='time',yaxis='phase',correlation='/',coloraxis='baseline',plotrange=[-1,-1,-180,180],showgui=False,plotfile='plotms_3c391-G1-phase-baseline.png',highres=True)

myscale=fluxscale(vis=vis,caltable='3c391_ctm_mosaic_10s_spw0.G1',fluxtable='3c391_ctm_mosaic_10s_spw0.fluxscale1',reference='J1331+3030',transfer=['J1822-0938'],incremental=False)

plotms(vis='3c391_ctm_mosaic_10s_spw0.fluxscale1',xaxis='time',yaxis='amp',correlation='R',coloraxis='baseline',showgui=False,plotfile='plotms_3c391-fluxscale1-amp-R.png',highres=True)

plotms(vis='3c391_ctm_mosaic_10s_spw0.fluxscale1',xaxis='time',yaxis='amp',correlation='L',coloraxis='baseline',showgui=False,plotfile='plotms_3c391-fluxscale1-amp-L.png',highres=True)

applycal(vis=vis,field='J1331+3030',gaintable=['3c391_ctm_mosaic_10s_spw0.antpos','3c391_ctm_mosaic_10s_spw0.fluxscale1','3c391_ctm_mosaic_10s_spw0.K0','3c391_ctm_mosaic_10s_spw0.B0'],gainfield=['','J1331+3030','',''],interp=['','nearest','',''],calwt=False)

applycal(vis=vis,field='J1822-0938',gaintable=['3c391_ctm_mosaic_10s_spw0.antpos','3c391_ctm_mosaic_10s_spw0.fluxscale1','3c391_ctm_mosaic_10s_spw0.K0','3c391_ctm_mosaic_10s_spw0.B0'],gainfield=['','J1822-0938','',''],interp=['','nearest','',''],calwt=False)

applycal(vis=vis,field='2~8',gaintable=['3c391_ctm_mosaic_10s_spw0.antpos','3c391_ctm_mosaic_10s_spw0.fluxscale1','3c391_ctm_mosaic_10s_spw0.K0','3c391_ctm_mosaic_10s_spw0.B0'],gainfield=['','J1822-0938','',''],interp=['','linear','',''],calwt=False)

plotms(vis=vis,field='0',correlation='RR,LL',antenna='',avgtime='60',xaxis='channel',yaxis='amp',ydatacolumn='corrected',coloraxis='corr',showgui=False,plotfile='plotms_3c391-fld0-corrected-amp.png',highres=True)

plotms(vis=vis,field='0',correlation='RR,LL',antenna='',avgtime='60',xaxis='channel',yaxis='phase',ydatacolumn='corrected',coloraxis='corr',plotrange=[-1,-1,-180,180],showgui=False,plotfile='plotms_3c391-fld0-corrected-phase.png',highres=True)

plotms(vis=vis,field='1',correlation='RR,LL',antenna='',avgtime='60',xaxis='channel',yaxis='amp',ydatacolumn='corrected',coloraxis='corr',showgui=False,plotfile='plotms_3c391-fld1-corrected-amp.png',highres=True)

plotms(vis=vis,field='1',correlation='RR,LL',antenna='',avgtime='60',xaxis='channel',yaxis='phase',ydatacolumn='corrected',coloraxis='corr',plotrange=[-1,-1,-180,180],showgui=False,plotfile='plotms_3c391-fld1-corrected-phase.png',highres=True)

split(vis=vis,outputvis=splitvis,datacolumn='corrected',field='2~8',correlation='RR,LL')

statwt(vis=splitvis,datacolumn='data')

plotms(vis=splitvis,xaxis='uvwave',yaxis='amp',ydatacolumn='data',field='0',avgtime='30',correlation='RR',showgui=False,plotfile='plotms_3c391-mosaic0-uvwave',highres=True)

tclean(vis=splitvis,imagename='3c391_ctm_spw0_multiscale',field='',spw='',specmode='mfs',niter=20000,gain=0.1,threshold='1.0mJy',gridder='mosaic',deconvolver='multiscale',scales=[0,5,15,45],smallscalebias=0.9,interactive=False,imsize=[480,480],cell=['2.5arcsec','2.5arcsec'],stokes='I',weighting='briggs',robust=0.5,pbcor=False,savemodel='modelcolumn')

impbcor(imagename='3c391_ctm_spw0_multiscale.image',pbimage='3c391_ctm_spw0_multiscale.pb',outfile='3c391_ctm_spw0_multiscale.pbcorimage')

exportfits(imagename='3c391_ctm_spw0_multiscale.image',fitsimage='3c391_ctm_spw0_multiscale_clean.fits')

delmod(vis=splitvis)

tclean(vis=splitvis,imagename='3c391_ctm_spw0_ms_I',field='',spw='',specmode='mfs',niter=500,gain=0.1,threshold='1mJy',gridder='mosaic',deconvolver='multiscale',scales=[0,5,15,45],smallscalebias=0.9,interactive=False,imsize=[480,480],cell=['2.5arcsec','2.5arcsec'],stokes='I',weighting='briggs',robust=0.5,pbcor=False,savemodel='modelcolumn')

gaincal(vis=splitvis,caltable='3c391_ctm_mosaic_spw0.selfcal1',field='',spw='',selectdata=False,solint='30s',refant='ea21',minblperant=4,minsnr=3,gaintype='G',calmode='p')

applycal(vis=splitvis,field='',spw='',selectdata=False,gaintable=['3c391_ctm_mosaic_spw0.selfcal1'],gainfield=[''],interp=['nearest'],calwt=[False],applymode='calflag')

tclean(vis=splitvis,imagename='3c391_ctm_spw0_multiscale_selfcal1',field='',spw='',specmode='mfs',niter=20000,gain=0.1,threshold='1mJy',gridder='mosaic',deconvolver='multiscale',scales=[0,5,15,45],smallscalebias=0.9,interactive=False,imsize=[480,480],cell=['2.5arcsec','2.5arcsec'],stokes='I',weighting='briggs',robust=0.5,pbcor=False,savemodel='modelcolumn')

exportfits(imagename='3c391_ctm_spw0_multiscale_selfcal1.image',fitsimage='3c391_ctm_spw0_multiscale_selfcal1_clean.fits')
