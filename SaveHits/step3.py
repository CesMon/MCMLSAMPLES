import FWCore.ParameterSet.Config as cms

process = cms.Process("Demo")

process.load("Configuration.Geometry.GeometryIdeal_cff")
process.load("Configuration.StandardSequences.MagneticField_38T_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Configuration.StandardSequences.Reconstruction_cff")
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")
process.load("RecoTracker.TransientTrackingRecHit.TTRHBuilders_cff")

process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.StandardSequences.Services_cff")
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")
process.load("RecoTracker.TrackProducer.TrackRefitters_cff") 


#process.GlobalTag.connect = cms.string('sqlite_file:/cvmfs/cms-opendata-conddb.cern.ch/START53_LV6A1.db')
# process.GlobalTag.globaltag = 'START53_LV6A1::All'
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag.connect = cms.string('sqlite_file:/cvmfs/cms-opendata-conddb.cern.ch/START53_V27.db')
process.GlobalTag = GlobalTag(process.GlobalTag, 'START53_V27::All', '')
#process.GlobalTag.connect = cms.string('sqlite_file:/cvmfs/cms-opendata-conddb.cern.ch/START53_LV6A1.db')
#process.GlobalTag = GlobalTag(process.GlobalTag, 'START53_LV6A1::All', '')

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
import FWCore.Utilities.FileUtils as FileUtils

process.source = cms.Source("PoolSource",
    # replace 'myfile.root' with the source file you want to use
    fileNames = cms.untracked.vstring(
        #'file:/afs/cern.ch/work/e/eusai/public/opendata/files/step2_qcd8.root'
        'file:recoML.root'
        #'root://cmsxrootd-site.fnal.gov//store/group/lpcml/eusai/CRAB_UserFiles/step2_TtbarFromOpen_01/190220_154334/0003/step2_TtbarFromOpen_3343.root'
        #'root://cmsxrootd-site.fnal.gov//store/group/lpcml/eusai/CRAB_UserFiles/step2_QCD600to3000_01/190213_183439/0000/step2_QCDPt_15_3000_Flat_V27_1.root'
    )
)


# process.AODSIMoutput = cms.OutputModule("PoolOutputModule",
#     eventAutoFlushCompressedSize = cms.untracked.int32(15728640),
#     outputCommands = cms.untracked.vstring('keep *'),#+cms.untracked.vstring('keep *_siStripMatchedRecHits_*_*','keep *_siPixelRecHits_*_*','keep *_siPixelClusters_*_*','keep *_siStripClusters_*_*'),#cms.untracked.vstring('keep *'),#process.AODSIMEventContent.outputCommands,
#     fileName = cms.untracked.string('file:/afs/cern.ch/work/e/eusai/public/opendata/files/step3_qcd8.root'),
#     dataset = cms.untracked.PSet(
#         filterName = cms.untracked.string(''),
#         dataTier = cms.untracked.string('AODSIM')
#     )
# )

# process.AODSIMoutput_step = cms.EndPath(process.AODSIMoutput)
process.source.skipEvents = cms.untracked.uint32(0)
process.load("RecoLocalTracker.SiPixelRecHits.SiPixelRecHits_cfi")
process.load("RecoLocalTracker.SiStripRecHitConverter.SiStripRecHitConverter_cfi")

process.demo = cms.EDAnalyzer('SaveHits',

   associateRecoTracks = cms.bool(True),
   associateHitbySimTrack = cms.bool(True),
   associatePixel = cms.bool(True),       
   associateStrip = cms.bool(True),
   #usePhase2Tracker = cms.bool(False),
   pixelSimLinkSrc = cms.InputTag("simSiPixelDigis"),
   stripSimLinkSrc = cms.InputTag("simSiStripDigis"),
   #phase2TrackerSimLinkSrc = cms.InputTag("simSiPixelDigis", "Tracker"),
   ROUList = cms.vstring('TrackerHitsPixelBarrelLowTof',
                         'TrackerHitsPixelBarrelHighTof',
                         'TrackerHitsPixelEndcapLowTof',
                         'TrackerHitsPixelEndcapHighTof',
                         'TrackerHitsTIBLowTof',
                         'TrackerHitsTIBHighTof',
                         'TrackerHitsTIDLowTof',
                         'TrackerHitsTIDHighTof',
                         'TrackerHitsTOBLowTof',
                         'TrackerHitsTOBHighTof',
                         'TrackerHitsTECLowTof',
                         'TrackerHitsTECHighTof'),

   TrackerRecHitBuilder = cms.string('WithAngleAndTemplate')

)


process.p = cms.Path(process.siStripMatchedRecHits*process.siPixelRecHits*process.TrackRefitter*process.demo)
process.schedule = cms.Schedule(process.p)#,process.AODSIMoutput_step)
