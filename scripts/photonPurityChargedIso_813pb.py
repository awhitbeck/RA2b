from ROOT import *
gROOT.SetBatch(True)
from optparse import OptionParser
parser = OptionParser()
parser.add_option("-c", "--cut", dest="cut", default="",
                  help="cut string")
parser.add_option("-s", "--saveTag", dest="saveTag", default="inclusive",
                  help="tag added to output file names")
parser.add_option("-e", "--encap", dest="endcap", default=False,action="store_true",
                  help="fit endcap photons")

(options, args) = parser.parse_args()

saveTag = options.saveTag
cut = options.cut
endcap = options.endcap

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

triggerIndex=38
print "######################"
print "      Trigger         "
Data_tree.GetEntry(0)
names = getattr(Data_tree,"TriggerNames")
for i,name in enumerate(names) : 
    print i,name
print "######################"

if endcap : 
    Gjets_tree.Draw("photon_pfChargedIsoRhoCorr[0]>>promptMC(40,0,20)","Photons[0].Pt()>200&&photon_isEB[0]==0&&photon_sigmaIetaIeta[0]<1.&&photon_sigmaIetaIeta[0]<0.0272&&photon_nonPrompt[0]==0{0}".format(cut,triggerIndex))
    QCD_tree.Draw("photon_pfChargedIsoRhoCorr[0]>>nonPromptMC(40,0,20)","Photons[0].Pt()>200&&photon_isEB[0]==0&&photon_sigmaIetaIeta[0]<1.&&photon_sigmaIetaIeta[0]<0.0272&&photon_nonPrompt[0]==1{0}".format(cut,triggerIndex))
    Data_tree.Draw("photon_pfChargedIso[0]>>nonPrompt(40,0,20)","Photons[0].Pt()>200&&photon_isEB[0]==0&&TriggerPass[{1}]==1&&photon_sigmaIetaIeta[0]<1.&&photon_sigmaIetaIeta[0]>0.028{0}".format(cut,triggerIndex))
    Data_tree.Draw("photon_pfChargedIso[0]>>data(40,0,20)","Photons[0].Pt()>200&&photon_isEB[0]==0&&TriggerPass[{1}]==1&&photon_sigmaIetaIeta[0]<1.&&photon_sigmaIetaIeta[0]<0.0272{0}".format(cut,triggerIndex))
else : 
    Gjets_tree.Draw("photon_pfChargedIsoRhoCorr[0]>>promptMC(40,0,20)","Photons[0].Pt()>200&&photon_isEB[0]==1&&photon_sigmaIetaIeta[0]<1.&&photon_sigmaIetaIeta[0]<0.0107&&photon_nonPrompt[0]==0{0}".format(cut,triggerIndex))
    QCD_tree.Draw("photon_pfChargedIsoRhoCorr[0]>>nonPromptMC(40,0,20)","Photons[0].Pt()>200&&photon_isEB[0]==1&&photon_sigmaIetaIeta[0]<1.&&photon_sigmaIetaIeta[0]<0.0107&&photon_nonPrompt[0]==1{0}".format(cut,triggerIndex))
    Data_tree.Draw("photon_pfChargedIso[0]>>nonPrompt(40,0,20)","Photons[0].Pt()>200&&photon_isEB[0]==1&&TriggerPass[{1}]==1&&photon_sigmaIetaIeta[0]<1.&&photon_sigmaIetaIeta[0]>0.0112{0}".format(cut,triggerIndex))
    Data_tree.Draw("photon_pfChargedIso[0]>>data(40,0,20)","Photons[0].Pt()>200&&photon_isEB[0]==1&&TriggerPass[{1}]==1&&photon_sigmaIetaIeta[0]<1.&&photon_sigmaIetaIeta[0]<0.0107{0}".format(cut,triggerIndex))


prompt_hist = gDirectory.Get("promptMC")
prompt_hist.SetFillColor(kCyan)
prompt_hist.SetLineWidth(2)
prompt_hist.SetLineColor(1)
prompt_hist.GetXaxis().SetTitle("Iso_{chrg} [GeV]")
prompt_hist.GetYaxis().SetTitle("Events")

nonPrompt_hist = gDirectory.Get("nonPrompt")
nonPrompt_hist.SetFillColor(kGray)
nonPrompt_hist.SetLineWidth(2)

nonPromptMC_hist = gDirectory.Get("nonPromptMC")
nonPromptMC_hist.SetFillColor(kGray)
nonPromptMC_hist.SetLineWidth(2)

Data_hist = gDirectory.Get("data")
Data_hist.SetMarkerStyle(8)

sieie = RooRealVar("sieie","Iso_{chrg} [GeV]",0.0,100.0)

promptDataHist = RooDataHist("promptDataHist","promptDataHist",RooArgList(sieie),prompt_hist)
promptPdf = RooHistPdf("promptPdf","promptPdf",RooArgSet(sieie),promptDataHist)

nonpromptDataHist = RooDataHist("nonpromptDataHist","nonpromptDataHist",RooArgList(sieie),nonPrompt_hist)
nonpromptDataPdf = RooHistPdf("nonpromptPdf","nonpromptPdf",RooArgSet(sieie),nonpromptDataHist)

nonpromptHist = RooDataHist("nonpromptHist","nonpromptHist",RooArgList(sieie),nonPromptMC_hist)
nonpromptPdf = RooHistPdf("nonpromptPdf","nonpromptPdf",RooArgSet(sieie),nonpromptHist)

dataHist = RooDataHist("dataHist","dataHist",RooArgList(sieie),Data_hist)

frac = RooRealVar("frac","frac",.85,0.,1.)
fracALT = RooRealVar("fracALT","fracALT",.85,0.,1.)
model = RooAddPdf("model","model",promptPdf,nonpromptPdf,frac)
modelALT = RooAddPdf("modelALT","modelALT",promptPdf,nonpromptDataPdf,fracALT)

model.fitTo(dataHist)
modelALT.fitTo(dataHist)

gROOT.ProcessLine(".L ~/tdrstyle.C")
gROOT.ProcessLine("setTDRStyle()")

can = TCanvas("can","can",500,500)

plot = sieie.frame()
dataHist.plotOn(plot)
model.plotOn(plot)
nonpromptPdf.plotOn(plot,RooFit.FillColor(2),RooFit.FillStyle(3144),RooFit.LineColor(2),RooFit.Normalization(1.0-frac.getVal()))

plot.GetXaxis().SetNdivisions(505)

plot.Draw()

if endcap : 
    sieie.setRange("SR",0.0,1.79);
else :
    sieie.setRange("SR",0.0,2.67);

promptIntegral   = promptPdf.createIntegral(RooArgSet(sieie));
modelIntegral    = model.createIntegral(RooArgSet(sieie));
promptSRIntegral = promptPdf.createIntegral(RooArgSet(sieie),"SR");
modelSRIntegral  = model.createIntegral(RooArgSet(sieie),"SR");

print "purity in SR: ",frac.getVal()*promptSRIntegral.getVal()*modelIntegral.getVal()/promptIntegral.getVal()/modelSRIntegral.getVal(),"+/-",frac.getError()*frac.getVal()*promptSRIntegral.getVal()*modelIntegral.getVal()/promptIntegral.getVal()/modelSRIntegral.getVal()/frac.getVal()
print "purity from fit: ",frac.getVal(),"+/-",frac.getError()

modelIntegral    = modelALT.createIntegral(RooArgSet(sieie));
modelSRIntegral  = modelALT.createIntegral(RooArgSet(sieie),"SR");

print "ALT purity in SR: ",fracALT.getVal()*promptSRIntegral.getVal()*modelIntegral.getVal()/promptIntegral.getVal()/modelSRIntegral.getVal(),"+/-",fracALT.getError()*frac.getVal()*promptSRIntegral.getVal()*modelIntegral.getVal()/promptIntegral.getVal()/modelSRIntegral.getVal()/fracALT.getVal()
print "ALT purity from fit: ",fracALT.getVal(),"+/-",fracALT.getError()

can.SetTopMargin(.1)

cmsText = TPaveText(.17,.9,.47,.96,"NDC")
cmsText.SetFillColor(0)
cmsText.SetBorderSize(0)
cmsText.AddText("CMS Preliminary")
cmsText.Draw()

lumiText = TPaveText(.72,.9,.97,.96,"NDC")
lumiText.SetFillColor(0)
lumiText.SetBorderSize(0)
lumiText.AddText("813 pb^{-1} (13 TeV)")
lumiText.Draw()

if endcap : 
    can.SaveAs("purityFit_813pb_endcap_{0}.png".format(saveTag))
    can.SaveAs("purityFit_813pb_endcap_{0}.eps".format(saveTag))
    can.SaveAs("purityFit_813pb_endcap_{0}.pdf".format(saveTag))
else : 
    can.SaveAs("purityFit_813pb_barrel_{0}.png".format(saveTag))
    can.SaveAs("purityFit_813pb_barrel_{0}.eps".format(saveTag))
    can.SaveAs("purityFit_813pb_barrel_{0}.pdf".format(saveTag))

gPad.SetLogy()
if endcap : 
    can.SaveAs("purityFit_813pb_endcap_{0}_LogY.png".format(saveTag))
    can.SaveAs("purityFit_813pb_endcap_{0}_LogY.eps".format(saveTag))
    can.SaveAs("purityFit_813pb_endcap_{0}_LogY.pdf".format(saveTag))
else : 
    can.SaveAs("purityFit_813pb_barrel_{0}_LogY.png".format(saveTag))
    can.SaveAs("purityFit_813pb_barrel_{0}_LogY.eps".format(saveTag))
    can.SaveAs("purityFit_813pb_barrel_{0}_LogY.pdf".format(saveTag))
