from ROOT import *
from math import sqrt
gROOT.SetBatch(True)
from optparse import OptionParser
parser = OptionParser()
parser.add_option("-l", "--lowHT", dest="lowHT",default=300,help="low HT cut")
parser.add_option("-u", "--highHT",dest="highHT",default=400,help="high HT cut")

(options, args) = parser.parse_args()

fitCurve = TF1("fitCurve","0.5*[0]*(1.+TMath::Erf((x-[1])/(sqrt(2.)*[2])))",150,500);
fitCurve.SetLineColor(4)
fitCurve.SetParameter(0,.988)
fitCurve.SetParameter(1,175.)
fitCurve.SetParameter(2,37.)
fitCurve.SetParNames("plateau","50%","width")

gROOT.ProcessLine(".L ~/tdrstyle.C")
gROOT.ProcessLine("setTDRStyle()")

Data_tree = TChain("tree")
Data_tree.Add("root://cmsxrootd.fnal.gov//store/user/lpcsusyhad/SusyRA2Analysis2015/Skims/Run2ProductionV8/tree_GJet_CleanVars/tree_JetHT_2016B.root")

can = TCanvas("can","can",500,500)

Data_tree.GetEntry(0)
names = getattr(Data_tree,"TriggerNames")
#for i,name in enumerate(names) :
#    print i,name

targetIndex = 48
HTlow=options.lowHT
HThigh=options.highHT

print "target trigger:",names[targetIndex]

#Data_tree.Draw("MHT>>numEB(40,100,900)","TriggerPass[{0}]==1&&TriggerPass[{1}]&&photon_pfChargedIsoRhoCorr[0]<2.67&&photon_sigmaIetaIeta[0]<0.0107&&photon_isEB[0]==1&&HT>300.&&NJets>=3".format(referenceIndex,targetIndex))
#Data_tree.Draw("MHT>>denEB(40,100,900)","TriggerPass[{0}]&&photon_pfChargedIsoRhoCorr[0]<2.67&&photon_sigmaIetaIeta[0]<0.0107&&photon_isEB[0]==1&&HT>300.&&NJets>=3".format(referenceIndex))

Data_tree.Draw("MHT>>numEB(40,100,900)","(TriggerPass[38]==1||TriggerPass[37]==1||TriggerPass[36]==1||TriggerPass[35]==1||TriggerPass[34]==1||TriggerPass[33]==1||TriggerPass[32]==1||TriggerPass[31]==1)&&TriggerPass[{0}]&&photon_isEB[0]==1&&Photons[0].Pt()>0.&&HT>{1}&&HT<{2}&&NJets>=3".format(targetIndex,HTlow,HThigh))
Data_tree.Draw("MHT>>denEB(40,100,900)","(TriggerPass[38]==1||TriggerPass[37]==1||TriggerPass[36]==1||TriggerPass[35]==1||TriggerPass[34]==1||TriggerPass[33]==1||TriggerPass[32]==1||TriggerPass[31]==1)&&photon_isEB[0]==1&&Photons[0].Pt()>0.&&HT>{0}&&HT<{1}&&NJets>=3".format(HTlow,HThigh))

ratioEB = TH1F(gDirectory.Get("numEB"))
ratioEB.Divide(gDirectory.Get("denEB"))
ratioEB.GetXaxis().SetRangeUser(165,500)
ratioEB.GetYaxis().SetRangeUser(0.,1.5)

ratioEB.GetYaxis().SetTitle("Efficiency")
ratioEB.GetXaxis().SetTitle("H_{T}^{miss} [GeV]")
ratioEB.SetMarkerStyle(8)

ratioEB.Draw()

barrelEff = TEfficiency(gDirectory.Get("numEB"),gDirectory.Get("denEB"))
barrelEff.Fit(fitCurve,"R")
print "HT>{0}".format(HTlow),"&&HT<{0}".format(HThigh)
print "Barrel par[0]=",fitCurve.GetParameter(0),"+/-",fitCurve.GetParError(0)
print "Barrel par[1]=",fitCurve.GetParameter(1),"+/-",fitCurve.GetParError(1)
print "Barrel par[2]=",fitCurve.GetParameter(2),"+/-",fitCurve.GetParError(2)
barrelEff.SetMarkerStyle(8)
barrelEff.SetMarkerColor(4)

barrelEff.Draw("A,P")
gPad.Update() 
graph = barrelEff.GetPaintedGraph()
graph.SetMinimum(0)
graph.SetMaximum(1.5)
gStyle.SetOptFit(0)
gPad.Update() 

cms = TLatex(0.18, 0.96, 'CMS preliminary,  4.0 fb^{-1},  #sqrt{s} = 13 TeV'  );
cms.SetTextFont(42)
cms.SetTextSize(0.05)
cms.SetNDC()
cms.Draw()

can.SaveAs("TriggerEffVersusMHT_HT{0}_{1}.png".format(HTlow,HThigh))
graph.SetMinimum(.8)
graph.SetMaximum(1.2)
gPad.Update() 
can.SaveAs("TriggerEffVersusMHT_HT{0}_{1}_zoom.png".format(HTlow,HThigh))
