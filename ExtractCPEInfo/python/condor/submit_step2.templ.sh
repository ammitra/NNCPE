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


# Run the step2. The py file will be modified to have the new name
sed -i 's/IJOB/${i}/g' step2_DIGI_L1_DIGI2RAW_HLT.py
cmsRun step2_DIGI_L1_DIGI2RAW_HLT.py

echo "------------------------------------------FINISHED------------------------------------------"
ls -alh

# Rename the output (step2_DIGI_L1_DIGI2RAW_HLT.root)
pwd
mv step2_DIGI_L1_DIGI2RAW_HLT.root step2_DIGI_L1_DIGI2RAW_HLT_${i}.root
ls -alh
