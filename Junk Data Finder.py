#!/usr/bin/env python
# -*- coding: utf-8 -*-
#--------------------------------------------------------------------------------
# Name        	: Junk Data Finder
# Date        	: 2015-07-17
# Author      	: Mark Pooley (mark-pooley@uiowa.edu)
# Github		: http:www.github.com/MarkPooley
# Link        	: http://www.ppc.uiowa.edu
# Version     	: 1.0
# Description 	: Finds potentially unused data in project folders and prints to
# 				to ouput window.
#--------------------------------------------------------------------------------
#################################################################################
#Import python modules
#################################################################################
import arcpy
from arcpy import env
import os

#################################################################################
#user input variables
#################################################################################
projectFolder = arcpy.GetParameterAsText(0)
mxdFolder = arcpy.GetParameterAsText(1)
checkForTables = arcpy.GetParameterAsText(2).capitalize()

arcpy.AddMessage("Check for Tables? {0}".format(checkForTables))

#################################################################################
#Declare Global variables
#################################################################################
mxdList = [] # list to house mxd files
gdbList = [] # list of Geodatabases to search
dataUsedList = [] #data sources used in all the mxd documents found
dataList = [] # List of data in geodatabases
tableList = [] # list of tables found in geodatabases
#################################################################################
#global functions
#################################################################################
def getLayersUsed(mxdFolder):
	for root, dirs, files in os.walk(mxdFolder):
		for f in files:
			if f.endswith('.mxd'):
				#join root and path, add to mxdList
				path = os.path.join(root, f)
				mxdList.append(path)

#find the geodatabases, this should be where data should be located
def getGDBList(projectFolder):
	for root, dirs, files in os.walk(projectFolder):
		for d in dirs:
			if d.endswith('.gdb'):
				#join root and name, add to GDB List
				gdbList.append(os.path.join(root,d))

#get layer names and get data being used in mxd documents
def getLayerNames(mxdList):
	for i in mxdList:
		mxd = arcpy.mapping.MapDocument(i)
		for lyr in arcpy.mapping.ListLayers(mxd):
			try:
				dataUsedList.append(lyr.dataSource)
			except NameError: #if broken layer data source, just pass
				pass

#list data in geodatabases
def getListOfData(gdbList):
	for i in gdbList:
		arcpy.env.workspace = i#define workspace for list arguments to work

		#list tables and feature classes
		tempLs = arcpy.ListFeatureClasses()
		tempTables = arcpy.ListTables()

		#iterate through lists and append to global data lists
		for d in tempLs:
			dataList.append(os.path.join(i,d))#join worskpace with featureclass
		for t in tempTables:
			tableList.append(os.path.join(i,t)) #join workspace with table

#find used data that is potentially unused
def findUnusedData(dataUsed,dataFound):
	for i in dataFound:
		if i not in dataUsed:
			arcpy.AddMessage("{0} may not be used".format(i))

#################################################################################
#Run functions and find potentially unused data
#################################################################################

getLayersUsed(mxdFolder)
getGDBList(projectFolder)
getLayerNames(mxdList)
getListOfData(gdbList)

#compare two lists and output to message window
findUnusedData(dataUsedList,dataList)

#check for unused tables if user indicated process to be done.
#--------------------------------------------------------------------------------
if checkForTables == "True":
	findUnusedData(dataUsedList,tableList)

arcpy.AddMessage("Process Complete!")
