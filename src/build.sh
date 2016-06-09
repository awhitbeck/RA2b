#!/bin/sh

cd ../../
source /cvmfs/cms.cern.ch/cmsset_default.sh
eval `scramv1 runtime -sh`
cd -

echo $CMSSW_BASE

g++ -g `root-config --cflags --glibs` -I$CMSSW_BASE/src/ $1.cc -o $1.exe
