from ROOT import * 
from array import *

lumi="7.6"

if lumi == "7.6":
    ###########################################################################
    ############################## Barrel #####################################
    ###########################################################################
    MHT = array("f",[212.5,237.5,275,325,425,575])
    MHTerror = array("f",[12.5,12.5,25,25,75,75])
    purity = array("f",[0.944341579209,0.959521101367,0.965271303725,0.971026134259,0.981720236136,0.991119098877])
    purityALT = array("f",[0.971150840258,0.96330746772,0.966452421566,0.939664173971,0.939664173971,0.961137266495,0.978286526734])
    error = array("f",[0.00656516245349,0.0057011177041,0.00450947435528,0.00558545647536,0.00480517500766,0.00689063603255])
    errorALT = array("f",[0.00542612229711,0.00571238731669,0.00451493391904,0.00682312384458,0.00577209974586,0.00865323967479])
    
    ###########################################################################
    ############################## Endcap #####################################
    ###########################################################################
    endcappurity = array("f",[0.880281923856,0.851392537431,0.87714646143,0.881599375369,0.915617885686,0.96367543583])
    endcappurityALT = array("f",[0.894688251853,0.861773659333,0.872903858477,0.854264110652,0.885721600484,0.930952319698])
    endcaperror = array("f",[0.0126939293588,0.0126458417857,0.00985619468983,0.0135603631547,0.0136247995514,0.0265895506679])
    endcaperrorALT = array("f",[0.0121912107837,0.0125372723245,0.00994165843326,0.0140977081982,0.0144650401384,0.0299978411411])
    ###########################################################################
    ###########################################################################

if lumi == "12.9" : 
    ###########################################################################
    ############################## Barrel #####################################
    ###########################################################################
    MHT = array("f",[212.5,237.5,275,325,425,575])
    MHTerror = array("f",[12.5,12.5,25,25,75,75])
    purity = array("f",[0.94467771346,0.960857324408,0.967318745542,0.972838809327,0.982380043414,0.993088056385])
    purityALT = array("f",[0.971347426286,0.963654172228,0.969890493795,0.938550345158,0.959378272551,0.981451193818])
    error = array("f",[0.00513550104204,0.00435111862215,0.00341652063016,0.00417202970992,0.00365185522531,0.00483044994172])
    errorALT = array("f",[0.00424498809225,0.0043905862494,0.00338190064011,0.0052742451016,0.00454840341187,0.00629083432742])
    
    ###########################################################################
    ############################## Endcap #####################################
    ###########################################################################
    endcappurity = array("f",[0.887412367289,0.853619277955,0.880334698036,0.885533466145,0.917127842075,0.962383962776])
    endcappurityALT = array("f",[0.888418628941,0.860411935153,0.871782908266,0.864017352141,0.891750578263,0.931105103956])
    endcaperror = array("f",[0.00956712242188,0.00975827221306,0.00764874174609,0.0103698193227,0.010649758573,0.0210272326187])
    endcaperrorALT = array("f",[0.00941653333241,0.00969523504158,0.00774547594021,0.0107101004403,0.011226183266,0.0235421129728])
    ###########################################################################
    ###########################################################################

###### Make graphs
graph = TGraphErrors(len(MHT),MHT,purity,MHTerror,error)
graph.SetMarkerStyle(8)
graph.SetMarkerColor(2)
graph.SetLineColor(2)
graph.GetXaxis().SetTitle("H_{T}^{miss} [GeV]")
graph.GetYaxis().SetTitle("Purity")
graph.GetXaxis().SetTitleSize(0.05)
graph.GetYaxis().SetTitleSize(1.3)
graph.GetYaxis().SetTitleSize(0.05)
graph.GetYaxis().SetRangeUser(.6,1.)

graphALT = TGraphErrors(len(MHT),MHT,purityALT,MHTerror,errorALT)
graphALT.SetMarkerStyle(4)
graphALT.SetMarkerColor(2)
graphALT.SetLineColor(2)

endcapgraph = TGraphErrors(len(MHT),MHT,endcappurity,MHTerror,endcaperror)
endcapgraph.SetMarkerStyle(8)
endcapgraph.SetMarkerColor(4)
endcapgraph.SetLineColor(4)
endcapgraph.GetXaxis().SetTitle("H_{T}^{miss} [GeV]")
endcapgraph.GetYaxis().SetTitle("Purity")
endcapgraph.GetXaxis().SetTitleSize(0.05)
endcapgraph.GetYaxis().SetTitleSize(1.3)
endcapgraph.GetYaxis().SetTitleSize(0.05)
endcapgraph.GetYaxis().SetRangeUser(0.,1.)

endcapgraphALT = TGraphErrors(len(MHT),MHT,endcappurityALT,MHTerror,endcaperrorALT)
endcapgraphALT.SetMarkerStyle(4)
endcapgraphALT.SetMarkerColor(4)
endcapgraphALT.SetLineColor(4)

##### plot graphs

gROOT.ProcessLine(".L ~/tdrstyle.C")
gROOT.ProcessLine("setTDRStyle()")

can = TCanvas("can","can",500,500)
can.SetTopMargin(.1)

graph.Draw("A,P")
graphALT.Draw("P,SAME")
endcapgraph.Draw("P,SAME")
endcapgraphALT.Draw("P,SAME")

### legend and CMS/lumi label
leg = TLegend(0.3,.2,.8,.5)
leg.SetBorderSize(0)
leg.SetFillColor(0)
leg.AddEntry(graph,"barrel","p")
leg.AddEntry(graphALT,"barrel (non-prompt from data)","p")
leg.AddEntry(endcapgraph,"endcap","p")
leg.AddEntry(endcapgraphALT,"endcap (non-prompt from data)","p")
leg.Draw()

cmsText = TPaveText(.17,.9,.47,.96,"NDC")
cmsText.SetFillColor(0)
cmsText.SetBorderSize(0)
cmsText.AddText("CMS Preliminary")
cmsText.Draw()

lumiText = TPaveText(.72,.9,.97,.96,"NDC")
lumiText.SetFillColor(0)
lumiText.SetBorderSize(0)
lumiText.AddText("7.6 fb^{-1} (13 TeV)")
lumiText.Draw()

can.SaveAs("purityVersusMHT_7p6fb.png")
can.SaveAs("purityVersusMHT_7p6fb.eps")
can.SaveAs("purityVersusMHT_7p6fb.pdf")
