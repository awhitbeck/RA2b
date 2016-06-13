from ROOT import *

gROOT.ProcessLine(".L ~/tdrstyle.C")
gROOT.ProcessLine("setTDRStyle()")

Data_tree = TChain("tree")
Data_tree.Add("root://cmsxrootd.fnal.gov//store/user/lpcsusyhad/SusyRA2Analysis2015/Skims/Run2ProductionV7/tree_GJetLoose_CleanVars/tree_SinglePhoton_2016B.root")

canBarrel = TCanvas("canBarrel","canBarrel",500,500)

Data_tree.Draw("MHT>>numEB(40,100,500)","TriggerPass[34]==1&&TriggerPass[33]&&photon_pfChargedIsoRhoCorr<2.67&&photon_isEB==1&&HT>500&&NJets>=2")
Data_tree.Draw("MHT>>denEB(40,100,500)","TriggerPass[33]&&photon_pfChargedIsoRhoCorr<2.67&&photon_isEB==1&&HT>500&&NJets>=2")

ratioEB = TH1F(gDirectory.Get("numEB"))
ratioEB.Divide(gDirectory.Get("denEB"))
ratioEB.GetXaxis().SetRangeUser(165,500)

gStyle.SetOptStat(0)
ratioEB.GetYaxis().SetTitle("Efficiency")
#ratioEB.GetXaxis().SetTitle("p_{T,#gamma}")
ratioEB.GetXaxis().SetTitle("H_{T}^{miss} [GeV]")
ratioEB.SetMarkerStyle(8)

Data_tree.Draw("MHT>>numEE(40,100,500)","TriggerPass[34]==1&&TriggerPass[33]&&photon_pfChargedIsoRhoCorr<1.79&&photon_isEB==0&&HT>500&&NJets>=2")
Data_tree.Draw("MHT>>denEE(40,100,500)","TriggerPass[33]&&photon_pfChargedIsoRhoCorr<1.79&&photon_isEB==0&&HT>500&&NJets>=2")

ratioEE = TH1F(gDirectory.Get("numEE"))
ratioEE.Divide(gDirectory.Get("denEE"))
ratioEE.GetXaxis().SetRangeUser(165,500)

gStyle.SetOptStat(0)
ratioEE.GetYaxis().SetTitle("Efficiency")
#ratioEE.GetXaxis().SetTitle("p_{T,#gamma}")
ratioEE.GetXaxis().SetTitle("H_{T}^{miss} [GeV]")
ratioEE.SetMarkerStyle(4)
ratioEE.SetMarkerColor(4)

ratioEB.Draw("p")
ratioEE.Draw("p,SAME")
