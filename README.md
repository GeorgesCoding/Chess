# **Overview** 
- A traditional chess game developed in python using the [PyGame](https://www.pygame.org/wiki/about) module.
- Includes two-player mode and a AI bot (work in progress) built using the minimax algorithm.
- Used pictures found on [Wikimedia](https://commons.wikimedia.org/wiki/Category:SVG_chess_pieces) as the pieces.
- Currently in the process of developing tooltips for buttons and the AI bot.


#
# **Dependencies**
Tested on Python 3.12.

Requires PyGame module installation (using pip): `pip install pygame`


#
# **Running the Program**
1. Clone repository
   `git clone https://github.com/GeorgesCoding/Chess.git`
   
NOTE: Make sure that the PyGame module is installed before step two.

2. Run the file with the terminal command: `py main.py`
   
   (The game window will resize according to the "main" display set in your computer settings.)


#
# **Files**
1. _main.py_: Game initialization and event handler
	- Is responsible for dictating how the game behaves by examining the event detected by PyGame.
	- Uses methods from _rules.py_ to determine how to draw the state of the board and handle button or mouse clicks.
	- Three main buttons are restart, two-player mode and computer.
	- In the process of developing AI generated moves for computer mode.

2. _gui.py_: Drawing and displaying components
   - Draws the board, pieces, buttons, side window and updates dialouge.
   - Also includes the dragging animation when moving pieces.
   - Each main component (ie. board, pieces, buttons) is created as a [_surface_](https://www.pygame.org/docs/ref/surface.html)
   - The surface is converted as a bitmap image and is added to the main window surface specified as "screen" in _main.py_.
   - The method [_blit_](https://www.pygame.org/docs/ref/surface.html#pygame.Surface.blit) is responsible for this process.
   - Images for the pieces and buttons are stored in the _assets_ folder.

3. _rules.py_: Game controller and move computations
	- Responsible for controlling the entirety of the game through functions.
	- Contains functions for move computations, move validity and helper functions for computations and checks.
 	- Includes en passant capture, castling, check, checkmate and pawn promotion.
	- The majority of the functions rely heavily on array computations.

#
# **Game Structure**
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
  - This is used to dictate castling and moving two spaces for pawn.

- Legal moves are structured in terms of a set()
	- If the space moved to is within the set, the move is valid.
  - Because all the legal moves of the piece are computed and compiled together, to test move validity, you need to check if the space the piece moved to is within this list.
  - When testing for membership, lists have O(n) efficiency while sets have O(1), making sets more faster.
  - Furthermore, values don't need to be accessed, only a check for membership.
  - Lastly sets ensure unique elements due to their properties, allowing for less checks and thus making sets the ideal choice.

- Computations for bishop and rook are grouped due to similarity.
- Constants BLACK and WHITE represent player turns.
