import FWCore.ParameterSet.Config as cms
from PhysicsTools.PatAlgos.tools.pfTools import *

def setupPatMuons (process, runOnMC):

     process.patMuons.pfMuonSource = cms.InputTag("pfSelectedMuons") #FIX: pfSelectedMuons is used instead of pfIsolatedMuons in ZH anlysis, reason no obvious need to use pre isolated muons -> isolation done after
     process.patMuons.useParticleFlow=True
     # embedding objects FIX: done in H to llqq  
     process.patMuons.embedTcMETMuonCorrs = False
     process.patMuons.embedCaloMETMuonCorrs = False
     process.patMuons.embedTrack = True
     #FIX: not done in H to llqq
     process.patMuons.embedCombinedMuon = cms.bool(True)
     process.patMuons.embedStandAloneMuon = cms.bool(False)
     process.patMuons.embedPickyMuon = cms.bool(False)
     process.patMuons.embedTpfmsMuon = cms.bool(False)
     process.patMuons.embedPFCandidate = cms.bool(True) 

     if runOnMC : process.muonMatch.src = "pfSelectedMuons"

     # use PFIsolation
     process.muIsoSequence = setupPFMuonIso(process, 'muons', 'PFIso')
     #adaptPFIsoMuons( process, applyPostfix(process,"patMuons",""), 'PFIso') #FIX: done in H to llqq
           
     #
     # MuscleFit for muons:
     #
     
     # identifier of the MuScleFit is Data2012_53X_ReReco for data
     # and Summer12_DR53X_smearReReco for MC (to compare with ReReco data)
     #muscleid = 'Data2012_53X_ReReco'
     #if runOnMC : muscleid = 'Summer12_DR53X_smearReReco'
     
     #process.MuScleFit = cms.EDProducer("MuScleFitPATMuonCorrector",
     #                                   src = cms.InputTag("patMuons"),
     #                                   debug = cms.bool(True),
     #                                   identifier = cms.string(muscleid),
     #                                   applySmearing = cms.bool(runOnMC), # Must be false in data
     #                                   fakeSmearing = cms.bool(False)
     #                                   )

     # Kinematic cuts on electrons: tight to reduce ntuple size:
     #process.selectedPatMuons.src = cms.InputTag("MuScleFit")
     
     process.selectedPatMuons.cut = (
         "pt > 18 && abs(eta) < 2.4"
         )

     # Classic Muons with UserData
     process.selectedMuonsWithIsolationData = cms.EDProducer(
         "MuonIsolationEmbedder",
         src = cms.InputTag("selectedPatMuons"),
         rho = cms.InputTag("kt6PFJets:rho"),
         )

     process.tightMuons = process.selectedPatMuons.clone(
         #src = cms.InputTag('selectedPatMuonsTriggerMatch'),
         src = cms.InputTag('selectedPatMuons'),
         cut = cms.string('isGlobalMuon &'
                          'isPFMuon &'
                          'innerTrack.hitPattern.trackerLayersWithMeasurement>5 &'
                          #fabs(recoMu.innerTrack()->dz(vertex->position())) < 0.5 # to be applied offline
                          'userFloat("RelativePFIsolationDBetaCorr") < 0.2 &' # PF isolation, tighter possibility: 0.12
                          'abs(dB) < 0.2 &' #not anymore 0.02? effect should be small anyway
                          'normChi2 < 10 &'
                          'innerTrack.hitPattern.numberOfValidPixelHits > 0 &'
                          'numberOfMatchedStations>1 &'
                          'globalTrack.hitPattern.numberOfValidMuonHits > 0'
                          )
         )    
     
     # Sequence for muons:
     process.preMuonSeq = cms.Sequence (
          process.muIsoSequence +
          process.pfMuonSequence
          )
     #process.patDefaultSequence.replace(process.patMuons, process.patMuons+process.MuScleFit)
     process.postMuonSeq = cms.Sequence (    
          process.selectedMuonsWithIsolationData +
          process.tightMuons
          )