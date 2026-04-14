# Generating TTbar clusters for the EDAnalyzer 

## CMSSW workflows

We will be generating TTbar clusters using the 12834.0 workflow. To get a list of workflows, run 
```
runTheMatrix.py -n | grep TTbar # gives you the list of all TTbar workflows. we will use 12834.0
runTheMatrix.py -nel 12834.0
```

From this workflow, we run steps 1 and 2. The process for submitting these steps with condor is as follows. 

## Condor submission

No dependencies are required that are not already included in the bare `CMSSW_16_1_0_pre4` environment.

```
python3 Submit_step1.py --nEvents [number of events/job] --nJobs [number of jobs to submit]
```
Then, make space on EOS
```
eosmkdir /store/user/USERNAME/NNCPE
```
Then
```
python3 Submit_step2.py --nJobs [number of jobs submitted in step1]
```

The output can be hadded before passing to the EDAnalyzer
```
hadd step2_DIGI_L1_DIGI2RAW_HLT.root step2_DIGI_L1_DIGI2RAW_HLT_*.root
```
