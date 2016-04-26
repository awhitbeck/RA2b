#include "RA2bNtuple.cc"
#include "analyzer.cc"
#include "lowDphiCR.cc"
#include "leptonCR.cc"
#include "signalRegion.cc"
#include "selectBaseline.cc"
#include "selectLowDphiCR.cc"
#include "selectLeptonCR.cc"
#include "selectPrompt.cc"
#include "selectHighMHT.cc"
#include "selectHighBTags.cc"
#include "selectBin.cc"
#include "skim.cc"
#include "weightProducer.cc"
#include "fillHisto.cc"
#include "fillPhotonTruth.cc"
#include "fillLeptonTruth.cc"

#include "TString.h"
#include "TChain.h"
#include "TFile.h"

#include <cstdio>
#include <string>
#include <iostream>

#include "helpers.h"

using namespace std;

/*  = = = = = = = = = = = = = = = = = =

    Things to develop:  
    
    = = = = = = = = = = = = = = = = = = */

typedef selectBin<RA2bNtuple> binCut;

int main(int argc, char** argv){

  // this code is setup specifically for analyzing one input file at a time.  The output histonames
  // are based on the sample key, from the fmap (see helper.h for details)
  TString fileTag = argv[1];
  fileMap fmap = parseInputs("inputFiles.txt");
  sampleMap rmap = reduceMap(fmap,fileTag);
  if( rmap.size() != 1 ){
    cout << "either no samples found or too many samples found..." << endl;
    return 1;
  }

  TString sampleTag = rmap.begin()->first;
  TChain* t = buildChain(rmap.begin()->second,"TreeMaker2/PreSelection");  
  RA2bNtuple *ntuple = new RA2bNtuple(t);
  
  binCut singlePhotonCut(ntuple,"photonCR");
  singlePhotonCut.minPhotons=1 ; singlePhotonCut.maxPhotons=1;
  signalRegion photonCR(ntuple,sampleTag,"singlePhotonCR");
  signalRegion.addProcessor(&singlePhotonCut,1);
  
  for( int i = 0 ; i < t->GetEntries() ; i++ ){

    t->GetEntry(i);
    if( i % 10000 == 0 ) 
      cout << "event: " << i << endl;
    ntuple->patchJetID();

    signalRegion.analyze();

  }

  cout << "save tree" << endl;

  TFile* outFile = new TFile("fullAnalysis_"+fileTag+".root","RECREATE");
  
  signalRegion.postProcess();

  outFile->Close();
  
  delete ntuple;

}  

