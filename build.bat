@ECHO OFF

rem Cleanup Releases folder
del ./Releases/new_release.zip
del -r ./Releases/new_release

rem Build new EXE
pyinstaller --onefile --distpath ./ FE4_Inheritance_Calculator.py

rem Create new zip named new_release.zip in the Releases folder
Tar -a -cf ./Releases/new_release.zip FE4_Inheritance_Calculator.exe Images Audio

rem Cleanup working directory
del FE4_Inheritance_Calculator.exe

PAUSE