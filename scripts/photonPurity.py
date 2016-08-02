from ROOT import *
#gROOT.SetBatch(True)
from optparse import OptionParser
parser = OptionParser()
parser.add_option("-c", "--cut", dest="cut", default="",
                  help="cut string")
parser.add_option("-s", "--saveTag", dest="saveTag", default="inclusive",
                  help="tag added to output file names")

(options, args) = parser.parse_args()

saveTag = options.saveTag
cut = options.cut

Gjets_tree = TChain("tree")
Gjets_tree.Add("root://cmsxrootd.fnal.gov//store/user/lpcsusyhad/SusyRA2Analysis2015/Skims/Run2ProductionV7/tree_GJetLoose_CleanVars/tree_GJets_HT-600toInf.root") 
Gjets_tree.Add("root://cmsxrootd.fnal.gov//store/user/lpcsusyhad/SusyRA2Analysis2015/Skims/Run2ProductionV7/tree_GJetLoose_CleanVars/tree_GJets_HT-400to600.root") 
Gjets_tree.Add("root://cmsxrootd.fnal.gov//store/user/lpcsusyhad/SusyRA2Analysis2015/Skims/Run2ProductionV7/tree_GJetLoose_CleanVars/tree_GJets_HT-200to400.root") 

QCD_tree = TChain("tree")
QCD_tree.Add("root://cmsxrootd.fnal.gov//store/user/lpcsusyhad/SusyRA2Analysis2015/Skims/Run2ProductionV7/tree_GJetLoose_CleanVars/tree_QCD_HT-1000to1500.root")
QCD_tree.Add("root://cmsxrootd.fnal.gov//store/user/lpcsusyhad/SusyRA2Analysis2015/Skims/Run2ProductionV7/tree_GJetLoose_CleanVars/tree_QCD_HT-1500to2000.root")
QCD_tree.Add("root://cmsxrootd.fnal.gov//store/user/lpcsusyhad/SusyRA2Analysis2015/Skims/Run2ProductionV7/tree_GJetLoose_CleanVars/tree_QCD_HT-2000toInf.root")
QCD_tree.Add("root://cmsxrootd.fnal.gov//store/user/lpcsusyhad/SusyRA2Analysis2015/Skims/Run2ProductionV7/tree_GJetLoose_CleanVars/tree_QCD_HT-300to500.root")
QCD_tree.Add("root://cmsxrootd.fnal.gov//store/user/lpcsusyhad/SusyRA2Analysis2015/Skims/Run2ProductionV7/tree_GJetLoose_CleanVars/tree_QCD_HT-200to300.root")
QCD_tree.Add("root://cmsxrootd.fnal.gov//store/user/lpcsusyhad/SusyRA2Analysis2015/Skims/Run2ProductionV7/tree_GJetLoose_CleanVars/tree_QCD_HT-500to700.root")
QCD_tree.Add("root://cmsxrootd.fnal.gov//store/user/lpcsusyhad/SusyRA2Analysis2015/Skims/Run2ProductionV7/tree_GJetLoose_CleanVars/tree_QCD_HT-700to1000.root")

Data_tree = TChain("tree")
Data_tree.Add("root://cmsxrootd.fnal.gov//store/user/lpcsusyhad/SusyRA2Analysis2015/Skims/Run2ProductionV7/tree_GJetLoose_CleanVars/tree_SinglePhoton_2016B.root")

Gjets_tree.Draw("photon_sigmaIetaIeta[0]>>promptMC(30,0.004,.019)","Weight*813.*(Photons[0].Pt()>200&&photon_isEB[0]==1&&photon_pfChargedIsoRhoCorr[0]<2.67&&photon_nonPrompt[0]==0{0})".format(cut),"hist,e")
QCD_tree.Draw("photon_sigmaIetaIeta[0]>>nonpromptMC(30,0.004,.019)","Weight*813.*(Photons[0].Pt()>200&&photon_isEB[0]==1&&photon_pfChargedIsoRhoCorr[0]<2.67&&photon_nonPrompt[0]==1{0})".format(cut),"hist,e")

Data_tree.Draw("photon_sigmaIetaIeta[0]>>Data(30,0.004,.019)","Photons[0].Pt()>200&&photon_isEB[0]==1&&photon_pfChargedIsoRhoCorr[0]<2.67&&TriggerPass[34]==1{0}".format(cut),"")

prompt_hist = gDirectory.Get("promptMC")
prompt_hist.SetFillColor(kCyan)
prompt_hist.SetLineWidth(2)
prompt_hist.SetLineColor(1)
prompt_hist.GetXaxis().SetTitle("#sigma_{i#etai#eta}")
prompt_hist.GetYaxis().SetTitle("Events")

nonPrompt_hist = gDirectory.Get("nonpromptMC")
nonPrompt_hist.SetFillColor(kGray)
nonPrompt_hist.SetLineWidth(2)

stack = THStack("stack","stack")
stack.Add(prompt_hist)
stack.Add(nonPrompt_hist)

Data_hist = gDirectory.Get("Data")
Data_hist.SetMarkerStyle(8)

sieie = RooRealVar("sieie","Iso_{chrg} [GeV]",0.004,0.019)

promptDataHist = RooDataHist("promptDataHist","promptDataHist",RooArgList(sieie),prompt_hist)
promptPdf = RooHistPdf("promptPdf","promptPdf",RooArgSet(sieie),promptDataHist)
nonpromptDataHist = RooDataHist("nonpromptDataHist","nonpromptDataHist",RooArgList(sieie),nonPrompt_hist)
nonpromptPdf = RooHistPdf("nonpromptPdf","nonpromptPdf",RooArgSet(sieie),nonpromptDataHist)

dataHist = RooDataHist("dataHist","dataHist",RooArgList(sieie),Data_hist)

frac = RooRealVar("frac","frac",.85,0.,1.)
model = RooAddPdf("model","model",promptPdf,nonpromptPdf,frac)
model.fitTo(dataHist)

gROOT.ProcessLine(".L ~/tdrstyle.C")
gROOT.ProcessLine("setTDRStyle()")

can = TCanvas("can","can",500,500)

plot = sieie.frame()
dataHist.plotOn(plot)
model.plotOn(plot)
nonpromptPdf.plotOn(plot,RooFit.FillColor(2),RooFit.FillStyle(3144),RooFit.LineColor(2),RooFit.Normalization(1.0-frac.getVal()))

plot.GetXaxis().SetNdivisions(505)

plot.Draw()

sieie.setRange("SR",0.009,0.0107);

promptIntegral   = promptPdf.createIntegral(RooArgSet(sieie));
modelIntegral    = model.createIntegral(RooArgSet(sieie));
promptSRIntegral = promptPdf.createIntegral(RooArgSet(sieie),"SR");
modelSRIntegral  = model.createIntegral(RooArgSet(sieie),"SR");

print "purity in SR: ",frac.getVal()*promptSRIntegral.getVal()*modelIntegral.getVal()/promptIntegral.getVal()/modelSRIntegral.getVal()

print "purity from fit: ",frac.getVal()
print "prompt SR integral: ",promptSRIntegral.getVal()
print "prompt integral: ",promptIntegral.getVal()
print "model SR integral: ",modelSRIntegral.getVal()
print "model integral: ",modelIntegral.getVal()

can.SaveAs("purityFit_{0}.png".format(saveTag))
can.SaveAs("purityFit_{0}.eps".format(saveTag))
can.SaveAs("purityFit_{0}.pdf".format(saveTag))

gPad.SetLogy()
can.SaveAs("purityFit_{0}_LogY.png".format(saveTag))
can.SaveAs("purityFit_{0}_LogY.eps".format(saveTag))
can.SaveAs("purityFit_{0}_LogY.pdf".format(saveTag))
