# !/usr/bin/env python
# -*- coding: utf-8 -*-
#--------------------------------------------------------------------------------------------------
# Name          : New Project Setup.py
# Author  	: Mark Pooley (mark-pooley@uiowa.edu)
# Github        : http://github.com/markpooley
# Link    	: http://www.ppc.uiowa.edu
# Date    	: 2015-02-04 09:25:08
# Version	: 1.0
# Description	: Script that creates three file geodatabases for a New Project that is named by
# the user. A GDB with the Project name is created, as well as an output and scratch GDB.
# Additionally, folders for outputs and MXDs are created. A scritps folder is created and a script
# for backing up work is written to this folder with the source and back up directory defined. The
# backup script can be run manually or set to run in a task scheduler.If needed a table GDB is also
# created.
#-------------------------------------------------------------------------------------------------


####################################################################################################
#import necessary modules
####################################################################################################
import arcpy
import shutil
import os

####################################################################################################
#user input variables
####################################################################################################
OutputLocation = arcpy.GetParameterAsText(0) #user specificed location of project
BackupLocation = arcpy.GetParameterAsText(1) #boolean table for script folder
ProjectName = arcpy.GetParameterAsText(2) #user specified project name
Table = arcpy.GetParameterAsText(3) #Boolean variables for table gdb

####################################################################################################
#removing spaces from the user project name so a GDB can be created
####################################################################################################
GDBName = ProjectName.replace(" ","")

####################################################################################################
#create folder names and subfolder for the project
####################################################################################################
ProjectLocation = arcpy.CreateFolder_management(OutputLocation,ProjectName)
subfolder = str(ProjectLocation) + "\\Output Files"

####################################################################################################
#create the three file geodabases
####################################################################################################
arcpy.CreateFileGDB_management(ProjectLocation,GDBName,"CURRENT")
arcpy.CreateFileGDB_management(ProjectLocation,"Output","CURRENT")
arcpy.CreateFileGDB_management(ProjectLocation,"Scratch","CURRENT")

####################################################################################################
#create folder for MXDs and maps created during the project
####################################################################################################
arcpy.CreateFolder_management(ProjectLocation,"MXDs")
arcpy.CreateFolder_management(ProjectLocation,"Output Files")

####################################################################################################
#creat subfolders within the output folder for exported maps and tables
####################################################################################################
arcpy.CreateFolder_management(subfolder,"Maps")
arcpy.CreateFolder_management(subfolder,"Tables")
arcpy.CreateFolder_management(ProjectLocation,"Scripts")

scriptsLoc = str(ProjectLocation) + "\Scripts"

####################################################################################################
#check boolean variables and create corresponding GDB or folder if either is True
####################################################################################################
if Table == "true":
	arcpy.CreateFileGDB_management(ProjectLocation,"Tables","CURRENT")


####################################################################################################
#Write the project backup script to the scripts folder and
####################################################################################################
# check variables, they may not be necessary, but help avoid mistakes - they're a failsafe.
src_check = True
back_check = True
cwd = os.getcwd()

#get location of the tool and copy project script file so it can be copied over
loc = os.path.dirname(os.path.realpath(__file__))
copy = loc + '\CopyProject.py' #path and filename of the copy projec script that will be copied

#open the Copy Project file to be read - the template file.
with open(copy, 'r') as src:
	#open the Copy Project that will be written with the new source and back up paths
	with open(scriptsLoc + '\CopyProject.py', 'w') as backup:
		for line in src:
			if 'sourcePath'in line and src_check == True:
				lineIndex = line.index("=")
				line = line[:lineIndex] + ' = r"' + os.path.realpath(str(ProjectLocation)) + '"\n'
				backup.write(line)
				src_check = False
			elif 'destPath' in line and back_check == True:
				lineIndex = line.index("=")
				line = line[:lineIndex] + ' = r"' + os.path.realpath(BackupLocation) + '"\n'
				backup.write(line)
				back_check = False
			else:
				backup.write(line)
src.close()
backup.close()

####################################################################################################
#Major process
####################################################################################################
arcpy.AddMessage('Project Name: {0} has been created in: {1}\n'.format(ProjectName,OutputLocation))
arcpy.AddMessage('Additionally a script called CopyProject.py has been saved to: {0}'.format(scriptsLoc))
arcpy.AddMessage("""You can run this script in python manually to backup your project to your specified
backup location, or it can be added to scheduled tasks and ran at regular times/intervals.\n""")
