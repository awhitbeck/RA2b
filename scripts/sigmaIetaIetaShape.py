from ROOT import *
gROOT.SetBatch(True)
from optparse import OptionParser
parser = OptionParser()
parser.add_option("-c", "--cut", dest="cut", default="",
                  help="cut string")
parser.add_option("-s", "--saveTag", dest="saveTag", default="inclusive",
                  help="tag added to output file names")
parser.add_option("-d", "--drawVar", dest="drawVar", default="photon_sigmaIetaIeta",
                  help="variable to draw")
parser.add_option("-b", "--binning", dest="binning", default="50,0.,0.02",
                  help="variable to draw")

(options, args) = parser.parse_args()

saveTag = options.saveTag
cut = options.cut
drawVar=options.drawVar
binning=options.binning

Gjets_tree = TChain("tree")
Gjets_tree.Add("root://cmsxrootd.fnal.gov//store/user/lpcsusyhad/SusyRA2Analysis2015/Skims/Run2ProductionV7/tree_GJet_CleanVars/tree_GJets_HT-600toInf.root") 
Gjets_tree.Add("root://cmsxrootd.fnal.gov//store/user/lpcsusyhad/SusyRA2Analysis2015/Skims/Run2ProductionV7/tree_GJet_CleanVars/tree_GJets_HT-400to600.root") 
Gjets_tree.Add("root://cmsxrootd.fnal.gov//store/user/lpcsusyhad/SusyRA2Analysis2015/Skims/Run2ProductionV7/tree_GJet_CleanVars/tree_GJets_HT-200to400.root") 

QCD_tree = TChain("tree")
QCD_tree.Add("root://cmsxrootd.fnal.gov//store/user/lpcsusyhad/SusyRA2Analysis2015/Skims/Run2ProductionV7/tree_GJet_CleanVars/tree_QCD_HT-1000to1500.root")
QCD_tree.Add("root://cmsxrootd.fnal.gov//store/user/lpcsusyhad/SusyRA2Analysis2015/Skims/Run2ProductionV7/tree_GJet_CleanVars/tree_QCD_HT-1500to2000.root")
QCD_tree.Add("root://cmsxrootd.fnal.gov//store/user/lpcsusyhad/SusyRA2Analysis2015/Skims/Run2ProductionV7/tree_GJet_CleanVars/tree_QCD_HT-2000toInf.root")
QCD_tree.Add("root://cmsxrootd.fnal.gov//store/user/lpcsusyhad/SusyRA2Analysis2015/Skims/Run2ProductionV7/tree_GJet_CleanVars/tree_QCD_HT-2000to300.root")
QCD_tree.Add("root://cmsxrootd.fnal.gov//store/user/lpcsusyhad/SusyRA2Analysis2015/Skims/Run2ProductionV7/tree_GJet_CleanVars/tree_QCD_HT-300to500.root")
QCD_tree.Add("root://cmsxrootd.fnal.gov//store/user/lpcsusyhad/SusyRA2Analysis2015/Skims/Run2ProductionV7/tree_GJet_CleanVars/tree_QCD_HT-200to300.root")
QCD_tree.Add("root://cmsxrootd.fnal.gov//store/user/lpcsusyhad/SusyRA2Analysis2015/Skims/Run2ProductionV7/tree_GJet_CleanVars/tree_QCD_HT-500to700.root")
QCD_tree.Add("root://cmsxrootd.fnal.gov//store/user/lpcsusyhad/SusyRA2Analysis2015/Skims/Run2ProductionV7/tree_GJet_CleanVars/tree_QCD_HT-700to1000.root")

Data_tree = TChain("tree")
Data_tree.Add("root://cmsxrootd.fnal.gov//store/user/lpcsusyhad/SusyRA2Analysis2015/Skims/Run2ProductionV7/tree_GJet_CleanVars/tree_SinglePhoton_2016B.root")

#Gjets_tree.Draw("HT>>promptMC(20,250,1500)","Weight*813.*(photon_isEB==1&&photon_pfChargedIsoRhoCorr<2.67&&photon_sigmaIetaIeta<0.0107&&photon_nonPrompt==0{0})".format(cut),"hist,e")
#QCD_tree.Draw("HT>>nonpromptMC(20,250,1500)","Weight*813.*(photon_isEB==1&&photon_pfChargedIsoRhoCorr<2.67&&photon_sigmaIetaIeta<0.0107&&photon_nonPrompt==1{0})".format(cut),"hist,e")
#Data_tree.Draw("HT>>data(20,250,1500)","(photon_isEB==1&&photon_pfChargedIsoRhoCorr<2.67&&photon_sigmaIetaIeta<0.0107{0})".format(cut),"hist,e")

#Gjets_tree.Draw("Photons.Pt()>>promptMC(50,190,1590)","Weight*813.*(photon_isEB==1&&photon_pfChargedIsoRhoCorr<2.67&&photon_sigmaIetaIeta<0.0107&&photon_nonPrompt==0{0})".format(cut),"hist,e")
#QCD_tree.Draw("Photons.Pt()>>nonpromptMC(50,190,1590)","Weight*813.*(photon_isEB==1&&photon_pfChargedIsoRhoCorr<2.67&&photon_sigmaIetaIeta<0.0107&&photon_nonPrompt==1{0})".format(cut),"hist,e")
#Data_tree.Draw("Photons.Pt()>>data(50,190,1590)","(photon_isEB==1&&photon_pfChargedIsoRhoCorr<2.67&&photon_sigmaIetaIeta<0.0107{0})".format(cut),"hist,e")

Gjets_tree.Draw("{0}>>promptMC({1})".format(drawVar,binning),"Weight*813.*(Photons.Pt()>200&&photon_isEB==1&&photon_pfChargedIsoRhoCorr<2.67&&photon_nonPrompt==0{0})".format(cut),"hist,e")
QCD_tree.Draw("{0}>>nonpromptMC({1})".format(drawVar,binning),"Weight*813.*(Photons.Pt()>200&&photon_isEB==1&&photon_pfChargedIsoRhoCorr<2.67&&photon_nonPrompt==1{0})".format(cut),"hist,e")
Data_tree.Draw("{0}>>nonpromptData({1})".format(drawVar,binning),"(Photons.Pt()>200&&photon_isEB==1&&photon_pfChargedIsoRhoCorr>2.67&&TriggerPass[34]==1{0})".format(cut),"hist,e")
Data_tree.Draw("{0}>>data({1})".format(drawVar,binning),"(Photons.Pt()>200&&photon_isEB==1&&photon_pfChargedIsoRhoCorr<2.67&&TriggerPass[34]==1{0})".format(cut),"hist,e")

gROOT.ProcessLine(".L ~/tdrstyle.C")
gROOT.ProcessLine("setTDRStyle()")

can = TCanvas("can","can",500,500)


pad1 = TPad("pad1","top pad",0.01,0.25,0.99,0.99);
pad1.Draw();
pad2 = TPad("pad2","bottom pad",0.01,0.01,0.99,0.25);
pad1.SetTopMargin(.1)
pad1.SetBottomMargin(0)
pad2.SetTopMargin(0)
pad2.Draw();
pad1.cd();

Gjets_histo = gDirectory.Get("promptMC")
Gjets_histo.SetFillColor(kCyan)
Gjets_histo.SetLineWidth(2)
Gjets_histo.SetLineColor(1)
Gjets_histo.GetXaxis().SetTitle("HT")
Gjets_histo.GetYaxis().SetTitle("Events")

QCD_histo = gDirectory.Get("nonpromptMC")
QCD_histo.SetFillColor(kGray)
QCD_histo.SetLineWidth(2)
QCD_histo.SetLineColor(1)
QCD_histo.GetXaxis().SetTitle("HT")
QCD_histo.GetYaxis().SetTitle("Events")

nonPromptData_histo = gDirectory.Get("nonpromptMC")
nonPromptData_histo.SetFillColor(kGray)
nonPromptData_histo.SetLineWidth(2)
nonPromptData_histo.SetLineColor(1)
nonPromptData_histo.Scale(QCD_histo.Integral()/nonPromptData_histo.Integral())
nonPromptData_histo.GetXaxis().SetTitle("HT")
nonPromptData_histo.GetYaxis().SetTitle("Events")

Data_histo = gDirectory.Get("data")
Data_histo.SetMarkerStyle(8)

ratio = TH1F(Gjets_histo)
ratio.Add(QCD_histo)
ratio.Divide(Data_histo)
ratio.GetYaxis().SetRangeUser(0.,2.)
ratio.GetXaxis().SetLabelSize(0.1)
ratio.GetYaxis().SetLabelSize(0.1)
ratio.SetMarkerStyle(8)
ratio.GetXaxis().SetTitle("HT")
ratio.GetYaxis().SetTitle("MC/Data")

stack = THStack("stack","stack")
stack.Add(Gjets_histo)
stack.Add(QCD_histo)
#stack.Add(nonPromptData_histo)

pad1.SetLogy()
Data_histo.Draw("")
stack.Draw("hist,SAME")
Data_histo.Draw("SAME")
pad1.RedrawAxis()

pad2.cd()
ratio.Draw("p")

can.SaveAs("test.png")
