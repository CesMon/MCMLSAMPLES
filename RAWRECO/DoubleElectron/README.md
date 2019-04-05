
## step: RECO (AOD)

Select input RAW sample from [CMS Open Data Portal](http://opendata.cern.ch), this example we will use the `root://eospublic.cern.ch//eos/opendata/cms/Run2011A/DoubleElectron/RAW/v1/000/160/431/080D15C9-FF4D-E011-9484-0030487C7828.root` RAW data.


- Execute the *cmsDriver* command as:

```
cmsDriver.py reco -s RAW2DIGI,L1Reco,RECO,USER:EventFilter/HcalRawToDigi/hcallaserhbhehffilter2012_cff.hcallLaser2012Filter --filein root://eospublic.cern.ch//eos/opendata/cms/Run2011A/DoubleElectron/RAW/v1/000/160/431/080D15C9-FF4D-E011-9484-0030487C7828.root --data --conditions FT_R_53_LV5::All --eventcontent AOD  --no_exec --python_filename recoee.py --fileout=recoee.root -n10
```
We now process the event : the reconstruction (RECO).  This command produces a file, *recoee.py*, which needs to be modified
like we did above.  I.e.,

- open the *recoee.py* config file with your favorite text editor and replace the line

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
cmsRun recoee.py > recoee.log 2>&1 &
``` 

- Check the development of the job:

```
tailf recoee.log
```
The resulting ROOT file, recoee.root, is in the same format as the MC and Data released by CMS.
