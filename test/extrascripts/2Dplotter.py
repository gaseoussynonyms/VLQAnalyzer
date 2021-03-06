import sys
import os
import subprocess
from array import array
from ROOT import TH1D,TH2D,TFile,TMath,TCanvas,THStack,TLegend,TPave,TLine,TLatex
from ROOT import gROOT,gStyle,gPad,gStyle
from ROOT import Double,kBlue,kRed,kOrange,kMagenta,kYellow,kCyan,kGreen,kGray,kBlack,kTRUE

gROOT.Macro("~/rootlogon.C")
gStyle.SetOptStat(0)
#gROOT.SetBatch()
gROOT.SetStyle("Plain")
gStyle.SetOptStat()
gStyle.SetOptTitle(0)
gStyle.SetPalette(1)
gStyle.SetNdivisions(405,"x");
gStyle.SetEndErrorSize(0.)
gStyle.SetErrorX(0.001)
gStyle.SetPadTickX(1)
gStyle.SetPadTickY(1)

# options

from optparse import OptionParser
parser = OptionParser()
parser.add_option('--var', metavar='T', type='string', action='store',
                  default='hEff',
                  dest='var',
                  help='variable to plot')
parser.add_option('--Lumi', metavar='D', type='float', action='store',
                  default= 3000000.,#2300., 
                  dest='Lumi',
                  help='Data Luminosity in pb-1')
parser.add_option('--plotDir', metavar='P', type='string', action='store',
                  default='Summer2018Plots',
                  dest='plotDir',
                  help='output directory of plots')
parser.add_option('--rebin', metavar='T', type='int', action='store',
                  default='1',
                  dest='rebin',
                  help='rebin the histograms')
parser.add_option('--logScale',action='store',
                  default=0,
                  dest='logScale',
                  help='draw on log scale (1/0)')
parser.add_option('--verbose',action='store_true',
                  default=False,
                  dest='verbose',
                  help='verbose switch')
parser.add_option('--legOnly',action='store_true',
                  default=False,
                  dest='legOnly',
                  help='plot legend only')
(options,args) = parser.parse_args()

var = options.var
rebinS = options.rebin
outDir = options.plotDir
lumi = options.Lumi
drawLog = options.logScale
verbose = options.verbose
legOnly = options.legOnly


# add input

execfile("input.py")

# input labels and legends

stopLabel = 'st_'
stopLeg = 'single t'
WToLNuLabel = 'WToLNu_'
WToLNuLeg = 'W to L Nu'
DYToLLLabel = 'DYToLL_'
DYToLLLeg = 'DY to LL'
topLabel = 'Top_'
topLeg = 'top#bar{t}'

TbjM1W1Label = 'Tbj_M1000_W10_'
TbjM1W1Leg = 'Tbj_M1000_W10 (T#rightarrow tH)'
TbjM1W2Label = 'Tbj_M1000_W20_'
TbjM1W2Leg = 'Tbj_M1000_W20 (T#rightarrow tH)'
TbjM1W3Label = 'Tbj_M1000_W30_'
TbjM1W3Leg = 'Tbj_M1000_W30 (T#rightarrow tH)'
TbjM15W1Label = 'Tbj_M1500_W10_'
TbjM15W1Leg = 'Tbj_M1500_W10 (T#rightarrow tH)'
TbjM15W2Label = 'Tbj_M1500_W20_'
TbjM15W2Leg = 'Tbj_M1500_W20 (T#rightarrow tH)'
TbjM15W3Label = 'Tbj_M1500_W30_'
TbjM15W3Leg = 'Tbj_M1500_W30 (T#rightarrow tH)'
TbjM2W1Label = 'Tbj_M2000_W10_'
TbjM2W1Leg = 'Tbj_M2000_W10 (T#rightarrow tH)'
TbjM2W2Label = 'Tbj_M2000_W20_'
TbjM2W2Leg = 'Tbj_M2000_W20 (T#rightarrow tH)'
TbjM2W3Label = 'Tbj_M2000_W30_'
TbjM2W3Leg = 'Tbj_M2000_W30 (T#rightarrow tH)'
TbjM25W1Label = 'Tbj_M2500_W10_'
TbjM25W1Leg = 'Tbj_M2500_W10 (T#rightarrow tH)'
TbjM25W2Label = 'Tbj_M2500_W20_'
TbjM25W2Leg = 'Tbj_M2500_W20 (T#rightarrow tH)'
TbjM25W3Label = 'Tbj_M12500_W30_'
TbjM25W3Leg = 'Tbj_M2500_W30 (T#rightarrow tH)'
TbjM3W1Label = 'Tbj_M3000_W10_'
TbjM3W1Leg = 'Tbj_M3000_W10 (T#rightarrow tH)'
TbjM3W2Label = 'Tbj_M3000_W20_'
TbjM3W2Leg = 'Tbj_M3000_W20 (T#rightarrow tH)'
TbjM3W3Label = 'Tbj_M3000_W30_'
TbjM3W3Leg = 'Tbj_M3000_W30 (T#rightarrow tH)'


# structures

top = [[f_tt_M2T4, tt_M2T4_xs, tt_M2T4_num, lumi]]

WToLNu = [
	[f_WToLNu_0J, WToLNu_0J_xs, WToLNu_0J_num, lumi],
	[f_WToLNu_1J, WToLNu_1J_xs, WToLNu_1J_num, lumi],
	[f_WToLNu_2J, WToLNu_2J_xs, WToLNu_2J_num, lumi],
	[f_WToLNu_3J, WToLNu_3J_xs, WToLNu_3J_num, lumi],
	 ]

DYToLL = [
	[f_DYToLL_0J, DYToLL_0J_xs, DYToLL_0J_num, lumi],
	[f_DYToLL_1J, DYToLL_1J_xs, DYToLL_1J_num, lumi],
	[f_DYToLL_2J, DYToLL_2J_xs, DYToLL_2J_num, lumi],
	[f_DYToLL_3J, DYToLL_3J_xs, DYToLL_3J_num, lumi],
	 ]

st = [
	[f_st_tch_antitop, st_tch_antitop_xs, st_tch_antitop_num, lumi],
	[f_st_tch_top, st_tch_top_xs, st_tch_top_num, lumi],
	[f_st_tW_DR_antitop, st_tW_DR_antitop_xs, st_tW_DR_antitop_num, lumi],
	[f_st_tW_DR_top, st_tW_DR_top_xs, st_tW_DR_top_num, lumi],
     ]

TbjM1000W10 = [[f_Tbj_M1000_W10, Tbj_M1000_W10_xs, Tbj_M1000_W10_num, lumi]]
TbjM1000W20 = [[f_Tbj_M1000_W20, Tbj_M1000_W20_xs, Tbj_M1000_W20_num, lumi]]
TbjM1000W30 = [[f_Tbj_M1000_W30, Tbj_M1000_W30_xs, Tbj_M1000_W30_num, lumi]]
TbjM1500W10 = [[f_Tbj_M1500_W10, Tbj_M1500_W10_xs, Tbj_M1500_W10_num, lumi]]
TbjM1500W20 = [[f_Tbj_M1500_W20, Tbj_M1500_W20_xs, Tbj_M1500_W20_num, lumi]]
TbjM1500W30 = [[f_Tbj_M1500_W30, Tbj_M1500_W30_xs, Tbj_M1500_W30_num, lumi]]
TbjM2000W10 = [[f_Tbj_M2000_W10, Tbj_M2000_W10_xs, Tbj_M2000_W10_num, lumi]]
TbjM2000W20 = [[f_Tbj_M2000_W20, Tbj_M2000_W20_xs, Tbj_M2000_W20_num, lumi]]
TbjM2000W30 = [[f_Tbj_M2000_W30, Tbj_M2000_W30_xs, Tbj_M2000_W30_num, lumi]]
TbjM2500W10 = [[f_Tbj_M2500_W10, Tbj_M2500_W10_xs, Tbj_M2500_W10_num, lumi]]
TbjM2500W20 = [[f_Tbj_M2500_W20, Tbj_M2500_W20_xs, Tbj_M2500_W20_num, lumi]]
TbjM2500W30 = [[f_Tbj_M2500_W30, Tbj_M2500_W30_xs, Tbj_M2500_W30_num, lumi]]
TbjM3000W10 = [[f_Tbj_M3000_W10, Tbj_M3000_W10_xs, Tbj_M3000_W10_num, lumi]]
TbjM3000W20 = [[f_Tbj_M3000_W20, Tbj_M3000_W20_xs, Tbj_M3000_W20_num, lumi]]
TbjM3000W30 = [[f_Tbj_M3000_W30, Tbj_M3000_W30_xs, Tbj_M3000_W30_num, lumi]]

# create histograms

h_top = getHisto(topLabel, topLeg, var, top, kBlue-9, verbose)
#h_st = getHisto(stopLabel, stopLeg, var, st, kOrange-4, verbose)
#h_WToLNu = getHisto(WToLNuLabel, WToLNuLeg, var, WToLNu, kYellow-7, verbose)
#h_DYToLL = getHisto(DYToLLLabel, DYToLLLeg, var, DYToLL, kRed-7, verbose)
#h_TbjM1W1 = getHisto(TbjM1W1Label, TbjM1W1Leg, var, TbjM1000W10, kMagenta, verbose)
#h_TbjM1W2 = getHisto(TbjM1W2Label, TbjM1W2Leg, var, TbjM1000W20, kYellow+5, verbose)
#h_TbjM1W3 = getHisto(TbjM1W3Label, TbjM1W3Leg, var, TbjM1000W30, kYellow-9, verbose)
#h_TbjM15W1 = getHisto(TbjM15W1Label, TbjM15W1Leg, var, TbjM1500W10, kMagenta+3, verbose)
#h_TbjM15W2 = getHisto(TbjM15W2Label, TbjM15W2Leg, var, TbjM1500W20, kYellow+9, verbose)
#h_TbjM15W3 = getHisto(TbjM15W3Label, TbjM15W3Leg, var, TbjM1500W30, kYellow+9, verbose)
h_TbjM2W1 = getHisto(TbjM2W1Label, TbjM2W1Leg, var, TbjM2000W10, kGreen, verbose)
#h_TbjM2W2 = getHisto(TbjM2W2Label, TbjM2W2Leg, var, TbjM2000W20, kYellow+5, verbose)
#h_TbjM2W3 = getHisto(TbjM2W3Label, TbjM2W3Leg, var, TbjM2000W30, kYellow+5, verbose)
#h_TbjM25W1 = getHisto(TbjM25W1Label, TbjM25W1Leg, var, TbjM2500W10, kCyan, verbose)
#h_TbjM25W2 = getHisto(TbjM25W2Label, TbjM25W2Leg, var, TbjM2500W20, kYellow+7, verbose)
#h_TbjM25W3 = getHisto(TbjM25W3Label, TbjM25W3Leg, var, TbjM2500W30, kYellow-7, verbose)
#h_TbjM3W1 = getHisto(TbjM3W1Label, TbjM3W1Leg, var, TbjM3000W10, kBlack, verbose)
#h_TbjM3W2 = getHisto(TbjM3W2Label, TbjM3W2Leg, var, TbjM3000W20, kYellow-4, verbose)
#h_TbjM3W3 = getHisto(TbjM3W3Label, TbjM3W3Leg, var, TbjM3000W30, kYellow-8, verbose)


c1 = TCanvas('c1', 'c1', 800, 600)


# histo properties

#else: hs.SetMinimum(100000)

if drawLog == '1':
    gPad.SetLogy()

h_TbjM2W1.Draw()

xTitle = h_top.GetXaxis().GetTitle()
yTitle = h_top.GetYaxis().GetTitle()

if var == 'hCutflow':
    hs.SetMinimum(100000)
    #hs.GetXaxis().SetRangeUser(1,11)
if var == 'hmuchanak4jetsPtafter' or var == 'helechanak4jetsPtafter' or var == 'hak4jetsPtafter':
    hs.GetXaxis().SetRangeUser(0,1000)
if var == 'hFwrdJetPt' or var == 'hmuchanFwrdJetPt' or var == 'helechanFwrdJetPt':
    hs.GetXaxis().SetRangeUser(0,250)
if var == 'hhiggssdmass':
    hs.GetXaxis().SetRangeUser(0,250)
if var == "hNForwardJets":
    hs.GetXaxis().SetRangeUser(0,20)

gPad.RedrawAxis()

ll = TLatex()
ll.SetNDC(kTRUE)
ll.SetTextSize(0.05)
ll.DrawLatex(0.5, 0.92, "3000 fb^{-1} (14 TeV)");

prel = TLatex()
prel.SetNDC(kTRUE)
prel.SetTextFont(52)
prel.SetTextFont(52)
prel.SetTextSize(0.05)
prel.DrawLatex(0.28, 0.92, "Simulation")

cms = TLatex()
cms.SetNDC(kTRUE)
cms.SetTextFont(61)
cms.SetTextFont(61)
cms.SetTextSize(0.05)
cms.DrawLatex(0.20, 0.92, "CMS")

c1.SaveAs(outDir+"/"+var+".png")
c1.SaveAs(outDir+"/"+var+".pdf")
