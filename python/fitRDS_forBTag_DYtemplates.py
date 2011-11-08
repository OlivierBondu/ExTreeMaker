
#######################################################
#
# Loop over entries
#
# Loop over jets per event
#
# Get flavor, pt, eta and select jets
#
# Get PV, pT, pTHat and determine per-event weight
#
# Save in a RooDataSet
#   - m(SV)
#   - PV-cat, pT-cat, pThat-cat
#   - weight
#
# (c) Zbb-CP3 Warriors, 2011
#
####################################################

from ROOT import *
import os

gROOT.SetStyle("Plain")
gStyle.SetErrorX(0)

WP       = "HE"    #"HP","HPMET","HP_excl","HE","HEmet","He_excl"
channel  = "El"    #"El","Mu"
template = "hist"  #"keys", "hist"
jec      = 0       #1,3,5
numbins  = 120      #20,40,80
PVreduce = 0

if template=="keys": numbins=40

### Getting a file and a tree

file  = TFile("File_rds_zbb_Mu_MC.root")
ws    = file.Get("ws")
myRDS = ws.data("rds_zbb")

print "myRDS.numEntries() = ", myRDS.numEntries()

#RooDataSet::rds_zbb(eventSelectionrun,
#                    eventSelectionevent,
#                    eventSelectionls,
#                    eventSelectiontriggerSelection,
#                    eventSelectiontriggerBits,
#                    eventSelectionzmassMu,
#                    eventSelectionbestzmassMu,
#                    eventSelectionzmassEle,
#                    eventSelectionbestzmassEle,
#                    eventSelectionzptMu,
#                    eventSelectionbestzptMu,
#                    eventSelectionzptEle,
#                    eventSelectionbestzptEle,
#                    eventSelectionscaldptZbj1,
#                    eventSelectiondrZbj1,
#                    eventSelectiondphiZbj1,
#                    eventSelectionscaldptZbb,
#                    eventSelectiondphiZbb,
#                    eventSelectiondrZbb,
#                    eventSelectiondijetM,
#                    eventSelectiondijetPt,
#                    eventSelectiondijetdR,
#                    eventSelectiondijetSVdR,
#                    eventSelectiondphidijetMET,
#                    eventSelectionZbM,
#                    eventSelectionZbPt,
#                    eventSelectionZbbM,
#                    eventSelectionZbbPt,
#                    eventSelectioncategory,
#                    eventSelectionmu1pt,
#                    eventSelectionmu2pt,
#                    eventSelectionmu1eta,
#                    eventSelectionmu2eta,
#                    eventSelectionmu1etapm,
#                    eventSelectionmu2etapm,
#                    eventSelectionel1pt,
#                    eventSelectionel2pt,
#                    eventSelectionel1eta,
#                    eventSelectionel2eta,
#                    eventSelectionel1etapm,
#                    eventSelectionel2etapm,
#                    eventSelectionSSVHEdisc,
#                    eventSelectionSSVHPdisc,
#                    eventSelectionSVmass,
#                    eventSelectionMET,
#                    eventSelectionMETphi,
#                    eventSelectionjetpt,
#                    eventSelectionjetpt_totunc,
#                    eventSelectionjeteta,
#                    eventSelectionjetetapm,
#                    eventSelectionjetphi,
#                    eventSelectionjetoverlapmu,
#                    eventSelectionjetoverlapele,
#                    eventSelectionjet1pt,
#                    eventSelectionjet1pt_totunc,
#                    eventSelectionjet1eta,
#                    eventSelectionjet1etapm,
#                    eventSelectionjet2pt,
#                    eventSelectionjet2pt_totunc,
#                    eventSelectionjet2eta,
#                    eventSelectionjet2etapm,
#                    eventSelectionbjet1pt,
#                    eventSelectionbjet1pt_totunc,
#                    eventSelectionbjet1eta,
#                    eventSelectionbjet1etapm,
#                    eventSelectionbjet1HEdisc,
#                    eventSelectionbjet1HPdisc,
#                    eventSelectionbjet1SVmass,
#                    eventSelectionbjet2pt,
#                    eventSelectionbjet2pt_totunc,
#                    eventSelectionbjet2eta,
#                    eventSelectionbjet2etapm,
#                    eventSelectionbjet2HEdisc,
#                    eventSelectionbjet2HPdisc,
#                    eventSelectionbjet2SVmass,
#                    eventSelectionnj,
#                    eventSelectionnb,
#                    eventSelectionnbP,
#                    eventSelectionnhf,
#                    eventSelectionnef,
#                    eventSelectionnpf,
#                    eventSelectionchf,
#                    eventSelectionnch,
#                    eventSelectioncef,
#                    eventSelectionjetid,
#                    BtaggingReweightingHE,
#                    BtaggingReweightingHP,
#                    BtaggingReweightingHEexcl,
#                    BtaggingReweightingHPexcl,
#                    BtaggingReweightingHEHE,
#                    BtaggingReweightingHEHP,
#                    BtaggingReweightingHPHP,
#                    LeptonsReweightingweight,
#                    rc_eventSelection_0,
#                    rc_eventSelection_1,
#                    rc_eventSelection_2,
#                    rc_eventSelection_3,
#                    rc_eventSelection_4,
#                    rc_eventSelection_5,
#                    rc_eventSelection_6,
#                    rc_eventSelection_7,
#                    rc_eventSelection_8,
#                    rc_eventSelection_9,
#                    rc_eventSelection_10,
#                    rc_eventSelection_11,
#                    rc_eventSelection_12,
#                    rc_eventSelection_13,
#                    rc_eventSelection_14,
#                    rc_eventSelection_15,
#                    rc_eventSelection_16,
#                    rc_eventSelection_17,
#                    rc_eventSelection_18,
#                    rc_eventSelection_19,
#                    rc_eventSelection_20,
#                    rc_eventSelection_21,
#                    rc_eventSelection_22)


rrv_msv    = ws.var("eventSelectionbjet1SVmass")
#rrv_bTagHE = ws.var("rrv_bTagHE")
#rrv_bTagHP = ws.var("rrv_bTagHP")
rrv_pT     = ws.var("eventSelectionjet1pt")
rrv_eta    = ws.var("eventSelectionjet1eta")
#rrv_nPV    = ws.var("eventSelectionnpf")
rrv_pT_unc = ws.var("ctionbjet1pt_totunc")
rc_flav    = ws.cat("mcSelectioneventType")
rc_sel     = ws.cat("rc_sel")

rrv_pT.setMin(25)
rrv_pT.setMax(150)
rrv_pT.setBins(25)

rrv_eta.setMin(-2.1)
rrv_eta.setMax( +2.1)
rrv_eta.setBins( 21)

rrv_msv.setMin(0)
rrv_msv.setMax(10)
rrv_msv.setBins(numbins)

#rrv_nPV.setMin(0)
#rrv_nPV.setMax(20)
#rrv_nPV.setBins(20)

f_data = 0
if channel == "El"  : f_data = TFile("File_rds_zbb_El_DATA.root")
elif channel == "Mu" : f_data = TFile("File_rds_zbb_Mu_DATA.root")

ws_data=f_data.Get("ws")
DATA = ws_data.data("rds_zbb")

if PVreduce == 1:
    DATA = DATA.reduce("rrv_nPV<4.5")
    myRDS=myRDS.reduce("rrv_nPV<4.5")
if PVreduce == 2:
    DATA = DATA.reduce("rrv_nPV>4.5")
    DATA = DATA.reduce("rrv_nPV<7.5")
    myRDS=myRDS.reduce("rrv_nPV>4.5")
    myRDS=myRDS.reduce("rrv_nPV<7.5")
if PVreduce == 3:
    DATA = DATA.reduce("rrv_nPV>7.5")
    myRDS=myRDS.reduce("rrv_nPV>7.5")

if WP=="HE"         :
    DATA = DATA.reduce("rc_eventSelection_5==1")
    myRDS=myRDS.reduce("rc_eventSelection_5==1")
if WP=="HEMET"      :
    DATA = DATA.reduce("rc_HEMET==1")
    myRDS=myRDS.reduce("rc_HEMET==1")
if WP=="HE_excl"    :
    DATA = DATA.reduce("rc_HE_excl==1")
    myRDS=myRDS.reduce("rc_HE_excl==1")
if WP=="HEMET_excl" :
    DATA = DATA.reduce("rc_HEMET_excl==1")
    myRDS=myRDS.reduce("rc_HEMET_excl==1")
if WP=="HP"         :
    DATA = DATA.reduce("rc_eventSelection_6==1")
    myRDS=myRDS.reduce("rc_eventSelection_6==1")
if WP=="HPMET"      :
    DATA = DATA.reduce("rc_HPMET==1")
    myRDS=myRDS.reduce("rc_HPMET==1")
if WP=="HP_excl"    :
    DATA = DATA.reduce("rc_HP_excl==1")
    myRDS=myRDS.reduce("rc_HP_excl==1")
if WP=="HPMET_excl" :
    DATA = DATA.reduce("rc_HPMET_excl==1")
    myRDS=myRDS.reduce("rc_HPMET_excl==1")

print "DATA.numEntries() = ", DATA.numEntries()


RAS = DATA.get()
DATA_withunc = RooDataSet("rds_zbb_with_unc","rds_zbb_with_unc",RAS)

for i in range(0,DATA.numEntries()):
    RASi = DATA.get(i)
    ptVal = RASi.getRealValue("rrv_pT")
    ptuncVal = RASi.getRealValue("rrv_pT_unc")*ptVal
    RAS.setRealValue("rrv_pT",ptVal+jec*ptuncVal)
    DATA_withunc.add(RAS)

DATA = DATA_withunc

myRDS_l = myRDS.reduce("mcSelectioneventType==1")
myRDS_c = myRDS.reduce("mcSelectioneventType==2")
myRDS_b = myRDS.reduce("mcSelectioneventType==3")

print "myRDS_l.numEntries() = ", myRDS_l.numEntries()
print "myRDS_c.numEntries() = ", myRDS_c.numEntries()
print "myRDS_b.numEntries() = ", myRDS_b.numEntries()

### This takes too long:
#print "redduced datasets, making keys"
#myRKP   = RooKeysPdf("myRKP",  "myRKP",  rrv_msv,myRDS)
#print "making b-keys"
#myRKP_b = RooKeysPdf("myRKP_b","myRKP_b",rrv_msv,myRDS_l)
#print "making c-keys"
#myRKP_c = RooKeysPdf("myRKP_c","myRKP_c",rrv_msv,myRDS_c)
#print "making l-keys"
#myRKP_l = RooKeysPdf("myRKP_l","myRKP_l",rrv_msv,myRDS_b)

print "making roodatahist"

myRDH   = RooDataHist("myRDH",   "myRDH",   RooArgSet(rrv_msv), myRDS  )
myRDH_b = RooDataHist("myRDH_b", "myRDH_b", RooArgSet(rrv_msv), myRDS_b)
myRDH_c = RooDataHist("myRDH_c", "myRDH_c", RooArgSet(rrv_msv), myRDS_c)
myRDH_l = RooDataHist("myRDH_l", "myRDH_l", RooArgSet(rrv_msv), myRDS_l)

print "made datahists, making histpdfs"

myRHP   = RooHistPdf("myRHP",  "myRHP",  RooArgSet(rrv_msv),myRDH  )
myRHP_b = RooHistPdf("myRHP_b","myRHP_b",RooArgSet(rrv_msv),myRDH_b)
myRHP_c = RooHistPdf("myRHP_c","myRHP_c",RooArgSet(rrv_msv),myRDH_c)
myRHP_l = RooHistPdf("myRHP_l","myRHP_l",RooArgSet(rrv_msv),myRDH_l)

print "made histpdfs, going to plot"

Can=TCanvas("Can","Can")
Can.Divide(2,2)

Can.cd(1)
freem1 = rrv_msv.frame(40)
myRDS.plotOn(freem1)
myRHP.plotOn(freem1,RooFit.LineColor(kBlack))
freem1.Draw()

Can.cd(2)
freem2 = rrv_msv.frame(40)
myRDS.plotOn(freem2)
myRHP.plotOn(freem2,RooFit.LineColor(kBlack))
#myRKP_l.plotOn(freem2,RooFit.LineColor(kBlue))
#myRKP_c.plotOn(freem2,RooFit.LineColor(kGreen))
#myRKP_b.plotOn(freem2,RooFit.LineColor(kRed))
freem2.Draw()

Can.cd(3)
freem3 = rrv_msv.frame(40)
myRHP_l.plotOn(freem3,RooFit.LineColor(kBlue))
myRHP_c.plotOn(freem3,RooFit.LineColor(kGreen))
myRHP_b.plotOn(freem3,RooFit.LineColor(kRed))
freem3.Draw()

pTRegion  = RooThresholdCategory("pTRegion", "region of pT", rrv_pT, "pT") 
etaRegion = RooThresholdCategory("etaRegion","region of eta",rrv_eta,"eta") 
#npvRegion = RooThresholdCategory("npvRegion","region of nPV",rrv_nPV,"nPV") 

# Specify thresholds and state assignments one-by-one.
# Each statement specifies that all values _below_ the given value
# (and above any lower specified threshold) are mapped to the
# category state with the given name
#
# Background | SideBand | Signal | SideBand | Background
#     4.23       5.23     8.23       9.23
pTRegion.addThreshold(             38, "1") 
pTRegion.addThreshold(             45, "2") 
pTRegion.addThreshold(             65, "3") 
pTRegion.addThreshold(            150, "4") 
pTRegion.addThreshold(rrv_pT.getMax(), "5") 

etaRegion.addThreshold(            3., "1")

#etaRegion.addThreshold(            -1., "1") 
#etaRegion.addThreshold(             1., "2") 
#etaRegion.addThreshold(rrv_eta.getMax(), "3") 

#npvRegion.addThreshold(             15, "1") 

#npvRegion.addThreshold(             3.5, "1") 
#npvRegion.addThreshold(             4.5, "2") 
#npvRegion.addThreshold(             6.5, "3") 
#npvRegion.addThreshold(             8.5, "4") 
#npvRegion.addThreshold(rrv_nPV.getMax(), "5") 

# Add values of threshold function to dataset so that it can be used as observable
myRDS.addColumn(pTRegion) 
myRDS_b.addColumn(pTRegion) 
myRDS_c.addColumn(pTRegion) 
myRDS_l.addColumn(pTRegion) 
DATA.addColumn(pTRegion) 

myRDS.addColumn(etaRegion) 
myRDS_b.addColumn(etaRegion) 
myRDS_c.addColumn(etaRegion) 
myRDS_l.addColumn(etaRegion) 
DATA.addColumn(etaRegion) 

#myRDS.addColumn(npvRegion) 
#myRDS_b.addColumn(npvRegion) 
#myRDS_c.addColumn(npvRegion) 
#myRDS_l.addColumn(npvRegion) 
#DATA.addColumn(npvRegion) 


RDS_per_pT = {}

RDS_b_per_pT = {}
RDS_c_per_pT = {}
RDS_l_per_pT = {}

RKP_b_per_pT = {}
RKP_c_per_pT = {}
RKP_l_per_pT = {}

#myRDH_b = {}
#myRDH_c = {}
#myRDH_l = {}
#myRHP_b = {}
#myRHP_c = {}
#myRHP_l = {}


b_pdfList = RooArgList()
g_pdfList = RooArgList()
c_pdfList = RooArgList()
l_pdfList = RooArgList()

RDS_sum = myRDS

rrv_pT.setMin(25)
rrv_pT.setMax(150)
rrv_pT.setBins(25)

rrv_eta.setMin(-2.5)
rrv_eta.setMax(2.5)
rrv_eta.setBins(10)

#rrv_nPV.setMin(0)
#rrv_nPV.setMax(20)
#rrv_nPV.setBins(20)

RDH_tot          = RooDataHist("myRDH_tot",   "myRDH_tot",   RooArgSet(rrv_pT,rrv_eta), RDS_sum)
RHP_tot          = RooHistPdf( "myRHP_tot",   "myRHP_tot",   RooArgSet(rrv_pT,rrv_eta), RDH_tot  )

Cee=TCanvas("Cee","Cee",600,1000)
Cee.Divide(2,3)

Cee.cd(1)
FRAME1 = rrv_pT.frame()
DATA.plotOn(FRAME1)
RHP_tot.plotOn(FRAME1,RooFit.LineColor(kGreen))
FRAME1.Draw()

Cee.cd(2).SetLogy()
FRAME2 = rrv_pT.frame()
DATA.plotOn(FRAME2)
RHP_tot.plotOn(FRAME2,RooFit.LineColor(kGreen))
FRAME2.Draw()

Cee.cd(3)
FRAME3 = rrv_eta.frame()
DATA.plotOn(FRAME3)
RHP_tot.plotOn(FRAME3,RooFit.LineColor(kGreen))
FRAME3.Draw()

Cee.cd(4).SetLogy()
FRAME4 = rrv_eta.frame()
DATA.plotOn(FRAME4)
RHP_tot.plotOn(FRAME4,RooFit.LineColor(kGreen))
FRAME4.Draw()

Cee.cd(5)
#FRAME5 = rrv_nPV.frame()
#DATA.plotOn(FRAME5)
#RHP_tot.plotOn(FRAME5,RooFit.LineColor(kGreen))
#FRAME5.Draw()

Cee.cd(6).SetLogy()
#FRAME6 = rrv_nPV.frame()
#DATA.plotOn(FRAME6)
#RHP_tot.plotOn(FRAME6,RooFit.LineColor(kGreen))
#FRAME6.Draw()

print "making the three keys pdfs" 

b_sumPdf=0
c_sumPdf=0
l_sumPdf=0

print "making the three hist pdfs"

myRDS_l = RDS_sum.reduce("mcSelectioneventType==1")
myRDS_c = RDS_sum.reduce("mcSelectioneventType==2")
myRDS_b = RDS_sum.reduce("mcSelectioneventType==3")

if template == "keys":
    b_sumPdf = RooKeysPdf("b_sumPdf","b_sumPdf",rrv_msv,myRDS_b)
    c_sumPdf = RooKeysPdf("c_sumPdf","c_sumPdf",rrv_msv,myRDS_c)
    l_sumPdf = RooKeysPdf("l_sumPdf","l_sumPdf",rrv_msv,myRDS_l)
elif template == "hist":
    b_sumHist = RooDataHist("b_sumHist", "b_sumHist", RooArgSet(rrv_msv), myRDS_b)
    b_sumPdf  = RooHistPdf( "b_sumPdf",  "b_sumPdf",  RooArgSet(rrv_msv), b_sumHist)
    c_sumHist = RooDataHist("c_sumHist", "c_sumHist", RooArgSet(rrv_msv), myRDS_c)
    c_sumPdf  = RooHistPdf( "c_sumPdf",  "c_sumPdf",  RooArgSet(rrv_msv), c_sumHist)
    l_sumHist = RooDataHist("l_sumHist", "l_sumHist", RooArgSet(rrv_msv), myRDS_l)
    l_sumPdf  = RooHistPdf( "l_sumPdf",  "l_sumPdf",  RooArgSet(rrv_msv), l_sumHist)

Nb = RooRealVar("N_{b}","N_{b}",DATA.numEntries()*0.70,0,DATA.numEntries())
Nc = RooRealVar("N_{c}","N_{c}",DATA.numEntries()*0.20,0,DATA.numEntries())
Nl = RooRealVar("N_{l}","N_{l}",DATA.numEntries()*0.10,0,DATA.numEntries())

f_Sum_b = RooRealVar("f_{b}","f_{b}", 0.70, 0.00, 1.  )
f_Sum_c = RooRealVar("f_{c}","f_{c}", 0.20, 0.00, 1.  )

sumPdf = RooAddPdf("sumPdf","sumPdf",
                   RooArgList(b_sumPdf, c_sumPdf, l_sumPdf),
                   RooArgList(Nb,      Nc       ,Nl        ) )
sumPdf2 = RooAddPdf("sumPdf2","sumPdf2",
                    RooArgList(b_sumPdf, c_sumPdf, l_sumPdf),
                    RooArgList(f_Sum_b,  f_Sum_c            ) )

rrv_msv.setRange("r",0,5)
rrv_msv.SetTitle("m(SV) (GeV/c^{2})")

print " fit DATA with JES"

sumPdf.fitTo(DATA,RooFit.Extended(),RooFit.Range("r"))

f_Sum_b.setVal(Nb.getVal()/(Nb.getVal()+Nc.getVal()+Nl.getVal()))
f_Sum_c.setVal(Nc.getVal()/(Nb.getVal()+Nc.getVal()+Nl.getVal()))

sumPdf2.fitTo(DATA,RooFit.Range("r"))

gROOT.SetStyle("Plain")
gStyle.SetErrorX(0)

C1 = TCanvas("C1","C1",1000,450)
C1.Divide(2)

C1.cd(1)
freem = rrv_msv.frame(rrv_msv.getMin(),rrv_msv.getMax()/2.,rrv_msv.getBins()/2)
freem.SetBarWidth(0.)
freem.SetMarkerSize(0.7)
freem.SetLineWidth(1)

DATA.plotOn(freem,
            RooFit.MarkerSize(0.3),
            RooFit.XErrorSize(0.035),
            RooFit.DrawOption("pe2"))
sumPdf.plotOn(freem,RooFit.LineWidth(1),RooFit.LineColor(kBlack))
sumPdf.plotOn(freem,RooFit.Components("b_sumPdf"),RooFit.LineWidth(1),RooFit.LineColor(kRed),  RooFit.LineStyle(kDashed))
sumPdf.plotOn(freem,RooFit.Components("g_sumPdf"),RooFit.LineWidth(1),RooFit.LineColor(kMagenta),RooFit.LineStyle(kDashed))
sumPdf.plotOn(freem,RooFit.Components("c_sumPdf"),RooFit.LineWidth(1),RooFit.LineColor(kGreen),RooFit.LineStyle(kDashed))
sumPdf.plotOn(freem,RooFit.Components("l_sumPdf"),RooFit.LineWidth(1),RooFit.LineColor(kBlue), RooFit.LineStyle(kDashed))
DATA.plotOn(freem,
            RooFit.MarkerSize(0.3),
            RooFit.XErrorSize(0.035),
            RooFit.DrawOption("pe2"))
sumPdf.paramOn(freem,DATA)
freem.Draw()

C1.cd(2)
freem2 = rrv_msv.frame(rrv_msv.getMin(),rrv_msv.getMax()/2.,rrv_msv.getBins()/2)
freem2.SetBarWidth(0.)
freem2.SetMarkerSize(0.7)
freem2.SetLineWidth(1)
               
DATA.plotOn(freem2,
            RooFit.MarkerSize(0.7),
            RooFit.XErrorSize(0.035),
            RooFit.DrawOption("pe2"))
sumPdf2.plotOn(freem2,RooFit.LineWidth(1),RooFit.Components("l_sumPdf,b_sumPdf,c_sumPdf"), RooFit.FillColor(kRed),  RooFit.DrawOption("F"), RooFit.LineColor(kBlack))
sumPdf2.plotOn(freem2,RooFit.LineWidth(1),RooFit.Components("l_sumPdf,b_sumPdf,c_sumPdf"), RooFit.FillColor(kBlue), RooFit.DrawOption("F"), RooFit.LineColor(kBlack))
sumPdf2.plotOn(freem2,RooFit.LineWidth(1),RooFit.Components("l_sumPdf,b_sumPdf,c_sumPdf"), RooFit.FillColor(kBlue), RooFit.LineColor(kBlack))
sumPdf2.plotOn(freem2,RooFit.LineWidth(1),RooFit.Components("c_sumPdf,b_sumPdf"),          RooFit.FillColor(kGreen),RooFit.DrawOption("F"), RooFit.LineColor(kBlack))
sumPdf2.plotOn(freem2,RooFit.LineWidth(1),RooFit.Components("c_sumPdf,b_sumPdf"),          RooFit.FillColor(kGreen),RooFit.LineColor(kBlack))
sumPdf2.plotOn(freem2,RooFit.LineWidth(1),RooFit.Components("b_sumPdf"),                   RooFit.FillColor(kRed),  RooFit.DrawOption("F"), RooFit.LineColor(kBlack))
sumPdf2.plotOn(freem2,RooFit.LineWidth(1),RooFit.Components("b_sumPdf"),                   RooFit.FillColor(kRed),  RooFit.LineColor(kBlack))
DATA.plotOn(freem2,
            RooFit.MarkerSize(0.7),
            RooFit.XErrorSize(0.035),
            RooFit.DrawOption("pe2"))
sumPdf2.paramOn(freem2,DATA)
freem2.Draw()

rrv_msv.SetTitle("Secondary vertex mass")
rrv_msv.setUnit("GeV/c^{2}")
  

FRAME = rrv_msv.frame(rrv_msv.getMin(),rrv_msv.getMax()/2.,rrv_msv.getBins()/2)
FRAME.SetMinimum(-0.000)
DATA.plotOn(FRAME,
            RooFit.MarkerSize(1.3),
            RooFit.XErrorSize(0.035),
            RooFit.DrawOption("pe2"))
#sumPdf2.plotOn(FRAME,RooFit.LineColor(kBlack), RooFit.FillColor(kBlue), RooFit.DrawOption("F"), RooFit.LineWidth(1))
#sumPdf2.plotOn(FRAME,RooFit.LineColor(kBlack), RooFit.FillColor(kBlue), RooFit.LineWidth(1))
sumPdf2.plotOn(FRAME,RooFit.Components("l_sumPdf,b_sumPdf,c_sumPdf"),RooFit.LineColor(kBlack), RooFit.FillColor(kBlue), RooFit.DrawOption("F"), RooFit.LineWidth(1))
sumPdf2.plotOn(FRAME,RooFit.Components("l_sumPdf,b_sumPdf,c_sumPdf"),RooFit.LineColor(kBlack), RooFit.FillColor(kBlue), RooFit.LineWidth(1))
sumPdf2.plotOn(FRAME,RooFit.Components("b_sumPdf,c_sumPdf"),RooFit.LineColor(kBlack), RooFit.FillColor(kGreen), RooFit.DrawOption("F"), RooFit.LineWidth(1))
sumPdf2.plotOn(FRAME,RooFit.Components("b_sumPdf,c_sumPdf"),RooFit.LineColor(kBlack), RooFit.FillColor(kGreen), RooFit.LineWidth(1))
sumPdf2.plotOn(FRAME,RooFit.Components("b_sumPdf"),RooFit.LineColor(kBlack), RooFit.FillColor(kRed), RooFit.DrawOption("F"), RooFit.LineWidth(1))
sumPdf2.plotOn(FRAME,RooFit.Components("b_sumPdf"),RooFit.LineColor(kBlack), RooFit.FillColor(kRed), RooFit.LineWidth(1))
DATA.plotOn(FRAME, RooFit.MarkerSize(1.3), RooFit.XErrorSize(0.035), RooFit.DrawOption("pe2"))
#sum_fb->paramOn(f_frac,myRDS);

#FRAME.SetYTitle("Events / ( 0.333 GeV/c^{2} )");

CANVAS = TCanvas("CANVAS","CANVAS",800,800)
CANVAS.Divide(1)
CANVAS.cd(1)
FRAME.SetBarWidth(0.)
FRAME.SetMarkerSize(1.3)
FRAME.SetLineWidth(1)
   
FRAME.SetMinimum(-0.000)
FRAME.Draw("F")

#leg1 = TLegend(0.50, 0.5625, 0.85, 0.95-0.20, "", "NDC")
#leg1.AddEntry( FRAME.getObject(0), "Data ","PLE")
#leg1.AddEntry( FRAME.getObject(5), "b-jets"  ,"F")
#leg1.AddEntry( FRAME.getObject(3), "c-jets"  ,"F")

leg1 = TLegend(0.50, 0.50, 0.85, 0.95-0.20, "", "NDC")
leg1.AddEntry( FRAME.getObject(0), "Data ", "PLE")
leg1.AddEntry( FRAME.getObject(5), "b-jets"  ,"F")
leg1.AddEntry( FRAME.getObject(3), "c-jets"  ,"F")
leg1.AddEntry( FRAME.getObject(1), "l-jets"  ,"F")

leg1.SetFillColor(0)
leg1.SetShadowColor(0)

leg1.Draw()

lat=TLatex()
#lat.SetTextSize(0.9)
lat.DrawLatex(2.5,0.9*FRAME.GetMaximum(),"#splitline{CMS Preliminary}{#sqrt{s} = 7 TeV, L = 2 fb^{-1}}")

lat2=TLatex()
#lat2.SetTextSize(0.9)
lat2.DrawLatex(2.5,0.45*FRAME.GetMaximum(),"High purity b-tagging")


                          



# TLegend* leg1 = new TLegend(0.50, 0.5625, 0.85, 0.95-0.20, "", "NDC");
# // leg1->AddEntry( f_frac->getObject(0), "data ");
# leg1->AddEntry( f_frac->getObject(0), "Data ","PLE");
# leg1->AddEntry( f_frac->getObject(5), "b-jets"  ,"F");
# leg1->AddEntry( f_frac->getObject(3), "c-jets"  ,"F");

# leg1->SetFillColor(0);
# leg1->SetShadowColor(0);

# leg1->Draw();

# TLatex lat;
# lat.DrawLatex(2.,14.,"#splitline{CMS Preliminary}{#sqrt{s} = 7 TeV, L = 36 pb^{-1}}");

# TLatex lat;
# lat.DrawLatex(2.5,6,"High purity b-tagging");
            

#C1.cd(3)
#freem3 = rrv_pT.frame(0,250)
#DATA.plotOn(freem3,RooLinkedList())
#sumPdf2.plotOn(freem3,RooFit.LineColor(kBlack))
#freem3.Draw()

jecString=""
if jec : jecString+="_"+str(jec)+"sigmaJEC"

pvString=""
if PVreduce : pvString+="_"+"PVregion"+str(PVreduce)

if not numbins == 40: template+="_"+str(numbins)+"bins"

C1.SaveAs("~/public/ZbbPaper/bPurity/bPurFit_DYtemplate_"+channel+"_"+WP+"_"+template+pvString+jecString+"_double.pdf")

CANVAS.SaveAs("~/public/ZbbPaper/bPurity/bPurFit_DYtemplate_"+channel+"_"+WP+"_"+template+pvString+jecString+".pdf")


#make RooDataHist
#make RooHistPdf

###---------------------------------------------------------------------------------------------####

#    for (int ijet = 0; ijet < nJet; ijet++) {
#        float residual = 1.
#        if ( Run > 0 ) residual = Jet_residual[ijet]
#        float ptjet = Jet_pt[ijet] * Jet_jes[ijet] * residual
#         float etajet = fabs(Jet_eta[ijet])
#         if ( !(etajet >= EtaMin && etajet < EtaMax) ) continue#
#
#         ngoodj++; selecjet[ngoodj]=ijet; #
#
## njets = nJet;
## int npv = nPV; 
## if ( npv >= 20 ) npv = 20;
## int npu = nPU; 
##
## if ( pthat > 0. ){
##   if (PU_bunch[nPU] != 0) continue;#
#
#     #### make weight #
#
#    ### Loop on jets
#    for (int isel = 0; isel < ngoodj; isel++) :
#        
#        int ijet = selecjet[isel];
#   if ( ijet == 0 ) {
#     allevents++;
#     if ( allevents%100000 == 0 ) std::cout << "events : " << allevents << std::endl ;
#      hData_All_NJets->Fill( njets , ww1 );
#     hData_NJets->Fill( numjet , ww1 );
##
#
#     numjet = 0;
#     ntagjet = 0;
#   }
#
#   float ptjet = Jet_pt[ijet] * Jet_jes[ijet] * residual;
#   int flavour = abs( Jet_flavour[ijet] );
#   if ( flavour >= 1 && flavour <= 3 ) flavour = 1;#
#
#   if ( !(ptjet >= PtMin && ptjet < PtMax) ) continue;
#   if ( !(etajet >= EtaMin && etajet < EtaMax) ) continue;
#
#   hData_All_JetPV->Fill( npv , 1. );
#   hData_All_JetPt->Fill( ptjet , ww1 );
#   hData_All_JetEta->Fill( fabs(etajet) , 1. );
#   hData_All_JetRun->Fill( Run , 1. );
#   hAllFlav_All_Flavour->Fill( flavour , 1. );
#
#   double mass2vx ;
#
#   #if (Jet_SvxMass[ijet] >6.5) mass2vx =6.499 ;
#   #else if (Jet_SvxMass[ijet] <0.05) mass2vx =-0.99 ;
#   else mass2vx=Jet_SvxMass[ijet];
#   
##// High Purity Secondary Vertex
##   else if ( NN == 5 ) {
##     if ( Jet_SvxHP[ijet] > 1.  )  varpos =  5.*Jet_SvxHP[ijet];
##     if ( Jet_SvxNHP[ijet] < -1. ) varneg = -5.*Jet_SvxNHP[ijet];
##     if ( Jet_SvxHP[ijet] > TagCut )  TagPos = true;
##     if (-Jet_SvxNHP[ijet] > TagCut ) TagNeg = true;
##     cat = Jet_histSvx[ijet];
##   }
#
#   if ( flavour == 1 || 2 || 3 || flavour == 21 ) : LIGHT
#   elif (flavour == 4)                            : C  
#   elif (flavour == 5)                            : B#
#
#   #check if (nBFromGSplit>0) {
#   #    for (int igluon =0; igluon<nBFromGSplit; igluon++){
#   #	 double comp = fabs( bFromGSplit_pT[igluon] - ptjet) ;  comp = comp/bFromGSplit_pT[igluon] ;
#   #	 if ( comp > 1.1 )  continue;
#   #	 if (bFromGSplit_eta[igluon] < 0.8*EtaMin )  continue;
#   #	 if (bFromGSplit_eta[igluon] > 1.2*EtaMax )  continue;
#   #	 double test = deltaR(etajet, phijet , bFromGSplit_eta[igluon],bFromGSplit_phi[igluon]) ;
#   #	 DeltaRGluonSp->Fill(test,ww);
#   #
#   #	 if (test < 0.15){issplit = 1 ; DeltaRGluonMass->Fill(test,mass2vx); break;}#
##
#
#  # todo: also check pos/neg



### some beautiful hardcoded arrays of weights

# float nevt[14] = {0,1650000,6583068,6600000,6589956,6127528,6220160,6432669,3990085,4245695,
#	4053888,2093222,2196200,293139};
# float xsec[14] = {3.675e+10, 8.159e+08, 5.312e+07, 6.359e+06, 7.843e+05, 1.151e+05, 2.426e+04, 1.168e+03, 7.022e+01,
#		  1.555e+01,1.8444,3.321e-01,1.087e-02,3.575e-04};

# float WeightPtHat[14];
# for (Int_t k=0; k<14; k++){
#   WeightPtHat[k] = lumidata*xsec[k]/nevt[k]/1000. ;
#   cout << "WeightPtHat[" << k << "] = " << WeightPtHat[k] << endl;
# }

# float WeightPU[20] = {0.747694 ,0.853661 ,0.882735 ,0.915668 ,0.951334 ,0.987061 ,1.021296 ,1.052876 ,1.081233 ,1.105996 ,1.126985 ,1.144090 ,1.157152 ,1.165910 ,1.169945 ,1.168780 ,1.161875 ,1.148769 ,1.129215 ,0.631684};
# float WeightPt[15] ={ 1., 0.617427, 0.181917, 0.720309, 2.317049, 8.048693, 18.743258, 35.954548, 107.985794, 130.051636, 219.512650, 331.493652, 340.109497, 
#346.113312, 350.579224};

#Long64_t nentries = fChain->GetEntriesFast();

#f = TFile("/scratch/tdupree/bMistagTuples/ForTristan/qcd30a50/JetTree_10_1_Hth.root");
##f.cd("JetTree_10_1_Hth.root.root:/mistag")
##tree = gDirectory.Get("ttree;3")
#mytsjeen = f.Get("mistag/ttree;3")

filename = "/home/fynu/tdupree/public/ZbbPaper/bPurity/bPurFit_DYtemplate_"+channel+"_"+WP+"_"+template+pvString+jecString+".txt"

my_file = open(filename,"w")
print "filename = ", filename
print >> my_file, "##############################################################"
print >> my_file, "WP = ", WP
print >> my_file, "channel = ", channel

print >> my_file, "--------------------> for di-", channel, "sample at selection step ", WP
print >> my_file, "--------------------> "
print >> my_file, "--------------------> P = (", str(f_Sum_b.getVal()*100.)[:4] , " +/- ",  str(f_Sum_b.getError()*100.)[:4] , " ) % "

print "VOILA!!!"

