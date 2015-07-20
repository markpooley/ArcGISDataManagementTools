#ArcGIS Project Data Management Toolset
A small toolset ot help create consistent project folder structures, identify idle/unused data within a project, and batch delete data with workspaces.

##New Project Setup
A small tool that helps maintain consistent folder/file struture accross multiple projects. Addtionally a backup script is created. The tool creates a folder named for the project. Within that folder a three geodatabases are created:

  1. User specifided Project Name

  2. Scratch

  3. Output

Addtionally, MXD and Output folders are created. Within the Output folder two subfolders are created:

  1. Maps

  2. Tables

A Script folder is created as well, and a script called "CopyProject.py" is copied over into this folder. It will backup your project when run, only changing files different from the last backup version. This script can be ran manually in python, or set up to run at regular intervals using "scheduled tasks" in Windows.

####Project folder structure will be as follows:
- Project Name
  - MXDs
  - Output
    - Tables
    - Maps
  - Scripts
  - ProjectName.gdb
  - Ouput.gdb
  - Scratch.gdb

**It is recommended that you adopt a consistent data naming convention as well. For example, using "temp_" as a prefix to all intermediate data will help identify said data for batch deletion.**

There is also an option to have a table GDB created, if it is needed for the project.

## Junk Data Finder
Python script and ArcGIS tool for finding junk data in project folders. User specifies the project folder location, and folder containing *'.mxd'* files. A list of data used in the *'.mxd'* files is generated and compared to all the data found in the project folder.

Potentially unused data is printed the output window.

## Batch Delete FC
Python script and ArcGIS tool for batch deleting feature classes. The user specifies a workspace/geodatabasee and a wildcard. Any feature classes or tables containing the wildcard will be deleted. For example, "temp_*" will delete any tables/feature classes starting with "temp_".

**Simply download all the files here and import the toolbox into ArcGIS**

