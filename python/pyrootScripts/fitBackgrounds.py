
#########################################################
#                                                       #
# Script to estimate backgrounds for Z+b-jets analysis. #
#                                                       #
# Functionality:                                        #
# - Estimate ttbar background                           #
# => Using m(ll) and MW/NN output                       #
# - Estimate Z+ucdsg background                         #
# => Using m(SV)                                        #
#                                                       #
#########################################################
#                                                       #
# Working points                                        #
# - SSV-HE                                              #
# - SSV-HP                                              #
#                                                       #
# Fit dimensionalities                                  #
# - 1D                                                  #
# - 1Dx1D (sim)                                         #
# - 2D                                                  #
# - 2Dx1D (sim)                                         #
#                                                       #
# Channels                                              #
# - El                                                  #
# - Mu                                                  #
# - Sum                                                 #
#                                                       #
# PDFs                                                  #
# - Hist                                                #
# - Keys                                                #
#                                                       #
# Fits                                                  #
# - With/without errors                                 #
# - RooFit & Root                                       #
#                                                       #
# - Fractions                                           #
# - Number of events                                    #
#                                                       #
# Also: include shape uncertainty                       #
#                                                       #
#########################################################

from ROOT import *
gROOT.SetStyle("Plain")
  
###############################################

### settings you want to give from outside ###
# to adjust by user:

channel   = "Mu"
dataLabel = "2011"

frac      = false
WP        = "HEHEMETsig"
extraCut  = "&eventSelectionbestzmassMu>76.&eventSelectionbestzmassMu<106.&jetmetbjet1pt>25&jetmetbjet2pt>25&jetmetMETsignificance<10&mlphiggsvszbb<0.5&mlphiggsvszbb>-0.5"
#extraCut  = "&eventSelectionbestzmassEle>76.&eventSelectionbestzmassEle<106.&jetmetbjet1pt>25&jetmetbjet2pt>25"
keys      = False

ttbarVarList  = [ "mwnn_1"]
mistagVarList = [ ]
##if channel=="Mu": ttbarVarList  = [ "mmumu" ]
#if channel=="El": ttbarVarList  = [ "melel" ]

totVarList = mistagVarList+ttbarVarList 

###############################################

# fixed definitions:

ttMCNameList = ["TT","DY","ZZ"]
# maybe different if using QCD:
mistagMCNameList  = ["Zb","Zc","Zl"]
dataNameList      = [dataLabel]
MCNameList        = ttMCNameList+mistagMCNameList
dataAndMCNameList = ttMCNameList+mistagMCNameList+dataNameList

dataAndMCList = {}

category={"HE"         : "rc_eventSelection_5",
          "HP"         : "rc_eventSelection_6",
          "HEMET"      : "rc_eventSelection_7",
          "HPMET"      : "rc_eventSelection_8",
          "HEMETsig"   : "rc_eventSelection_15",
          "HPMETsig"   : "rc_eventSelection_16",
          "HEHE"       : "rc_eventSelection_9",
          "HPHP"       : "rc_eventSelection_11",
          "HEHEMET"    : "rc_eventSelection_12",
          "HPHPMET"    : "rc_eventSelection_14",
          "HEHEMETsig" : "rc_eventSelection_17",
          "HPHPMETsig" : "rc_eventSelection_19",
          }


varNamesList = { "msv1"  : "jetmetbjet1SVmass"          ,
                 "msv2"  : "jetmetbjet2SVmass"          ,
                 #"msv"   : "jetmetbjetSVmass"           ,
                 "melel" : "eventSelectionbestzmassEle" ,
                 "mmumu" : "eventSelectionbestzmassMu"  ,
                 #"mwnn"  : "mlpzbbvstt_multi_EE_tight"   ,
                 "mwnn"  : "mlpZbbvsTTtight"            ,
                 #"mwnn"  : "mlpZbbvsTT_mu"            ,
                 "mwnn_1"  : "mlphiggsvszbb"            ,
                 "mwnn_2"  : "mlphiggsvstt"            ,
                 #"mwnn"  : "mlpzbbttmmll_MeTtest_mll_met",
                 #"mwnn"  : "mlpzbbttmlltest_mll",
                 "w_b_HE"    : "BtaggingReweightingHE"  ,
                 "w_b_HP"    : "BtaggingReweightingHP"  ,
                 "w_b_HEHE"  : "BtaggingReweightingHEHE",
                 "w_b_HEHEMET"  : "BtaggingReweightingHEHE",
                 "w_b_HEHEMETsig"  : "BtaggingReweightingHEHE",
                 "w_b_HPHP"  : "BtaggingReweightingHPHP",
                 "w_b_HPHPMETsig"  : "BtaggingReweightingHPHP",
                 "w_lep"     : "LeptonsReweightingweight",
                 "jmul"      : "jetmetnj",
                 "w_lumi"    : "lumiReweightingLumiWeight",
                }

min = {"msv1"   :   0,
       "msv2"   :   0,
       "msv"    :   0,
       "melel"  :  73,
       "mmumu"  :  76,
       "mwnn"   : 0.0,
       "mwnn_1"   :-0.2,
       "mwnn_2"   : 0.,
       "w_b_HE" : 0. , 
       "w_b_HP"    : 0.,
       "w_b_HEHE"  : 0.,
       "w_b_HEHEMET"  : 0.,
       "w_b_HEHEMETsig"  : 0.,
       "w_b_HPHPMETsig"  : 0.,
       "w_b_HPHP"  : 0.,
       "w_lep"     : 0.,
       "w_lumi"    : 0.,
       "jmul"      :2.
       }

max = {"msv1" :    5,
       "msv2" :    5,
       "msv"  :    5,
       "melel":  107,
       "mmumu":  106,
       "mwnn" :    1,
       "mwnn_1"   : 0.5,
       "mwnn_2"   : 0.5,
       "w_b_HE"    : 2., 
       "w_b_HP"    : 2.,
       "w_b_HEHE"  : 2.,
       "w_b_HEHEMET"  : 2.,
       "w_b_HEHEMETsig"  : 2.,
       "w_b_HPHPMETsig"  : 2.,
       "w_b_HPHP"  : 2.,
       "w_lep"     : 2.,
       "w_lumi"    : 2.,
       "jmul"      : 8. 
       }

bins = {"msv1" :   20,
        "msv2" :   20,
        "msv"  :   20,
        "melel":   34,
        "mmumu":   30,
        "mwnn" :   36,
        "mwnn_1"   : 20,
        "mwnn_2"   : 16,
        "w_b_HE"    : 100, 
        "w_b_HP"    : 100,
        "w_b_HEHE"  : 100,
        "w_b_HEHEMET"  : 100,
        "w_b_HEHEMETsig"  : 100,
        "w_b_HPHPMETsig"  : 100,
        "w_b_HPHP"  : 100,
        "w_lep"     : 100,
        "w_lumi"    : 100,
        "jmul"      : 6, 
        }

color = {"msv1" : kRed,
         "msv2" : kRed,
         "msv"  : kRed,
         "melel": kYellow,
         "mmumu": kYellow,
         "mwnn_1" :kYellow,
         }

C={}

#path = "~acaudron/scratch/Pat444/CMSSW_4_4_4/src/UserCode/zbb_louvain/python/condorRDSmakerNoWS/outputs/"
path = "/home/fynu/arnaudp/scratch/Zbb_2012/CMSSW_4_4_4/src/UserCode/zbb_louvain/python/testsMergeRDSnoWS120721/"

fileNameList = {}


fileNameList = { "2011A"   : path+"RDS_rdsME_"+channel+"A_DATA.root",
                 "2011B"   : path+"RDS_rdsME_"+channel+"B_DATA.root",
                 "DY"      : path+"RDS_rdsME_"+channel+"_MC.root",
                 "TT"      : path+"RDS_rdsME_TT_"+channel+"_MC.root",
                 "Zb"      : path+"RDS_rdsME_"+channel+"_MC.root",
                 "Zc"      : path+"RDS_rdsME_"+channel+"_MC.root",
                 "Zl"      : path+"RDS_rdsME_"+channel+"_MC.root",
                 "ZZ"      : path+"RDS_rdsME_ZZ_"+channel+"_MC.root",
                 }



#fileNameList = { "2011A"    : path+"File_rds_zbb_"+channel+"A_DATA.root",
#                 "2011B"    : path+"File_rds_zbb_"+channel+"B_DATA.root",
#                 "DY"       : path+"File_rds_zbb_"+channel+"_MC.root",
#                 "TT"       : path+"File_rds_zbb_TT_"+channel+"_MC.root",
#                 "Zb"       : path+"File_rds_zbb_"+channel+"_MC.root",
#                 "Zc"       : path+"File_rds_zbb_"+channel+"_MC.root",
#                 "Zl"       : path+"File_rds_zbb_"+channel+"_MC.root"
#                 }


##############################################

def getVariables(varNamesList,varName,dataAndMCList) :
    var=varNamesList[varName]
    y=dataAndMCList["Zl"]
    print "var = ", var
    print "ras = ", y.get()
    print "var = ", y.get()[var]
    x = y.get()[var]
    if x :
        x.setMin(min[varName])
        x.setMax(max[varName])
        x.setBins(bins[varName])
        return x
    else: return 0
    

def getDataAndMC(dataAndMCNameList,dataAndMCList) :

    # check ws
    # otherwise: directly rds

    file = {}
    ws   = {}
    myRDS = {}


    for name in dataAndMCNameList :
        print "name = ", name
        if name=="2011":
            print "making 2011 dataset"
            file["2011A"]  = TFile.Open(fileNameList["2011A"])
            myRDS["2011A"] = file["2011A"].Get("rds_zbb")
            print "A.numEntries() = ", myRDS["2011A"].numEntries()
            file["2011B"]  = TFile.Open(fileNameList["2011B"])
            myRDS["2011B"] = file["2011B"].Get("rds_zbb")
            print "B.numEntries() = ", myRDS["2011B"].numEntries()
            myRDS["2011"]=myRDS["2011A"]
            print "2011.numEntries() = ", myRDS["2011"].numEntries()
            myRDS["2011"].append(myRDS["2011B"])
            print "2011.numEntries() = ", myRDS["2011"].numEntries()
        else :
            print "fileNameList[name] = ", fileNameList[name]
            file[name]  = TFile.Open(fileNameList[name])
            ws[name]    = file[name].Get("ws")
            if ws[name]:
                print "getting RDS from RooWorkspace"
                myRDS[name] = ws[name].data("rds_zbb")
            else :   
                print "No ws, getting RDS directly"
                myRDS[name] = file[name].Get("rds_zbb")
        print "*** Going to reduce RDS ", name        
        myRDS[name] = myRDS[name].reduce(category[WP]+"==1"+extraCut)
        if channel=="El": myRDS[name] = myRDS[name].reduce("eventSelectionbestzmassEle<106&eventSelectionbestzmassEle>76")
        if channel=="Mu": myRDS[name] = myRDS[name].reduce("eventSelectionbestzmassMu<106&eventSelectionbestzmassMu>76")
        print "#entries for sample", name , " at WP ",  WP ," =", myRDS[name].numEntries() 
        dataAndMCList[name]=myRDS[name]

    return 

def setWeights(dataAndMCList,MCNameList,w) :
    for name in MCNameList :
        print "***BEFORE numEntries() = ", dataAndMCList[name].numEntries()
        dataAndMCList[name].addColumn(w)
    for name in MCNameList :
        dataAndMCList[name] = RooDataSet(dataAndMCList[name].GetName(),
                                         dataAndMCList[name].GetName(),
                                         dataAndMCList[name],
                                         dataAndMCList[name].get(),
                                         "",
                                         w.GetName())
        print "***AFTER numEntries() for sample ", name , " = ", dataAndMCList[name].numEntries()
        print "sumEntries() = ", dataAndMCList[name].sumEntries()

    return
        


def makePdfList(dataAndMCList, mcName, var, RDH, RHP ) :
    varName=var.GetName()
    name=mcName+varName

    print "mcName    = ", mcName
    print "varName   = ", varName
    print "name      = ", name

    print "**** before cut: number of entries = " , dataAndMCList[mcName].numEntries()

    if varName=="jetmetbjet1SVmass":
        if mcName=="Zl":
            print "Zl dataset, going to cut on udsgc flav"
            dataAndMCList[name] = dataAndMCList[mcName].reduce("jetmetbjet1Flavor==1||jetmetbjet1Flavor==-1||jetmetbjet1Flavor==2||jetmetbjet1Flavor==-2||jetmetbjet1Flavor==3||jetmetbjet1Flavor==-3||jetmetbjet1Flavor==21")
        if mcName=="Zc":
            print "Zc dataset, going to cut on c flav"
            dataAndMCList[name]=dataAndMCList[mcName].reduce("jetmetbjet1Flavor==4||jetmetbjet1Flavor==-4")
        if mcName=="Zb":
            print "Zb dataset, going to cut on b flav"
            dataAndMCList[name]=dataAndMCList[mcName].reduce("jetmetbjet1Flavor==5||jetmetbjet1Flavor==-5")
    elif varName=="jetmetbjet2SVmass":
        if mcName=="Zl":
            print "Zl dataset, going to cut on udsgc flav"
            dataAndMCList[name] = dataAndMCList[mcName].reduce("jetmetbjet2Flavor==1||jetmetbjet2Flavor==-1||jetmetbjet2Flavor==2||jetmetbjet2Flavor==-2||jetmetbjet2Flavor==3||jetmetbjet2Flavor==-3||jetmetbjet2Flavor==21")
        if mcName=="Zc":
            print "Zc dataset, going to cut on c flav"
            dataAndMCList[name]=dataAndMCList[mcName].reduce("jetmetbjet2Flavor==4||jetmetbjet2Flavor==-4")
        if mcName=="Zb":
            print "Zb dataset, going to cut on b flav"
            dataAndMCList[name]=dataAndMCList[mcName].reduce("jetmetbjet2Flavor==5||jetmetbjet2Flavor==-5")
    else:
        dataAndMCList[name]=dataAndMCList[mcName]
        print "DID NOT MATCH SAMPLE NAME"

    print "**** after cut: number of entries = " , dataAndMCList[mcName].numEntries()
    print "**** after cut: number of entries = " , dataAndMCList[name].numEntries()
        
    # todo: something goes wrong here with the cut on the dataset. Somethow it is not given to the RooDataHist correctly
    
    if keys:
        RKP[name] = RooKeysPdf( "RKP_tt_"+name,"myRKP_tt_"+name, var, dataAndMCs  )
    else :    
        RDH[name] = RooDataHist("RDH_"+name,"RDH_"+name, RooArgSet(var), dataAndMCList[name]   )
        RHP[name] = RooHistPdf( "RHP_"+name,"RHP_"+name, RooArgSet(var), RDH[name] )
    # else:    
    # parameterized?
    return

#############################################################################################################

# def makeMsvPDF :

#def makeSimMistagPdf(msvPdfs) :
    # use b/c/l fraction simultaneously

#def makeSimTotPdf(ttPdfList+msvPdfList) :
    # use ttbar fraction simultaneuously
    
#def performFit :

#def plot:
    # loop over MC components
    
##############################################
    
def main():

    vars          = {}

    getDataAndMC(dataAndMCNameList, dataAndMCList)

    for varName in varNamesList      : vars[varName] = getVariables(varNamesList,varName,dataAndMCList)

    weight = RooFormulaVar("w","w", "@0*@1*@2", RooArgList(vars["w_lep"],vars["w_lumi"],vars["w_b_"+WP]))
    setWeights(dataAndMCList,MCNameList,weight)

    ttPdfList       = RooArgList()
    ttFracList      = RooArgList()
    ttYieldList     = RooArgList()

    mistagPdfList   = RooArgList()
    mistagFracList  = RooArgList()
    mistagYieldList = RooArgList()

    RDH_tt={}
    RHP_tt={}
    RDH_mistag={}
    RHP_mistag={}

    Ntt=[]
    Nmistag=[]
    ftt=[] 
    fmistag=[] 
    

    if len(ttbarVarList):
        for ttVarName in ttbarVarList:
            for ttMCName in ttMCNameList :
                pdfName = ttMCName+vars[ttVarName].GetName() 
                makePdfList(dataAndMCList, ttMCName, vars[ttVarName], RDH_tt, RHP_tt )
                ttPdfList.add(RHP_tt[pdfName])
                if ttMCName=="TT":Ntt.append(RooRealVar("N_"+ttMCName,"N_"+ttMCName,0,75))#dataAndMCList[ttMCName].numEntries()))
                elif ttMCName=="ZZ": Ntt.append(RooRealVar("N_"+ttMCName,"N_"+ttMCName,0,8))#dataAndMCList[ttMCName].numEntries()))
                else : Ntt.append(RooRealVar("N_"+ttMCName,"N_"+ttMCName,0,dataAndMCList[ttMCName].numEntries()))
                ftt.append(RooRealVar("f_"+ttMCName,"f_{"+ttMCName+"}",0,1.))
        for Ntts in Ntt: ttYieldList.add(Ntts)
        ftt = ftt[:len(ftt)-1]
        for ftts in ftt: ttFracList.add(ftts)

    if len(mistagVarList):        
        for mistagVarName in mistagVarList :
            for mistagMCName in mistagMCNameList :
                pdfName = mistagMCName+vars[mistagVarName].GetName() 
                makePdfList(dataAndMCList, mistagMCName, vars[mistagVarName], RDH_mistag, RHP_mistag )
                mistagPdfList.add(RHP_mistag[pdfName])

                Nmistag.append(RooRealVar("N_"+mistagMCName,"N_"+mistagMCName,0,dataAndMCList[mistagMCName].numEntries()))
                fmistag.append(RooRealVar("f_"+mistagMCName,"f_{"+mistagMCName+"}",0,1.))

        for Nmistags in Nmistag: mistagYieldList.add(Nmistags)
        fmistag = fmistag[:len(fmistag)-1]
        for fmistags in fmistag: mistagFracList.add(fmistags)
                

    if len(mistagVarList):
        if frac : mistagPdf = RooAddPdf("mistagPdf","mistagPdf",mistagPdfList,mistagFracList)
        else    : mistagPdf = RooAddPdf("mistagPdf","mistagPdf",mistagPdfList,mistagYieldList)
        mistagPdf.fitTo(dataAndMCList[dataLabel])
        ## for vars in list
        frame = vars[mistagVarName].frame()
        dataAndMCList[dataLabel].plotOn(frame)
        mistagPdf.plotOn(frame)
        for mistagVarName in mistagVarList:
            mistagPdf.plotOn(frame,
                             RooFit.Components("RHP_Zb"+vars[mistagVarName].GetName()+",RHP_Zc"+vars[mistagVarName].GetName()+",RHP_Zl"+vars[mistagVarName].GetName()),
                             RooFit.DrawOption("F"),
                             RooFit.LineColor(kBlack),
                             RooFit.FillColor(kBlue-7),
                             RooFit.LineWidth(1)
                             )
            mistagPdf.plotOn(frame,
                             RooFit.Components("RHP_Zb"+vars[mistagVarName].GetName()+",RHP_Zc"+vars[mistagVarName].GetName()+",RHP_Zl"+vars[mistagVarName].GetName()),
                             RooFit.LineColor(kBlack),
                             RooFit.FillColor(kBlue-7),
                             RooFit.LineWidth(1))
            mistagPdf.plotOn(frame,
                             RooFit.Components("RHP_Zc"+vars[mistagVarName].GetName()+",RHP_Zb"+vars[mistagVarName].GetName()),
                             RooFit.DrawOption("F"),
                             RooFit.LineColor(kBlack),
                             RooFit.FillColor(kGreen-7),
                             RooFit.LineWidth(1))
            mistagPdf.plotOn(frame,
                             RooFit.Components("RHP_Zc"+vars[mistagVarName].GetName()+",RHP_Zb"+vars[mistagVarName].GetName()),
                             RooFit.LineColor(kBlack),
                             RooFit.FillColor(kGreen-7),
                             RooFit.LineWidth(1))
            mistagPdf.plotOn(frame,
                             RooFit.Components("RHP_Zb"+vars[mistagVarName].GetName()),
                             RooFit.DrawOption("F"),
                             RooFit.LineColor(kBlack),
                             RooFit.FillColor(kRed-7),
                             RooFit.LineWidth(1))
            mistagPdf.plotOn(frame,
                             RooFit.Components("RHP_Zb"+vars[mistagVarName].GetName()),
                             RooFit.LineColor(kBlack),
                             RooFit.FillColor(kRed-7),
                             RooFit.LineWidth(1))
        dataAndMCList[dataLabel].plotOn(frame)
        mistagPdf.paramOn(frame,dataAndMCList[dataLabel])
        C["mistag"]=TCanvas("mistag","mistag")
        frame.Draw()
        mystring  = channel+"_"+dataLabel+"_"+WP
        mystring2 ="purity"+"_"+vars[mistagVarName].GetName()+"_"
        print "mystring = ", mystring
        lat=TLatex()
        lat.SetTextSize(0.04)
        lat.DrawLatex(2.8,0.8*frame.GetMaximum(),mystring)

            
        C["mistag"].SaveAs("~/backgroundPlots/"+mystring2+mystring+".pdf")

    if len(ttbarVarList):
        if frac : ttPdf = RooAddPdf("ttPdf","ttPdf",ttPdfList,ttFracList)
        else    : ttPdf = RooAddPdf("ttPdf","ttPdf",ttPdfList,ttYieldList)
        
        ttPdf.fitTo(dataAndMCList[dataLabel])
    
        frame = vars[ttVarName].frame()
        dataAndMCList[dataLabel].plotOn(frame)
        ttPdf.plotOn(frame)
        for ttVarName in ttbarVarList:
            ttPdf.plotOn(frame,
                         RooFit.Components("RHP_DY"+vars[ttVarName].GetName()+",RHP_TT"+vars[ttVarName].GetName()),
                         RooFit.DrawOption("F"),
                         RooFit.LineColor(kBlack),
                         RooFit.FillColor(kBlue-7),
                         RooFit.LineWidth(1)
                         )
            ttPdf.plotOn(frame,
                         RooFit.Components("RHP_DY"+vars[ttVarName].GetName()+",RHP_TT"+vars[ttVarName].GetName()),
                         RooFit.LineColor(kBlack),
                         RooFit.FillColor(kBlue-7),
                         RooFit.LineWidth(1))
            ttPdf.plotOn(frame,
                         RooFit.Components("RHP_TT"+vars[ttVarName].GetName()),
                         RooFit.DrawOption("F"),
                         RooFit.LineColor(kBlack),
                         RooFit.FillColor(kYellow-7),
                         RooFit.LineWidth(1)
                         )
            ttPdf.plotOn(frame,
                         RooFit.Components("RHP_TT"+vars[ttVarName].GetName()),
                         RooFit.LineColor(kBlack),
                         RooFit.FillColor(kYellow-7),
                         RooFit.LineWidth(1))
        dataAndMCList[dataLabel].plotOn(frame)
        ttPdf.paramOn(frame,dataAndMCList[dataLabel])

        C["tt"]=TCanvas("tt","tt")
        frame.Draw()
        mystring  = channel+"_"+dataLabel+"_"+WP
        mystring2 ="ttbar"+"_"+vars[mistagVarName].GetName()+"_"
        print "mystring = ", mystring
        lat=TLatex()
        lat.SetTextSize(0.04)
        lat.DrawLatex(95,0.8*frame.GetMaximum(),mystring)
        C["tt"].SaveAs("~/backgroundPlots/"+mystring2+mystring+".pdf")

    #totPdfList = msvPdfList+ttPdfList    

    #if len(mistagVarList) >1 : msvPdf = makeSimMistagPdf(msvPdfs)
    #else                     : msvPdf = msvPdf.at(0)
    #if len(totVarList) >1    : totPdf = makeSimTotPdf(ttPdfList+msvPdfList)
    #else                     : totPdf = msvPdf.at(0)
        

    #totPdf.fitTo(dataAndMc["DATA"])

    #plot(data,pdfs,componentList)
