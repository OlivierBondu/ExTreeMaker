from eventSelection import *
# we use the class from Andrea, with an additional method to add jets to the "event"
# that class also fills automatically the efficiency and SF.
import ROOT
ROOT.gSystem.Load("libFWCoreFWLite.so")
ROOT.AutoLibraryLoader.enable()
ROOT.gSystem.Load("libUserCodezbb_louvain.so")
from DataFormats.FWLite import Events, Handle
from zbbCommons import zbblabel,zbbfile
#from myFuncTimer import print_timing

class btaggingWeight:
  """compute the event weight based on btagging SF"""

  def __init__(self,jmin1,jmax1,jmin2,jmax2, file=zbbfile.ssvperfData):
    self.engine=ROOT.BTagWeight(jmin1,jmax1,jmin2,jmax2)
    self.jetHandle = Handle ("vector<pat::Jet>")
    self.zmuHandle = Handle ("vector<reco::CompositeCandidate>")
    self.zeleHandle = Handle ("vector<reco::CompositeCandidate>")
    self.myJetSet = ROOT.JetSet(zbblabel.SF_running_mode,file)
    self.vertexHandle = Handle ("vector<reco::Vertex>")

  def setLimits(self,jmin1,jmax1,jmin2,jmax2):
    self.engine.setLimits(jmin1,jmax1,jmin2,jmax2)

  def setMode(self,mode):
    #reminder: in the engine, the HP includes always HE.
    if mode=="HE": self.engine.setLimits(1,999,0,999)
    elif mode=="HP": self.engine.setLimits(1,999,1,999)
    elif mode=="HEexcl": self.engine.setLimits(1,1,0,1)
    elif mode=="HPexcl": self.engine.setLimits(1,1,1,1)
    elif mode=="HEHE": self.engine.setLimits(2,999,0,999)
    elif mode=="HEHP": self.engine.setLimits(2,999,1,999)
    elif mode=="HPHP": self.engine.setLimits(2,999,2,999)
    else: 
      print "btaggingWeight.py: Unknown mode:",mode
      self.engine.setLimits(0,999,0,999)

  #@print_timing    
  def weight(self,event,muChannel):
    """btag eff weight"""
    # for data, immediately return 1.
    if event.object().event().eventAuxiliary().isRealData():
      return 1.
    # retrieve the objects (jets and Z candidates)
    event.getByLabel(zbblabel.jetlabel,self.jetHandle)
    event.getByLabel(zbblabel.zmumulabel,self.zmuHandle)
    event.getByLabel(zbblabel.zelelabel,self.zeleHandle)
    event.getByLabel (zbblabel.vertexlabel,self.vertexHandle)          
    jets = self.jetHandle.product()
    zCandidatesMu  = self.zmuHandle.product()
    zCandidatesEle = self.zeleHandle.product()
    vertices = self.vertexHandle.product()
    if vertices.size()>0 :
      vertex = vertices[0]
    else:
      vertex = None    
    Z = findBestCandidate(muChannel, vertex, zCandidatesMu, zCandidatesEle)
    # initialize counters
    self.myJetSet.reset()
    ntagsHE = 0
    ntagsHP = 0
    ntagsNoFlvavorHE = 0
    ntagsNoFlvavorHP = 0
    # retrieve the jets
    for jet in jets:
      # apply selection
      if not isGoodJet(jet, Z): continue
      # check flavor
      flavor = jet.partonFlavour()
      # check btagging
      if isBJet(jet,"HP","SSV"):
        ntagsHP += 1
        if flavor == 0:
          if jet.et() > 100. : print "WARNING : SSVHP tagged jet with no flavor and high transverse energy : ", jet.et(), ", eta : ", jet.eta()
          ntagsNoFlvavorHP += 1
      if isBJet(jet,"HE","SSV"):
        ntagsHE += 1
        if flavor == 0:
          if jet.et() > 100. : print "WARNING : SSVHE tagged jet with no flavor and high transverse energy : ", jet.et(), ", eta : ", jet.eta()
          ntagsNoFlvavorHE += 1
      # add to the jetset class
      self.myJetSet.addJet(zbblabel.SF_uncert, flavor,jet.et(),jet.eta())
    if ntagsNoFlvavorHP>=2 and ntagsNoFlvavorHE<2: print "IMPORTANT WARNING : 2 SSVHP tagged jets with no flavour !! Event should be checked !! Event number : ", event.eventAuxiliary().id().event()
    if ntagsNoFlvavorHE>=2 : print "IMPORTANT WARNING : 2 SSVHE tagged jets with no flavour !! Event should be checked !! Event number : ", event.eventAuxiliary().id().event()
    return self.getWeight(self.myJetSet,ntagsHE,ntagsHP)

  def getWeight(self,jetset, ntags1, ntags2):
    return self.engine.weight2(jetset, ntags1, ntags2)

