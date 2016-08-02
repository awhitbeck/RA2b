
void TPskim(int firstFile = 1 , int lastFile = 999999 , int outputIndex = 1){

  TChain* t = new TChain("TreeMaker2/PreSelection");
  t->SetBranchStatus("*",0);

  string line;
  //ifstream myfile("DYinputs.txt");
  ifstream myfile("tagProbeDataInputs.txt");
  char fileName[256];
  int count = 0;
  if (myfile.is_open()){
    while ( getline (myfile,line) ){
      count++;
      if( count < firstFile || count > lastFile ) continue;
      sprintf(fileName,"root://cmseos.fnal.gov///store/user/lpcsusyhad/SusyRA2Analysis2015/photonTagProbeStudies/%s",line.c_str());
      //sprintf(fileName,"root://cmseos.fnal.gov///store/user/awhitbe1/photonTagProbeStudies/%s",line.c_str());
      t->Add(fileName);
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
  
  TTree* outputTree = t->CloneTree(0);

  for( int iEvt = 0 ; iEvt < t->GetEntries() ; iEvt++){
    t->GetEntry(iEvt);
    if( iEvt % 100000 == 0 ) cout << iEvt << endl;
    //if(mGG>10.)
    //  cout << "mGG: " << mGG << " Weight: " << Weight << " isPhotonTPpass: " << isPhotonTPpass << endl;
    if( mGG>60.&&mGG<120. ) 
      outputTree->Fill();

  }

  char outputFileName[256];
  sprintf(outputFileName,"TPskim_Data_%i.root",outputIndex);
  TFile* outputFile = new TFile(outputFileName,"RECREATE");
  outputTree->Write();
  outputFile->Close();

}
