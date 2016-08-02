#!/bin/bash

""" Code to looper over different regions of phase space and compute the photon purity """
""" Currently this code will grab a prompt and non-prompt shape from MC, using the cuts 
    provided by the -c option.  It will also use the sieie sideband, after the cuts provided
    with the -n option, to compute and alternative non-prompt shape.  The purity calculated 
    with both non-prompt shapes are printed.
"""

python photonPurityChargedIso_7p6fb.py -c "&&MHT>200&&MHT<225&&NJets>=3&&HT>300" -s "MHT200_225" -n "&&MHT>200&&MHT<225&&NJets>=3&&HT>300"
python photonPurityChargedIso_7p6fb.py -c "&&MHT>225&&MHT<250&&NJets>=3&&HT>300" -s "MHT225_250" -n "&&MHT>225&&MHT<250&&NJets>=3&&HT>300" 
python photonPurityChargedIso_7p6fb.py -c "&&MHT>250&&MHT<300&&NJets>=3&&HT>300" -s "MHT250_300" -n "&&MHT>250&&MHT<300&&NJets>=3&&HT>300" 
python photonPurityChargedIso_7p6fb.py -c "&&MHT>300&&MHT<350&&NJets>=3&&HT>300" -s "MHT300_350" -n "&&MHT>300&&NJets>=3&&HT>300" 
python photonPurityChargedIso_7p6fb.py -c "&&MHT>350&&MHT<500&&NJets>=3&&HT>300" -s "MHT350_500" -n "&&MHT>300&&NJets>=3&&HT>300"
python photonPurityChargedIso_7p6fb.py -c "&&MHT>500&&NJets>=3&&HT>300" -s "MHT500" -n "&&MHT>300&&NJets>=3&&HT>300"

python photonPurityChargedIso_7p6fb.py -c "&&MHT>200&&MHT<225&&NJets>=3&&HT>300" -s "MHT200_225" -n "&&MHT>200&&MHT<225&&NJets>=3&&HT>300" -e
python photonPurityChargedIso_7p6fb.py -c "&&MHT>225&&MHT<250&&NJets>=3&&HT>300" -s "MHT225_250" -n "&&MHT>225&&MHT<250&&NJets>=3&&HT>300" -e
python photonPurityChargedIso_7p6fb.py -c "&&MHT>250&&MHT<300&&NJets>=3&&HT>300" -s "MHT250_300" -n "&&MHT>250&&MHT<300&&NJets>=3&&HT>300" -e
python photonPurityChargedIso_7p6fb.py -c "&&MHT>300&&MHT<350&&NJets>=3&&HT>300" -s "MHT300_350" -n "&&MHT>300&&NJets>=3&&HT>300" -e
python photonPurityChargedIso_7p6fb.py -c "&&MHT>350&&MHT<500&&NJets>=3&&HT>300" -s "MHT350_500" -n "&&MHT>300&&NJets>=3&&HT>300" -e 
python photonPurityChargedIso_7p6fb.py -c "&&MHT>500&&NJets>=3&&HT>300" -s "MHT500" -n "&&MHT>300&&NJets>=3&&HT>300" -e 

#scp purityFit*_7p6fb_*.png whitbeck@lxplus.cern.ch:www/RA2bPurity/2016/7p6fb/.
