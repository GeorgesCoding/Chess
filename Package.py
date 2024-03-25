import os
import shutil

# python script to effeciently make a executable from the three main files

# copies files to a new folder called 'temp'
shutil.copytree('Assets', 'temp')
shutil.copy('Main.py', 'temp')
shutil.copy('GUI.py', 'temp')
shutil.copy('Controller.py', 'temp')

# change directory to 'temp' folder
os.chdir('temp')

# Read in the file
with open('Main.py', 'r') as file:
    filedata = file.read()

# Replace the target string
filedata = filedata.replace("'Assets\icon.png'", "resource_path('icon.png')")

# Write the file out again
with open('Main.py', 'w') as file:
    file.write(filedata)

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

with open('GUI.py', 'r') as file:
    filedata = file.read()

for a, b in zip(old, new):
    filedata = filedata.replace(a, b)

# Write the file out again
with open('GUI.py', 'w') as file:
    file.write(filedata)


with open('Controller.py', 'r') as file:
    filedata = file.read()

filedata = filedata.replace("from GUI import getPiece, getPos, addText, testBoard", "from GUI import getPiece, getPos, addText")

with open('Controller.py', 'w') as file:
    file.write(filedata)

# run the pyinstaller terminal command to package all files into executable
os.system('pyinstaller --onefile --windowed --add-data "*.png:." Main.py')

# change directory back to original 'Chess' folder
os.chdir("C:\\Users\\cheng\\Downloads\\Coding\\Chess")

# copy the created executable 'main.exe' into the main 'chess' folder and rename it to 'Chess.exe'
shutil.copy('temp\dist\Main.exe', '.\Chess.exe')

# deletes folder named temp
shutil.rmtree("temp")
