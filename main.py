import pygame
import numpy
from gui import *
from rules import *


""" 
========================
=== NOTES FOR VIEWER ===
========================
• This file is responsible for running the entire game
• Make sure 'pygame' and 'numpy' modules are installed prior to running file
    - Using pip: pip install pygame
    - pip install numpy
    - Run file with terminal command: 'py main.py'
"""


# main control function
def main():

    # automatically changes game SIZE according to monitor SIZE
    pygame.init()
    size = pygame.display.Info().current_h
    SIZE = size - 120
    PSIZE = (SIZE-50)/8

    # initialize window
    screen = pygame.display.set_mode((SIZE + 500, SIZE))

    # customize window
    pygame.display.set_caption("Chess")
    icon = pygame.image.load('Assets\icon.png')
    pygame.display.set_icon(icon)

    # 2D array to represent state of board
    board = [[5, 3, 4, 7, 9, 4, 3, 5], [11]*8, [0]*8, [0]*8, [0]*8, [0]*8, [-11]*8, [-5, -3, -4, -7, -9, -4, -3, -5]]

    # toggable variables
    selected = None
    turn = 1
    outline = False
    promotion = None, None, None

    # list of all possible enemy piece moves
    moveList = []

    # draw board, pieces and side bar
    buttonSurface = buttons(SIZE)
    boardSurface = createBoard(SIZE, PSIZE)
    piecesSurface = drawPieces(board, PSIZE, SIZE, turn)

    # button information
    BUTTONLENGTH = int(((SIZE/1.9)-25 - 60)/3)
    BUTTONHEIGHT = int((SIZE - 45)/6)
    INTSIZE = int(SIZE)
    INTPSIZE = int(PSIZE)
    restartInfo = (INTSIZE + 15, 45, BUTTONLENGTH, BUTTONHEIGHT)
    twoPlayerInfo = (INTSIZE + 30 + BUTTONLENGTH, 45, BUTTONLENGTH, BUTTONHEIGHT)
    computerInfo = (INTSIZE + 45 + BUTTONLENGTH * 2, 45, BUTTONLENGTH, BUTTONHEIGHT)
    bishopInfo = (INTSIZE + 15, 45 + INTPSIZE + BUTTONHEIGHT, INTPSIZE, INTPSIZE)
    knightInfo = (INTSIZE + 25 + INTPSIZE, 45 + INTPSIZE + BUTTONHEIGHT, INTPSIZE, INTPSIZE)
    rookInfo = (INTSIZE + 35 + INTPSIZE * 2, 45 + INTPSIZE + BUTTONHEIGHT, INTPSIZE, INTPSIZE)
    queenInfo = (INTSIZE + 45 + INTPSIZE * 3, 45 + INTPSIZE + BUTTONHEIGHT, INTPSIZE, INTPSIZE)
    promoInfo = bishopInfo, knightInfo, rookInfo, queenInfo

    # starting position of piece being moved
    oldX, oldY = 0, 0

    # main loop
    while True:
        tempPiece, x, y = getPiece(board, PSIZE, SIZE)  # checks if there is a piece under the mouse
        for event in pygame.event.get():

            # exit button pressed
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            # if left mouse button is pressed
            if event.type == pygame.MOUSEBUTTONDOWN:

                # promotion buttons are outlined
                if outline:
                    i = 1
                    for p in promoInfo:
                        if button(i, p, promotion, board):
                            outline = False
                            break
                        i += 1

                # restarts program
                elif button(0, restartInfo, None, None):
                    pygame.quit()
                    main()
                    return

                #  two player mode
                elif button(0, twoPlayerInfo, None, None):
                    print("Two Player")

                # vs Computer
                elif button(0, computerInfo, None, None):
                    print("Computer")

                # checks if a piece has been selected
                elif tempPiece != 10 and playerTurn(pieceColour(tempPiece), turn):
                    selected = tempPiece, x, y  # piece is selected, toggles selected variable
                    board[y][x] = 0  # remove piece from board
                    pygame.draw.rect(boardSurface, (244, 246, 128, 50), ((x * PSIZE) + 25, (y * PSIZE) + 25, PSIZE, PSIZE), 5)  # outline old space
                    piecesSurface = drawPieces(board, PSIZE, SIZE, turn)
                    oldX, oldY = x, y

            # mouse button is released
            if event.type == pygame.MOUSEBUTTONUP:
                # A piece was selected
                if selected != None:
                    piece = selected[0]
                    newX, newY = getPos(PSIZE, SIZE)

                    # creates a board with the temporary state of the board with the moved piece
                    tempBoard = [row[:] for row in board]
                    tempBoard[newY][newX] = piece
                    moveList = computeAll(piece, tempBoard)

                    # king castles
                    if castle(piece, board, oldY, oldX, PSIZE, SIZE, moveList, tempBoard):
                        turn = -turn

                    # piece is moved to a valid position
                    elif newX != 10 and move(piece, newY, newX, oldY, oldX, board) and (newY, newX) != (oldY, oldX):
                        firstMove(piece, tempBoard, newY, newX)

                        # king is in check after move
                        if kingCoord(piece, tempBoard) in moveList:
                            board[oldY][oldX] = piece

                        else:  # legal move
                            board[newY][newX] = piece

                            # pawn at end of board
                            if endPawn(piece, board, newY, newX):
                                outline = True
                                promotion = piece, newY, newX
                            else:
                                outline = False
                                promotion = None, None, None

                            firstMove(piece, board, newY, newX)
                            turn = -turn

                            # rotates the pieces on the board for 2 player mode
                            # problems with check case when rotation
                            # will return after checkmate case is complete
                            # board = numpy.rot90(board, 2)

                    else:  # piece moved to invalid position
                        board[oldY][oldX] = piece

                # redraw surfaces, reset temp variables
                boardSurface = createBoard(SIZE, PSIZE)
                buttonSurface = buttons(SIZE)
                piecesSurface = drawPieces(board, PSIZE, SIZE, turn)
                selected = None
                oldY, oldX = 0, 0

        # add surfaces to screen
        screen.blit(boardSurface, (0, 0))
        screen.blit(buttonSurface, (0, 0))
        screen.blit(piecesSurface, (0, 0))

        # outline promotion buttons
        promoOutline(screen, SIZE, outline)

        # numbers the board
        numBoard(screen)

        # creates 'dragging' animation for pieces
        drag(screen, selected, PSIZE, SIZE)

        # update display
        pygame.display.flip()


if __name__ == '__main__':
    main()
