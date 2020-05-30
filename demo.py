import mpath




















"""
D:/p4/wwe2k/main
    Art
        Characters
    Assets
        Characters
            CharacterMapping.jtable
    Tools/maya/scripts/vclaMenu.py
N:/dl/thirdParty
    ExportThing/v23/exporter.py
C:/msys64/home/gfixler/vc2k/code/py/chardb/wwe2k22_chars.json
"""






















projLayoutStr = """
root|D:/p4/wwe2k/main
    art|Art
        chars|Characters
    assets|Assets
        charsExp|Characters
            roster|CharacterMapping.jtable
    menu|Tools/maya/scripts/vclaMenu.py
dltools|N:/dl/thirdParty
    exporter|ExportThing/v23/exporter.py
db|C:/msys64/home/gfixler/vc2k/code/py/chardb/wwe2k22_chars.json
"""

projLayout = mpath.mpath.parseLayoutStr(projLayoutStr)
demoMPaths = mpath.MPaths("foo", projLayout)

mpaths = mpath.fromLayoutStr("foo", projLayoutStr)

mpaths.pathTree

mpaths.paths

mpaths.pprint()

mpaths["roster"]


mpaths.roster




mpaths.roster.exists()

mpaths.roster.isfile()

mpaths.roster.isdir()












mpaths.chars.extend("100_The_Rock", "BaseModel", "baseModel.ma")








mpaths.chars.extend("100_The_Rock", "BaseModel/baseModel.ma")







mpaths.chars.extend("\\\\\\\\\\100_The_Rock//////////", "\\\\/BaseModel\\/\\baseModel.ma///\\\\")

















superstars = ["Al", "Sumit", "Norbert"]

for superstar in superstars:
    print mpaths.chars.extend(superstar, "BaseModel", "baseModel.ma")




























mpaths.mayaForm()



mpaths.pprint()



















help(mpath)

help(mpath.mpath.parseLayoutStr)

help(mpath.fromLayoutStr)






























def myToolWin (myToolMPaths):

    import os

    def openRoster (*_):
        os.system("start " + myToolMPaths.roster)

    win = cmds.window(title="The Best Window", widthHeight=(200,100))
    cmds.showWindow()
    cmds.menuBarLayout()

    cmds.menu(label="File")
    cmds.menuItem(label="Open...")
    cmds.menuItem(label="Open Recent...")
    cmds.menuItem(label="Save")
    cmds.menuItem(label="Save As...")
    cmds.menuItem(divider=True)
    cmds.menuItem(label="Quit")

    cmds.menu(label="Edit")
    cmds.menuItem(label="Settings")
    cmds.menuItem(label="Unsettings")
    cmds.menuItem(divider=True)
    myToolMPaths.createMenuItem()
    cmds.menuItem(divider=True)
    cmds.menuItem(label="Export...")

    cmds.paneLayout(parent=win)
    cmds.button(label="Edit Roster...", command=openRoster)


myToolWin(mpaths)



















mpaths.db

mpaths.db.loadJSON()

























TESTS!

















