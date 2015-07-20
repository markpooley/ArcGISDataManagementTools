# !/usr/bin/env python
# -*- coding: utf-8 -*-
#--------------------------------------------------------------------------------------------------
# Name          : CopyProject.py
# Author        : Mark Pooley (mark-pooley@uiowa.edu)
# Github        : http://github.com/markpooley
# Link          : http://www.ppc.uiowa.edu
# Date          : 2015-02-13 11:09:58
# Version       : $Id$
# Description   : Script to backup data in a source location to a backup location if files have
# the same size and modification date, they are left alone. Otherwise, files are deleted and the
# more recent version is written to the backup location.
#-------------------------------------------------------------------------------------------------

###################################################################################################
#Import python modules
###################################################################################################
import os
import shutil
import time

####################################################################################################
#global function
####################################################################################################

####################################################################################################
#Declare Global variables
####################################################################################################

sourcePath = r'C:\Path\To\Project'
destPath = r'C:\Path\To\BackupLocation'

####################################################################################################
#walk through source path and compare files in the destination path. If files have different sizes
#and different modification dates, then delete and overwrite them.
####################################################################################################
for root, dirs, files in os.walk(sourcePath):

    #figure out where we're going
    dest = destPath + root.replace(sourcePath, '')

    #if we're in a directory that doesn't exist in the destination folder
    #then create a new folder
    if not os.path.isdir(dest):
        os.mkdir(dest)
        print 'Directory created at: ' + dest

    #-------------------------------------------------------------------------------------------
    #loop through all files in the directory. Check if the current file already exists. If so, check that
    #the file size is the same in the copy/backup directory. If it is, do nothing
    #-------------------------------------------------------------------------------------------
    for f in files:

        #compute current (old) & and new file locations, as well as get size and
        #date modified of both files to compare them.
        #---------------------------------------------------------------------------
        oldLoc = root + '\\' + f #location of native file
        newLoc = dest + '\\' + f #back up location of native file


        #check if files are the same size (if they are they're likely the same)
        #so copying isn't necessary
        #---------------------------------------------------------------------------
        if os.path.exists(newLoc):
            oldSize = os.path.getsize(oldLoc) #size of native file
            newSize = os.path.getsize(newLoc) # size of back up version
            oldMod = time.ctime(os.path.getmtime(oldLoc)) #modification date/time of native file
            newMod = time.ctime(os.path.getmtime(newLoc)) #modificaiton date/time of the back up version
            if oldSize == newSize and oldMod == newMod:
                pass
            else:
                #back version is old and has been changed
                os.remove(newLoc)
                print 'Removing {0}, size and/or date modified are different'.format(os.path.basename(newLoc))

        #if file doesn't exist create new ones
        if not os.path.isfile(newLoc):
            try:
                shutil.copy2(oldLoc, newLoc)
                print 'File ' + f + ' copied.'
            except IOError:
                print 'file "' + f + '" already exists'
