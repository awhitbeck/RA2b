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
parser.add_option("-b", "--binning", dest="binning", default="40,0.,20.",
                  help="histo binning")
parser.add_option("-n", "--nonpromptCut", dest="nonpromptCut", default="&MHT>200&&NJets>=3&&HT>200",
                  help="cut for non-prompt shape from data.")

(options, args) = parser.parse_args()

saveTag = options.saveTag
cut = options.cut
endcap = options.endcap
nonpromptCut = options.nonpromptCut
binning = options.binning
sieie = RooRealVar("sieie","Iso_{chrg} [GeV]",float(binning.split(',')[1]),float(binning.split(',')[2]))
#sieie.setBins(40)

Gjets_tree = TChain("tree")
Gjets_tree.Add("root://cmsxrootd.fnal.gov//store/user/lpcsusyhad/SusyRA2Analysis2015/Skims/Run2ProductionV9/tree_GJetLoose_CleanVars/tree_GJets_HT-600toInf.root") 
Gjets_tree.Add("root://cmsxrootd.fnal.gov//store/user/lpcsusyhad/SusyRA2Analysis2015/Skims/Run2ProductionV9/tree_GJetLoose_CleanVars/tree_GJets_HT-400to600.root") 
Gjets_tree.Add("root://cmsxrootd.fnal.gov//store/user/lpcsusyhad/SusyRA2Analysis2015/Skims/Run2ProductionV9/tree_GJetLoose_CleanVars/tree_GJets_HT-200to400.root") 

QCD_tree = TChain("tree")
QCD_tree.Add("root://cmsxrootd.fnal.gov//store/user/lpcsusyhad/SusyRA2Analysis2015/Skims/Run2ProductionV9/tree_GJetLoose_CleanVars/tree_QCD_HT-1000to1500.root")
QCD_tree.Add("root://cmsxrootd.fnal.gov//store/user/lpcsusyhad/SusyRA2Analysis2015/Skims/Run2ProductionV9/tree_GJetLoose_CleanVars/tree_QCD_HT-1500to2000.root")
QCD_tree.Add("root://cmsxrootd.fnal.gov//store/user/lpcsusyhad/SusyRA2Analysis2015/Skims/Run2ProductionV9/tree_GJetLoose_CleanVars/tree_QCD_HT-2000toInf.root")
QCD_tree.Add("root://cmsxrootd.fnal.gov//store/user/lpcsusyhad/SusyRA2Analysis2015/Skims/Run2ProductionV9/tree_GJetLoose_CleanVars/tree_QCD_HT-300to500.root")
QCD_tree.Add("root://cmsxrootd.fnal.gov//store/user/lpcsusyhad/SusyRA2Analysis2015/Skims/Run2ProductionV9/tree_GJetLoose_CleanVars/tree_QCD_HT-200to300.root")
QCD_tree.Add("root://cmsxrootd.fnal.gov//store/user/lpcsusyhad/SusyRA2Analysis2015/Skims/Run2ProductionV9/tree_GJetLoose_CleanVars/tree_QCD_HT-500to700.root")
QCD_tree.Add("root://cmsxrootd.fnal.gov//store/user/lpcsusyhad/SusyRA2Analysis2015/Skims/Run2ProductionV9/tree_GJetLoose_CleanVars/tree_QCD_HT-700to1000.root")

Data_tree = TChain("tree")
Data_tree.Add("root://cmsxrootd.fnal.gov//store/user/lpcsusyhad/SusyRA2Analysis2015/Skims/Run2ProductionV9/tree_GJetLoose_CleanVars/tree_SinglePhoton_2016C.root")
Data_tree.Add("root://cmsxrootd.fnal.gov//store/user/lpcsusyhad/SusyRA2Analysis2015/Skims/Run2ProductionV9/tree_GJetLoose_CleanVars/tree_SinglePhoton_2016B.root")

triggerIndex=49
print "######################"
print "      Trigger         "
Data_tree.GetEntry(0)
names = getattr(Data_tree,"TriggerNames")
for i,name in enumerate(names) : 
    print i,name
print getattr(Data_tree,"TriggerNames")[triggerIndex]
print "######################"

print "nonpromptCut:",nonpromptCut

if endcap : 
    Gjets_tree.Draw("photon_pfChargedIsoRhoCorr[0]>>promptMC({0})".format(binning),"(Photons[0].Pt()>200&&photon_isEB[0]==0&&photon_sigmaIetaIeta[0]<1.&&photon_sigmaIetaIeta[0]<0.0272&&photon_nonPrompt[0]==0{0})*Weight".format(cut))
    QCD_tree.Draw("photon_pfChargedIsoRhoCorr[0]>>nonPromptMC({0})".format(binning),"(Photons[0].Pt()>200&&photon_isEB[0]==0&&photon_sigmaIetaIeta[0]<1.&&photon_sigmaIetaIeta[0]<0.0272&&photon_nonPrompt[0]==1{0})*Weight".format(cut))
    Data_tree.Draw("photon_pfChargedIso[0]>>nonPrompt({0})".format(binning),"Photons[0].Pt()>200&&photon_isEB[0]==0&&TriggerPass[{1}]==1&&photon_sigmaIetaIeta[0]<1.&&photon_sigmaIetaIeta[0]>0.028{0}".format(nonpromptCut,triggerIndex))
    Data_tree.Draw("photon_pfChargedIso[0]>>data({0})".format(binning),"Photons[0].Pt()>200&&photon_isEB[0]==0&&TriggerPass[{1}]==1&&photon_sigmaIetaIeta[0]<1.&&photon_sigmaIetaIeta[0]<0.0272{0}".format(cut,triggerIndex))
else : 
    Gjets_tree.Draw("photon_pfChargedIsoRhoCorr[0]>>promptMC({0})".format(binning),"(Photons[0].Pt()>200&&photon_isEB[0]==1&&photon_sigmaIetaIeta[0]<1.&&photon_sigmaIetaIeta[0]<0.0107&&photon_nonPrompt[0]==0{0})*Weight".format(cut))
    QCD_tree.Draw("photon_pfChargedIsoRhoCorr[0]>>nonPromptMC({0})".format(binning),"(Photons[0].Pt()>200&&photon_isEB[0]==1&&photon_sigmaIetaIeta[0]<1.&&photon_sigmaIetaIeta[0]<0.0107&&photon_nonPrompt[0]==1{0})*Weight".format(cut))
    Data_tree.Draw("photon_pfChargedIso[0]>>nonPrompt({0})".format(binning),"Photons[0].Pt()>200&&photon_isEB[0]==1&&TriggerPass[{1}]==1&&photon_sigmaIetaIeta[0]<1.&&photon_sigmaIetaIeta[0]>0.0112{0}".format(nonpromptCut,triggerIndex))
    Data_tree.Draw("photon_pfChargedIso[0]>>data({0})".format(binning),"Photons[0].Pt()>200&&photon_isEB[0]==1&&TriggerPass[{1}]==1&&photon_sigmaIetaIeta[0]<1.&&photon_sigmaIetaIeta[0]<0.0107{0}".format(cut,triggerIndex))

prompt_hist = gDirectory.Get("promptMC")
prompt_hist.Sumw2()
prompt_hist.Scale(1./prompt_hist.Integral())
prompt_hist.SetFillColor(kCyan)
prompt_hist.SetLineWidth(2)
prompt_hist.SetLineColor(1)
prompt_hist.GetXaxis().SetTitle("Iso_{chrg} [GeV]")
prompt_hist.GetYaxis().SetTitle("Events")

nonPrompt_hist = gDirectory.Get("nonPrompt")
#nonPrompt_hist.Sumw2()
nonPrompt_hist.Scale(1./nonPrompt_hist.Integral())
nonPrompt_hist.SetFillColor(kGray)
nonPrompt_hist.SetLineWidth(2)

nonPromptMC_hist = gDirectory.Get("nonPromptMC")
nonPromptMC_hist.Sumw2()
nonPromptMC_hist.Scale(1./nonPromptMC_hist.Integral())
nonPromptMC_hist.SetFillColor(kGray)
nonPromptMC_hist.SetLineWidth(2)

Data_hist = gDirectory.Get("data")
Data_hist.SetMarkerStyle(8)

promptDataHist = RooDataHist("promptDataHist","promptDataHist",RooArgList(sieie),prompt_hist)
promptPdf = RooHistPdf("promptPdf","promptPdf",RooArgSet(sieie),promptDataHist)

nonpromptDataHist = RooDataHist("nonpromptDataHist","nonpromptDataHist",RooArgList(sieie),nonPrompt_hist)
nonpromptDataPdf = RooHistPdf("nonpromptDataPdf","nonpromptDataPdf",RooArgSet(sieie),nonpromptDataHist)

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

fitPad = TPad("fit","fit",0.01,0.3,0.99,0.99)
fitPad.SetTopMargin(.1)
fitPad.Draw()
ratioPad = TPad("ratio","ratio",0.01,0.01,0.99,0.29)
ratioPad.SetBottomMargin(.07)
ratioPad.SetTopMargin(0.)
ratioPad.Draw()

fitPad.cd()
plot = sieie.frame()
dataHist.plotOn(plot)
model.plotOn(plot)
nonpromptPdf.plotOn(plot,RooFit.FillColor(2),RooFit.FillStyle(3144),RooFit.LineColor(2),RooFit.Normalization(1.0-frac.getVal()))
plot.GetXaxis().SetNdivisions(505)
plot.Draw()
ratioPad.cd()
ratio = TH1F(prompt_hist)
ratio.Scale(Data_hist.Integral()*frac.getVal()/prompt_hist.Integral())
ratio.Add(nonPromptMC_hist,float(Data_hist.Integral()*(1.-frac.getVal())/nonPromptMC_hist.Integral()))
ratio.Divide(Data_hist)
ratio.SetMarkerStyle(8)
ratio.GetYaxis().SetRangeUser(0.,3.)
ratio.GetXaxis().SetTitleOffset(1.5)
ratio.GetXaxis().SetTitleSize(1.2)
ratio.GetXaxis().SetLabelOffset(1.5)
ratio.GetXaxis().SetNdivisions(505)
ratio.GetYaxis().SetLabelSize(.1)
ratio.GetYaxis().SetTitleSize(.15)
ratio.GetYaxis().SetTitleOffset(.5)
ratio.GetYaxis().SetTitle("Model/Data")
ratio.Draw("e1")

canALT = TCanvas("canALT","canALT",500,500)

fitPadALT = TPad("fitALT","fitALT",0.01,0.3,0.99,0.99)
fitPadALT.SetTopMargin(.1)
fitPadALT.Draw()
ratioPadALT = TPad("ratioALT","ratioALT",0.01,0.01,0.99,0.29)
ratioPadALT.SetBottomMargin(.07)
ratioPadALT.SetTopMargin(0.)
ratioPadALT.Draw()

fitPadALT.Draw()
ratioPadALT.Draw()

fitPadALT.cd()
plotALT = sieie.frame()
dataHist.plotOn(plotALT)
modelALT.plotOn(plotALT)
nonpromptDataPdf.plotOn(plotALT,RooFit.FillColor(2),RooFit.FillStyle(3144),RooFit.LineColor(2),RooFit.Normalization(1.0-fracALT.getVal()))
plotALT.GetXaxis().SetNdivisions(505)
plotALT.Draw()
ratioPadALT.cd()
ratioALT = TH1F(prompt_hist)
ratioALT.Scale(Data_hist.Integral()*fracALT.getVal()/prompt_hist.Integral())
ratioALT.Add(nonPrompt_hist,float(Data_hist.Integral()*(1.-fracALT.getVal())/nonPrompt_hist.Integral()))
ratioALT.Divide(Data_hist)
ratioALT.SetMarkerStyle(8)
ratioALT.GetYaxis().SetRangeUser(0.,3.)
ratioALT.GetXaxis().SetTitleOffset(1.5)
ratioALT.GetXaxis().SetTitleSize(1.2)
ratioALT.GetXaxis().SetLabelOffset(1.5)
ratioALT.GetXaxis().SetNdivisions(505)
ratioALT.GetYaxis().SetLabelSize(.1)
ratioALT.GetYaxis().SetTitleSize(.15)
ratioALT.GetYaxis().SetTitleOffset(.5)
ratioALT.GetYaxis().SetTitle("Model/Data")
ratioALT.Draw("e1")

if endcap : 
    sieie.setRange("SR",0.0,1.79);
else :
    sieie.setRange("SR",0.0,2.67);

promptIntegral   = promptPdf.createIntegral(RooArgSet(sieie));
promptSRIntegral = promptPdf.createIntegral(RooArgSet(sieie),"SR");
nonpromptIntegral = nonpromptPdf.createIntegral(RooArgSet(sieie));
nonpromptSRIntegral = nonpromptPdf.createIntegral(RooArgSet(sieie),"SR");
nonpromptDataIntegral = nonpromptDataPdf.createIntegral(RooArgSet(sieie));
nonpromptDataSRIntegral = nonpromptDataPdf.createIntegral(RooArgSet(sieie),"SR");
modelIntegral    = model.createIntegral(RooArgSet(sieie));
modelSRIntegral  = model.createIntegral(RooArgSet(sieie),"SR");

print "promptALL:",promptIntegral.getVal()
print "promptSR:",promptSRIntegral.getVal()
print "nonpromptALL:",nonpromptIntegral.getVal()
print "nonpromptSR:",nonpromptSRIntegral.getVal()
print "nonpromptDataALL:",nonpromptDataIntegral.getVal()
print "nonpromptDataSR:",nonpromptDataSRIntegral.getVal()
print "modelALL:",modelIntegral.getVal()
print "modelSR:",modelSRIntegral.getVal()

r_prompt = promptSRIntegral.getVal()/promptIntegral.getVal() 
r_nonprompt = nonpromptSRIntegral.getVal()/nonpromptIntegral.getVal()
r_nonpromptData = nonpromptDataSRIntegral.getVal()/nonpromptDataIntegral.getVal() 

purity = frac.getVal()/( (1.-frac.getVal()) * r_nonprompt/r_prompt + frac.getVal() )
print "purity from fit: ",frac.getVal(),"+/-",frac.getError()
print "purity in SR: ",purity,"+/-",frac.getError()/frac.getVal()*purity
purityALT = fracALT.getVal()/( (1.-fracALT.getVal()) * r_nonpromptData/r_prompt + fracALT.getVal() )
print "ALT purity from fit: ",fracALT.getVal(),"+/-",fracALT.getError() 
print "ALT purity in SR: ",purityALT,"+/-",fracALT.getError()/fracALT.getVal()*purityALT

can.SetTopMargin(.1)
canALT.SetTopMargin(.1)

cmsText = TPaveText(.17,.9,.47,.96,"NDC")
cmsText.SetFillColor(0)
cmsText.SetBorderSize(0)
cmsText.AddText("CMS Preliminary")

fitPad.cd()
cmsText.Draw()
fitPadALT.cd()
cmsText.Draw()

lumiText = TPaveText(.72,.9,.97,.96,"NDC")
lumiText.SetFillColor(0)
lumiText.SetBorderSize(0)
lumiText.AddText("7.6 fb^{-1} (13 TeV)")

fitPad.cd()
lumiText.Draw()
fitPadALT.cd()
lumiText.Draw()

if endcap : 
    can.SaveAs("purityFit_7p6fb_endcap_{0}.png".format(saveTag))
    can.SaveAs("purityFit_7p6fb_endcap_{0}.eps".format(saveTag))
    can.SaveAs("purityFit_7p6fb_endcap_{0}.pdf".format(saveTag))
    canALT.SaveAs("purityFit_ALT_7p6fb_endcap_{0}.png".format(saveTag))
    canALT.SaveAs("purityFit_ALT_7p6fb_endcap_{0}.eps".format(saveTag))
    canALT.SaveAs("purityFit_ALT_7p6fb_endcap_{0}.pdf".format(saveTag))
else : 
    can.SaveAs("purityFit_7p6fb_barrel_{0}.png".format(saveTag))
    can.SaveAs("purityFit_7p6fb_barrel_{0}.eps".format(saveTag))
    can.SaveAs("purityFit_7p6fb_barrel_{0}.pdf".format(saveTag))
    canALT.SaveAs("purityFit_ALT_7p6fb_barrel_{0}.png".format(saveTag))
    canALT.SaveAs("purityFit_ALT_7p6fb_barrel_{0}.eps".format(saveTag))
    canALT.SaveAs("purityFit_ALT_7p6fb_barrel_{0}.pdf".format(saveTag))

fitPad.SetLogy()
fitPadALT.SetLogy()

if endcap : 
    can.SaveAs("purityFit_7p6fb_endcap_{0}_LogY.png".format(saveTag))
    can.SaveAs("purityFit_7p6fb_endcap_{0}_LogY.eps".format(saveTag))
    can.SaveAs("purityFit_7p6fb_endcap_{0}_LogY.pdf".format(saveTag))
    canALT.SaveAs("purityFit_ALT_7p6fb_endcap_{0}_LogY.png".format(saveTag))
    canALT.SaveAs("purityFit_ALT_7p6fb_endcap_{0}_LogY.eps".format(saveTag))
    canALT.SaveAs("purityFit_ALT_7p6fb_endcap_{0}_LogY.pdf".format(saveTag))

else : 
    can.SaveAs("purityFit_7p6fb_barrel_{0}_LogY.png".format(saveTag))
    can.SaveAs("purityFit_7p6fb_barrel_{0}_LogY.eps".format(saveTag))
    can.SaveAs("purityFit_7p6fb_barrel_{0}_LogY.pdf".format(saveTag))
    canALT.SaveAs("purityFit_ALT_7p6fb_barrel_{0}_LogY.png".format(saveTag))
    canALT.SaveAs("purityFit_ALT_7p6fb_barrel_{0}_LogY.eps".format(saveTag))
    canALT.SaveAs("purityFit_ALT_7p6fb_barrel_{0}_LogY.pdf".format(saveTag))
