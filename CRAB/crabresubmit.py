import os

PPNdir = os.environ['CMSSW_BASE']+'/src/Upgrades/VLQAnalyzer/CRAB/background/'

subdirs = [x[0] for x in os.walk(PPNdir)]
for dirs in subdirs:
    print dirs
    os.chdir(dirs)
    print os.getcwd()
    os.system('crab resubmit --dir $PWD --maxmemory 4000')
    os.chdir(PPNdir)
