#include "cp3-llbb/ExTreeMaker/interface/btagPerfBase.h"

class TH1F;
class TF1;

class btagPerfPOGFormulas : public btagPerfBase {
  public:
    btagPerfPOGFormulas();
    virtual ~btagPerfPOGFormulas();
  protected:
    virtual btagPerfBase::value getbEffScaleFactor(int flavor, int algo, double pt, double eta) const;
    virtual btagPerfBase::value getbEfficiency(int flavor, int algo, double pt, double eta) const;
  private:
    TF1* eff_;
    static float SFb_error_CSVL[16];
    static float SFb_error_CSVM[16];
    static float SFb_error_CSVT[16];
};

