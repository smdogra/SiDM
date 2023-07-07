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

            # Set decay channel of dark photon to chi2+chi1                                                                                                      
            #'32:oneChannel = 1 1.0 0 1000023 1000022',                                                                                                          
            # Set decay length of chi2                                                                                                                           
            #'1000023:mWidth = 4.618802e-07', # must set decay length by width; doing it by tau0 has not worked in the past                                      
            #'1000023:tau0 = 1', # try setting tau0 directly                                                                                                     
            # Set decay channels of chi2 (only mu or e+mu)                                                                                                       
            #'1000023:oneChannel = 1 1.0 0 1000022 11 -11'#,                                                                                                     

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
        'abs(eta)<2.4',
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
