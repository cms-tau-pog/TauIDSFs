import re
import ROOT

input_file = 'data/HighPT_tauIdSF_4eras.txt'
vs_ele_wp=None

sf_maps = {}

with open(input_file) as file:
    for line in file:
        if 'TightVSmu' in line and 'discriminants' in line:
          vs_ele_wp=line.split()[2]
          sf_maps[vs_ele_wp] = {}
        if 'VSjet' in line and not 'TightVSmu' in line and not 'discriminants' in line:
          vs_jet_wp=line.split()[0]
          sf_maps[vs_ele_wp][vs_jet_wp] = {}


        if vs_ele_wp and ('r_lowpt' in line or 'r_highpt' in line):
          var=line.split('=')[0].split()[0]
          vals=line.split('=')[1].split('+/-')
          for i,v in enumerate(vals): 
            vals[i]= float(re.findall("[+-]?\d+\.\d+",v)[0])

          if 'low' in var:  pt = [145., 25.]
          if 'high' in var: pt = [250., 50.]

          if '17' in var: year = '2017'
          elif '18' in var: year = '2018'
          elif '16APV' in var: year = '2016_preVFP'
          elif '16' in var: year = '2016_postVFP'
          else: continue
          # add for 2016 eventually as well

          if year in sf_maps[vs_ele_wp][vs_jet_wp]: sf_maps[vs_ele_wp][vs_jet_wp][year] += [pt+vals]

          else: sf_maps[vs_ele_wp][vs_jet_wp][year] = [pt+vals]
 

outname = 'data/TauID_SF_Highpt_DeepTau2017v2p1VSjet_VSjetXXX_VSeleYYY_Mar07.root'

for key1 in sf_maps:
  for key2 in sf_maps[key1]:

    fout = ROOT.TFile(outname.replace('XXX', key2.replace('VSjet','')).replace('YYY',key1.replace('VSe','')), 'RECREATE')

    for year in ['2016_preVFP','2016_postVFP','2017','2018']:
      name = 'DMinclusive_'+year
      g1=ROOT.TGraphAsymmErrors()
      g2=ROOT.TGraphAsymmErrors()
      g3=ROOT.TGraphAsymmErrors()
      for x in sf_maps[key1][key2][year]:
        pt = x[0]
        pt_e = x[1]
        sf=x[2]
        sf_e_syst=x[3]
        sf_e_syst_byera=x[4]
        sf_e_stat=x[5]
        Npoint = g1.GetN()
        g1.SetPoint(Npoint,pt,sf) 
        g2.SetPoint(Npoint,pt,0.) 
        g3.SetPoint(Npoint,pt,0.) 
        g1.SetPointError(Npoint,pt_e, pt_e, sf_e_stat, sf_e_stat) 
        g2.SetPointError(Npoint,pt_e, pt_e, sf_e_syst, sf_e_syst) 
        g3.SetPointError(Npoint,pt_e, pt_e, sf_e_syst_byera, sf_e_syst_byera) 
      g1.Write(name)
      g2.Write(name+'_syst_alleras')
      g3.Write(name+'_syst_%s' % year)

    fout.Close()

