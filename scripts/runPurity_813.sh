#!/bin/bash

python photonPurityChargedIso_813pb.py -c "&&MHT>200&&MHT<250&&NJets>=3" -s "MHT200_250" 
python photonPurityChargedIso_813pb.py -c "&&MHT>250&&MHT<350&&NJets>=3" -s "MHT250_350" 
python photonPurityChargedIso_813pb.py -c "&&MHT>350&&MHT<450&&NJets>=3" -s "MHT350_450" 
python photonPurityChargedIso_813pb.py -c "&&MHT>450&&NJets>=3" -s "MHT450" 

python photonPurityChargedIso_813pb.py -c "&&MHT>200&&MHT<250&&NJets>=3" -s "MHT200_250" -e
python photonPurityChargedIso_813pb.py -c "&&MHT>250&&MHT<350&&NJets>=3" -s "MHT250_350" -e
python photonPurityChargedIso_813pb.py -c "&&MHT>350&&MHT<450&&NJets>=3" -s "MHT350_450" -e
python photonPurityChargedIso_813pb.py -c "&&MHT>450&&NJets>=3" -s "MHT450" -e

scp purityFit_813pb*.png whitbeck@lxplus.cern.ch:www/RA2bPurity/2016/.
