# **Introduction**                       
- I decided to learn Python by creating a chess game 
- Used a low-level module, PyGame because chess doesn't require much processing, 
    so a simple module was sufficient
- Also allowed me to learn some basic skills in front-end development
- Only runnable on a desktop, preferably through an IDE
- Functional programming is used as opposed to OOP as I require functions to perform various checks and computations. 
  - Even if OOP was used, these functions must exist to perform checks
  - I go around not using attributes from OOP by changing the values of certain pieces to dictate their states (see [Game Structure)](https://github.com/GeorgesCoding/Chess/edit/main/README.md#game-structure)
  - The focus of this project is to gain basic Python skills and create a chess AI
  - Using OOP would've made the structure of the code more complicated and taken away from the main purpose
  
#
# **PyGame Install and Running the Game**
- _main.py_ is responsible for running the entire game
- Make sure that the PyGame module is installed before running _main.py_
    - Using pip: `pip install pygame`
    - Run the file with the terminal command: `py main.py`
- The game window will resize according to the "main" display set in your computer settings

#
# File Organization
- _main.py_: contains the _main()_ method that triggers game activation and contains all applicable event handlers
  - Is responsible for dictating how the game behaves by checking the event detected by PyGame
  - Uses methods from rules.py to determine how to draw the state of the board, or handle button presses
  - Three main buttons are restart, two-player mode and computer
  - Currently, only two-player mode is available

- _gui.py_: responsible for all frontend tasks
   - Includes the dragging animation for moving pieces
   - Drawing the board, pieces, buttons and side windows
   - Each main component (ie. board, pieces, buttons) is created as a "surface"
   - The returned "surface" is then "blitted" onto the main window, specified as "screen" in _main.py_
   - The pieces are stored in the assets folder and are all put into a map constant "_IMAGEPATH_" to be accessed throughout the file

- _rules.py_: game controller and move computations
  - Responsible for controlling the entirety of the game through functions
  - Various functions for move computations, move validity, checkmate, check and more.
  - The majority of the functions rely on array computations

#
# Game Structure
- The chess board is represented through a 2D array
- Each space is an index in the array with a sub-array in the board array being a row in the board
- Index starts at [0][0], in the following format: [y][x]
- Indexes go from 0 to 7 for both y and x directions
- Values "10'" or "None" are used for null cases

- Initialized to the starting position of the board with the following specifications:
  - Black is positive, white is negative, 0 is a space
  - Pawn: 11 when unmoved, 1 when moved
  - Rook: 5 when unmoved, 55 when moved
  - Knight: 3
  - Bishop: 4
  - Queen: 7
  - King: 9 when unmoved, 99 when moved
- King, rook and pawn change values after moving for the first time
    - This is used to dictate castling and moving two spaces for pawn

- All legal moves are computed in terms of a set()
  - If the space moved to is within the set, the move is valid
  - Because all the legal moves of the piece are computed and compiled together, to test move validity,
    you just need to check if the space the piece moved to is within this list
  - When testing for membership, lists have O(n) efficiency while sets have O(1), making sets more faster
  - Furthermore, I don't access the values within, just check for membership
  - Also these lists require uniqueness for more efficiency, making set the ideal choice

- Computations for bishop and rook are grouped due to similarity
- Constants BLACK and WHITE represent player turns
