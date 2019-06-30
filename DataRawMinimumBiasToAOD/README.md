# RAW Reconstruction
This sample shows the process of reconstructing RAW data located in CMS Open Data Portal.

To start, first create a [VM](http://opendata.cern.ch/record/252 "CMS Open Data Portal") from the CMS Open Data website.

Then follow these steps:

- Create a CMSSW environment: 

    ```
    cmsrel CMSSW_5_3_32
    ```

- Change to the CMSSW_5_3_32/src/ directory:

    ```
    cd CMSSW_5_3_32/src/
    ```

- Initialize the CMSSW environment:

  ```
  cmsenv
  ```   

- Note that we need to be able to locate the database conditions as required by the *--conditions* switch.  Therefore, we need to make the following
 symbolic links:

```
ln -sf /cvmfs/cms-opendata-conddb.cern.ch/FT_53_LV5_AN1_RUNA FT_53_LV5_AN1

ln -sf /cvmfs/cms-opendata-conddb.cern.ch/FT_53_LV5_AN1_RUNA.db FT_53_LV5_AN1_RUNA.db
```

- Make sure the `cms-opendata-conddb.cern.ch` directory has actually expanded in your VM.  One way of doing this is executing:

```
ls -l
ls -l /cvmfs/
```
# step: RECO (AOD)

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

