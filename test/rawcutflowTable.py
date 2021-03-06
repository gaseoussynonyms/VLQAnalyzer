import sys
import os
import subprocess
from array import array
from ROOT import TH1D,TH2D,TFile,TMath,TCanvas,THStack,TLegend,TPave,TLine,TLatex,TPaveText
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
gStyle.SetErrorX(0.1000)
gStyle.SetPadTickX(1)
gStyle.SetPadTickY(1)

from optparse import OptionParser
parser = OptionParser()
parser.add_option('--plotDir', metavar='P', type='string', action='store',
                  default='Summer2018Plots',
                  dest='plotDir',
                  help='output directory of plots')
(options,args) = parser.parse_args()

outDir = options.plotDir

execfile("input.py")

c1 = TCanvas('c1', 'c1', 1800, 1000)
pt1 = TPaveText(.05,.05,.12,.95)
pt2 = TPaveText(0.12, 0.05, 0.19, 0.95)
pt3 = TPaveText(0.19, 0.05, 0.26, 0.95)
pt4 = TPaveText(0.26, 0.05, 0.33, 0.95)
pt5 = TPaveText(0.33, 0.05, 0.40, 0.95)
pt6 = TPaveText(0.40, 0.05, 0.47, 0.95)
pt7 = TPaveText(0.47, 0.05, 0.53, 0.95)
pt8 = TPaveText(0.53, 0.05, 0.60, 0.95)
pt9 = TPaveText(0.60, 0.05, 0.67, 0.95)
pt10 = TPaveText(0.67, 0.05, 0.74, 0.95)
pt11 = TPaveText(0.74, 0.05, 0.81, 0.95)
pt12 = TPaveText(0.81, 0.05, 0.88, 0.95)
pt13 = TPaveText(0.88, 0.05, 0.95, 0.95)

pt1.AddText("Sample")
pt1.AddLine(0.0, 0.1, 1.0, 0.1)
pt1.AddText("DYToLL")
pt1.AddLine(0.0, 0.2, 1.00, .200)
pt1.AddText("SingleT")
pt1.AddLine(0.0, .3, 1.00, .300)
pt1.AddText("TTbar")
pt1.AddLine(0.0, .4, 1.00, .400)
pt1.AddText("WJets")
pt1.AddLine(0.0, .5, 1.00, .5)
pt1.AddText("T_M1000_W10")
pt1.AddLine(0.0, .6, 1.00, .6)
pt1.AddText("T_M1500_W10")
pt1.AddLine(0.0, .7, 1.00, .7)
pt1.AddText("T_M2000_W10")
pt1.AddLine(0.0, .8, 1.00, .8)
pt1.AddText("T_M2500_W10")
pt1.AddLine(0.0, .9, 1.00, .9)
pt1.AddText("T_M3000_W10")
pt1.Draw()

pt2.AddText("Preselection")
pt2.AddLine(00, .100, 1.00, .100)
pt2.AddText(str(round(DYToLLnums[1],3)))
pt2.AddLine(00, .200, 1.00, .200)
pt2.AddText(str(round(stnums[1],3)))
pt2.AddLine(00, .300, 1.00, .300)
pt2.AddText(str(round(tt_M2T4nums[1],3)))
pt2.AddLine(00, .400, 1.00, .400)
pt2.AddText(str(round(WToLNunums[1],3)))
pt2.AddLine(00, .500, 1.00, .500)
pt2.AddText(str(round(T_M1000_W10nums[1],3)))
pt2.AddLine(00, .600, 1.00, .600)
pt2.AddText(str(round(T_M1500_W10nums[1],3)))
pt2.AddLine(00, .700, 1.00, .700)
pt2.AddText(str(round(T_M2000_W10nums[1],3)))
pt2.AddLine(00, .800, 1.00, .800)
pt2.AddText(str(round(T_M2500_W10nums[1],3)))
pt2.AddLine(00, .900, 1.00, .900)
pt2.AddText(str(round(T_M3000_W10nums[1],3)))
pt2.Draw()

pt3.AddText("Exactly 1 Lepton")
pt3.AddLine(00, .100, 1.00, .100)
pt3.AddText(str(round(DYToLLnums[2],3)))
pt3.AddLine(00, .200, 1.00, .200)
pt3.AddText(str(round(stnums[2],3)))
pt3.AddLine(00, .300, 1.00, .300)
pt3.AddText(str(round(tt_M2T4nums[2],3)))
pt3.AddLine(00, .400, 1.00, .400)
pt3.AddText(str(round(WToLNunums[2],3)))
pt3.AddLine(00, .500, 1.00, .500)
pt3.AddText(str(round(T_M1000_W10nums[2],3)))
pt3.AddLine(00, .600, 1.00, .600)
pt3.AddText(str(round(T_M1500_W10nums[2],3)))
pt3.AddLine(00, .700, 1.00, .700)
pt3.AddText(str(round(T_M2000_W10nums[2],3)))
pt3.AddLine(00, .800, 1.00, .800)
pt3.AddText(str(round(T_M2500_W10nums[2],3)))
pt3.AddLine(00, .900, 1.00, .900)
pt3.AddText(str(round(T_M3000_W10nums[2],3)))
pt3.Draw()

pt4.AddText("3 or More Central Jets")
pt4.AddLine(00, .100, 1.00, .100)
pt4.AddText(str(round(DYToLLnums[3],3)))
pt4.AddLine(00, .200, 1.00, .200)
pt4.AddText(str(round(stnums[3],3)))
pt4.AddLine(00, .300, 1.00, .300)
pt4.AddText(str(round(tt_M2T4nums[3],3)))
pt4.AddLine(00, .400, 1.00, .400)
pt4.AddText(str(round(WToLNunums[3],3)))
pt4.AddLine(00, .500, 1.00, .500)
pt4.AddText(str(round(T_M1000_W10nums[3],3)))
pt4.AddLine(00, .600, 1.00, .600)
pt4.AddText(str(round(T_M1500_W10nums[3],3)))
pt4.AddLine(00, .700, 1.00, .700)
pt4.AddText(str(round(T_M2000_W10nums[3],3)))
pt4.AddLine(00, .800, 1.00, .800)
pt4.AddText(str(round(T_M2500_W10nums[3],3)))
pt4.AddLine(00, .900, 1.00, .900)
pt4.AddText(str(round(T_M3000_W10nums[3],3)))
pt4.Draw()

pt5.AddText("1 or More Forward Jets")
pt5.AddLine(00, .100, 1.00, .100)
pt5.AddText(str(round(DYToLLnums[4],3)))
pt5.AddLine(00, .200, 1.00, .200)
pt5.AddText(str(round(stnums[4],3)))
pt5.AddLine(00, .300, 1.00, .300)
pt5.AddText(str(round(tt_M2T4nums[4],3)))
pt5.AddLine(00, .400, 1.00, .400)
pt5.AddText(str(round(WToLNunums[4],3)))
pt5.AddLine(00, .500, 1.00, .500)
pt5.AddText(str(round(T_M1000_W10nums[4],3)))
pt5.AddLine(00, .600, 1.00, .600)
pt5.AddText(str(round(T_M1500_W10nums[4],3)))
pt5.AddLine(00, .700, 1.00, .700)
pt5.AddText(str(round(T_M2000_W10nums[4],3)))
pt5.AddLine(00, .800, 1.00, .800)
pt5.AddText(str(round(T_M2500_W10nums[4],3)))
pt5.AddLine(00, .900, 1.00, .900)
pt5.AddText(str(round(T_M3000_W10nums[4],3)))
pt5.Draw()

pt6.AddText("Leading Jet pt > 250")
pt6.AddLine(00, .100, 1.00, .100)
pt6.AddText(str(round(DYToLLnums[5],3)))
pt6.AddLine(00, .200, 1.00, .200)
pt6.AddText(str(round(stnums[5],3)))
pt6.AddLine(00, .300, 1.00, .300)
pt6.AddText(str(round(tt_M2T4nums[5],3)))
pt6.AddLine(00, .400, 1.00, .400)
pt6.AddText(str(round(WToLNunums[5],3)))
pt6.AddLine(00, .500, 1.00, .500)
pt6.AddText(str(round(T_M1000_W10nums[5],3)))
pt6.AddLine(00, .600, 1.00, .600)
pt6.AddText(str(round(T_M1500_W10nums[5],3)))
pt6.AddLine(00, .700, 1.00, .700)
pt6.AddText(str(round(T_M2000_W10nums[5],3)))
pt6.AddLine(00, .800, 1.00, .800)
pt6.AddText(str(round(T_M2500_W10nums[5],3)))
pt6.AddLine(00, .900, 1.00, .900)
pt6.AddText(str(round(T_M3000_W10nums[5],3)))
pt6.Draw()

pt7.AddText("Second Leading Jet Pt #geq 150 GeV")
pt7.AddLine(00, .100, 1.00, .100)
pt7.AddText(str(round(DYToLLnums[6],3)))
pt7.AddLine(00, .200, 1.00, .200)
pt7.AddText(str(round(stnums[6],3)))
pt7.AddLine(00, .300, 1.00, .300)
pt7.AddText(str(round(tt_M2T4nums[6],3)))
pt7.AddLine(00, .400, 1.00, .400)
pt7.AddText(str(round(WToLNunums[6],3)))
pt7.AddLine(00, .500, 1.00, .500)
pt7.AddText(str(round(T_M1000_W10nums[6],3)))
pt7.AddLine(00, .600, 1.00, .600)
pt7.AddText(str(round(T_M1500_W10nums[6],3)))
pt7.AddLine(00, .700, 1.00, .700)
pt7.AddText(str(round(T_M2000_W10nums[6],3)))
pt7.AddLine(00, .800, 1.00, .800)
pt7.AddText(str(round(T_M2500_W10nums[6],3)))
pt7.AddLine(00, .900, 1.00, .900)
pt7.AddText(str(round(T_M3000_W10nums[6],3)))
pt7.Draw()

pt8.AddText("ST > 1000")
pt8.AddLine(00, .100, 1.00, .100)
pt8.AddText(str(round(DYToLLnums[7],3)))
pt8.AddLine(00, .200, 1.00, .200)
pt8.AddText(str(round(stnums[7],3)))
pt8.AddLine(00, .300, 1.00, .300)
pt8.AddText(str(round(tt_M2T4nums[7],3)))
pt8.AddLine(00, .400, 1.00, .400)
pt8.AddText(str(round(WToLNunums[7],3)))
pt8.AddLine(00, .500, 1.00, .500)
pt8.AddText(str(round(T_M1000_W10nums[7],3)))
pt8.AddLine(00, .600, 1.00, .600)
pt8.AddText(str(round(T_M1500_W10nums[7],3)))
pt8.AddLine(00, .700, 1.00, .700)
pt8.AddText(str(round(T_M2000_W10nums[7],3)))
pt8.AddLine(00, .800, 1.00, .800)
pt8.AddText(str(round(T_M2500_W10nums[7],3)))
pt8.AddLine(00, .900, 1.00, .900)
pt8.AddText(str(round(T_M3000_W10nums[7],3)))
pt8.Draw()

pt9.AddText("2D lep iso")
pt9.AddLine(00, .100, 1.00, .100)
pt9.AddText(str(round(DYToLLnums[8],3)))
pt9.AddLine(00, .200, 1.00, .200)
pt9.AddText(str(round(stnums[8],3)))
pt9.AddLine(00, .300, 1.00, .300)
pt9.AddText(str(round(tt_M2T4nums[8],3)))
pt9.AddLine(00, .400, 1.00, .400)
pt9.AddText(str(round(WToLNunums[8],3)))
pt9.AddLine(00, .500, 1.00, .500)
pt9.AddText(str(round(T_M1000_W10nums[8],3)))
pt9.AddLine(00, .600, 1.00, .600)
pt9.AddText(str(round(T_M1500_W10nums[8],3)))
pt9.AddLine(00, .700, 1.00, .700)
pt9.AddText(str(round(T_M2000_W10nums[8],3)))
pt9.AddLine(00, .800, 1.00, .800)
pt9.AddText(str(round(T_M2500_W10nums[8],3)))
pt9.AddLine(00, .900, 1.00, .900)
pt9.AddText(str(round(T_M3000_W10nums[8],3)))
pt9.Draw()

pt10.AddText("1 or More B-Jet")
pt10.AddLine(00, .100, 1.000, .100)
pt10.AddText(str(round(DYToLLnums[9],3)))
pt10.AddLine(00, .200, 1.000, .200)
pt10.AddText(str(round(stnums[9],3)))
pt10.AddLine(00, .300, 1.000, .300)
pt10.AddText(str(round(tt_M2T4nums[9],3)))
pt10.AddLine(00, .400, 1.000, .400)
pt10.AddText(str(round(WToLNunums[9],3)))
pt10.AddLine(00, .500, 1.000, .500)
pt10.AddText(str(round(T_M1000_W10nums[9],3)))
pt10.AddLine(00, .600, 1.000, .600)
pt10.AddText(str(round(T_M1500_W10nums[9],3)))
pt10.AddLine(00, .700, 1.000, .700)
pt10.AddText(str(round(T_M2000_W10nums[9],3)))
pt10.AddLine(00, .800, 1.000, .800)
pt10.AddText(str(round(T_M2500_W10nums[9],3)))
pt10.AddLine(00, .900, 1.000, .900)
pt10.AddText(str(round(T_M3000_W10nums[9],3)))
pt10.Draw()

pt11.AddText("Missing E_{t} #geq 20 GeV")
pt11.AddLine(000, .100, 1.00, .100)
pt11.AddText(str(round(DYToLLnums[10],3)))
pt11.AddLine(000, .200, 1.00, .200)
pt11.AddText(str(round(stnums[10],3)))
pt11.AddLine(000, .300, 1.00, .300)
pt11.AddText(str(round(tt_M2T4nums[10],3)))
pt11.AddLine(000, .400, 1.00, .400)
pt11.AddText(str(round(WToLNunums[10],3)))
pt11.AddLine(000, .500, 1.00, .500)
pt11.AddText(str(round(T_M1000_W10nums[10],3)))
pt11.AddLine(000, .600, 1.00, .600)
pt11.AddText(str(round(T_M1500_W10nums[10],3)))
pt11.AddLine(000, .700, 1.00, .700)
pt11.AddText(str(round(T_M2000_W10nums[10],3)))
pt11.AddLine(000, .800, 1.00, .800)
pt11.AddText(str(round(T_M2500_W10nums[10],3)))
pt11.AddLine(000, .900, 1.00, .900)
pt11.AddText(str(round(T_M3000_W10nums[10],3)))
pt11.Draw()

pt12.AddText("1 or More Higgs")
pt12.AddLine(000, .100, 1.00, .100)
pt12.AddText(str(round(DYToLLnums[11],3)))
pt12.AddLine(000, .200, 1.00, .200)
pt12.AddText(str(round(stnums[11],3)))
pt12.AddLine(000, .300, 1.00, .300)
pt12.AddText(str(round(tt_M2T4nums[11],3)))
pt12.AddLine(000, .400, 1.00, .400)
pt12.AddText(str(round(WToLNunums[11],3)))
pt12.AddLine(000, .500, 1.00, .500)
pt12.AddText(str(round(T_M1000_W10nums[11],3)))
pt12.AddLine(000, .600, 1.00, .600)
pt12.AddText(str(round(T_M1500_W10nums[11],3)))
pt12.AddLine(000, .700, 1.00, .700)
pt12.AddText(str(round(T_M2000_W10nums[11],3)))
pt12.AddLine(000, .800, 1.00, .800)
pt12.AddText(str(round(T_M2500_W10nums[11],3)))
pt12.AddLine(000, .900, 1.00, .900)
pt12.AddText(str(round(T_M3000_W10nums[11],3)))
pt12.Draw()

pt13.AddText("#Delta R(higgs, top) > 2")
pt13.AddLine(000, .100, 1.00, .100)
pt13.AddText(str(round(DYToLLnums[12],3)))
pt13.AddLine(000, .200, 1.00, .200)
pt13.AddText(str(round(stnums[12],3)))
pt13.AddLine(000, .300, 1.00, .300)
pt13.AddText(str(round(tt_M2T4nums[12],3)))
pt13.AddLine(000, .400, 1.00, .400)
pt13.AddText(str(round(WToLNunums[12],3)))
pt13.AddLine(000, .500, 1.00, .500)
pt13.AddText(str(round(T_M1000_W10nums[12],3)))
pt13.AddLine(000, .600, 1.00, .600)
pt13.AddText(str(round(T_M1500_W10nums[12],3)))
pt13.AddLine(000, .700, 1.00, .700)
pt13.AddText(str(round(T_M2000_W10nums[12],3)))
pt13.AddLine(000, .800, 1.00, .800)
pt13.AddText(str(round(T_M2500_W10nums[12],3)))
pt13.AddLine(000, .900, 1.00, .900)
pt13.AddText(str(round(T_M3000_W10nums[12],3)))
pt13.Draw()

c1.SaveAs(outDir+"/"+"rawcutflowTable.png")
c1.SaveAs(outDir+"/"+"rawcutflowTable.pdf")
raw_input("hold on")
