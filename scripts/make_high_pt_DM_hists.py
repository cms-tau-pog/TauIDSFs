import re
import ROOT

#tauid='DeepTau2017v2p1VSjet'
tauid='DeepTau2018v2p5VSjet'

input_file = 'data/HighPT_fractions_4eras_%s.txt' % tauid
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
          vals = [float(x) for x in re.findall(r'\d+\.\d+', line)]
          vals = [x / sum(vals) for x in vals]
          print var, vals

          if 'low' in var:  pt = [145.]
          if 'high' in var: pt = [250.]

          if '17' in var: year = '2017'
          elif '18' in var: year = '2018'
          elif '16APV' in var: year = '2016_preVFP'
          elif '16' in var: year = '2016_postVFP'
          else: continue
          # add for 2016 eventually as well

          if year in sf_maps[vs_ele_wp][vs_jet_wp]: sf_maps[vs_ele_wp][vs_jet_wp][year] += [pt+vals]

          else: sf_maps[vs_ele_wp][vs_jet_wp][year] = [pt+vals]

if tauid=='DeepTau2017v2p1VSjet':
  outname = 'data/TauID_Highpt_DMFracts_DeepTau2017v2p1VSjet_VSjetXXX_VSeleYYY_Mar07.root'
else:
  outname = 'data/TauID_Highpt_DMFracts_DeepTau2018v2p5VSjet_VSjetXXX_VSeleYYY_Jul18.root'

for key1 in sf_maps:
  for key2 in sf_maps[key1]:

    fout = ROOT.TFile(outname.replace('XXX', key2.replace('VSjet','')).replace('YYY',key1.replace('VSe','')), 'RECREATE')

    for year in ['2016_preVFP','2016_postVFP','2017','2018']:
      for dm in [0,1,10,11]:
        g1=ROOT.TGraph()
        for x in sf_maps[key1][key2][year]:
          pt = x[0]
          if dm<10: dm_index = 1+dm
          else: dm_index=dm-10+3
          print dm_index, x
          dm_val=x[dm_index]
          Npoint = g1.GetN()
          g1.SetPoint(Npoint,pt,dm_val) 
        g1.Write('DMFrac_DM%i_%s' % (dm, year))

    fout.Close()

