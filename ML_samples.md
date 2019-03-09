# ML samples with tracker hits
## Description

#### How to produce 

### Examples for CMS 2012 data

#### How to produce ML samples with tracker hits

We will produce these events in four steps.  First we perform the simulation up to the *SIM* step, then another intermedite step
up to the HLT simulation, then the reconstruction, and then finaly use a tipe ED to extract the information. 

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

Next, identify the configuration fragment that determines what physics event generator we wish to use and what topology we intend to generate.  In
this example we will use the `QCDForPF_8TeV_cfi.py` fragment , which can be found in the [/Configuration/Generator/python](https://github.com/cms-sw/cmssw/blob/CMSSW_5_3_X/Configuration/Generator/python) area of CMSSW.  More information on the parameters within this
fragment can be found in the [MC production overview](/docs/cms-mc-production-overview) documentation.

##### Step 0: Generation and simulation

- Execute the *cmsDriver* command as:

```
cmsDriver.py QCDForPF_8TeV_cfi.py --fileout file:gensimML.root --mc --eventcontent RAWSIM --customise Configuration/StandardSequences/SimWithCastor_cff.customise,Configuration/DataProcessing/Utils.addMonitoring --beamspot Realistic8TeVCollision --datatier GEN-SIM --conditions=START53_V27::All --step GEN,SIM --datamix NODATAMIXER --python_filename gensimML.py --no_exec -n 10
```

Note that we put the naked name of our input fragment (*QCDForPF_8TeV_cfi.py*) because the script will look, by default, in
the */Configuration/Generator/python* area of the CMSSW release.  More information about the *--datatier* used can be found at the [CMS Workbook](https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookDataFormats); that is the level of information we need/want in our ROOT output file.

Notice also that wee have used
the `START53_V27::All` conditions, because this is the snapshot of the conditions database we need.  More information about this can
be found at the [CMS Guide for Conditions](docs/cms-guide-for-condition-database) documentation.  As noted above, for this first step, step 0, we
only do the *GEN* and *SIM* parts of the whole chain.  We only generate 10 events for this example and choose the name of *gensimML* for the output files
in order to identify them correctly.

After executing this command, we will get the *gensimML.py* configuration file, which will be run with the *cmsRun* executable.  First, however, we need
to do a few modifications.

- Note that we need to be able to locate the database conditions as required by the *--conditions* switch.  Therefore, we need to make the following
 symbolic links:

```
ln -sf /cvmfs/cms-opendata-conddb.cern.ch/START53_V27 START53_V27

ln -sf /cvmfs/cms-opendata-conddb.cern.ch/START53_V27.db START53_V27.db
```

- Make sure the `cms-opendata-conddb.cern.ch` directory has actually expanded in your VM.  One way of doing this is executing:

```
ls -l
ls -l /cvmfs/
```

You should now see the `cms-opendata-conddb.cern.ch` link in the `/cvmfs` area.

- Open the *gensimML.py* config file with your favorite text editor and change the line

```
process.GlobalTag = GlobalTag(process.GlobalTag, 'START53_V27::All', '')
```

with

```
process.GlobalTag.connect = cms.string('sqlite_file:/cvmfs/cms-opendata-conddb.cern.ch/START53_V27.db')
process.GlobalTag = GlobalTag(process.GlobalTag, 'START53_V27::All', '')
```
- Note for QCD (Pythia) re-generating events from scratch.
GEN-level cut at pThat>600 (need boosted events!) for this in the *gensimML.py* change the line

```
'CKIN(3)=15.           ! minimum pt hat for hard interactions',

```
with


```
'CKIN(3)=600.           ! minimum pt hat for hard interactions',

```


- Run the CMSSW executable in the background

```
cmsRun gensimML.py > gensimML.log 2>&1 &
``` 

- Check the development of the job:

```
tailf gensimML.log
```


##### Step 1: HLT


- Execute the *cmsDriver* command as:

```
cmsDriver.py step1 --filein file:gensimDY.root --step=DIGI,L1,DIGI2RAW,HLT:2011 --datatier GEN-RAW --conditions=START53_LV6A1::All --fileout=hltDY.root --eventcontent RAWSIM --python_filename hltDY.py --number=10 --mc --no_exec
```

Note here that the ROOT file *gensimDY.root*, which was obtained in the last step (step 0), serves as input for step1.  
We now process the event up to the high level trigger (HLT) simulation.  This command produces a file, *hltDY.py*, which needs to be modified
like we did above.  I.e.,

- open the *hltDY.py* config file with your favorite text editor and change the line

```
process.GlobalTag = GlobalTag(process.GlobalTag, 'START53_V27::All', '')
```

with

```
process.GlobalTag.connect = cms.string('sqlite_file:/cvmfs/cms-opendata-conddb.cern.ch/START53_V27.db')
process.GlobalTag = GlobalTag(process.GlobalTag, 'START53_V27::All', '')
```

- Now, run the CMSSW executable in the background

```
cmsRun hltDY.py > hltDY.log 2>&1 &
``` 

- Check the development of the job:

```
tailf hltDY.log
```


##### step 2: RECO (AOD)

- Execute the *cmsDriver* command as:

```
cmsDriver.py step2 --filein file:hltML.root --step RAW2DIGI,L1Reco,RECO,VALIDATION:validation_prod,DQM:DQMOfflinePOGMC --datatier AODSIM,DQM --conditions START53_V27::All --fileout file:hltML.root --mc --eventcontent AODSIM,DQM --python_filename recoML.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n 10
```

Note here that the ROOT file *hltML.root*, which was obtained in the last step (step 1), serves as input for step2.  
We now process the event up to the final step: the reconstruction (RECO).  This command produces a file, *recoML.py*, which needs to be modified
like we did above.  I.e.,

- open the *recoML.py* config file with your favorite text editor and change the line

```
process.GlobalTag = GlobalTag(process.GlobalTag, 'START53_V27::All', '')
```

with

```
process.GlobalTag.connect = cms.string('sqlite_file:/cvmfs/cms-opendata-conddb.cern.ch/START53_V27.db')
process.GlobalTag = GlobalTag(process.GlobalTag, 'START53_V27::All', '')
```


- Now, run the CMSSW executable in the background

```
cmsRun recoML.py > recoML.log 2>&1 &
``` 

- Check the development of the job:

```
tailf recoML.log
```

The resulting ROOT file, *recoML.root*, is in the same format as 
the MC and Data released by CMS.

##### step 3:Extract Information NTUPLE

- Obtain the code from git:
```
git clone git://github.com/cms-legacydata-analyses/PhysObjectExtractorTool.git
cd PhysObjectExtractorTool
```
- Compile everything:
```
cd 
scram b
```
- Make a soft link to the python configuration file
```
ln -s python/physicsobjectsinfo_cfg.py .
```
- Run the CMSSW configuration file
```
cmsRun step3.py
```

##### As a result you will get a ObjectInfoNtuple.root and histo.root file with simple variables and histograms.

