import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *

# Hadronizer configuration                                                                                                                                      \
                                                                                                                                                                 
generator = cms.EDFilter("Pythia8HadronizerFilter",
    maxEventsToPrint = cms.untracked.int32(1),
    pythiaPylistVerbosity = cms.untracked.int32(1),
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(13000.),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        pythia8PSweightsSettingsBlock,
        processParameters = cms.vstring(
            'SLHA:allowUserOverride = on',
            'ParticleDecays:tau0Max = 1000.1',
            'LesHouches:setLifetime = 2',
            'ParticleDecays:allowPhotonRadiation = on',
            '32:mayDecay = on',
            "32:mWidth = 200"
            '32:doForceWidth = on'                                                                      
        ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'pythia8PSweightsSettings',
                                    'processParameters',
                                    )
    )
)
genParticlesForFilter = cms.EDProducer(
    "GenParticleProducer",
    saveBarCodes=cms.untracked.bool(True),
    src=cms.InputTag("generator", "unsmeared"),
    abortOnUnknownPDGCode=cms.untracked.bool(False)
)

genfilter = cms.EDFilter(
    "GenParticleSelector",
    src = cms.InputTag("genParticlesForFilter"),
    cut = cms.string(' && '.join([
        '(abs(pdgId)==11 || abs(pdgId)==13)',
        'abs(eta)<2.7',
        '(vertex.rho<740. && abs(vertex.Z)<960.)',
        'pt>4.',
        'isLastCopy()',
        'isPromptFinalState()',
        'fromHardProcessFinalState()',
    ]))
)
gencount = cms.EDFilter(
    "CandViewCountFilter",
    src = cms.InputTag("genfilter"),
    minNumber = cms.uint32(4)
)

ProductionFilterSequence = cms.Sequence(
    generator * (genParticlesForFilter + genfilter + gencount)
)
