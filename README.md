# NNCPE

## Instructions 

To produce an output TTree with this EDAnalyzer, run the following steps:

```
cmsrel CMSSW_14_0_1 
cd CMSSW_14_0_1/
cd src/
cmsenv
git cms-addpkg RecoLocalTracker/SiPixelRecHits
git cms-addpkg RecoLocalTracker/Records
git cms-addpkg RecoTracker/TransientTrackingRecHit
git clone https://github.com/CMSTrackerDPG/SiPixelTools-PixelTrees.git SiPixelTools/PixelTrees
scram b -j
git clone https://github.com/ammitra/NNCPE.git
cd NNCPE/ExtractCPEInfo
scram b -j
cd python
cmsRun ConfFile_cfg.py
```
