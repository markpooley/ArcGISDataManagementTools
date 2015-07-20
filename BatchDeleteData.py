#!/usr/bin/env python
# -*- coding: utf-8 -*-
#--------------------------------------------------------------------------------
# Name        	: Batch Delete Data
# Date        	: 2015-07-20
# Author      	: Mark Pooley (mark-pooley@uiowa.edu)
# Github		: http:www.github.com/MarkPooley
# Link        	: http://www.ppc.uiowa.edu
# Version     	: 1.0
# Description 	: Batch Delete data containing the user specified wildcard.
#--------------------------------------------------------------------------------
#################################################################################
#Import python modules
#################################################################################
import arcpy
from arcpy import env

#################################################################################
#user input variables
#################################################################################
env.workspace = arcpy.GetParameterAsText(0)
wildCard = arcpy.GetParameterAsText(1)
env.overWriteOutput = True

arcpy.AddMessage("Features and tables containing {0} will be deleted.".format(wildCard))
#################################################################################
#global functions
#################################################################################
def deleteData(ls):
	if len(ls) > 0:
		arcpy.SetProgressor('step','Deleting data containing {0}'.format(wildCard),0,len(ls),1)
		for d in ls:
			arcpy.SetProgressorLabel('deleting {0}'.format(d))
			arcpy.Delete_management(d)
			arcpy.SetProgressorPosition()

#################################################################################
#Declare Global variables
#################################################################################
tempFeatures = arcpy.ListFeatureClasses(wildCard) #list of features containing wild card
tempTables = arcpy.ListTables(wildCard, "All") # list of tables containing wild card

arcpy.AddMessage("{0} data files found containing {1}".format(len(tempTables) + len(tempFeatures),wildCard))
#################################################################################
#Run deleteData function on both lists
#################################################################################
arcpy.AddMessage("Removing Temporary files...")
deleteData(tempFeatures)
deleteData(tempTables)


arcpy.AddMessage("Process Complete!")