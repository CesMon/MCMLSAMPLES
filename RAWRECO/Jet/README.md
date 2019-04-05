
## step 0: RECO (AOD)

Select input RAW sample from [CMS Open Data Portal](http://opendata.cern.ch), this example we will use the `root://eospublic.cern.ch//eos/opendata/cms/Run2011A/Jet/RAW/v1/000/163/589/06C39F3E-6471-E011-AE08-0030487CD7B4.root` RAW data.


- Execute the *cmsDriver* command as:

```
cmsDriver.py reco -s RAW2DIGI,L1Reco,RECO,USER:EventFilter/HcalRawToDigi/hcallaserhbhehffilter2012_cff.hcallLaser2012Filter --filein root://eospublic.cern.ch//eos/opendata/cms/Run2011A/Jet/RAW/v1/000/163/589/06C39F3E-6471-E011-AE08-0030487CD7B4.root --data --conditions FT_R_53_LV5::All --eventcontent AOD  --no_exec --python_filename recojet.py --fileout=recojet.root -n10
```
We now process the event : the reconstruction (RECO).  This command produces a file, *recojet.py*, which needs to be modified
like we did above.  I.e.,

- open the *recojet.py* config file with your favorite text editor and replace the line

```
process.GlobalTag.globaltag = 'FT_53_LV5_AN1::All'
```

with

```
process.GlobalTag.connect = cms.string('sqlite_file:/cvmfs/cms-opendata-conddb.cern.ch/FT_53_LV5_AN1_RUNA.db')
process.GlobalTag.globaltag = 'FT_53_LV5_AN1::All'
```

- Now, run the CMSSW executable in the background

```
cmsRun recojet.py > recojet.log 2>&1 &
``` 

- Check the development of the job:

```
tailf recojet.log
```