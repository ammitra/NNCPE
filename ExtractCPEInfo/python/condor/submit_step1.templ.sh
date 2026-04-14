#!/bin/bash
echo "Starting job on $$(date)" # Date/time of start of job
echo "Running on: $$(uname -a)" # Condor job is running on this node
echo "System software: $$(cat /etc/redhat-release)" # Operating System on that node

# Create the CMSSW env
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=el9_amd64_gcc13
eval `scramv1 project CMSSW CMSSW_16_1_0_pre4`
cd CMSSW_16_1_0_pre4/src/
eval `scramv1 runtime -sh`
echo "CMSSW: "$CMSSW_BASE
cd ../../

# Run the step1
cmsDriver.py TTbar_14TeV_TuneCP5_cfi  -s GEN,SIM -n ${nEvents} --conditions auto:phase1_2024_realistic --beamspot DBrealistic --datatier GEN-SIM --eventcontent FEVTDEBUG --geometry DB:Extended --era Run3_2024 --relval 9000,100

echo "------------------------------------------FINISHED------------------------------------------"
ls -alh

# Rename the output (TTbar_14TeV_TuneCP5_cfi_GEN_SIM.root)
pwd
mv TTbar_14TeV_TuneCP5_cfi_GEN_SIM.root TTbar_14TeV_TuneCP5_cfi_GEN_SIM_${i}.root
ls -alh
