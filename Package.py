import os
import shutil

# delete old files
if os.path.exists('temp'):
    shutil.rmtree('temp')

if os.path.exists('Chess.exe'):
    os.remove('Chess.exe')

if os.path.exists('certificate.pfx'):
    os.remove('certificate.pfx')

if os.path.exists('signtool.exe'):
    os.remove('signtool.exe')


# text to replace and write in files
method = """def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)"""

replace = """# testing function: prints the state of the board
def testBoard(board):
    for row in board:
        print(row)
    print("--------------------------------")"""

newImport = """import pygame
import os
import sys
"""

old = [
    "'Assets\Restart.png'", "'Assets\TPlayer.png'", "'Assets\Computer.png'", "'Assets\BishopIcon.png'",
    "'Assets\KnightIcon.png'", "'Assets\RookIcon.png'", "'Assets\QueenIcon.png'", "(path)", "'Assets\Pawn.png'",
    "'Assets\Knight.png'", "'Assets\Bishop.png'", "'Assets\Rook.png'", "'Assets\Queen.png'",  "'Assets\King.png'",
    "'Assets\wPawn.png'",  "'Assets\wKnight.png'", "'Assets\wBishop.png'", "'Assets\wRook.png'", "'Assets\wQueen.png'",
    "'Assets\wKing.png'", "import pygame", replace,
]

new = [
    "resource_path('Restart.png')", "resource_path('TPlayer.png')", "resource_path('Computer.png')", "resource_path('BishopIcon.png')",
    "resource_path('KnightIcon.png')", "resource_path('RookIcon.png')", "resource_path('QueenIcon.png')", "(resource_path(path))",
    "'Pawn.png'", "'Knight.png'", "'Bishop.png'", "'Rook.png'", "'Queen.png'",  "'King.png'", "'wPawn.png'",  "'wKnight.png'",
    "'wBishop.png'", "'wRook.png'", "'wQueen.png'", "'wKing.png'", newImport, method
]

versionData = """
VSVersionInfo(
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
)
"""


# copies files to a new folder called 'temp'
shutil.copytree('Assets', 'temp')
shutil.copy('Main.py', 'temp')
shutil.copy('GUI.py', 'temp')
shutil.copy('Controller.py', 'temp')
os.chdir('temp')


# read and write in the files that need editing
with open('Main.py', 'r') as file:
    filedata = file.read()

filedata = filedata.replace("'Assets\icon.png'", "resource_path('icon.png')")

with open('Main.py', 'w') as file:
    file.write(filedata)

with open('GUI.py', 'r') as file:
    filedata = file.read()

for a, b in zip(old, new):
    filedata = filedata.replace(a, b)

with open('GUI.py', 'w') as file:
    file.write(filedata)

with open('Controller.py', 'r') as file:
    filedata = file.read()

filedata = filedata.replace('from GUI import getPiece, getPos, addText, testBoard', 'from GUI import getPiece, getPos, addText')

with open('Controller.py', 'w') as file:
    file.write(filedata)

file = open('version.txt', 'a')

with open('version.txt', 'r') as file:
    filedata = file.read()

filedata = filedata.replace("", versionData)

with open('version.txt', 'w') as file:
    file.write(filedata)


# package files into executable using PyInstaller command
os.system('pyinstaller --onefile  --windowed --add-data "*.png:." Main.py --version-file version.txt')
os.chdir('C:\\Users\\cheng\\Downloads\\Coding\\Chess')
shutil.copy('temp\dist\Main.exe', '.\Chess.exe')
shutil.copy('C:\\Users\\cheng\\certificate.pfx', '.\certificate.pfx')


# check to see if packaging was successful
if os.path.exists('Chess.exe'):
    # sign the executable using hash function SHA-256 and verify the signature
    shutil.copy('C:\\Program Files (x86)\\Windows Kits\\10\\bin\\10.0.22621.0\\x86\\signtool.exe', '.\signtool.exe')
    os.system('Signtool sign /fd SHA256 /f certificate.pfx /p <password> /t http://timestamp.comodoca.com Chess.exe')
    os.system('Signtool verify /pa Chess.exe')

    shutil.rmtree("temp")
    os.remove('certificate.pfx')
    os.remove('signtool.exe')
    os.system('cls||clear')
    print('Packaging Complete!')
else:
    print('ERROR: Chess.exe was not created.')

# shutil.copy('C:\\Users\\cheng\\Downloads\\Coding\\Chess\\Chess.exe', 'C:\\Users\\cheng\\OneDrive\\Desktop\\Chess.exe')
