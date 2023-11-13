import clr, sys, os

import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()

SystemLibrary = oDesktop.GetSysLibDirectory()
path = os.path.join(SystemLibrary, "Toolkits\\Icepak\\Lib\\")

if os.path.exists(path) == False:
        path = path.replace("\\","/")
        path = path.replace("//","/")

sys.path.append(str(path))
clr.AddReferenceToFileAndPath("Monitor_Based_Convergence_Control.dll")
import Monitor_Based_Convergence_Control

#script_arg = ScriptArgument
#SolutionSetupWizard.Main(script_arg)