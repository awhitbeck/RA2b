#!/bin/bash

python photonPurity.py -c "" -s "inclusive"

python photonPurity.py -c "&&NJets==2" -s "NJets2"
python photonPurity.py -c "&&NJets==3" -s "NJets3"
python photonPurity.py -c "&&NJets>=4" -s "NJetsGTE4"

python photonPurity.py -c "&&MHT>250&&MHT<300" -s "MHT250_300"
python photonPurity.py -c "&&MHT>300&&MHT<400" -s "MHT300_400"
python photonPurity.py -c "&&MHT>400&&MHT<500" -s "MHT400_500"
python photonPurity.py -c "&&MHT>500" -s "MHT500"

python photonPurity.py -c "&&HT>500&&HT<650" -s "HT500_650"
python photonPurity.py -c "&&HT>650&&HT<800" -s "HT650_800"
python photonPurity.py -c "&&HT>800" -s "HT800"