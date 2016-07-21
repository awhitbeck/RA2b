from ROOT import *
from test import *

dR = TH1F("dR",";#Delta R;Events",40,0,3.1415)

tree = QCD_tree

tree.SetBranchStatus("*",0)
tree.SetBranchStatus("GenParticles",1)
tree.SetBranchStatus("GenParticles_PdgId",1)
tree.SetBranchStatus("GenParticles_Status",1)
tree.SetBranchStatus("Photons",1)
tree.SetBranchStatus("Weight",1)

numEntries = tree.GetEntries()
for i in range(numEntries):
    tree.GetEntry(i)

    if i % 10000 == 0 : print i,"/",numEntries
    if i > 100000 : break 

    genParticles = getattr(tree,"GenParticles")
    genParticles_id = getattr(tree,"GenParticles_PdgId")
    genParticles_status = getattr(tree,"GenParticles_Status")
    photons = getattr(tree,"Photons")

    genPhoton = -1
    for j,parId in enumerate(genParticles_id):
        
        if len(photons) == 0 : continue

        if( (genParticles_status[j] == 1) and (genParticles_id[j] == 22) and (genParticles[j].DeltaR(photons[0])<0.1) ) : 
            #print "found Gen photon"
            genPhoton = j
            break

    if genPhoton<0 : continue

    minDR = 99999.
    for j,parId in enumerate(genParticles_id):

        if( (genParticles_status[j]/10 == 7) and (abs(genParticles_id[j]) <= 6 ) and genParticles[j].DeltaR(genParticles[genPhoton]) < minDR ) :
            minDR = genParticles[j].DeltaR(genParticles[genPhoton])

    #print genParticles[j].DeltaR(photons[0])
    dR.Fill(minDR,getattr(tree,"Weight"))    
            
dR.Draw()
    
