from ROOT import *

DY_tree = TChain("tree")
DY_tree.Add("root://cmsxrootd.fnal.gov//store/user/lpcsusyhad/SusyRA2Analysis2015/Skims/Run2ProductionV9/tree_DYe_CleanVars/tree_DYJetsToLL_M-50_HT-100to200.root")
DY_tree.Add("root://cmsxrootd.fnal.gov//store/user/lpcsusyhad/SusyRA2Analysis2015/Skims/Run2ProductionV9/tree_DYe_CleanVars/tree_DYJetsToLL_M-50_HT-200to400.root")
DY_tree.Add("root://cmsxrootd.fnal.gov//store/user/lpcsusyhad/SusyRA2Analysis2015/Skims/Run2ProductionV9/tree_DYe_CleanVars/tree_DYJetsToLL_M-50_HT-400to600.root")
DY_tree.Add("root://cmsxrootd.fnal.gov//store/user/lpcsusyhad/SusyRA2Analysis2015/Skims/Run2ProductionV9/tree_DYe_CleanVars/tree_DYJetsToLL_M-50_HT-600toInf.root")

Data_tree = TChain("tree")
Data_tree.Add("root://cmsxrootd.fnal.gov//store/user/lpcsusyhad/SusyRA2Analysis2015/Skims/Run2ProductionV9/tree_GJetLoose_CleanVars/tree_SinglePhoton_2016B.root")
Data_tree.Add("root://cmsxrootd.fnal.gov//store/user/lpcsusyhad/SusyRA2Analysis2015/Skims/Run2ProductionV9/tree_GJetLoose_CleanVars/tree_SinglePhoton_2016C.root")

triggerIndex=48
print "######################"
print "      Trigger         "
Data_tree.GetEntry(0)
names = getattr(Data_tree,"TriggerNames")
for i,name in enumerate(names) : 
    print i,name
print "######################"

print " - - - - - - - - - - - - - - - - "
print "DY_tree"
print "Data_tree"
print " - - - - - - - - - - - - - - - - "
