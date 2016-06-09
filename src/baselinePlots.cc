#include "AnalysisTools/src/analyzer.cc"
#include "AnalysisTools/src/fillHisto.cc"

#include "RA2bUtils/src/RA2bNtuple.cc"
#include "RA2bUtils/src/signalRegion.cc"
#include "RA2bUtils/src/selectBaseline.cc"
#include "RA2bUtils/src/selectPrompt.cc"
#include "RA2bUtils/src/selectBin.cc"
#include "RA2bUtils/src/weightProducer.cc"
#include "RA2bUtils/src/helpers.h"

#include "TString.h"
#include "TChain.h"
#include "TFile.h"

#include <cstdio>
#include <string>
#include <iostream>

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
  
  signalRegion SR(ntuple,sampleTag,"SR");
  
  for( int i = 0 ; i < 100000 /*t->GetEntries()*/ ; i++ ){

    t->GetEntry(i);
    if( i % 10000 == 0 ) 
      cout << "event: " << i << endl;
    ntuple->patchJetID();

    SR.analyze();

  }

  cout << "save tree" << endl;

  TFile* outFile = new TFile("baselinePlots_"+fileTag+".root","RECREATE");
  
  SR.postProcess();

  outFile->Close();
  
  delete ntuple;

}  

