# monitor convergence criteria inputs

criteria = 0.01
iterations = 50

# general methods

import ScriptEnv
import os
import sys
import shutil

ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()
oModule = oDesign.GetModule("AnalysisSetup")

prj_name = oProject.GetName()
des_name = oDesign.GetName()
path = oProject.GetPath()

try:
    setup_name = str(oDesign.GetChildObject('Analysis').GetChildNames()[0])
except:
    oDesktop.AddMessage(prj_name, des_name, 2, "please add an analysis setup")
    sys.exit(1)

try:
    monitors = oDesign.GetChildObject('Monitor').GetChildNames()
    num = len(monitors)
except:
    oDesktop.AddMessage(prj_name, des_name, 2, "please add at least one monitor")
    sys.exit(1)

solver_files_path = os.path.join(path + prj_name + ".aedtexport/" + des_name + "/" + setup_name + "/SolverFiles/")

# export solver input files

oDesign.WriteSolverFiles(setup_name)

# edit solver journal file to include convergence criteria on all monitors
     
init = open(solver_files_path + "/" + setup_name + ".uns_in", 'r')
temp = open(solver_files_path + "/" + setup_name + ".tmp", 'w')
    
for line in init:
    if line.find('(set-mon-f 1)') == -1:
        temp.write(line)
    else:      
        temp.write(line)
        for i in range(num):
            n = i + 1 
            mon_conv = "/solve/convergence-conditions/conv-reports/add/report-" + str(n) + " report monitor-" + str(n) + " stop " + str(criteria) + " previous " + str(iterations) + " active yes print yes"
            temp.write(mon_conv + "\n")
            temp.write("q\n")
            temp.write("q\n")
            temp.write("q\n")
            temp.write("q\n")
        
init.close()
temp.close()

os.remove(solver_files_path + "/" + setup_name + ".uns_in")
os.rename(solver_files_path + "/" + setup_name + ".tmp", solver_files_path + "/" + setup_name + ".uns_in")

# import solver input files with modified journal and run the simulation   
    
oDesign.ImportSolverFiles(setup_name, solver_files_path)

# cleanup

shutil.rmtree(path + prj_name + ".aedtexport")