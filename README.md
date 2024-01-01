## FE4 Inheritance Calculator ##
This is an Inheritance Stat Calculator for FE4.

In FE4, also known as Fire Emblem: Geneaology of the Holy War, there is a timeskip halfway through the game.
Before this timeskip, you have the option to pair up characters, who will then have children that you get in Gen 2 (post timeskip).
Pairing up units in Gen 1 grants a variety of advantages, namely better starting stats, items, and stat growths.
With how drastically pairings can alter a child character's abilities, optimization quickly becomes quite complex. This program aims to help simplify this process.
While there already exist online resources to give you the growth rates and expected starting stats for level 30 parents (which I would recommend, see: SerenesForest.net), I couldn't find anything to give you a child's starting stats given SPECIFIC stat layouts for parents, which can vary significantly due to RNG and/or stat boosters (visiting certain villages, participating in conversations, etc). As such, I thought I'd make something to do that for you.

# Current Features #
- Given the parents' stats at the end of Gen 1, calculate the child(ren)'s starting stats and growth rates in Gen 2.
- Simple User Interface that lets you select the parents from a list and enter each parent's stats
- View just stats or just growth rates

# Installation #
Option 1: Run from exe
- Navigate to the **Releases** directory
- Pick a version and download the corresponding zip
- Unzip and navigate to new directory
- Run **FE4_Inheritance_Calculator.exe**  

Option 2: Run as Python Program
- Download everything but **dist** directory to the same directory
- From directory, run **./FE4_Inheritance_Calculator.py**

# Building Custom Releases #
Included in this repository is a batch file called **build.bat** which will try to build & zip up a new release.
This was created to automate the process of building new releases for myself, but could similarly be used by anyone wishing to fork/work on the project themselves and publish their own version.
Using the repository in this manner is OK as long as credit is given to myself and the forked project is never monetized.

How to build a new release:
- Alter any of the python files in the main working directory
- Run **build.bat** to create a new zip file named **new_release.zip** in the Releases directory
- Navigate to the Releases directory and give **new_release.zip** a fancy new name
- Aaaaand you're done!

# Release Notes #
ver2.0
- Organizational/Productivity Improvements, including a batch file to build new releases and .gitignore
- Fixed bug when trying to make calculations involving Thief Fighters
- Added '%' to Growths Display

# TODO #
- ~~Add GUI to select parents and input stats~~
- Add support for displaying inherited personal skills (specifically with Icons to indicate all personal skills)
- ~~Add support for displaying just stats or just growths~~
- ~~Make UI look cleaner/more visually appealing~~
- ~~Bundle into folder/exe using PyInstaller~~
- ~~Fix Issue where it still checks for valid stats when only looking for growths~~
- ~~Add option to calculate children's expected starting stats using parents' expected stats at a given level~~
- ~~Reset stat forms/boxes every time you select a new parent~~
