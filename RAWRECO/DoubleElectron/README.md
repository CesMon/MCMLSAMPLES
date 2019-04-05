
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
