#!/usr/bin/env python
import os, sys
import numpy as np
from ROOT import gROOT,std,ROOT,TFile,TTree,TH1D,TH2D,TStopwatch,TMatrix,TLorentzVector,TMath,TVector
gROOT.Macro("~/rootlogon.C")

def SolveNuPz(vlep, vnu, wmass, nuz1, nuz2):
    solutionBool = True
    tempsol = 0.0
    x = vlep.X()*vnu.X() + vlep.Y()*vnu.Y() + wmass*wmass/2
    a = vlep.Z()*vlep.Z() - vlep.E()*vlep.E()
    b = 2*x*vlep.Z()
    c = x*x - vnu.Perp2() * vlep.E()*vlep.E()
    d = b*b - 4*a*c
    if d < 0:
        d = 0
        solutionBool = False
    nuz1 = (-b + np.sqrt(d))/2/a
    nuz2 = (-b -np.sqrt(d))/2/a
    if solutionBool:
	if abs(nuz2) < abs(nuz1):
	    tempsol = nuz1
	    nuz1 = nuz2
	    nuz2 = tempsol
    return solutionBool, nuz1, nuz2;

def AdjustEnergyForMass(v, mass):
    v.SetE(np.sqrt(v.Vect().Mag2() + mass*mass))
    return v;

def nextPerm(lis):
    n = len(lis)

    i = n-2
    while i >= 0 and lis[i] >= lis[i+1]:
	i -= 1

    if i == -1:
	return False;

    j = i + 1
    while j < n and lis[j] > lis[i]:
	j += 1
    j -= 1

    lis[i], lis[j] = lis[j], lis[i]

    left = i + 1
    right = n -1

    while left < right:
	lis[left], lis[right] = lis[right], lis[left]
	left += 1
	right -= 1

    return True;

def GetChi2Boosted(ak4jetsP4, higgsJet, higgsSoftDropMass, leptonP4, nuP4, topMass, higgsMass, topP4, higgsP4, dR):
    top = 0.0; higgs = 0.0; top_chi2 = 0.0; higgs_chi2 = 0.0; dR_topH = 0.0; dR_topH_chi2 = 0.0
    
    top = abs( (ak4jetsP4[0] + leptonP4 + nuP4).M() - topMass)
    top_chi2 = top*top / (14.5*14.5)
    topP4 = ak4jetsP4[0] + leptonP4 + nuP4

    higgs = abs(higgsJet[0].M() - higgsMass)
    higgs_chi2 = higgs*higgs / (14.5*14.5)
    higgsP4 = higgsJet[0]


    dR_topH = abs(topP4.DeltaR(higgsP4) - 3.15)
    dR_topH_chi2 = dR_topH*dR_topH / (0.196*0.196)
    dR = topP4.DeltaR(higgsP4)

    if ak4jetsP4[0].DeltaR(higgsP4) < 1.0:
	return 100000.0, 100000.0, TLorentzVector(0.0, 0.0, 0.0, 0.0), TLorentzVector(0.0, 0.0, 0.0, 0.0)
    else:
	return top_chi2 + higgs_chi2 + dR_topH_chi2, dR, topP4, higgsP4
 
def DoMassRecoBoost(ak4Jets, higgsJet, higgsSoftDropMass, leptonP4, nuP4, higgsMass, topMass, chi2_dR1, chi2_dR2, chi2_higgs1, chi2_higgs2, chi2_top1, chi2_top2):
    ak4JetsP4 = [TLorentzVector(0.0, 0.0, 0.0, 0.0), TLorentzVector(0.0, 0.0, 0.0, 0.0)]
    chi2 = 100000.0; dR = 100000.0; minChi2 = 100000.0
    topP4 = TLorentzVector(0.0, 0.0, 0.0, 0.0)
    higgsP4 = TLorentzVector(0.0, 0.0, 0.0, 0.0)
    indexnum = 2

    if len(higgsJet) > 0 and len(ak4Jets) > 0:
	if len(ak4Jets) >= indexnum and len(higgsJet) >= indexnum:
       	    for i in range(0, indexnum):
	        for j in range(0, indexnum):
	            jetsP4PassToChi2 = []
  	            higgsjetsP4PassToChi2 = []

	            if len(jetsP4PassToChi2) != 0:
	                jetsP4PassToChi2.clear()
		    if len(higgsjetsP4PassToChi2) != 0:
		        higgsjetsP4PassToChi2.clear()
	            topP4.Clear()
	            higgsP4.Clear()
	            ak4JetsP4 = []
		    higgsJetsP4 = []

		    jetsP4PassToChi2.append(ak4Jets[i])

                    higgsjetsP4PassToChi2.append(higgsJet[j])

	            chi2, dR, topP4, higgsP4 = GetChi2Boosted(jetsP4PassToChi2, higgsjetsP4PassToChi2, higgsSoftDropMass, leptonP4, nuP4, topMass, higgsMass, topP4, higgsP4, dR)

	            if (chi2 < minChi2):
	                minChi2 = chi2
	    
	                chi2_higgs1 = minChi2
	                chi2_higgs2 = higgsP4

	                chi2_top1 = minChi2
	                chi2_top2 = topP4

	                chi2_dR1 = minChi2
	                chi2_dR2 = dR
	elif len(ak4Jets) < indexnum and len(higgsJet) >= indexnum:
	    for i in range(0, len(ak4Jets)):
                for j in range(0, indexnum):
                    jetsP4PassToChi2 = []               
                    higgsjetsP4PassToChi2 = []

                    if len(jetsP4PassToChi2) != 0:
                        jetsP4PassToChi2.clear()
                    if len(higgsjetsP4PassToChi2) != 0:
                        higgsjetsP4PassToChi2.clear()
                    topP4.Clear()
                    higgsP4.Clear()
                    ak4JetsP4 = []
                    higgsJetsP4 = []

                    jetsP4PassToChi2.append(ak4Jets[i])

                    higgsjetsP4PassToChi2.append(higgsJet[j])

                    chi2, dR, topP4, higgsP4 = GetChi2Boosted(jetsP4PassToChi2, higgsjetsP4PassToChi2, higgsSoftDropMass, leptonP4, nuP4, topMass, higgsMass, topP4, higgsP4, dR)

                    if (chi2 < minChi2):
                        minChi2 = chi2

                        chi2_higgs1 = minChi2
                        chi2_higgs2 = higgsP4

                        chi2_top1 = minChi2
                        chi2_top2 = topP4

                        chi2_dR1 = minChi2
                        chi2_dR2 = dR
	elif len(ak4Jets) >= indexnum and len(higgsJet) < indexnum:
	    for i in range(0, indexnum):
                for j in range(0, len(higgsJet)):
                    jetsP4PassToChi2 = []               
                    higgsjetsP4PassToChi2 = []

                    if len(jetsP4PassToChi2) != 0:
                        jetsP4PassToChi2.clear()
                    if len(higgsjetsP4PassToChi2) != 0:
                        higgsjetsP4PassToChi2.clear()
                    topP4.Clear()
                    higgsP4.Clear()
                    ak4JetsP4 = []
                    higgsJetsP4 = []

                    jetsP4PassToChi2.append(ak4Jets[i])

                    higgsjetsP4PassToChi2.append(higgsJet[j])

                    chi2, dR, topP4, higgsP4 = GetChi2Boosted(jetsP4PassToChi2, higgsjetsP4PassToChi2, higgsSoftDropMass, leptonP4, nuP4, topMass, higgsMass, topP4, higgsP4, dR)

                    if (chi2 < minChi2):
                        minChi2 = chi2

                        chi2_higgs1 = minChi2
                        chi2_higgs2 = higgsP4

                        chi2_top1 = minChi2
                        chi2_top2 = topP4

                        chi2_dR1 = minChi2
                        chi2_dR2 = dR
	elif len(ak4Jets) < indexnum and len(higgsJet) < indexnum:
	    for i in range(0, len(ak4Jets)):
                for j in range(0, len(higgsJet)):
                    jetsP4PassToChi2 = []               
                    higgsjetsP4PassToChi2 = []

                    if len(jetsP4PassToChi2) != 0:
                        jetsP4PassToChi2.clear()
                    if len(higgsjetsP4PassToChi2) != 0:
                        higgsjetsP4PassToChi2.clear()
                    topP4.Clear()
                    higgsP4.Clear()
                    ak4JetsP4 = []
                    higgsJetsP4 = []

                    jetsP4PassToChi2.append(ak4Jets[i])

                    higgsjetsP4PassToChi2.append(higgsJet[j])

                    chi2, dR, topP4, higgsP4 = GetChi2Boosted(jetsP4PassToChi2, higgsjetsP4PassToChi2, higgsSoftDropMass, leptonP4, nuP4, topMass, higgsMass, topP4, higgsP4, dR)

                    if (chi2 < minChi2):
                        minChi2 = chi2

                        chi2_higgs1 = minChi2
                        chi2_higgs2 = higgsP4

                        chi2_top1 = minChi2
                        chi2_top2 = topP4

                        chi2_dR1 = minChi2
                        chi2_dR2 = dR

    return chi2_higgs1, chi2_higgs2, chi2_top2, chi2_dR2

from optparse import OptionParser

# Create a command line option parser
options  = OptionParser()

options.add_option('--inDir', metavar='T', type='string', action='store',
                  default='inDir', 
                  dest='input directory', 
                  help='input data directory name')
options.add_option('-f', '--files',  
                   dest="files", 
                   default="T_M1500_W10.txt",
                   type="string")
options.add_option('-n', '--maxEvts',  
                   dest="maxEvts", 
                   default=-1,
                   type="int")

(options,args) = options.parse_args()
# ==========end: options =============

##options.add_option_group(evtsel)

#opt, remainder = options.parse_args()

print options
maxEvts = options.maxEvts

# Define the output histograms
fname = options.files.rstrip()
ftemp = fname.split("//")[2]
fout = TFile(ftemp.split("/")[6].replace('.root', '_out.root'), 'RECREATE')
print 'here is something: ', ftemp.split("/")[6].replace('.root', '_out.root')
fout.cd()

hCutflow = TH1D("hCutflow" ,";;Events;" ,12, 0.5, 12.5)
cutsName = ['Preselection', 'Exactly 1 lepton', '3 or more central jets', '1 or more forward jet', 'leading jet pt > 250', '2nd leading jet pt > 150', 'ST > 1000', '2D lep Iso', '1 or more B-tagged jet', 'MET > 20 GeV', '#geq 1 Higgs Candidate', '#Delta R(higgs, top) > 2']
ibin = 0
for n in cutsName:
   ibin = ibin+1
   hCutflow.GetXaxis().SetBinLabel(ibin, n)

hNGenEvents = TH1D("hNGenEvents", "Total Events; Total Events; Events", 2, 0.5, 2.5) 
hlepPt     = TH1D("hlepPt",  "Lepton p_{T}; p_{T}(GeV); Events;", 50, 0, 300)
hlepEta    = TH1D("hlepEta", "Lepton #eta; #eta; Events;", 80, -4.0, 4.0)
hlepIso_sig    = TH1D("hlepIso_sig", "Lepton isolation; Lepton Isolation; Events;", 50, 0.0, 5.0)
hjetsPt    = TH1D("hJetsPt", "Jets Pt; Jets Pt (GeV); Events/15 GeV", 80, 0, 2000)
hjetsEta   = TH1D("hJetsEta", "Jets #eta; Jets #eta; Events", 50, -5.0, 5.0)
hDRMin     = TH1D("hDRMin", "#Delta R_{MIN}(l, jet); #Delta R_{MIN}(l,jet); Events", 50, 0.0,3.0)
hDR        = TH1D("hDR", "#Delta R(l, jet); #Delta R (l,jet); Events", 50, 0.0,3.0) 
hPtRel     = TH1D("hPtRel", "p_{T,rel}; p_{T,rel} (GeV); Events", 50, 0, 100); 
hDPtRel    = TH1D("hDPtRel", "p_{T}^{REL}; p_{T}^{REL} (GeV); Events",50, 0, 100)   
hDelPtRel  = TH1D("hDelPtRel", "p_{T}^{REL}; p_{T}^{REL} (GeV); Events;", 50, 0, 100) 
h2DdPtReldR = TH2D("h2DdPtReldR", "2D Isolation;#Delta R(l,j);p_{T}^{REL} (GeV(", 50, 0.0, 1.0, 20, 0., 200.)
h2DdPtRelDRMin = TH2D("h2DdPtRelDRMin", ";#Delta R_{MIN}(l,j);p_{T}^{REL} (GeV)", 50, 0.0, 1.0, 20, 0., 200.)
hNForwardJets = TH1D("hNForwardJets", "Number of Forward Jets; Number of Forward Jets; Events;", 20, 0, 20)
hLeadingJetPt = TH1D("hLeadingJetPt", "Leading Jet p_{T}; p_{T} (GeV); Events;", 100, 0, 1000)
hLeadingJetEta = TH1D("hLeadingJetEta", "Leading Jet #eta; #eta; Events;", 80, -5.0, 5.0)
hNCentJets = TH1D("hNCentJets", "Number of Central Jets; Number of Central Jets; Events;", 20, 0, 20)
hSecJetPt = TH1D("hSecJetPt", "Second Leading Jet p_{T}; p_{T} (GeV); Events;", 100, 0, 1000)
hSecJetEta = TH1D("hSecJetEta", "Second Leading Jet #eta; #eta; Events;", 80, -5.0, 5.0)
hMET = TH1D("hMET", "Missing E_{T}; MET (GeV); Events;", 50, 0, 1000)
hFwrdJetPt = TH1D("hFwrdJetPt", "P_{T} of Most Forward Jet; P_{T} (GeV); Events;", 60, 0, 600)
hFwrdJetEta = TH1D("hFwrdJetEta", "#eta of Most Forward Jet; #eta; Events;", 40, -5.0, 5.0)
hNumBJets = TH1D("hNumBJets", "Number of B Jets; Number of B Jets; Events;", 20, 0.0, 20)
hak8JetPt = TH1D("hak8JetPt", "ak8Jet p_{T}; p_{T} (GeV); Events;", 100, 0, 1000)
hhiggsJetPt = TH1D("hhiggsJetPt", "higgsJet p_{T}; p_{T} (GeV); Events;", 100, 0, 1000)
hak8JetEta = TH1D("hak8JetEta", "ak8Jet #eta; #eta; Events;", 80, -4.0, 4.0)
hhiggsJetEta = TH1D("hhiggsJetEta", "higgsJet #eta; #eta; Events;", 80, -4.0, 4.0)
hak8JetTau21 = TH1D("hak8JetTau21", "ak8Jet tau2/tau1; tau2/tau1; Events;", 50, 0.0, 1.0)
hhiggsTau21 = TH1D("hhiggsTau21", "higgs tau2/tau1; tau2/tau1; Events;", 50, 0.0, 1.0)
hdRak8JetlepP4 = TH1D("hdRak8JetlepP4", "dR(ak8Jet, lepton); dR; Events;", 50, 0.0, 5.0)
hdRhiggslepP4 = TH1D("hdRhiggslepP4", "dR(higgs, lepton); dR; Events;", 50, 0.0, 5.0)
hak8Jetsdmass = TH1D("hak8Jetsdmass", "SoftDrop Mass of ak8Jets; SoftDrop Mass (GeV); Events;", 100, 0, 400)
hhiggssdmass = TH1D("hhiggssdmass", "SoftDrop Mass of Higgs; SoftDrop Mass (GeV); Events;", 100, 0, 400)
hak8jetsj1deepcsv = TH1D("hak8jetsj1deepcsv", "ak8SubJet 1 DeepCSV; DeepCSV Value; Events;", 50, 0, 1)
hhiggssj1deepcsv = TH1D("hhiggssj1deepcsv", "Higgs SubJet 1 DeepCSV; DeepCSV Value; Events;", 50, 0, 1)
hak8jetsj2deepcsv = TH1D("hak8jetsj2deepcsv", "ak8SubJet 2 DeepCSV; DeepCSV Value; Events;", 50, 0, 1)
hhiggssj2deepcsv = TH1D("hhiggssj2deepcsv", "Higgs SubJet 2 DeepCSV; DeepCSV Value; Events;", 50, 0, 1)
hak4jetsPtafter = TH1D("hak4jetsPtafter", "p_{T} of Ak4Jets After Cuts; p_{T} (GeV); Events;", 100, 0, 1000)
hak4jetsEtaafter = TH1D("hak4jetsEtaafter", "#eta of Ak4Jets After Cuts; #eta; Events;", 50, -5.0, 5.0)
hnumak4jets = TH1D("hnumak4jets", "Number of Ak4Jets After Cuts; Number of Ak4Jets; Events;", 25, 0, 25)
hak8jetsPtafter = TH1D("hak8jetsPtafter", "p_{T} of Ak8Jets After Cuts; p_{T} (GeV); Events;", 100, 0, 1000)
hak8jetsEtaafter = TH1D("hak8jetsEtaafter", "#eta of Ak8Jets After Cuts; #eta; Events;", 50, -5.0, 5.0)
hnumak8jets = TH1D("hnumak8jets", "Number of Ak8Jets After Cuts; Number of Ak8Jets; Events;", 10, 0, 10)
h2DdPtRelDRMinafter = TH2D("h2DdPtRelDRMinafter", ";#Delta R_{MIN}(l,j) After Cuts; p_{T}^{REL} (GeV)", 50, 0.0, 1.0, 20, 0., 200.)
hhiggsmass = TH1D("hhiggsmass", "Higgs Mass; Mass (GeV),; Events;", 40, 0, 400)
htopmass = TH1D("htopmass", "Top Mass; Mass (GeV); Events;", 40, 0, 400)
hWmass = TH1D("hWmass", "W Mass; Mass (GeV); Events;", 30, 0, 200)
htprimemass = TH1D("htprimemass", "TPrime Mass; Mass (GeV); Events;", 50, 0, 5000)
hdRtophiggsbefore = TH1D("hdRtophiggsbefore", "#Delta R(top, higgs) before cut; #Delta R; Events;", 50, 0.0, 5.0)
hdRtophiggsafter = TH1D("hdRtophiggsafter", "#Delta R(top, higgs) after cut; #Delta R(top, higgs); Events;", 50, 0.0, 5.0)
hchi2 = TH1D("hchi2", "#chi^{2}; #chi^{2}; Events;", 60, 0.0, 600.0)
hhiggspt = TH1D("hhiggspt", "p_{T} of Higgs; p_{T}; Events;", 100, 0, 1000)
hhiggseta = TH1D("hhiggseta", "Higgs #eta; #eta; Events;", 80, -4.0, 4.0)
htoppt = TH1D("htoppt", "p_{T} of Top; p_{T}; Events;", 100, 0, 1000)
htopeta = TH1D("htopeta", "Top #eta; #eta; Events;", 80, -4.0, 4.0)
htprimept = TH1D("htprimept", "p_{T} of Tprime; p_{T}; Events;", 100, 0, 1000)
htprimeeta = TH1D("htprimeeta", "Tprime #eta; #eta; Events;", 80, -4.0, 4.0)
hST = TH1D("hST", "S_{T}; S_{T} (GeV); Events;", 150, 0.0, 4000.0)
hCentJetPt = TH1D("hCentJetPt", "Central Jets Pt; p_{t} (GeV); Events;", 100, 0, 1000)
hCentJetEta = TH1D("hCentJetEta", "Central Jets Eta; #eta; Events;", 40, -4.0, 4.0)
hdRleadjetMET = TH1D("hdRleadjetMET", "#Delta R(leadingjet, MET); #Delta R; Events;", 50, 0.0, 5.0)
h2Daftercut = TH2D("h2Daftercut", "2D Isolation Variables After Cut; #Delta r; p_{T}^{REL} (GeV)", 50, 0.0, 1.0, 20, 0.0, 200.0)
hpTRelafterall = TH1D("hpTRelafterall", "p_{T}^{REL} After All Cuts; p_{T}^{REL} (GeV); Events", 50, 0.0, 200.0)
hdRMinafterall = TH1D("hdRMinafterall", "#Delta R_{Min} After All Cuts; #Delta R_{Min}; Events", 30, 0.0, 1.0)

hnumlepbefore = TH1D("hnumlepbefore", "Number of Leptons Before Cut; Number of Leptons; Events", 20, 0.0, 20.0)
hnumlepafter = TH1D("hnumlepafter", "Number of Leptons After Cut; Number of Leptons; Events", 20, 0.0, 20.0)
hnumcentjetsbefore = TH1D("hnumcentjetsbefore", "Number of Central Jets Before Cut; Number of Central Jets; Events", 30, 0.0, 30.0)
hnumcentjetsafter = TH1D("hnumcentjetsafter", "Number of Central Jets After Cut; Number of Central Jets; Events", 30, 0.0, 30.0)
hnumfjetsbefore = TH1D("hnumfjetsbefore", "Number of Forward Jets Before Cut; Number of Forward Jets; Events", 30, 0.0, 30.0)
hnumfjetsafter = TH1D("hnumfjetsafter", "Number of Forward Jets After Cut; Number of Forward Jets; Events", 30, 0.0, 30.0)
hleadjetptbefore = TH1D("hleadjetptbefore", "p_{T} of Leading Jet Before Cut; p_{T} (GeV); Events", 100, 0.0, 1000.0)
hleadjetptafter = TH1D("hleadjetptafter", "p_{T} of Leading Jet After Cut; p_{T} (GeV); Events", 100, 0.0, 1000.0)
hsecjetptbefore = TH1D("hsecjetptbefore", "p_{T} of Second Leading Jet Before Cut; p_{T} (GeV); Events", 100, 0.0, 1000.0)
hsecjetptafter = TH1D("hsecjetptafter", "p_{T} of Second Leading Jet After Cut; p_{T} (GeV); Events", 100, 0.0, 1000.0)
hpTRelafter = TH1D("hpTRelafter", "p_{T}^{REL} After Cuts; p_{T}^{REL} (GeV); Events", 50, 0.0, 200.0)
hdRMinafter = TH1D("hdRMinafter", "#Delta R_{Min} After Cuts; #Delta R_{Min}; Events", 30, 0.0, 1.0)
hnumBjetsbefore = TH1D("hnumBjetsbefore", "Number of B Jets Before Cut; Number of B Jets; Events", 30, 0.0, 30.0)
hnumBjetsafter = TH1D("hnumBjetsafter", "Number of B Jets After Cut; Number of B Jets; Events", 30, 0.0, 30.0)
hMETbefore = TH1D("hMETbefore", "MET Before Cut; MET (GeV); Events", 100, 0.0, 1000.0)
hMETafter = TH1D("hMETafter", "MET After Cut; MET (GeV); Events", 100, 0.0, 1000.0)
hnumhiggsbefore = TH1D("hnumhiggsbefore", "Number of Higgs Before Cut; Number of Higgs; Events", 30, 0.0, 30.0)
hnumhiggsafter = TH1D("hnumhiggsafter", "Number of Higgs After Cut; Number of Higgs; Events", 30, 0.0, 30.0)
hSTatdef = TH1D("hSTatdef", "ST; ST (GeV); Events;", 150, 0.0, 4000.0)

helechanak4jetsPtafter = TH1D("helechanak4jetsPtafter", "Electron Channelp_{T} of Ak4Jets After Cuts; p_{T} (GeV); Events;", 100, 0, 1000)
helechanak4jetsEtaafter = TH1D("helechanak4jetsEtaafter", "Electron Channel#eta of Ak4Jets After Cuts; #eta; Events;", 50, -5.0, 5.0)
helechannumak4jets = TH1D("helechannumak4jets", "Electron Channel Number of Ak4Jets After Cuts; Number of Ak4Jets; Events;", 25, 0, 25)
helechanak8jetsPtafter = TH1D("helechanak8jetsPtafter", "Electron Channelp_{T} of Ak8Jets After Cuts; p_{T} (GeV); Events;", 100, 0, 1000)
helechanak8jetsEtaafter = TH1D("helechanak8jetsEtaafter", "Electron Channel#eta of Ak8Jets After Cuts; #eta; Events;", 50, -5.0, 5.0)
helechannumak8jets = TH1D("helechannumak8jets", "Electron Channel Number of Ak8Jets After Cuts; Number of Ak8Jets; Events;", 10, 0, 10)
helechan2DdPtRelDRMinafter = TH2D("helechan2DdPtRelDRMin", "Electron Channel #Delta R_{MIN}(l,j) After Cuts; min #Delta p_{T}^{REL} (GeV)", 50, 0.0, 1.0, 20, 0., 200.)
helechanhiggsmass = TH1D("helechanhiggsmass", "Electron Channel Higgs Mass; Mass (GeV),; Events;", 40, 0, 400)
helechantopmass = TH1D("helechantopmass", "Electron Channel Top Mass; Mass (GeV); Events;", 40, 0, 400)
helechanWmass = TH1D("helechanWmass", "Electron Channel W Mass; Mass (GeV); Events;", 30, 0, 200)
helechantprimemass = TH1D("helechantprimemass", "Electron Channel TPrime Mass; Mass (GeV); Events;", 40, 0, 5000)
helechandRtophiggsafter = TH1D("helechandRtophiggsafter", "Electron Channel dR(top, higgs) after cut; dR; Events;", 50, 0.0, 5.0)
helechanchi2 = TH1D("helechanchi2", "Electron Channel chi2; chi2; Events;", 60, 0.0, 600.0)
helechanhiggspt = TH1D("helechanhiggspt", "Electron Channel p_{T} of Higgs; p_{T}; Events;", 100, 0, 1000)
helechanhiggseta = TH1D("helechanhiggseta", "Electron Channel Higgs #eta; #eta; Events;", 80, -4.0, 4.0)
helechantoppt = TH1D("helechantoppt", "Electron Channel p_{T} of Top; p_{T}; Events;", 100, 0, 1000)
helechantopeta = TH1D("helechantopeta", "Electron Channel Top #eta; #eta; Events;", 80, -4.0, 4.0)
helechantprimept = TH1D("helechantprimept", "Electron Channel p_{T} of Tprime; p_{T}; Events;", 100, 0, 1000)
helechantprimeeta = TH1D("helechantprimeeta", "Electron Channel Tprime #eta; #eta; Events;", 80, -4.0, 4.0)
helechanlepPt     = TH1D("helechanlepPt",  "Electron Channel Lepton p_{T}; p_{T}(GeV); Events/60 GeV;", 50, 0, 300)
helechanlepEta    = TH1D("helechanlepEta", "Electron Channel Lepton #eta; #eta; Events/10 bins;", 80, -4.0, 4.0)
helechanNForwardJets = TH1D("helechanNForwardJets", "Electron Channel Number of Forward Jets; Number of Forward Jets; Events;", 20, 0, 20)
helechanLeadingJetPt = TH1D("helechanLeadingJetPt", "Electron Channel Leading Jet p_{T}; p_{T} (GeV); Events;", 100, 0, 1000)
helechanLeadingJetEta = TH1D("helechanLeadingJetEta", "Electron Channel Leading Jet #eta; #eta; Events;", 80, -5.0, 5.0)
helechanNCentJets = TH1D("helechanNCentJets", "Electron Channel Number of Central Jets; Number of Central Jets; Events;", 20, 0, 20)
helechanSecJetPt = TH1D("helechanSecJetPt", "Electron Channel Second Leading Jet p_{T}; p_{T} (GeV); Events;", 100, 0, 1000)
helechanSecJetEta = TH1D("helechanSecJetEta", "Electron Channel Second Leading Jet #eta; #eta; Events;", 80, -5.0, 5.0)
helechanMET = TH1D("helechanMET", "Electron Channel Missing E_{T}; MET (GeV); Events;", 50, 0, 1000)
helechanFwrdJetPt = TH1D("helechanFwrdJetPt", "Electron Channel p_{T} of Most Forward Jet; p_{T} (GeV); Events;", 100, 0, 1000)
helechanFwrdJetEta = TH1D("helechanFwrdJetEta", "Electron Channel #eta of Most Forward Jet; #eta; Events;", 40, -5.0, 5.0)
helechanNumBJets = TH1D("helechanNumBJets", "Electron Channel Number of B Jets; Number of B Jets; Events;", 20, 0.0, 20)
heleST = TH1D("heleST", "Electron Channel ST; ST (GeV); Events;", 50, 0.0, 2000.0)
helechanCentJetPt = TH1D("helechanCentJetPt", "Electron Channel Central Jets Pt; p_{t} (GeV); Events;", 100, 0, 1000)
helechanCentJetEta = TH1D("helechanCentJetEta", "Electron Channel Central Jets Eta; #eta; Events;", 40, -4.0, 4.0)
helechandRleadjetMET = TH1D("helechandRleadjetMET", "Electron Channel #Delta R(leadingjet, MET); #Delta R; Events;", 50, 0.0, 5.0)
helechanpTRelafter = TH1D("helechanpTRelafter", "Electron Channel p_{T}^{REL} After All Cuts; p_{T}^{REL} (GeV); Events", 50, 0.0, 200.0)
helechandRMinafter = TH1D("helechandRMinafter", "Electron Channel #Delta R_{Min} After All Cuts; #Delta R_{Min}; Events", 30, 0.0, 1.0)

hmuchanak4jetsPtafter = TH1D("hmuchanak4jetsPtafter", "Muon Channelp_{T} of Ak4Jets After Cuts; p_{T} (GeV); Events;", 100, 0, 1000)
hmuchanak4jetsEtaafter = TH1D("hmuchanak4jetsEtaafter", "Muon Channel#eta of Ak4Jets After Cuts; #eta; Events;", 50, -5.0, 5.0)
hmuchannumak4jets = TH1D("hmuchannumak4jets", "Muon Channel Number of Ak4Jets After Cuts; Number of Ak4Jets; Events;", 25, 0, 25)
hmuchanak8jetsPtafter = TH1D("hmuchanak8jetsPtafter", "Muon Channelp_{T} of Ak8Jets After Cuts; p_{T} (GeV); Events;", 100, 0, 1000)
hmuchanak8jetsEtaafter = TH1D("hmuchanak8jetsEtaafter", "Muon Channel#eta of Ak8Jets After Cuts; #eta; Events;", 50, -5.0, 5.0)
hmuchannumak8jets = TH1D("hmuchannumak8jets", "Muon Channel Number of Ak8Jets After Cuts; Number of Ak8Jets; Events;", 10, 0, 10)
hmuchan2DdPtRelDRMinafter = TH2D("hmuchan2DdPtRelDRMin", "Muon Channel #Delta R_{MIN}(l,j) After Cuts; min #Delta p_{T}^{REL} (GeV)", 50, 0.0, 1.0, 20, 0., 200.)
hmuchanhiggsmass = TH1D("hmuchanhiggsmass", "Muon Channel Higgs Mass; Mass (GeV),; Events;", 40, 0, 400)
hmuchantopmass = TH1D("hmuchantopmass", "Muon Channel Top Mass; Mass (GeV); Events;", 40, 0, 400)
hmuchanWmass = TH1D("hmuchanWmass", "Muon Channel W Mass; Mass (GeV); Events;", 30, 0, 200)
hmuchantprimemass = TH1D("hmuchantprimemass", "Muon Channel TPrime Mass; Mass (GeV); Events;", 40, 0, 5000)
hmuchandRtophiggsafter = TH1D("hmuchandRtophiggsafter", "Muon Channel dR(top, higgs) after cut; dR; Events;", 50, 0.0, 5.0)
hmuchanchi2 = TH1D("hmuchanchi2", "Muon Channel chi2; chi2; Events;", 60, 0.0, 600.0)
hmuchanhiggspt = TH1D("hmuchanhiggspt", "Muon Channel p_{T} of Higgs; p_{T}; Events;", 100, 0, 1000)
hmuchanhiggseta = TH1D("hmuchanhiggseta", "Muon Channel Higgs #eta; #eta; Events;", 80, -4.0, 4.0)
hmuchantoppt = TH1D("hmuchantoppt", "Muon Channel p_{T} of Top; p_{T}; Events;", 100, 0, 1000)
hmuchantopeta = TH1D("hmuchantopeta", "Muon Channel Top #eta; #eta; Events;", 80, -4.0, 4.0)
hmuchantprimept = TH1D("hmuchantprimept", "Muon Channel p_{T} of Tprime; p_{T}; Events;", 100, 0, 1000)
hmuchantprimeeta = TH1D("hmuchantprimeeta", "Muon Channel Tprime #eta; #eta; Events;", 80, -4.0, 4.0)
hmuchanlepPt     = TH1D("hmuchanlepPt",  "Muon Channel Lepton p_{T}; p_{T}(GeV); Events/60 GeV;", 50, 0, 300)
hmuchanlepEta    = TH1D("hmuchanlepEta", "Muon Channel Lepton #eta; #eta; Events/10 bins;", 80, -4.0, 4.0)
hmuchanNForwardJets = TH1D("hmuchanNForwardJets", "Muon Channel Number of Forward Jets; Number of Forward Jets; Events;", 20, 0, 20)
hmuchanLeadingJetPt = TH1D("hmuchanLeadingJetPt", "Muon Channel Leading Jet p_{T}; p_{T} (GeV); Events;", 100, 0, 1000)
hmuchanLeadingJetEta = TH1D("hmuchanLeadingJetEta", "Muon Channel Leading Jet #eta; #eta; Events;", 80, -5.0, 5.0)
hmuchanNCentJets = TH1D("hmuchanNCentJets", "Muon Channel Number of Central Jets; Number of Central Jets; Events;", 20, 0, 20)
hmuchanSecJetPt = TH1D("hmuchanSecJetPt", "Muon Channel Second Leading Jet p_{T}; p_{T} (GeV); Events;", 100, 0, 1000)
hmuchanSecJetEta = TH1D("hmuchanSecJetEta", "Muon Channel Second Leading Jet #eta; #eta; Events;", 80, -5.0, 5.0)
hmuchanMET = TH1D("hmuchanMET", "Muon Channel Missing E_{T}; MET (GeV); Events;", 50, 0, 1000)
hmuchanFwrdJetPt = TH1D("hmuchanFwrdJetPt", "Muon Channel p_{T} of Most Forward Jet; p_{T} (GeV); Events;", 100, 0, 1000)
hmuchanFwrdJetEta = TH1D("hmuchanFwrdJetEta", "Muon Channel #eta of Most Forward Jet; #eta; Events;", 40, -5.0, 5.0)
hmuchanNumBJets = TH1D("hmuchanNumBJets", "Muon Channel Number of B Jets; Number of B Jets; Events;", 20, 0.0, 20)
hmuST = TH1D("hmuST", "Muon Channel ST; ST (GeV); Events;", 50, 0.0, 2000.0)
hmuchanCentJetPt = TH1D("hmuchanCentJetPt", "Muon Channel Central Jets Pt; p_{t} (GeV); Events;", 100, 0, 1000)
hmuchanCentJetEta = TH1D("hmuchanCentJetEta", "Muon Channel Central Jets Eta; #eta; Events;", 40, -5.0, 5.0)
hmuchandRleadjetMET = TH1D("hmuchandRleadjetMET", "Muon Channel #Delta R(leadingjet, MET); #Delta R; Events;", 50, 0.0, 5.0)
hmuchanpTRelafter = TH1D("hmuchanpTRelafter", "Muon Channel p_{T}^{REL} After All Cuts; p_{T}^{REL} (GeV); Events", 50, 0.0, 200.0)
hmuchandRMinafter = TH1D("hmuchandRMinafter", "Muon Channel #Delta R_{Min} After All Cuts; #Delta R_{Min}; Events", 30, 0.0, 1.0)

h0bjetshiggsmass = TH1D("h0bjetshiggsmass", "Higgs Mass in 0 B-jet Region; Mass (GeV); Events;", 40, 0, 400)
h0bjetstopmass = TH1D("h0bjetstopmass", "Top Mass in 0 B-jet Region; Mass (GeV); Events;", 40, 0, 400)
h0bjetstprimemass = TH1D("h0bjetstprimemass", "TPrime Mass in 0 B-jet Region; Mass (GeV); Events;", 50, 0, 5000)
h0bjetsdRtophiggs = TH1D("h0bjetsdRtophiggs", "#Delta R(top, higgs) in 0 B-jet Region; #Delta R; Events", 50, 0.0, 5.0)
h0bjetschi2 = TH1D("h0bjetschi2", "Chi2 in 0 B-jet Region; Chi2; Events;", 60, 0.0, 600.0)
h1bjetshiggsmass = TH1D("h1bjetshiggsmass", "Higgs Mass in 1 B-jet Region; Mass (GeV); Events;", 40, 0, 400)
h1bjetstopmass = TH1D("h1bjetstopmass", "Top Mass in 1 B-jet Region; Mass (GeV); Events;", 40, 0, 400)
h1bjetstprimemass = TH1D("h1bjetstprimemass", "TPrime Mass in 1 B-jet Region; Mass (GeV); Events;", 50, 0, 5000)
h1bjetsdRtophiggs = TH1D("h1bjetsdRtophiggs", "#Delta R(top, higgs) in 1 B-jet Region; #Delta R; Events", 50, 0.0, 5.0)
h1bjetschi2 = TH1D("h1bjetschi2", "Chi2 in 1 B-jet Region; Chi2; Events;", 60, 0.0, 600.0)
h2bjetshiggsmass = TH1D("h2bjetshiggsmass", "Higgs Mass in 2+ B-jet Region; Mass (GeV); Events;", 40, 0, 400)
h2bjetstopmass = TH1D("h2bjetstopmass", "Top Mass in 2+ B-jet Region; Mass (GeV); Events;", 40, 0, 400)
h2bjetstprimemass = TH1D("h2bjetstprimemass", "TPrime Mass in 2+ B-jet Region; Mass (GeV); Events;", 50, 0, 5000)
h2bjetsdRtophiggs = TH1D("h2bjetsdRtophiggs", "#Delta R(top, higgs) in 2+ B-jet Region; #Delta R; Events", 50, 0.0, 5.0)
h2bjetschi2 = TH1D("h2bjetschi2", "Chi2 in 2+ B-jet Region; Chi2; Events;", 60, 0.0, 600.0)

lepP4        = TLorentzVector(0.0, 0.0, 0.0, 0.0)
jetP4        = TLorentzVector(0.0, 0.0, 0.0, 0.0)
nearestJetP4 = TLorentzVector(0.0, 0.0, 0.0, 0.0)

# Open the input ntuples

# Begin running over all trees
ievt = 0
#if ievt%100 == 0: print " Processing evt %i" % ievt

print 'Opening file %s' % fname
f = TFile.Open(fname)
print f.ls()

tree = f.Get("ana/anatree")
entries = tree.GetEntriesFast()

for t in tree:
    ncut = 0
    if maxEvts > 0 and ievt > maxEvts: break
    if ievt%100 == 0: print " Processing evt %i" % ievt

    ievt += 1
    #ncut += 1
    # call the Gen weights
    evtwt = t.GenEvt_genWt
    numevt = 0
    numevt += 1
    hNGenEvents.Fill(numevt, evtwt)
    #hCutflow.Fill(ncut, evtwt)
 
#------------------------------------------------------------------------
#                          PRESELECTION
#------------------------------------------------------------------------
 
    # require at least one good primary vertex
    vertices = t.SelectedEvt_nGoodVtx
    if vertices <= 0: continue;

    ncut += 1
    hCutflow.Fill(ncut, evtwt)

#------------------------------------------------------------------------
#                          BASELINE CUTS
#------------------------------------------------------------------------

  # require exactly one medium WP electron or muon in event
    nMedium=0
    elelepcand = []
    ele_eta = t.Electrons_eta
    ele_phi = t.Electrons_phi
    ele_pt  = t.Electrons_pt
    ele_m   = t.Electrons_mass
    ele_mva = t.Electrons_mva
    ele_iso = t.Electrons_relIso
    eWP = t.Electrons_eleWP

    nmuMedium=0
    mulepcand = []
    mu_eta = t.Muons_eta
    mu_phi = t.Muons_phi
    mu_pt  = t.Muons_pt
    mu_m   = t.Muons_mass
    mu_iso = t.Muons_relIso
    muWP = t.Muons_muWP

    for i in range(0, len(t.Electrons_pt)):
	lepcand = TLorentzVector(0.0, 0.0, 0.0, 0.0)
        # choose the WP: 1 = loose, 2 = medium, 4 = tight
        if eWP[i] <= 1: continue
        if ele_pt[i] < 40.: continue 
        if abs(ele_eta[i]) > 2.8: continue
        nMedium += 1
	lepcand.SetPtEtaPhiM(ele_pt[i], ele_eta[i], ele_phi[i], ele_m[i])
	elelepcand.append(lepcand)
        #print 'mva = ',  ele_mva[i], 'eta = ', abs(ele_eta[i]), 'pt = ', ele_pt[i], 'eWP = ', eWP 

    for i in range(0, len(t.Muons_pt)):
	lepcand = TLorentzVector(0.0, 0.0, 0.0, 0.0)
        # choose the WP: 1 = loose, 2 = medium, 4 = tight
        if muWP[i] <= 1: continue
        if mu_pt[i] < 40.: continue
        if abs(mu_eta[i]) > 4.0: continue
        nmuMedium += 1
	lepcand.SetPtEtaPhiM(mu_pt[i], mu_eta[i], mu_phi[i], mu_m[i])
	mulepcand.append(lepcand)
        #print 'mva = ',  mu_mva[i], 'eta = ', abs(mu_eta[i]), 'pt = ', mu_pt[i], 'muWP = ', muWP 

    #require exactly one lepton   
    hnumlepbefore.Fill(nMedium + nmuMedium, evtwt)
    if nMedium + nmuMedium != 1: continue 
    ncut += 1
    hCutflow.Fill(ncut, evtwt)
    hnumlepafter.Fill(nMedium + nmuMedium, evtwt)

    # store lep variables:
    if nMedium ==  1:
    	lepP4.SetPtEtaPhiM(elelepcand[0].Pt(), elelepcand[0].Eta(), elelepcand[0].Phi(), elelepcand[0].M())
    elif nmuMedium == 1:
        lepP4.SetPtEtaPhiM(mulepcand[0].Pt(), mulepcand[0].Eta(), mulepcand[0].Phi(), mulepcand[0].M())
    else: continue
    lep_p3 = lepP4.Vect();

    # 3 or more central jets
    ak4jet_pt  = t.AK4JetsCHS_pt
    ak4jet_eta = t.AK4JetsCHS_eta #barrel: eta< 1.479
    ak4jet_phi = t.AK4JetsCHS_phi
    ak4jet_m   = t.AK4JetsCHS_mass
    ak4jet_deepcsv = t.AK4JetsCHS_deepcsv
    nak4jet = len(ak4jet_pt)

    jetsP4 = [] #define a list to store P4 of all good jets
    goodjetcsv = []
    dR = 900.0; dRMin = 999.0; delPtRel = 999.0

    for j in range(0, nak4jet):
        #funny enough: if I define the jetP4 in this line, then the address of object is never changed, hence its content
        hjetsPt.Fill(ak4jet_pt[j], evtwt)
        hjetsEta.Fill(ak4jet_eta[j], evtwt)
        if ak4jet_pt[j] < 30. : continue
        if abs(ak4jet_eta[j]) > 5.0 : continue
        jetP4 = TLorentzVector(0.0, 0.0, 0.0, 0.0)
        jetP4.SetPtEtaPhiM(ak4jet_pt[j], ak4jet_eta[j], ak4jet_phi[j], ak4jet_m[j])
        #print 'what is going inside: ', jetP4.Pt()
        jetsP4.append(jetP4)
        goodjetcsv.append(ak4jet_deepcsv[j])

    # separate the jets into central and forward jet collections 
    centjets = []
    fjets = []
    for j in jetsP4:
        jet1 = j
        eta1 = j.Eta()
        if abs(eta1) < 2.4:
            centjets.append(jet1)
        else:
            fjets.append(jet1)

    hnumcentjetsbefore.Fill(len(centjets), evtwt)
    if len(centjets) < 3: continue
    ncut += 1
    hCutflow.Fill(ncut, evtwt)
    hnumcentjetsafter.Fill(len(centjets), evtwt)
    # 1 or more forward jets
    hnumfjetsbefore.Fill(len(fjets), evtwt)
    if len(fjets) < 1: continue
    ncut += 1
    hCutflow.Fill(ncut, evtwt)
    hnumfjetsafter.Fill(len(fjets), evtwt)

    if centjets[0].Pt() < centjets[1].Pt(): print 'not ordered properly'

    # leading jet pt > 250
    leadjet = centjets[0]
    leadjetpt = leadjet.Pt()
    leadjeteta = leadjet.Eta()
    hleadjetptbefore.Fill(leadjetpt, evtwt)
    if leadjetpt <= 250: continue
    ncut += 1
    hCutflow.Fill(ncut, evtwt)
    hleadjetptafter.Fill(leadjetpt, evtwt)

    # second leading jet pt > 150
    secondjet = centjets[1]
    secondjetpt = secondjet.Pt()
    secondjeteta = secondjet.Eta()
    hsecjetptbefore.Fill(secondjetpt, evtwt)
    if secondjetpt <= 150: continue
    ncut += 1
    hCutflow.Fill(ncut, evtwt)
    hsecjetptafter.Fill(secondjetpt, evtwt)

    #ST cut
    preST = 0.0
    HT = 0.0
    met_pt = t.MET_pt
    preST = met_pt + lepP4.Pt()
    #print 'preST: ', preST
    for j in centjets:
        HT += j.Pt()
    ST = preST + HT
    if ST < 1000: continue
    ncut += 1
    hCutflow.Fill(ncut, evtwt)
    hSTatdef.Fill(ST, evtwt)

    # Pass 2D Isolation
    dRMin = 999.9
    for j in jetsP4:
        dR = j.DeltaR(lepP4)
        jet_p3 = j.Vect()
        delPtRel = (lep_p3.Cross( jet_p3 )).Mag()/ jet_p3.Mag()
        hDR.Fill(dR, evtwt)
        hDelPtRel.Fill(delPtRel, evtwt)
        h2DdPtReldR.Fill(dR, delPtRel, evtwt)
        if dR < dRMin:
            nearestJetP4 = j
	    nearestJetP3 = jet_p3
            dRMin = dR
            dPtRel = delPtRel
    # Store extra variables
    ptRel = lepP4.Perp(nearestJetP3)
    hDRMin.Fill(dRMin, evtwt)
    hDPtRel.Fill(ptRel, evtwt)
    h2DdPtRelDRMin.Fill(dRMin, ptRel, evtwt)
    Pass2D = ptRel > 25.0 or dRMin > 0.4
    if not Pass2D: continue
    ncut += 1
    hCutflow.Fill(ncut, evtwt)

    h2Daftercut.Fill(dRMin, ptRel, evtwt)
    hpTRelafter.Fill(ptRel, evtwt)
    hdRMinafter.Fill(dRMin, evtwt)

    # At least 1 B jet (using deepcsvm value) 
    ngoodjets = len(jetsP4)
    #print 'ngoodjets: ', ngoodjets
    centBjetsP4 = []
    BjetsP4 = []
    deepcsvm = 0.4941
    nMedBjets = 0
    for j in range(0, ngoodjets):
	tempjet = TLorentzVector(0.0, 0.0, 0.0, 0.0)
	tempjet = jetsP4[j]
	tempjetcsv = goodjetcsv[j]
        if tempjetcsv >= deepcsvm:
            nMedBjets += 1
	    BjetsP4.append(tempjet)
	    jeteta = tempjet.Eta()
	    if abs(jeteta) < 2.4:
	        centBjetsP4.append(tempjet)

    hnumBjetsbefore.Fill(nMedBjets, evtwt)
    if nMedBjets == 0: continue
    ncut += 1
    hCutflow.Fill(ncut, evtwt)
    hnumBjetsafter.Fill(nMedBjets, evtwt)

    # Met > 20 GeV
    met_px = t.MET_px
    met_py = t.MET_py
    met_pz = t.MET_pz

    hMETbefore.Fill(met_pt, evtwt)
    if met_pt < 20: continue
    ncut += 1
    hCutflow.Fill(ncut, evtwt)
    hMETafter.Fill(met_pt, evtwt)

    ak8jet_pt = t.AK8Jets_pt
    ak8jet_eta = t.AK8Jets_eta
    ak8jet_phi = t.AK8Jets_phi
    ak8jet_m = t.AK8Jets_mass
    ak8jet_tau1 = t.AK8Jets_tau1Puppi
    ak8jet_tau2 = t.AK8Jets_tau2Puppi
    ak8jet_sj1pt = t.AK8Jets_sj0pt
    ak8jet_sj1eta = t.AK8Jets_sj0eta
    ak8jet_sj1phi = t.AK8Jets_sj0phi
    ak8jet_sj2pt = t.AK8Jets_sj1pt
    ak8jet_sj2eta = t.AK8Jets_sj1eta
    ak8jet_sj2phi = t.AK8Jets_sj1phi
    ak8jet_sdmass = t.AK8Jets_softDropMassPuppi
    ak8jet_sj1deepcsv = t.AK8Jets_sj0deepcsv
    ak8jet_sj2deepcsv = t.AK8Jets_sj1deepcsv
    nak8jet = len(ak8jet_pt)
    nHiggs = 0
    nhiggsmatched = 0
    sj1P4 = TLorentzVector(0.0, 0.0, 0.0, 0.0)
    sj2P4 = TLorentzVector(0.0, 0.0, 0.0, 0.0)
    numsubBjets = 0

    ak8jetsP4 = []
    higgsjets = []
    higgsSoftDropM = []

    # Higgs Tagging with cuts
    for j in range(0, nak8jet):
	# fill histos with ak8pt and ak8eta
	ak8jetP4 = TLorentzVector(0.0, 0.0, 0.0, 0.0)
        ak8jetP4.SetPtEtaPhiM(ak8jet_pt[j], ak8jet_eta[j], ak8jet_phi[j], ak8jet_m[j])
	hak8JetPt.Fill(ak8jetP4.Pt(), evtwt)
	hak8JetEta.Fill(ak8jetP4.Eta(), evtwt)
	hak8JetTau21.Fill(ak8jet_tau2[j]/ak8jet_tau1[j], evtwt)
	hdRak8JetlepP4.Fill(ak8jetP4.DeltaR(lepP4), evtwt)
	hak8Jetsdmass.Fill(ak8jet_sdmass[j], evtwt)
	if ak8jetP4.Pt() < 300.0: continue
	if abs(ak8jetP4.Eta()) > 2.4: continue
	if (ak8jet_tau2[j]/ak8jet_tau1[j]) > 0.6: continue
	if len(ak8jet_sj1pt) == 0 or len(ak8jet_sj2pt) == 0: continue
	if ak8jetP4.DeltaR(lepP4) <= 1.0: continue
	if ak8jet_sdmass[j] > 160 or ak8jet_sdmass[j] < 90: continue

	if len(ak8jet_sj1deepcsv) <= j or len(ak8jet_sj2deepcsv) <= j: continue
	hak8jetsj1deepcsv.Fill(ak8jet_sj1deepcsv[j], evtwt)
        hak8jetsj2deepcsv.Fill(ak8jet_sj2deepcsv[j], evtwt)

	# b tagging of subjets
	if ak8jet_sj1deepcsv[j] < deepcsvm: numsubBjets += 1
	if ak8jet_sj2deepcsv[j] < deepcsvm: numsubBjets += 1
	#for i in range(0, len(centjets)):
        #    if ak8jetP4.DeltaR(centjets[i]) < 0.4:
        #        nhiggsmatched += 1
	sj1P4.SetPtEtaPhiM(ak8jet_sj1pt[j], ak8jet_sj1eta[j], ak8jet_sj1phi[j], 4.18)
	sj2P4.SetPtEtaPhiM(ak8jet_sj2pt[j], ak8jet_sj2eta[j], ak8jet_sj2phi[j], 4.18) 

	nHiggs += 1

	higgsSoftDropM.append(ak8jet_sdmass[j])
	higgsjets.append(ak8jetP4)
	hhiggssj1deepcsv.Fill(ak8jet_sj1deepcsv[j], evtwt)
	hhiggssj2deepcsv.Fill(ak8jet_sj2deepcsv[j], evtwt)
	hhiggsJetPt.Fill(ak8jet_pt[j], evtwt)
	hhiggsJetEta.Fill(ak8jet_eta[j], evtwt)
	hhiggsTau21.Fill(ak8jet_tau2[j]/ak8jet_tau1[j], evtwt)
	hdRhiggslepP4.Fill(ak8jetP4.DeltaR(lepP4), evtwt)
	hhiggssdmass.Fill(ak8jet_sdmass[j], evtwt)

    hnumhiggsbefore.Fill(nHiggs, evtwt)
    if nHiggs < 1: continue
    #if nhiggsmatched < 1: continue
    ncut += 1
    hCutflow.Fill(ncut, evtwt)
    hnumhiggsafter.Fill(nHiggs, evtwt)

    preST = 0.0
    HT = 0.0
    preST = met_pt + lepP4.Pt()
    #print 'preST: ', preST
    for j in centjets:
        HT += j.Pt()
    ST = preST + HT
    hST.Fill(ST, evtwt)

#------------------------------------------------------------------------
#                          MASS RECONSTRUCTION
#------------------------------------------------------------------------

    # Finding Pz for Neutrino
    nuP4 = TLorentzVector(0.0, 0.0, 0.0, 0.0)
    nuP4.SetPx(met_px)
    nuP4.SetPy(met_py)
    nuP4.SetPz(met_pz)
    sol1 = 0.0; sol2 = 0.0
    isNuPz, sol1, sol2 = SolveNuPz(lepP4, nuP4, 80.4, sol1, sol2)

    if abs(sol1) < abs(sol2):
	nuP4.SetPz(sol1)
    else:
	nuP4.SetPz(sol2)
    nuP4 = AdjustEnergyForMass(nuP4, 0.0)

    # Initialize
    topMass = 174.0; higgsMass = 125.0; chi2_dR_boost1 = 0.0; chi2_dR_boost2 = 0.0; chi2_higgs_boost1 = 0.0; chi2_top_boost1 = 0.0
    chi2_higgs2 = TLorentzVector(0.0, 0.0, 0.0, 0.0)
    chi2_top2 = TLorentzVector(0.0, 0.0, 0.0, 0.0)
    chi2_higgs_boost2 = TLorentzVector(0.0, 0.0, 0.0, 0.0)
    chi2_top_boost2 = TLorentzVector(0.0, 0.0, 0.0, 0.0)
    higgsP4 = TLorentzVector(0.0, 0.0, 0.0, 0.0)
    topP4 = TLorentzVector(0.0, 0.0, 0.0, 0.0)
    chi2 = 100000.0

    Bjetschi2_dR_boost1 = 0.0; Bjetschi2_dR_boost2 = 0.0; Bjetschi2_higgs_boost1 = 0.0; Bjetschi2_top_boost1 = 0.0
    Bjetschi2_higgs_boost2 = TLorentzVector(0.0, 0.0, 0.0, 0.0)
    Bjetschi2_top_boost2 = TLorentzVector(0.0, 0.0, 0.0, 0.0)
    BjetshiggsP4 = TLorentzVector(0.0, 0.0, 0.0, 0.0)
    BjetstopP4 = TLorentzVector(0.0, 0.0, 0.0, 0.0)
    Bjetschi2 = 100000.0

    WP4 = TLorentzVector(0.0, 0.0, 0.0, 0.0)
    WP4 = lepP4 + nuP4

    nonhiggscentBjetsP4 = []
    for j in centBjetsP4:
	if j.DeltaR(sj1P4) > 0.2 and j.DeltaR(sj2P4) > 0.2:
	    nonhiggscentBjetsP4.append(j)

    chi2, higgsP4, topP4, tophiggsdR = DoMassRecoBoost(jetsP4, higgsjets, higgsSoftDropM, lepP4, nuP4, higgsMass, topMass, chi2_dR_boost1, chi2_dR_boost2, chi2_higgs_boost1, chi2_higgs_boost2, chi2_top_boost1, chi2_top_boost2)

    # Tprime Reconstruction
    tprimeP4 = TLorentzVector(0.0, 0.0, 0.0, 0.0)
    tprimeP4 = topP4 + higgsP4

    hdRtophiggsbefore.Fill(tophiggsdR, evtwt)

    # Filling Histos
    if chi2 != 100000.0:
        if tophiggsdR > 2.0:
	    ncut += 1
            hCutflow.Fill(ncut, evtwt)
	    if nMedBjets == 0:
		h0bjetshiggsmass.Fill(higgsP4.M(), evtwt)
		h0bjetstopmass.Fill(topP4.M(), evtwt)
		h0bjetstprimemass.Fill(tprimeP4.M(), evtwt)
		h0bjetsdRtophiggs.Fill(tophiggsdR, evtwt)
		h0bjetschi2.Fill(chi2, evtwt)
	    if nMedBjets == 1:
		h1bjetshiggsmass.Fill(higgsP4.M(), evtwt)
                h1bjetstopmass.Fill(topP4.M(), evtwt)
                h1bjetstprimemass.Fill(tprimeP4.M(), evtwt)
                h1bjetsdRtophiggs.Fill(tophiggsdR, evtwt)
                h1bjetschi2.Fill(chi2, evtwt)
	    if nMedBjets >= 2:
		h2bjetshiggsmass.Fill(higgsP4.M(), evtwt)
                h2bjetstopmass.Fill(topP4.M(), evtwt)
                h2bjetstprimemass.Fill(tprimeP4.M(), evtwt)
                h2bjetsdRtophiggs.Fill(tophiggsdR, evtwt)
                h2bjetschi2.Fill(chi2, evtwt)
	    hhiggsmass.Fill(higgsP4.M(), evtwt)
            htopmass.Fill(topP4.M(), evtwt)
	    hWmass.Fill(WP4.M(), evtwt)
            htprimemass.Fill(tprimeP4.M(), evtwt) 
	    hhiggspt.Fill(higgsP4.Pt(), evtwt)
	    hhiggseta.Fill(higgsP4.Eta(), evtwt)
	    htoppt.Fill(topP4.Pt(), evtwt)
	    htopeta.Fill(topP4.Eta(), evtwt)
	    htprimept.Fill(tprimeP4.Pt(), evtwt)
	    htprimeeta.Fill(tprimeP4.Eta(), evtwt)
	    hchi2.Fill(chi2,evtwt)
	    hdRtophiggsafter.Fill(tophiggsdR, evtwt)
	    hlepPt.Fill(lepP4.Pt(), evtwt)
            hlepEta.Fill(lepP4.Eta(), evtwt)
	    if len(elelepcand) > 0:
        	hlepIso_sig.Fill(ele_iso[0], evtwt)
    	    else:
        	hlepIso_sig.Fill(mu_iso[0], evtwt)
	    hLeadingJetPt.Fill(leadjetpt, evtwt)
    	    hLeadingJetEta.Fill(leadjeteta, evtwt)
    	    hSecJetPt.Fill(secondjetpt, evtwt)
    	    hSecJetEta.Fill(secondjeteta, evtwt)
	    for i in range(0, len(jetsP4)):
	        hak4jetsPtafter.Fill(jetsP4[i].Pt(), evtwt)
	        hak4jetsEtaafter.Fill(jetsP4[i].Eta(), evtwt)
	    hnumak4jets.Fill(len(jetsP4), evtwt)
	    for i in range(0, len(higgsjets)):
		hak8jetsPtafter.Fill(higgsjets[i].Pt(), evtwt)
		hak8jetsEtaafter.Fill(higgsjets[i].Eta(), evtwt)
	    hnumak8jets.Fill(len(higgsjets), evtwt)
	    for i in range(0, len(fjets)):
		hFwrdJetPt.Fill(fjets[i].Pt(), evtwt)
		hFwrdJetEta.Fill(fjets[i].Eta(), evtwt)
	    hMET.Fill(met_pt, evtwt)
	    hNForwardJets.Fill(len(fjets), evtwt)
    	    hNCentJets.Fill(len(centjets), evtwt)
	    hNumBJets.Fill(len(centBjetsP4), evtwt)
	    h2DdPtRelDRMinafter.Fill(dRMin, ptRel, evtwt)
	    for i in range(0, len(centjets)):
		hCentJetPt.Fill(centjets[i].Pt(), evtwt)
		hCentJetEta.Fill(centjets[i].Eta(), evtwt)
	    hdRleadjetMET.Fill(centjets[0].DeltaR(nuP4), evtwt)
	    hpTRelafterall.Fill(ptRel, evtwt)
	    hdRMinafterall.Fill(dRMin, evtwt)
	    hST.Fill(ST, evtwt)
	    if nMedium > 0: # electron channel
		helechanhiggsmass.Fill(higgsP4.M(), evtwt)
                helechantopmass.Fill(topP4.M(), evtwt)
                helechanWmass.Fill(WP4.M(), evtwt)
                helechantprimemass.Fill(tprimeP4.M(), evtwt)
                helechanhiggspt.Fill(higgsP4.Pt(), evtwt)
                helechanhiggseta.Fill(higgsP4.Eta(), evtwt)
                helechantoppt.Fill(topP4.Pt(), evtwt)
                helechantopeta.Fill(topP4.Eta(), evtwt)
                helechantprimept.Fill(tprimeP4.Pt(), evtwt)
                helechantprimeeta.Fill(tprimeP4.Eta(), evtwt)
                helechanchi2.Fill(chi2,evtwt)
                helechandRtophiggsafter.Fill(tophiggsdR, evtwt)
                helechanlepPt.Fill(lepP4.Pt(), evtwt)
                helechanlepEta.Fill(lepP4.Eta(), evtwt)
		helechanLeadingJetPt.Fill(leadjetpt, evtwt)
                helechanLeadingJetEta.Fill(leadjeteta, evtwt)
                helechanSecJetPt.Fill(secondjetpt, evtwt)
                helechanSecJetEta.Fill(secondjeteta, evtwt)
                for i in range(0, len(jetsP4)):
                    helechanak4jetsPtafter.Fill(jetsP4[i].Pt(), evtwt)
                    helechanak4jetsEtaafter.Fill(jetsP4[i].Eta(), evtwt)
                helechannumak4jets.Fill(len(jetsP4), evtwt)
                for i in range(0, len(higgsjets)):
                    helechanak8jetsPtafter.Fill(higgsjets[i].Pt(), evtwt)
                    helechanak8jetsEtaafter.Fill(higgsjets[i].Eta(), evtwt)
                helechannumak8jets.Fill(len(higgsjets), evtwt)
                for i in range(0, len(fjets)):
                    helechanFwrdJetPt.Fill(fjets[i].Pt(), evtwt)
                    helechanFwrdJetEta.Fill(fjets[i].Eta(), evtwt)
                helechanMET.Fill(met_pt, evtwt)
                helechanNForwardJets.Fill(len(fjets), evtwt)
                helechanNCentJets.Fill(len(centjets), evtwt)
                helechanNumBJets.Fill(len(centBjetsP4), evtwt)
                helechan2DdPtRelDRMinafter.Fill(dRMin, ptRel, evtwt)
		for i in range(0, len(centjets)):
                    helechanCentJetPt.Fill(centjets[i].Pt(), evtwt)
                    helechanCentJetEta.Fill(centjets[i].Eta(), evtwt)
		helechandRleadjetMET.Fill(centjets[0].DeltaR(nuP4), evtwt)
		helechanpTRelafter.Fill(ptRel, evtwt)
                helechandRMinafter.Fill(dRMin, evtwt)
	    elif nmuMedium > 0: # muon channel
		hmuchanhiggsmass.Fill(higgsP4.M(), evtwt)
                hmuchantopmass.Fill(topP4.M(), evtwt)
                hmuchanWmass.Fill(WP4.M(), evtwt)
                hmuchantprimemass.Fill(tprimeP4.M(), evtwt)
                hmuchanhiggspt.Fill(higgsP4.Pt(), evtwt)
                hmuchanhiggseta.Fill(higgsP4.Eta(), evtwt)
                hmuchantoppt.Fill(topP4.Pt(), evtwt)
                hmuchantopeta.Fill(topP4.Eta(), evtwt)
                hmuchantprimept.Fill(tprimeP4.Pt(), evtwt)
                hmuchantprimeeta.Fill(tprimeP4.Eta(), evtwt)
                hmuchanchi2.Fill(chi2,evtwt)
                hmuchandRtophiggsafter.Fill(tophiggsdR, evtwt)
                hmuchanlepPt.Fill(lepP4.Pt(), evtwt)
                hmuchanlepEta.Fill(lepP4.Eta(), evtwt)
                hmuchanLeadingJetPt.Fill(leadjetpt, evtwt)
                hmuchanLeadingJetEta.Fill(leadjeteta, evtwt)
                hmuchanSecJetPt.Fill(secondjetpt, evtwt)
                hmuchanSecJetEta.Fill(secondjeteta, evtwt)
                for i in range(0, len(jetsP4)):
                    hmuchanak4jetsPtafter.Fill(jetsP4[i].Pt(), evtwt)
                    hmuchanak4jetsEtaafter.Fill(jetsP4[i].Eta(), evtwt)
                hmuchannumak4jets.Fill(len(jetsP4), evtwt)
                for i in range(0, len(higgsjets)):
                    hmuchanak8jetsPtafter.Fill(higgsjets[i].Pt(), evtwt)
                    hmuchanak8jetsEtaafter.Fill(higgsjets[i].Eta(), evtwt)
                hmuchannumak8jets.Fill(len(higgsjets), evtwt)
                for i in range(0, len(fjets)):
                    hmuchanFwrdJetPt.Fill(fjets[i].Pt(), evtwt)
                    hmuchanFwrdJetEta.Fill(fjets[i].Eta(), evtwt)
                hmuchanMET.Fill(met_pt, evtwt)
                hmuchanNForwardJets.Fill(len(fjets), evtwt)
                hmuchanNCentJets.Fill(len(centjets), evtwt)
                hmuchanNumBJets.Fill(len(centBjetsP4), evtwt)
                hmuchan2DdPtRelDRMinafter.Fill(dRMin, ptRel, evtwt)
		for i in range(0, len(centjets)):
                    hmuchanCentJetPt.Fill(centjets[i].Pt(), evtwt)
                    hmuchanCentJetEta.Fill(centjets[i].Eta(), evtwt)
		hmuchandRleadjetMET.Fill(centjets[0].DeltaR(nuP4), evtwt)
		hmuchanpTRelafter.Fill(ptRel, evtwt)
                hmuchandRMinafter.Fill(dRMin, evtwt)

    del jetsP4[:]
    del fjets[:]
    del centjets[:]
    del ak8jetsP4[:]
    del higgsjets[:]
    del higgsSoftDropM[:]
    del BjetsP4[:]
    del centBjetsP4[:]
    del nonhiggscentBjetsP4[:]
    #print ievt

fout.Write()
fout.Close()
