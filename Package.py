import os
import shutil
import keyboard
from getpass import getpass
import time


# text to replace and write in files
METHOD = """def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)"""

REPLACE = """# testing function: prints the state of the board
def testBoard(board):
    for row in board:
        print(row)
    print("--------------------------------")"""

NEWIMPORT = """import pygame
import math
import os
import sys
"""

OLDIMPORT = """import pygame
import math
"""

OLD = [
    "'Assets\Restart.png'", "'Assets\TPlayer.png'", "'Assets\Computer.png'", "'Assets\BishopIcon.png'",
    "'Assets\KnightIcon.png'", "'Assets\RookIcon.png'", "'Assets\QueenIcon.png'", "(path)", "'Assets\Pawn.png'",
    "'Assets\Knight.png'", "'Assets\Bishop.png'", "'Assets\Rook.png'", "'Assets\Queen.png'",  "'Assets\King.png'",
    "'Assets\wPawn.png'",  "'Assets\wKnight.png'", "'Assets\wBishop.png'", "'Assets\wRook.png'", "'Assets\wQueen.png'",
    "'Assets\wKing.png'", OLDIMPORT, REPLACE,
]

NEW = [
    "resource_path('Restart.png')", "resource_path('TPlayer.png')", "resource_path('Computer.png')", "resource_path('BishopIcon.png')",
    "resource_path('KnightIcon.png')", "resource_path('RookIcon.png')", "resource_path('QueenIcon.png')", "(resource_path(path))",
    "'Pawn.png'", "'Knight.png'", "'Bishop.png'", "'Rook.png'", "'Queen.png'",  "'King.png'", "'wPawn.png'",  "'wKnight.png'",
    "'wBishop.png'", "'wRook.png'", "'wQueen.png'", "'wKing.png'", NEWIMPORT, METHOD
]

VERSIONDATA = """VSVersionInfo(
    ffi=FixedFileInfo(
        filevers=(0, 4, 1, 0),
        prodvers=(0, 4, 1, 0),
        mask=0x3f,
        flags=0x0,
        OS=0x4,
        fileType=0x1,
        subtype=0x0,
        date=(0, 0)
    ),
    kids=[
        StringFileInfo(
        [
            StringTable(
            u'040904B0',
            [StringStruct(u'CompanyName', u'George Chen'),
            StringStruct(u'FileDescription', u'Chess'),
            StringStruct(u'FileVersion', u'0.4.1'),
            StringStruct(u'InternalName', u'Chess'),
            StringStruct(u'LegalCopyright', u'Copyright (c) George Chen'),
            StringStruct(u'OriginalFilename', u'Chess.exe'),
            StringStruct(u'ProductName', u'Chess Game App'),
            StringStruct(u'ProductVersion', u'0.4.1')])
        ]), 
        VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
    ]
)"""


# open and edits file
def readWrite(fileName, oldText, newText, multiple):
    with open(fileName, 'r') as file:
        filedata = file.read()

    if multiple:
        for old, new in zip(oldText, newText):
            filedata = filedata.replace(old, new)
    else:
        filedata = filedata.replace(oldText, newText)

    with open(fileName, 'w') as file:
        file.write(filedata)


def main():
    # delete old files
    for fileName in ('temp', 'Chess.exe', 'certificate.pfx', 'signtool.exe'):
        if os.path.exists(fileName):
            os.remove(fileName) if fileName != 'temp' else shutil.rmtree(fileName)

    # copies files to a new folder called 'temp'
    shutil.copytree('Assets', 'temp')
    for fileName in ('Main.py', 'GUI.py', 'Controller.py', 'Engine.py'):
        shutil.copy(fileName, 'temp')
    os.chdir('temp')

    # replace text in files
    readWrite('Main.py', "'Assets\icon.png'", "GUI.resource_path('icon.png')", False)
    readWrite('GUI.py', OLD, NEW, True)
    readWrite('Controller.py', 'from GUI import getPiece, getPos, addText, testBoard', 'from GUI import getPiece, getPos, addText', False)
    open('version.txt', 'a')
    readWrite('version.txt', "", VERSIONDATA, False)

    # package files into executable using PyInstaller
    os.system('pyinstaller --onefile --windowed --add-data "*.png:." Main.py --version-file version.txt')
    os.system('cls||clear')
    os.chdir('C:\\Users\\cheng\\Downloads\\Coding\\Chess')

    # check to see if packaging was successful
    if os.path.exists('temp\dist\Main.exe'):
        shutil.copy('temp\dist\Main.exe', '.\Chess.exe')
        shutil.rmtree("temp")
        shutil.copy('C:\\Users\\cheng\\certificate.pfx', '.\certificate.pfx')
        shutil.copy('C:\\Program Files (x86)\\Windows Kits\\10\\bin\\10.0.22621.0\\x86\\signtool.exe', '.\signtool.exe')
        keyboard.press_and_release('ctrl+`')

        # sign the executable using hash function SHA-256 and verify the signature
        while True:
            password = getpass("Please enter the password for the digital certificate or press enter to skip signing process:" + "\n(password is protected and won't be shown in terminal)\n")
            os.system('cls||clear')

            if password != "":
                result = os.system('Signtool sign /fd SHA256 /f certificate.pfx /p ' + password + ' /t http://timestamp.comodoca.com Chess.exe')
                os.system('cls||clear')

                if result != 0:
                    print("ERROR: Wrong password, please try again.")
                else:
                    os.system('Signtool verify /pa Chess.exe')
                    os.system('cls||clear')
                    os.remove('certificate.pfx')
                    os.remove('signtool.exe')
                    break
            else:
                os.remove('certificate.pfx')
                os.remove('signtool.exe')
                break

        print('Packaging Complete!')
        print("Copy Chess.exe to Desktop?")
        print("Yes - Ctrl     No - Shift")
        time.sleep(0.5)

        while True:
            if keyboard.read_key() != 'ctrl':
                os.system('cls||clear')
                break
            else:
                shutil.copy('C:\\Users\\cheng\\Downloads\\Coding\\Chess\\Chess.exe', 'C:\\Users\\cheng\\OneDrive\\Desktop\\Chess.exe')
                os.system('cls||clear')
                print("Successfully Copied!")
                break
    else:
        os.system('cls||clear')
        print('ERROR: Chess.exe was not created.')


if __name__ == '__main__':
    main()
