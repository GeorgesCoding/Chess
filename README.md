
# **Overview** 
- A traditional chess game developed in Python using only the [PyGame](https://www.pygame.org/wiki/about) module.
- Utilizes piece-square tables found from the [Chess Programming Wiki](https://www.chessprogramming.org/PeSTO%27s_Evaluation_Function).
- Includes two-player mode and an AI bot using a minimax algorithm with alpha-beta pruning.
- Incorporates a dialogue window to announce moves, game state and special moves.

https://github.com/GeorgesCoding/Chess/assets/118407807/88b3ea94-de94-4dbb-b189-552dcc79c38a

Notes: 
- The yellow highlight around the mouse is meant to display the mouse clicks and is not part of the game.
- The game may appear to run slower due to screen recording software.


#
# **Dependencies**
Tested on Python 3.12.

Requires PyGame module installation: `pip install pygame`


#
# **Running the Program**
Below are the steps for downloading and running the program locally or using the release file. The release file can run the game without using an IDE or the need to download Python and the PyGame module.

  A. __Downloading the release file__
  1. Go to the repository's release page: [click me!](https://github.com/GeorgesCoding/Chess/releases)
  2. On the latest release (the topmost of the page), click on _Assets_.
  4. Click on the file called _Chess.exe_. This will download the program's file.
  5. Run this file. Windows Defender may abort the program as it's a random .exe file downloaded.
  6. To run, click "_More Info_", then "_Run anyway_".

  B. __Running locally through an IDE with Python installed__
  1. Clone repository: `git clone https://github.com/GeorgesCoding/Chess.git`
  2. Install PyGame: `pip install pygame`
  3. In the IDE terminal, run the file with the command: `py Main.py`

__Notes__
- If you are running the program through an IDE, ensure that the PyGame module and Python are installed before step two.
- Regardless of the method you downloaded the program, the game window will automatically resize according to the "main" display set in your computer settings.
- Text and images may appear incorrectly sized if the monitor size is below 13 inches, but still playable. 


#
# **Files/Modules**
For a more in-depth explanation of the game's functionality, see [Game Structure](https://github.com/GeorgesCoding/Chess/tree/main?tab=readme-ov-file#game-structure).

1. ___Main.py_: Game initialization and event handler__
	- Running this file will initialize the game window to the starting state, an empty board waiting for a button press.
	- Is responsible for dictating game behaviour by examining the event (mouse/keyboard clicks) detected by PyGame.
	- Uses functions from other modules to determine how to draw the state of the board from these events.
	- Three main buttons are restart, two-player mode and computer with the pawn promotion buttons underneath.

2. ___GUI.py_: Drawing and displaying components__
	- Draws the board, pieces, buttons, and side window and updates dialogue text throughout the game.
 	- The dialogue window is altered through the recursive function _addText_.
	- Also includes the dragging animation when moving pieces with functions that help locate and identify the piece.
	- Images for the pieces and buttons are stored in the _Assets_ folder.

3. ___Controller.py_: Game controller and move computations__
	- Responsible for controlling the game logistics and button/keyboard presses.
	- Contains functions for move computations, move validity and helper functions for computations and checks.
 	- Includes en passant capture, castling, check, checkmate, stalemate and pawn promotion.

4. ___Engine.py_: Chess Engine__
   	- Uses a minimax algorithm with alpha-beta pruning for the computer-generated moves.
   	- Utilizes piece-square tables for middle and end-game scenarios for stronger move computations.
	- Currently reaches a max depth of 3 in the search tree within an appropriate response time.

5. ___Package.py_: Executable packaging script__
	- First, the script copies all necessary modules and files into a temporary folder.
	- Then edits the main files, _Main.Py_, _GUI.py_ and _Controller.py_ to include the _resource_path_ function and replace the old image paths.
	- This function allows the picture binary data to be read through the compiled Python code.
	- After will create a [version info resource file](https://learn.microsoft.com/en-us/windows/win32/menurc/versioninfo-resource) to be read by PyInstaller to include file information.
 	- Will then sign the file using Microsoft's [SignTool](https://learn.microsoft.com/en-us/windows/win32/appxpkg/how-to-sign-a-package-using-signtool).
  	- Automatically deletes any unnecessary files leaving only the executable in the current working directory.  	


#
# **Game Structure**
- Each main component (ie. board, pieces, buttons, dialogue text) is created as a [_surface_](https://www.pygame.org/docs/ref/surface.html)
- The surface is converted as a bitmap image and is added to the main window surface specified as "screen" in _Main.py_.
- The method [_blit_](https://www.pygame.org/docs/ref/surface.html#pygame.Surface.blit) is responsible for this process.
  
- The chess board is represented through a 2D array.
- Each space is an index in the sub-arrays with the sub-arrays in the 2D array being a row in the board.
- Index starts at [0][0] to [7][7] in the following format: [y][x].
- Values "10'" or "None" are used for null cases.

- Initialized to the starting position of the board with the following specifications:
  - Black is positive, white is negative, 0 is a space
  - Pawn: 11 when unmoved, 1 when moved
  - Rook: 5 when unmoved, 55 when moved
  - Knight: 3
  - Bishop: 4
  - Queen: 7
  - King: 9 when unmoved, 99 when moved
- King, rook and pawn change values after moving for the first time.
  - This is used to dictate castling and moving two spaces for the pawn.
 
![image](https://github.com/GeorgesCoding/Chess/assets/118407807/b41d4b56-6169-49aa-83af-9a6347365767)


- Legal moves are structured in terms of a set()
	- If the space moved to is within the set, the move is valid.
  - All the legal moves of the piece are computed and compiled together, s0 to test move validity, you need to check if the space the piece moved to is within this list.
  - When testing for membership, lists have [O(n) efficiency while sets have O(1)](https://wiki.python.org/moin/TimeComplexity), making sets more faster.
  - Furthermore, values don't need to be accessed, only a check for membership.
  - Lastly sets ensure unique elements due to their properties, allowing for fewer checks and thus making sets the ideal choice.

- Computations for bishop and rook are grouped due to similarity.
- Constants BLACK and WHITE represent player turns.


#
# **Features: Buttons and Dialogue Window**
In this program, there are three main buttons: 

1. __Restart__
	- Restarts the game to the beginning state, waiting for the user to select a game mode.

		![image-removebg-preview](https://github.com/GeorgesCoding/Chess/assets/118407807/207e81d6-65f7-4795-97b2-d2b2a1c88ae6)


2. __Two Player Mode__
	- Two-player mode initializes the game to white to move, rotating the board after every move.

 		 ![image-removebg-preview (1)](https://github.com/GeorgesCoding/Chess/assets/118407807/6ca2c3c3-8bee-4699-b484-14c9719998b5)
   

3. __Computer Mode__   
	- Computer moves will prompt the user to press the key on their keyboard to determine their colour:
	- B for black, W for white and R for random. 
	- The game will be initialized accordingly.

		![image-removebg-preview (2)](https://github.com/GeorgesCoding/Chess/assets/118407807/af4c78d0-0214-43e4-aab9-948f4bf245e6)

\
Underneath these buttons are the pawn promotion buttons:

![image-removebg-preview (12)](https://github.com/GeorgesCoding/Chess/assets/118407807/5b414c11-aad5-4b74-a7f9-67777050699c)

- When the pawn reaches the end of the board from their respective side, the four buttons with pieces will be outlined in red symbolizing the piece the pawn can be promoted to.
- When pressed, the pawn will be promoted to that piece, the board will rotate (for two-player mode) and the turn will end.
- If pressed under any other conditions, the button will do nothing.

![image-removebg-preview (11)](https://github.com/GeorgesCoding/Chess/assets/118407807/7c6cdc3f-b711-4a4a-ac32-cc0580198a3d)

During checkmate, all piece movements and buttons are disabled with only the restart button enabled.

There is a black box on the bottom right-hand side of the screen underneath the pawn promotion buttons. Here, commentary will be displayed according to the moves of the players. It will also display if the move is invalid if the king is in check, castling, checkmate and more. The most recent comment is at the bottom.

![Chess - frame at 0m59s](https://github.com/GeorgesCoding/Chess/assets/118407807/fa434f2e-0a77-42ce-a092-9a218224c755)
