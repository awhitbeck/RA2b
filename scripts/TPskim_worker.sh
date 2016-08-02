#!/bin/bash

FIRST_FILE=$1
LAST_FILE=$2
OUTPUT_INDEX=$3

source /cvmfs/cms.cern.ch/cmsset_default.sh
scram p CMSSW CMSSW_7_4_2
cd CMSSW_7_4_2/src
eval `scramv1 runtime -sh`
cd -

root -l -n -q -b "TPskim.cc(${FIRST_FILE},${LAST_FILE},${OUTPUT_INDEX})"

xrdcp TPskim_Data_${OUTPUT_INDEX}.root root://cmseos.fnal.gov//store/user/awhitbe1/TPskims/TPskim_Data_${OUTPUT_INDEX}.root
rm *root