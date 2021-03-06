#######################################################
###                                                 ###
### Hgg.py                                          ###  
###                                                 ###
### RooFit/RooStats example of a toy H->gg search   ###
### - construction of exp+gauss pdf                 ###
### - fit                                           ###
### - profile likelihood for search                 ###
###                                                 ###
### To be run as                                    ###
### >python -i Hgg.py                               ###
###                                                 ###
### Questions/comments: tristan.dupree@uclouvain.be ###
###                                                 ###
#######################################################

from ROOT import *
gROOT.SetStyle("Plain")

N=501
  
##################
### observable ###
##################

m_gg = RooRealVar("m_gg","m_gg",125-60,125+60,"GeV/c^{2}")

#################################
### expected number of events ###
#################################

f = RooRealVar("f","fraction",0.04,0,0.1)

B = RooRealVar("B","N(B)",(1-f.getVal())*N,0,1.1*N)
S = RooRealVar("S","N(S)",f.getVal()*N,0,2.*f.getVal()*N)


####################
### signal model ###
####################

m_H = RooRealVar("m_H","mean", 125)
s_H = RooRealVar("s_H","sigma",  2)

sig = RooGaussian("sig","signal",m_gg,m_H,s_H)



########################
### background model ###
########################

Gamma_bkg = RooRealVar("Gamma_bkg","Gamma_bkg",-0.03,-0.1,-0.01)

bkg = RooExponential("bkg","bkg",m_gg,Gamma_bkg)

###################
### total model ###
###################

sum = RooAddPdf("sum","sum",RooArgList(sig,bkg),RooArgList(f))

#####################
### total model 2 ###
#####################

sum_ext = RooAddPdf("sum_ext","sum_ext",RooArgList(sig,bkg),RooArgList(S,B))

#######################
### generate toy mc ###
#######################

data = sum.generate(RooArgSet(m_gg),N)

###########
### fit ###
###########

sum.fitTo(data)

############
### draw ###
############

C=TCanvas("C","C",1200,800)
C.Divide(3,2)

C.cd(1)
f1 = m_gg.frame()
sig.plotOn(f1,RooFit.LineColor(kGreen))
f1.Draw()

C.cd(2)
f2 = m_gg.frame()
bkg.plotOn(f2,RooFit.LineColor(kRed))
f2.Draw()

C.cd(3)
f3 = m_gg.frame(50)
data.plotOn(f3)
sum.plotOn(f3)
sum.plotOn(f3,RooFit.Components("sig"),RooFit.LineColor(kGreen),RooFit.LineStyle(kDashed))
sum.plotOn(f3,RooFit.Components("bkg"),RooFit.LineColor(kRed),  RooFit.LineStyle(kDotted))
sum.plotOn(f3)
data.plotOn(f3)
sum.paramOn(f3,data)
f3.Draw()

##########################
### PROFILE LIKELIHOOD ###
##########################

Gamma_bkg.setConstant(kTRUE)
#m_H.setConstant(kTRUE)
#s_H.setConstant(kTRUE)

sum_ext.fitTo(data,RooFit.Extended())

### see also http://root.cern.ch/root/html/tutorials/roostats/StandardProfileLikelihoodDemo.C.html

# can also do 2D
# 1D (number of signal events) should be sufficient

plc_S = RooStats.ProfileLikelihoodCalculator(data,sum_ext,RooArgSet(S))
plot_S = RooStats.LikelihoodIntervalPlot(plc_S.GetInterval())

plot_S.SetMaximum(10)

print "plotting likelihood of S alone"

#C_profLik=TCanvas("C_profLik","C_profLik",400,350)
C.cd(4)
plot_S.Draw()

###########
### CLs ###
###########

ntoys=501

myHybridCalc = {}
myHybridResult={}
myHybridPlot={}
sum_bb = {}
clsb_data={}
clb_data={}
cls_data={}
cls_error={}
data_significance={}
min2lnQ_data={}
mean_sb_toys_test_stat={}
toys_significance={}
sig_bb = {}

sig={}
sig_ext={}
sum_ext={}
S={}

mH_hypoList = [105,110,115,120,125,130,135,140,145]

CLsSampleList = ["data","mc"]

m_H={}

for mH_hypo in mH_hypoList:
   print "hypo = ", mH_hypo
   m_H[mH_hypo]=RooRealVar("m"+str(mH_hypo),"m"+str(mH_hypo),mH_hypo)
   S[mH_hypo] = RooRealVar("S"+str(mH_hypo),"N(S)"+str(mH_hypo),f.getVal()*N,0,2.*f.getVal()*N)
   sig[mH_hypo] = RooGaussian("sig","signal",m_gg,m_H[mH_hypo],s_H)
   sig_ext[mH_hypo] = RooExtendPdf("sig_ext"+str(mH_hypo),
                                   "sig_ext"+str(mH_hypo),
                                   sig[mH_hypo],
                                   S[mH_hypo])
   sum_ext[mH_hypo] = RooAddPdf("sum_ext"+str(mH_hypo),"sum_ext"+str(mH_hypo),
                                RooArgList(sig[mH_hypo],bkg),RooArgList(S[mH_hypo],B))

bkg_ext = RooExtendPdf("bkg_ext",
                       "bkg_ext",
                       bkg,
                       B)

testsample={}
testsample["data"] = data
testsample["mc"]   = bkg_ext.generate(RooArgSet(m_gg),RooFit.Extended())

#C_hybrid = TCanvas("C_hybrid","C_hybrid")
C.cd(5)

for sample in CLsSampleList:
   for mH_hypo in mH_hypoList:

      print "mH-hypothese = ", mH_hypo
      sum_ext[mH_hypo].fitTo(testsample[sample],RooFit.Extended())
      ### run HybridCalculator on those inputs
      exp_yield     = RooRealVar("exp_yield",    "exp_yield",    N)
      exp_yield_unc = RooRealVar("exp_yield_unc","exp_yield_unc",N/5)
      bkg_yield_prior = RooGaussian("bkg_yield_prior",
                                    "bkg_yield_prior",
                                    B,
                                    exp_yield,
                                    exp_yield_unc)
      nuisance_parameters = RooArgSet(B)
      ### use interface from HypoTest calculator by default
      myHybridCalc[mH_hypo,sample] = RooStats.HybridCalculatorOriginal(testsample[sample], sum_ext[mH_hypo], bkg_ext,
                                                                           nuisance_parameters, bkg_yield_prior)
      ## here I use the default test statistics: 2*lnQ (optional)
      myHybridCalc[mH_hypo,sample].SetTestStatistic(1);
      ###//myHybridCalc.SetTestStatistic(3); // profile likelihood ratio
      myHybridCalc[mH_hypo,sample].SetNumberOfToys(ntoys)
      ##
      myHybridCalc[mH_hypo,sample].UseNuisance(false)
      ### for speed up generation (do binned data)
      myHybridCalc[mH_hypo,sample].SetGenerateBinned(false);
      ### calculate by running ntoys for the S+B and B hypothesis and retrieve the result
      print "myHybridCalc[mH_hypo,sample] = ", myHybridCalc[mH_hypo,sample]
      print "going to get hypo test"
      myHybridResult[mH_hypo,sample] = myHybridCalc[mH_hypo,sample].GetHypoTest()
      print "got hypo test"
      if not myHybridResult[mH_hypo,sample] : print "***Error returned from Hypothesis test"
      ### run 1000 toys without gaussian prior on the background yield
      ### HybridResult* myHybridResult = myHybridCalc.Calculate(*data,1000,false);
      ## nice plot of the results
      myHybridPlot[mH_hypo,sample] = myHybridResult[mH_hypo,sample].GetPlot("myHybridPlot","Plot of results with HybridCalculatorOriginal",200)
      print "done with getting results for mH_hypo=", mH_hypo
      myHybridPlot[mH_hypo,sample].Draw()

### recover and display the results
for mH_hypo in mH_hypoList:
   for sample in CLsSampleList:
      clsb_data[mH_hypo,sample] = myHybridResult[mH_hypo,sample].CLsplusb()
      clb_data[mH_hypo,sample] = myHybridResult[mH_hypo,sample].CLb()
      cls_data[mH_hypo,sample] = myHybridResult[mH_hypo,sample].CLs()
      cls_error[mH_hypo,sample] = myHybridResult[mH_hypo,sample].CLsError()
      
      data_significance[mH_hypo,sample] = myHybridResult[mH_hypo,sample].Significance()
      min2lnQ_data[mH_hypo,sample] = myHybridResult[mH_hypo,sample].GetTestStat_data()
      
    ### compute the mean expected significance from toys
      mean_sb_toys_test_stat[mH_hypo,sample] = myHybridPlot[mH_hypo,sample].GetSBmean()
      myHybridResult[mH_hypo,sample].SetDataTestStatistics(mean_sb_toys_test_stat[mH_hypo,sample])
      toys_significance[mH_hypo,sample] = myHybridResult[mH_hypo,sample].Significance()
      
      print "==> m(Higgs) = ", mH_hypo ," <==="
      print " - -2lnQ = " , min2lnQ_data[mH_hypo,sample]
      print " - CL_sb = " , clsb_data[mH_hypo,sample]
      print " - CL_b  = " , clb_data[mH_hypo,sample]
      print " - CL_s  = " , cls_data[mH_hypo,sample]
      print " - CL_s 'error' = " , cls_error[mH_hypo,sample]
      print " - significance of data  = " , data_significance[mH_hypo,sample]
      print " - mean significance of toys  = " , toys_significance[mH_hypo,sample]
      
###########################
### BRAZILIAN BAND PLOT ###
###########################

myTH1_cls       = {}
myTH1_cls_plus  = {}
myTH1_cls_2plus = {}
myTH1_cls_min   = {}
myTH1_cls_2min  = {}

for sample in CLsSampleList:
   myTH1_cls[sample]       = TH1F(""+sample,   "",len(mH_hypoList),min(mH_hypoList),max(mH_hypoList))
   myTH1_cls_plus[sample]  = TH1F("xxx"+sample,"",len(mH_hypoList),min(mH_hypoList),max(mH_hypoList))
   myTH1_cls_2plus[sample] = TH1F("22x"+sample,"",len(mH_hypoList),min(mH_hypoList),max(mH_hypoList))
   myTH1_cls_min[sample]   = TH1F("yyy"+sample,"",len(mH_hypoList),min(mH_hypoList),max(mH_hypoList))
   myTH1_cls_2min[sample]  = TH1F("22y"+sample,"",len(mH_hypoList),min(mH_hypoList),max(mH_hypoList))
   #myTH1_cls_2plus[sample].GetXaxis().SetRange(min(mH_hypoList),max(mH_hypoList))
   #myTH1_cls_plus[sample].GetXaxis().SetRange(min(mH_hypoList),max(mH_hypoList))
   #myTH1_cls[sample].GetXaxis().SetRange(min(mH_hypoList),max(mH_hypoList))
   #myTH1_cls_min[sample].GetXaxis().SetRange(min(mH_hypoList),max(mH_hypoList))
   #myTH1_cls_2min[sample].GetXaxis().SetRange(min(mH_hypoList),max(mH_hypoList))

for sample in CLsSampleList:
   for x in range(1,len(mH_hypoList)+1):
      myTH1_cls[sample].SetBinContent(     x, 1-cls_data[mH_hypoList[x-1],sample])
      myTH1_cls_plus[sample].SetBinContent(x, 1-(cls_data[mH_hypoList[x-1],sample]-cls_error[mH_hypoList[x-1],sample]))
      myTH1_cls_min[sample].SetBinContent( x, 1-(cls_data[mH_hypoList[x-1],sample]+cls_error[mH_hypoList[x-1],sample]))
      myTH1_cls_2plus[sample].SetBinContent(x, 1-(cls_data[mH_hypoList[x-1],sample]-2*cls_error[mH_hypoList[x-1],sample]))
      myTH1_cls_2min[sample].SetBinContent( x, 1-(cls_data[mH_hypoList[x-1],sample]+2*cls_error[mH_hypoList[x-1],sample]))

g_cls={}
g_cls_min={}
g_cls_plus={}
for sample in CLsSampleList:
   g_cls[sample]      = TGraph(myTH1_cls[sample])
   g_cls_plus[sample] = TGraph(myTH1_cls_plus[sample])
   g_cls_min[sample]  = TGraph(myTH1_cls_min[sample])

   g_cls[sample].GetYaxis().SetTitle("1-CL_{S}")
   g_cls[sample].GetXaxis().SetTitle("m_{H} (GeV/c^{2})")
   g_cls[sample].SetMaximum(1.)
   g_cls[sample].SetMinimum(0.00001)

   g_cls[sample].GetXaxis().SetRange(min(mH_hypoList),max(mH_hypoList))

#Ccls = TCanvas("Ccls","Ccls",500,400)
#Ccls.Divide(1)

#Ccls.cd(1).SetLogy()

C.cd(6)

g_cls["mc"].Draw("AC")
myTH1_cls_2plus["mc"].Draw("AC,same")
myTH1_cls_plus["mc"].Draw("AC,same")
myTH1_cls["mc"].Draw("AC,same")
myTH1_cls_min["mc"].Draw("AC,same")
myTH1_cls_2min["mc"].Draw("AC,same")

myTH1_cls_2plus["mc"].SetFillColor(kGreen)
myTH1_cls_plus["mc"].SetFillColor(kYellow)
myTH1_cls_min["mc"].SetFillColor(kGreen)
myTH1_cls_2min["mc"].SetFillColor(1001)

myTH1_cls["data"].SetLineWidth(3)
myTH1_cls["data"].Draw("AC*,same")

##################
### THE END :( ###
##################

### more statistical methods? see http://root.cern.ch/root/html/tutorials/roostats/index.html

###########
### FIN ###
###########
