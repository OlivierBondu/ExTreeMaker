# configuration of the ControlPlot machinery
from collections import namedtuple

controlPlot = namedtuple("controlPlot", ["label", "module", "classname", "kwargs"])
eventCollection = namedtuple("eventCollection", ["label", "handle", "collection"])
eventProducer = namedtuple("eventProducer", ["label", "module", "function", "kwargs"])
eventWeight = namedtuple("eventWeight", ["label", "module", "classname", "kwargs"])


class configuration:
    # default I/O
    defaultFilename = "controlPlots"
    RDSname = "rds_zbb"
    WSname = "workspace_ras"

    # mode: plots or dataset
    runningMode = "plots"

    # event selection class
    eventSelection = ""

    # control plot classes
    controlPlots = []

    # event content: lists of eventCollection, eventProducer, and eventWeight objects respectively.
    eventCollections = []
    eventProducers = []
    eventWeights = []


class eventDumpConfig:
    # fine-tuning of the event content for display
    productsToPrint = []  # list of product to display (use the producer label)
    collectionsToHide = []  # collections used in the analysis but not printed (use the collection label)

# import the actual implementation of the configuration
import os

theConfig = os.getenv("PatAnalysisCfg")
if theConfig is not None:
    configImplementation = __import__(theConfig)
    atts = theConfig.split(".")[1:]
    for att in atts: configImplementation = getattr(configImplementation, att)
    configuration = configImplementation.configuration
    eventDumpConfig = configImplementation.eventDumpConfig


def printConfig(conf=None):
    if conf is None: return
    print "#########################################################################"
    print "#                        print configuration                            #"
    print "#########################################################################"
    print ""
    for attr in conf.toprint: print "                " + attr + " =", getattr(conf, attr)
    print ""
    print "#########################################################################"
    print "#                         end configuration                             #"
    print "#########################################################################"
    print ""
    return
