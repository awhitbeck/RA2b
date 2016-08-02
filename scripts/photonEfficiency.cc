#ifndef __CINT__
#include "RooGlobalFunc.h"
#endif
#include "TLorentzVector.h"
#include "TChain.h"
#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooGaussian.h"
#include "RooConstVar.h"
#include "RooChebychev.h"
#include "RooAddPdf.h"
#include "RooBernstein.h"
#include "RooSimultaneous.h"
#include "RooCategory.h"
#include "TCanvas.h"
#include "TTree.h"
#include "TFile.h"
#include "TAxis.h"
#include "RooPlot.h"
#include <fstream>
#include <iostream>
#include <string>
#include <stdio.h>

using namespace RooFit ;


void photonEfficiency(){

  // C r e a t e   m o d e l   f o r   p a s s   s a m p l e
  // -------------------------------------------------------------

  // Create observables
  RooRealVar x("x","m_{#gamma#gamma}",60,120) ;
  //RooRealVar w("w","w",0.,999999.);

  // Construct signal pdf
  RooRealVar mean("mean","mean",90,50,150) ;
  RooRealVar sigma("sigma","sigma",0.3,0.1,20) ;
  RooGaussian gx("gx","gx",x,mean,sigma) ;
  RooRealVar mean_fail("mean_fail","mean_fail",90.,60.,120.);
  RooRealVar sigma_fail("sigma_fail","sigma_fail",10.,0.,50.);
  RooGaussian gx_fail("gx_fail","gx_fail",x,mean,sigma) ;

  // Construct background pdf
  RooRealVar a0("a0","a0",0.1,0,1) ;
  RooRealVar a1("a1","a1",0.004,0,1) ;
  RooRealVar a2("a2","a2",0.004,0,1) ;
  RooRealVar a3("a3","a3",0.004,0,1) ;
  RooRealVar a4("a4","a4",0.004,0,1) ;
  RooRealVar a5("a5","a5",0.004,0,1) ;
  RooBernstein px("px","px",x,RooArgSet(a0,a1,a2,a3,a4,a5)) ;

  RooRealVar a0_fail("a0_fail","a0_fail",0.1,0,1) ;
  RooRealVar a1_fail("a1_fail","a1_fail",0.004,0,1) ;
  RooRealVar a2_fail("a2_fail","a2_fail",0.004,0,1) ;
  RooRealVar a3_fail("a3_fail","a3_fail",0.004,0,1) ;
  RooRealVar a4_fail("a4_fail","a4_fail",0.004,0,1) ;
  RooRealVar a5_fail("a5_fail","a5_fail",0.004,0,1) ;
  RooBernstein px_fail("px_fail","px_fail",x,RooArgSet(a0_fail,a1_fail,a2_fail,a3_fail,a4_fail,a5_fail)) ;

  // Construct composite pdf
  RooRealVar f("f","f",0.2,0.,1.) ;
  RooAddPdf myModel("myModel","myModel",RooArgList(gx,px),f) ;

  RooRealVar f_fail("f_fail","f_fail",0.2,0.,1.);
  RooAddPdf myModel_fail("myModel_fail","myModel_fail",RooArgList(gx_fail,px_fail),f_fail);

  RooArgSet vars(x);

  // G e n e r a t e   e v e n t s   f o r   b o t h   s a m p l e s 
  // ---------------------------------------------------------------

  const int numPtCut = 5;
  int ptCut[numPtCut] = {75,100,150,250,1000};

  RooDataSet *dataPass[numPtCut];
  RooDataSet *dataFail[numPtCut];
  //data->weightError(RooAbsData::SumW2);
  //data->weightError(RooAbsData::SumW2);

  char datasetName[256];
  for( int iBin = 0 ; iBin < numPtCut ; iBin++ ){
    sprintf(datasetName,"dataPass_%i",ptCut[iBin]);
    dataPass[iBin] = new RooDataSet(datasetName,datasetName,vars);
    sprintf(datasetName,"dataFail_%i",ptCut[iBin]);
    dataFail[iBin] = new RooDataSet(datasetName,datasetName,vars);
  }

  TChain* t = new TChain("PreSelection");
  //TChain* t = new TChain("TreeMaker2/PreSelection");
  t->SetBranchStatus("*",0);

  string line;
  //ifstream myfile("TPskimDYMCInputs.txt");
  //ifstream myfile("tagProbeDataInputs.txt");
  ifstream myfile("TPskimDataInputs.txt");
  char fileName[256];
  int count = 0;
  if (myfile.is_open()){
    while ( getline (myfile,line) ){
      //cout << "root://cmseos.fnal.gov//" << line << endl;
      //sprintf(fileName,"root://cmseos.fnal.gov///store/user/awhitbe1/photonTagProbeStudies/%s",line.c_str());
      //sprintf(fileName,"root://cmseos.fnal.gov///store/user/lpcsusyhad/SusyRA2Analysis2015/photonTagProbeStudies/%s",line.c_str());
      sprintf(fileName,"root://cmseos.fnal.gov///store/user/awhitbe1/TPskims/%s",line.c_str());
      //cout << fileName << endl;
      t->Add(fileName);
      count++;
      //if( count > 300 ) break;
    }
    myfile.close();
  }else cout << "Unable to open file"; 

  double mGG,Weight;
  bool isPhotonTPpass;
  vector<TLorentzVector> *probePhoton=0;
  t->SetBranchAddress("mGamGam",&mGG);
  //t->SetBranchAddress("Weight",&Weight);
  t->SetBranchAddress("isPhotonTPpass",&isPhotonTPpass);
  t->SetBranchAddress("probePhoton",&probePhoton);

  int numEntries = t->GetEntries();

  for( int iEvt = 0 ; iEvt < numEntries ; iEvt++){
    t->GetEntry(iEvt);
    if( iEvt % 1000000 == 0 ) cout << iEvt << "/" << numEntries << endl;
    //if(mGG>10.)
    //  cout << "mGG: " << mGG << " Weight: " << Weight << " isPhotonTPpass: " << isPhotonTPpass << endl;
    if( mGG<60.||mGG>120. ) continue; 
    x.setVal(mGG);
   
    if( probePhoton->at(0).Pt() < ptCut[0] ) continue;
    int iBin = 0 ;
    while( probePhoton->at(0).Pt() > ptCut[iBin] )
      iBin++;
    
    //cout << "PhotonPt: " << probePhoton->at(0).Pt() << " iBin: " << iBin << endl;
    //w.setVal(Weight);
    if( isPhotonTPpass )
      dataPass[iBin]->add(vars);
    else
      dataFail[iBin]->add(vars);
  }

  
  for( int iBin = 0 ; iBin < numPtCut ; iBin++ ){
    // C r e a t e   i n d e x   c a t e g o r y   a n d   j o i n   s a m p l e s 
    // ---------------------------------------------------------------------------
    
    // Define category to distinguish physics and control samples events
    RooCategory sample("sample","sample") ;
    sample.defineType("pass") ;
    sample.defineType("fail") ;
    
    // Construct combined dataset in (x,sample)
    RooDataSet combData("combData","combined data",x,Index(sample),Import("pass",*(dataPass[iBin])),Import("fail",*(dataFail[iBin]))) ;
    
    // C o n s t r u c t   a   s i m u l t a n e o u s   p d f   i n   ( x , s a m p l e )
    // -----------------------------------------------------------------------------------
    
    // Construct a simultaneous pdf using category sample as index
    RooSimultaneous simPdf("simPdf","simultaneous pdf",sample) ;
    
    // Associate model with the physics state and model_ctl with the control state
    simPdf.addPdf(myModel,"pass") ;
    simPdf.addPdf(myModel_fail,"fail") ;
    
    // P e r f o r m   a   s i m u l t a n e o u s   f i t
    // ---------------------------------------------------
    
    // Perform simultaneous fit of model to data and model_ctl to data_ctl
    simPdf.fitTo(combData) ;
    
    // P l o t   m o d e l   s l i c e s   o n   d a t a    s l i c e s 
    // ----------------------------------------------------------------
    
    // Make a frame for the physics sample
    RooPlot* frame1 = x.frame(Bins(30),Title("Pass sample")) ;
    
    // Plot all data tagged as physics sample
    combData.plotOn(frame1,Cut("sample==sample::pass")) ;
    
    // Plot "physics" slice of simultaneous pdf. 
    // NBL You _must_ project the sample index category with data using ProjWData 
    // as a RooSimultaneous makes no prediction on the shape in the index category 
    // and can thus not be integrated
    simPdf.plotOn(frame1,Slice(sample,"pass"),ProjWData(sample,combData)) ;
    simPdf.plotOn(frame1,Slice(sample,"pass"),Components("px"),ProjWData(sample,combData),LineStyle(kDashed)) ;
    
    // The same plot for the control sample slice
    RooPlot* frame2 = x.frame(Bins(30),Title("Fail sample")) ;
    combData.plotOn(frame2,Cut("sample==sample::fail")) ;
    simPdf.plotOn(frame2,Slice(sample,"fail"),ProjWData(sample,combData)) ;
    simPdf.plotOn(frame2,Slice(sample,"fail"),Components("px_fail"),ProjWData(sample,combData),LineStyle(kDashed)) ;
    
    TCanvas* c = new TCanvas("rf501_simultaneouspdf","rf403_simultaneouspdf",800,400) ;
    c->Divide(2) ;
    c->cd(1) ; gPad->SetLeftMargin(0.15) ; frame1->GetYaxis()->SetTitleOffset(1.4) ; frame1->Draw() ;
    c->cd(2) ; gPad->SetLeftMargin(0.15) ; frame2->GetYaxis()->SetTitleOffset(1.4) ; frame2->Draw() ;
    
    cout << "efficiency(pt>" << ptCut[iBin] << "): " << f.getVal()*dataPass[iBin]->numEntries()/(f.getVal()*dataPass[iBin]->numEntries()+f_fail.getVal()*dataFail[iBin]->numEntries()) << endl;
    char outputFileName[256];
    sprintf(outputFileName,"TagProbeFit_Data_pt%i.png",ptCut[iBin]);
    c->SaveAs(outputFileName);

  }
}
