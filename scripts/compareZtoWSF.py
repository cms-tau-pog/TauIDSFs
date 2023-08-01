import ROOT
import numpy as np

pt_vals = [145, 250]
#pt_vals = [145]

#vs_jet_wps = ['Loose','Medium','Tight','VTight']
#vs_ele_wps = ['VVLoose','Tight']

vs_jet_wps = ['Medium']
vs_ele_wps = ['VVLoose','Tight']

syst_key = {
  'syst_up' : 'syst_alleras_up_fit',
  'syst_down' : 'syst_alleras_down_fit',
  'syst_byera_up' : 'syst_alldms_$ERA_up_fit',
  'syst_byera_down' : 'syst_alldms_$ERA_down_fit',
  #'syst_byera_bydm_up' : 'syst_dm$DM_$ERA_up_fit',
  #'syst_byera_bydm_down' : 'syst_dm$DM_$ERA_down_fit',
  'syst_TES_up': 'TESUp_fit', 
  'syst_TES_down': 'TESDown_fit', 
  'stat_uncert0_up': 'fit_uncert0_up',
  'stat_uncert0_down': 'fit_uncert0_down',
  'stat_uncert1_up': 'fit_uncert1_up',
  'stat_uncert1_down': 'fit_uncert1_down',
}

def GetDMAveragedSF(f1,f2,pt,era):
  # f1 = graph containing average DM's
  # f2 = graph containing fitted functions
  dms=[0,1,10,11]
  dm_weights=[]
  values=[]
  errors=[]
  for dm in dms:
    dm_weights.append(f1.Get('DMFrac_DM%(dm)s_%(era)s' % vars()).Eval(pt))
    nom=f2.Get('DM%(dm)s_%(era)s_fit' % vars()).Eval(pt)
    values.append(nom) 
    err_up=0.
    err_down=0.
    for syst in syst_key:
      syst_func = syst_key[syst].replace('$ERA',era).replace('$DM',str(dm))
      e=f2.Get('DM%(dm)s_%(era)s_%(syst_func)s' % vars()).Eval(pt)-nom
      if e>0: err_up+=e**2
      else: err_down+=e**2
    err_up=err_up**.5
    err_down=err_down**.5
    err=(err_up+err_down)/2
    errors.append(err) 

  dm_weights = [x / sum(dm_weights) for x in dm_weights] # make sure weights sum to 1
  values = [max(v,0.) for v in values]

  dm_weights = np.array(dm_weights)
  values = np.array(values)
  errors = np.array(errors)
 
  weighted_values = dm_weights*values
  weighted_errors = dm_weights*errors
  #print dm_weights, values, weighted_values
  ave_val= sum(weighted_values)
  ave_err= sum(weighted_errors)
  return ave_val, ave_err

N_2sig=0
N_1sig=0
N_tot=0

for wp in vs_jet_wps:
  for wp_VSe in vs_ele_wps:
    print '\n-----------------------------------'
    print 'VSjet = %(wp)s, VSe = %(wp_VSe)s' % vars()   
    print '-----------------------------------'

    f1 = ROOT.TFile('data/TauID_Highpt_DMFracts_DeepTau2018v2p5VSjet_VSjet%(wp)s_VSele%(wp_VSe)s_Jul18.root' % vars()) # note DM fracts were not updated for DeepTauv2p5, but should be very similar
    f2 = ROOT.TFile('data/TauID_SF_Highpt_DeepTau2018v2p5VSjet_VSjet%(wp)s_VSele%(wp_VSe)s_Jul18.root' % vars())
    f3 = ROOT.TFile('data/TauID_SF_dm_DeepTau2018v2p5VSjet_VSjet%(wp)s_VSele%(wp_VSe)s_Jul18.root' % vars())


    for y in ['2016_preVFP','2016_postVFP', '2017', '2018']:
      h1 = f2.Get('DMinclusive_%(y)s_hist' % vars())

      for pt in pt_vals:
        W_val = h1.GetBinContent(h1.FindBin(pt))
        W_e = h1.GetBinError(h1.FindBin(pt))


        Z_val, Z_e = GetDMAveragedSF(f1,f3,pt,y)
        max_pt=140.
        Z_val_noextrap, Z_e_noextrap  = GetDMAveragedSF(f1,f3,max_pt,y)
        r = W_val/Z_val
        r_noextrap = W_val/Z_val_noextrap

        r_e = r*((Z_e/Z_val)**2 + (W_e/W_val)**2)**.5
        r_e_noextrap = r_noextrap*((Z_e_noextrap/Z_val_noextrap)**2 + (W_e/W_val)**2)**.5

        sig=(1.-r)/r_e
        sig_noextrap=(1.-r_noextrap)/r_e_noextrap

        y_str = y.ljust(12)

        print_out= 'ERA = %(y_str)s, pT = %(pt)s GeV, W*TNu = %(W_val).3f +/- %(W_e).3f, ZTT (extrap) = %(Z_val).3f +/- %(Z_e).3f, ZTT (no extrap above %(max_pt).0f GeV) %(Z_val_noextrap).3f +/- %(Z_e_noextrap).3f,  ratio (extrap) = %(r).3f +/- %(r_e).3f, ratio (no extrap) %(r_noextrap).3f +/- %(r_e_noextrap).3f, pull (extrap) = %(sig).2f, pull (no extrap) = %(sig_noextrap).2f ' % vars()
        
       # # uncomment for short version
       # print_out= 'ERA = %(y_str)s, pT = %(pt)s GeV, W/Z ratio (extrap) = %(r).3f +/- %(r_e).3f, W/Z ratio (no extrap) %(r_noextrap).3f +/- %(r_e_noextrap).3f, pull (extrap) = %(sig)+.2f, pull (no extrap) = %(sig_noextrap)+.2f ' % vars()

        N_tot+=1
        if abs(sig)>1 or abs(sig_noextrap)>1: 
          print_out = "\033[1;31m" + print_out + "\033[0m"
          N_1sig+=1
        if abs(sig>2) or abs(sig_noextrap)>2: 
        #  print_out="\033[1;31;47m" + print_out + "\033[0m"  
          N_2sig+=1
        print print_out

        # uncomment to compare SF for different DM mix (using DY events)
        #if (wp=='Medium' and wp_VSe=='VVLoose'):
        #  f4=ROOT.TFile('data/TauID_Highpt_DMFracts_DY_DeepTau2017v2p1VSjet_VSjetMedium_VSeleVVLoose_Mar07.root')
        #  Z_val_noextrap_alt, Z_e_noextrap_alt = GetDMAveragedSF(f4,f3,max_pt.,y)

        #  alt_dm_ratio = Z_val_noextrap/Z_val_noextrap_alt
        #  print '\n Also comparing average scale factors using W DM fractions and DR DM fractions'
        #  print 'W fracs = %(Z_val_noextrap).3f, Z fracs = %(Z_val_noextrap_alt).3f, ratio = %(alt_dm_ratio).3f \n' % vars()
    print '-----------------------------------\n'


frac_1sig = float(N_1sig)/float(N_tot)*100
frac_2sig = float(N_2sig)/float(N_tot)*100

print '%(N_1sig)i / %(N_tot)i (%(frac_1sig).0f%%) 1 sigma pulls' % vars()
print '%(N_2sig)i / %(N_tot)i (%(frac_2sig).0f%%) 2 sigma pulls' % vars()

print 'Note that these numbers do not account for correlations between measurments'
