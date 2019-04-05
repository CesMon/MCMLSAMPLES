# RAW Reconstruction
This example shows the reconstruction process from RAW data, We will produce these events in three steps.  First we perform the simulation up to the *SIM* step, then another intermedite step
up to the HLT simulation, and then the reconstruction. 

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

Select input RAW sample from [CMS Open Data Portal](http://opendata.cern.ch), this example we will use the `root://eospublic.cern.ch//eos/opendata/cms/Run2011A/DoubleElectron/RAW/v1/000/160/431/080D15C9-FF4D-E011-9484-0030487C7828.root` RAW data.



## step 0: RECO (AOD)

- Execute the *cmsDriver* command as:

```
cmsDriver.py reco -s --filein root://eospublic.cern.ch//eos/opendata/cms/Run2011A/DoubleElectron/RAW/v1/000/160/431/080D15C9-FF4D-E011-9484-0030487C7828.root --fileout=recoee.root RAW2DIGI,L1Reco,RECO,USER:EventFilter/HcalRawToDigi/hcallaserhbhehffilter2012_cff.hcallLaser2012Filter --data --conditions FT_R_53_LV5::All --eventcontent AOD --customise Configuration/DataProcessing/RecoTLR.customisePrompt --no_exec --python recoee.py -n 10 

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
