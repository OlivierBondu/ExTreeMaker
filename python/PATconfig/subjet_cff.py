import FWCore.ParameterSet.Config as cms
from RecoJets.JetProducers.ak5PFJets_cfi import ak5PFJets
from RecoJets.JetProducers.ak5PFJetsPruned_cfi import ak5PFJetsPruned
from PhysicsTools.PatAlgos.tools.jetTools import *
from RecoJets.JetProducers.SubJetParameters_cfi import SubJetParameters
from UserCode.zbb_louvain.PATconfig.jet_cff import btagInfo, btagdiscriminators
from RecoJets.JetAssociationProducers.ak5JTA_cff import ak5JetTracksAssociatorExplicit


def setupPatSubJets(process, runOnMC):
    # CA8 jets
    process.ca8PFJetsCHS = ak5PFJets.clone(
        src='pfNoElectron',  # or pfNoPileUp, does it make a difference?
        jetPtMin=cms.double(10.0),
        doAreaFastjet=cms.bool(True),
        rParam=cms.double(0.8),
        jetAlgorithm=cms.string("CambridgeAachen"),
    )

    process.ca8PFJetsCHSpruned = ak5PFJetsPruned.clone(  # Pruned CA8 jets
                                                         src='pfNoElectron',
                                                         # or pfNoPileUp, does it make a difference?
                                                         jetPtMin=cms.double(10.0),
                                                         doAreaFastjet=cms.bool(True),
                                                         rParam=cms.double(0.8),
                                                         jetAlgorithm=cms.string("CambridgeAachen"),
                                                         )

    # Add to PAT
    inputJetCorrLabel = ('AK7PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute', 'L2L3Residual'])  # data
    if runOnMC: inputJetCorrLabel = ('AK7PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute'])

    addJetCollection(process,
                     cms.InputTag('ca8PFJetsCHS'),
                     'CA8', 'CHS',
                     doJTA=True,
                     doBTagging=True,
                     jetCorrLabel=inputJetCorrLabel,
                     doType1MET=False,
                     genJetCollection=cms.InputTag("ca8GenJetsNoNu"),  # Why NoNu
                     doJetID=True,
                     btagInfo=btagInfo,
                     btagdiscriminators=btagdiscriminators
                     )
    process.patJetsCA8CHS.embedCaloTowers = False
    process.patJetsCA8CHS.embedPFCandidates = True
    process.patJetsCA8CHS.addTagInfos = cms.bool(True)
    process.selectedPatJetsCA8CHS.cut = 'pt > 15. & abs(eta) < 2.5'  # harder cut?

    process.pileupJetIdProducerChsCA8 = process.pileupJetIdProducerChs.clone(
        jets=cms.InputTag("selectedPatJetsCA8CHS"),
        jec=cms.string("AK7PFchs")
    )

    process.selectedPatJetsCA8CHSWithBeta = cms.EDProducer('JetBetaProducer',
                                                           src=cms.InputTag("selectedPatJetsCA8CHS"),
                                                           primaryVertices=cms.InputTag("goodPV"),
                                                           puJetIdMVA=cms.InputTag("pileupJetIdProducerChsCA8",
                                                                                   "fullDiscriminant"),
                                                           puJetIdFlag=cms.InputTag("pileupJetIdProducerChsCA8",
                                                                                    "fullId"),
                                                           puJetIdentifier=cms.InputTag("pileupJetIdProducerChsCA8"),
                                                           )

    process.cleanPatJetsCA8CHS.src = cms.InputTag("selectedPatJetsCA8CHSWithBeta")
    process.cleanPatJetsCA8CHS.checkOverlaps.muons.requireNoOverlaps = cms.bool(True)
    process.cleanPatJetsCA8CHS.checkOverlaps.muons.deltaR = cms.double(0.8)
    process.cleanPatJetsCA8CHS.checkOverlaps.electrons.requireNoOverlaps = cms.bool(True)
    process.cleanPatJetsCA8CHS.checkOverlaps.electrons.deltaR = cms.double(0.8)

    addJetCollection(process,  # pruned CA8 jets to PAT
                     cms.InputTag('ca8PFJetsCHSpruned'),
                     'CA8', 'CHSpruned',
                     doJTA=True,
                     doBTagging=True,
                     jetCorrLabel=inputJetCorrLabel,
                     doType1MET=False,
                     genJetCollection=cms.InputTag("ca8GenJetsNoNu"),
                     doJetID=True,
                     btagInfo=btagInfo,
                     btagdiscriminators=btagdiscriminators
                     )
    process.patJetsCA8CHSpruned.embedCaloTowers = False
    process.patJetsCA8CHSpruned.embedPFCandidates = True
    process.patJetsCA8CHSpruned.addTagInfos = cms.bool(True)
    process.selectedPatJetsCA8CHSpruned.cut = 'pt > 15. & abs(eta) < 2.5'  # harder cut?
    process.cleanPatJetsCA8CHSpruned.checkOverlaps.muons.requireNoOverlaps = cms.bool(True)
    process.cleanPatJetsCA8CHSpruned.checkOverlaps.muons.deltaR = cms.double(0.8)
    process.cleanPatJetsCA8CHSpruned.checkOverlaps.electrons.requireNoOverlaps = cms.bool(True)
    process.cleanPatJetsCA8CHSpruned.checkOverlaps.electrons.deltaR = cms.double(0.8)

    # subjets
    process.ak5JetTracksAssociatorExplicitCA8PrunedSubjetsPF = ak5JetTracksAssociatorExplicit.clone(
        jets=cms.InputTag("ca8PFJetsCHSpruned", "SubJets")
    )
    process.expImpactParameterTagInfos = process.impactParameterTagInfos.clone(
        jetTracks=cms.InputTag("ak5JetTracksAssociatorExplicitCA8PrunedSubjetsPF"))
    process.expSecondaryVertexTagInfos = process.secondaryVertexTagInfos.clone(
        trackIPTagInfos="expImpactParameterTagInfos")
    process.expInclusiveSecondaryVertexFinderTagInfos = process.inclusiveSecondaryVertexFinderTagInfos.clone(
        trackIPTagInfos="expImpactParameterTagInfos")
    process.expInclusiveSecondaryVertexFinderFilteredTagInfos = process.inclusiveSecondaryVertexFinderFilteredTagInfos.clone(
        trackIPTagInfos="expImpactParameterTagInfos")

    process.expTrackCountingHighEffBJetTags = process.trackCountingHighEffBJetTags.clone(
        tagInfos=cms.VInputTag(cms.InputTag("expImpactParameterTagInfos")))
    process.expTrackCountingHighPurBJetTags = process.trackCountingHighPurBJetTags.clone(
        tagInfos=cms.VInputTag(cms.InputTag("expImpactParameterTagInfos")))
    process.expJetProbabilityBJetTags = process.jetProbabilityBJetTags.clone(
        tagInfos=cms.VInputTag(cms.InputTag("expImpactParameterTagInfos")))
    process.expJetBProbabilityBJetTags = process.jetBProbabilityBJetTags.clone(
        tagInfos=cms.VInputTag(cms.InputTag("expImpactParameterTagInfos")))

    process.expSimpleSecondaryVertexHighEffBJetTags = process.simpleSecondaryVertexHighEffBJetTags.clone(
        tagInfos=cms.VInputTag(cms.InputTag("expSecondaryVertexTagInfos")))
    process.expSimpleSecondaryVertexHighPurBJetTags = process.simpleSecondaryVertexHighPurBJetTags.clone(
        tagInfos=cms.VInputTag(cms.InputTag("expSecondaryVertexTagInfos")))
    process.expSimpleInclusiveSecondaryVertexHighEffBJetTags = process.simpleInclusiveSecondaryVertexHighEffBJetTags.clone(
        tagInfos=cms.VInputTag(cms.InputTag("expInclusiveSecondaryVertexFinderFilteredTagInfos")))
    process.expSimpleInclusiveSecondaryVertexHighPurBJetTags = process.simpleInclusiveSecondaryVertexHighPurBJetTags.clone(
        tagInfos=cms.VInputTag(cms.InputTag("expInclusiveSecondaryVertexFinderFilteredTagInfos")))
    process.expDoubleSecondaryVertexHighEffBJetTags = process.doubleSecondaryVertexHighEffBJetTags.clone(
        tagInfos=cms.VInputTag(cms.InputTag("expInclusiveSecondaryVertexFinderFilteredTagInfos")))

    process.expCombinedSecondaryVertexBJetTags = process.combinedSecondaryVertexBJetTags.clone(
        tagInfos=cms.VInputTag(cms.InputTag("expImpactParameterTagInfos"),
                               cms.InputTag("expSecondaryVertexTagInfos"))
    )
    process.expCombinedSecondaryVertexV1BJetTags = process.combinedSecondaryVertexV1BJetTags.clone(
        tagInfos=cms.VInputTag(cms.InputTag("expImpactParameterTagInfos"),
                               cms.InputTag("expSecondaryVertexTagInfos"))
    )

    process.expCombinedInclusiveSecondaryVertexBJetTags = process.combinedInclusiveSecondaryVertexBJetTags.clone(
        tagInfos=cms.VInputTag(cms.InputTag("expImpactParameterTagInfos"),
                               cms.InputTag("expInclusiveSecondaryVertexFinderFilteredTagInfos"))
    )
    process.expCombinedSecondaryVertexSoftPFLeptonV1BJetTags = process.combinedSecondaryVertexSoftPFLeptonV1BJetTags.clone(
        tagInfos=cms.VInputTag(cms.InputTag("expImpactParameterTagInfos"),
                               cms.InputTag("expInclusiveSecondaryVertexFinderFilteredTagInfos"),
                               cms.InputTag("expSoftPFMuonsTagInfos"),
                               cms.InputTag("expSoftPFElectronsTagInfos")
                               )
    )

    process.expSoftPFMuonsTagInfos = process.softPFMuonsTagInfos.clone(
        jets=cms.InputTag("ca8PFJetsCHSpruned", "SubJets"))
    process.expSoftPFElectronsTagInfos = process.softPFElectronsTagInfos.clone(
        jets=cms.InputTag("ca8PFJetsCHSpruned", "SubJets"))
    process.expSoftPFMuonBJetTags = process.softPFMuonBJetTags.clone(
        tagInfos=cms.VInputTag(cms.InputTag("expSoftPFMuonsTagInfos")))
    process.expSoftPFElectronBJetTags = process.softPFElectronBJetTags.clone(
        tagInfos=cms.VInputTag(cms.InputTag("expSoftPFElectronsTagInfos")))

    process.explicitBtag = cms.Sequence(process.ak5JetTracksAssociatorExplicitCA8PrunedSubjetsPF *
                                        process.expImpactParameterTagInfos * process.expSecondaryVertexTagInfos *
                                        process.expInclusiveSecondaryVertexFinderTagInfos * process.expInclusiveSecondaryVertexFinderFilteredTagInfos *
                                        process.expTrackCountingHighEffBJetTags * process.expTrackCountingHighPurBJetTags *
                                        process.expJetProbabilityBJetTags * process.expJetBProbabilityBJetTags *
                                        process.expSimpleSecondaryVertexHighEffBJetTags * process.expSimpleSecondaryVertexHighPurBJetTags *
                                        process.expSimpleInclusiveSecondaryVertexHighEffBJetTags * process.expSimpleInclusiveSecondaryVertexHighPurBJetTags *
                                        process.expDoubleSecondaryVertexHighEffBJetTags *
                                        process.expSoftPFMuonsTagInfos * process.expSoftPFElectronsTagInfos *
                                        process.expSoftPFMuonBJetTags * process.expSoftPFElectronBJetTags *
                                        process.expCombinedSecondaryVertexBJetTags * process.expCombinedSecondaryVertexV1BJetTags *
                                        process.expCombinedInclusiveSecondaryVertexBJetTags * process.expCombinedSecondaryVertexSoftPFLeptonV1BJetTags
                                        )
    expinfo = cms.VInputTag(
        cms.InputTag("expImpactParameterTagInfos"),
        cms.InputTag("expSecondaryVertexTagInfos"),
        cms.InputTag("expInclusiveSecondaryVertexFinderTagInfos"),
        cms.InputTag("expInclusiveSecondaryVertexFinderFilteredTagInfos"),
        cms.InputTag("expSoftPFMuonsTagInfos"),
        cms.InputTag("expSoftPFElectronsTagInfos")
    )
    expbtag = cms.VInputTag(
        cms.InputTag("expTrackCountingHighEffBJetTags"),
        cms.InputTag("expTrackCountingHighPurBJetTags"),
        cms.InputTag("expJetProbabilityBJetTags"),
        cms.InputTag("expJetBProbabilityBJetTags"),
        cms.InputTag("expSimpleSecondaryVertexHighEffBJetTags"),
        cms.InputTag("expSimpleSecondaryVertexHighPurBJetTags"),
        cms.InputTag("expSimpleInclusiveSecondaryVertexHighEffBJetTags"),
        cms.InputTag("expSimpleInclusiveSecondaryVertexHighPurBJetTags"),
        cms.InputTag("expDoubleSecondaryVertexHighEffBJetTags"),
        cms.InputTag("expSoftPFMuonBJetTags"),
        cms.InputTag("expSoftPFElectronBJetTags"),
        cms.InputTag("expCombinedSecondaryVertexBJetTags"),
        cms.InputTag("expCombinedSecondaryVertexV1BJetTags"),
        cms.InputTag("expCombinedInclusiveSecondaryVertexBJetTags"),
        cms.InputTag("expCombinedSecondaryVertexSoftPFLeptonV1BJetTags")
    )
    inputJetCorrLabel = ('AK5PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute', 'L2L3Residual'])  # data
    if runOnMC: inputJetCorrLabel = ('AK5PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute'])
    addJetCollection(process,
                     cms.InputTag('ca8PFJetsCHSpruned', 'SubJets'),
                     'CA8PrunedSubjets', 'PF',
                     doJTA=True,
                     doBTagging=True,
                     jetCorrLabel=inputJetCorrLabel,
                     doType1MET=False,
                     genJetCollection=cms.InputTag('ca8GenJetsNoNuPruned', 'SubJets'),
                     doJetID=True,
                     btagInfo=btagInfo,
                     btagdiscriminators=btagdiscriminators
                     )
    process.patJetsCA8PrunedSubjetsPF.addJetCharge = False
    process.patJetsCA8PrunedSubjetsPF.embedCaloTowers = False
    process.patJetsCA8PrunedSubjetsPF.embedPFCandidates = True
    process.patJetsCA8PrunedSubjetsPF.addTagInfos = cms.bool(True)
    process.patJetsCA8PrunedSubjetsPF.tagInfoSources += expinfo
    process.patJetsCA8PrunedSubjetsPF.discriminatorSources += expbtag

    process.patDefaultSequence.replace(
        process.patJetsCA8PrunedSubjetsPF,
        process.explicitBtag * process.patJetsCA8PrunedSubjetsPF
    )

    # CA8 genJets
    process.ca8GenJetsNoNu = process.ak7GenJetsNoNu.clone()
    process.ca8GenJetsNoNu.rParam = 0.8
    process.ca8GenJetsNoNu.jetAlgorithm = "CambridgeAachen"

    process.ca8GenJets = process.ak7GenJets.clone()
    process.ca8GenJets.rParam = 0.8
    process.ca8GenJets.jetAlgorithm = "CambridgeAachen"

    process.ca8GenJetsNoNuPruned = process.ca8GenJetsNoNu.clone(  # Pruned gen jets
                                                                  SubJetParameters,
                                                                  usePruning=cms.bool(True),
                                                                  useExplicitGhosts=cms.bool(True),
                                                                  writeCompound=cms.bool(True),
                                                                  jetCollInstanceName=cms.string("SubJets")
                                                                  )

    process.ca8GenJetsPruned = process.ca8GenJets.clone(  # Pruned gen jets
                                                          SubJetParameters,
                                                          usePruning=cms.bool(True),
                                                          useExplicitGhosts=cms.bool(True),
                                                          writeCompound=cms.bool(True),
                                                          jetCollInstanceName=cms.string("SubJets")
                                                          )

    # Nsubjettiness
    process.selectedPatJetsCA8CHSwithNsub = cms.EDProducer("NjettinessAdder",
                                                           src=cms.InputTag("selectedPatJetsCA8CHSWithBeta"),
                                                           cone=cms.double(0.8)
                                                           )

    # BoostedJetMerger: map properly pat fat jets and pat subjets
    process.selectedPatJetsCA8CHSPrunedPacked = cms.EDProducer("BoostedJetMerger",
                                                               jetSrc=cms.InputTag("selectedPatJetsCA8CHSpruned"),
                                                               subjetSrc=cms.InputTag(
                                                                   "selectedPatJetsCA8PrunedSubjetsPF")
                                                               )

    # Sequences
    process.jetMCSequenceCA8CHS = cms.Sequence(
        process.ca8GenJetsNoNu *
        process.ca8GenJets *
        process.ca8GenJetsNoNuPruned *
        process.ca8GenJetsPruned
    )

    process.preSequenceCA8CHS = cms.Sequence(
        process.ca8PFJetsCHS +
        process.ca8PFJetsCHSpruned
    )
    if runOnMC: process.preSequenceCA8CHS += cms.Sequence(process.jetMCSequenceCA8CHS)

    process.patDefaultSequence.replace(
        process.selectedPatJetsCA8CHS,
        cms.Sequence(
            process.selectedPatJetsCA8CHS * process.pileupJetIdProducerChsCA8 * process.selectedPatJetsCA8CHSWithBeta * process.selectedPatJetsCA8CHSwithNsub)
    )
