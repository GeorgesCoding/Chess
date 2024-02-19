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

    # automatically changes game size according to monitor size
    pygame.init()
    size = pygame.display.Info().current_h
    size = size - 120
    pSize = (size-50)/8

    # initialize window
    screen = pygame.display.set_mode((size + 500, size))

    # customize window
    pygame.display.set_caption("Chess")
    icon = pygame.image.load('Assets\icon.png')
    pygame.display.set_icon(icon)

    # 2D array to represent state of board
    board = [[5, 3, 4, 7, 9, 4, 3, 5], [11]*8, [0]*8, [0]*8, [0]*8, [0]*8, [-11]*8, [-5, -3, -4, -7, -9, -4, -3, -5]]

    # selected and turn variable
    selected = None
    turn = 1

    # draw board, pieces and side bar
    buttonSurface = buttons(size)
    boardSurface = createBoard(size, pSize)
    piecesSurface = drawPieces(board, pSize, size, turn)

    # check variable
    # 0 for no check, 1 for black check, -1 for white check
    check = 0
    moveList = []

    selection = 0

    # button information
    buttonLength = int(((size/1.9)-25 - 60)/3)
    buttonHeight = int((size - 45)/6)
    intSize = int(size)
    restartInfo = (intSize + 15, 45, buttonLength, buttonHeight)
    twoPlayerInfo = (intSize + 30 + buttonLength, 45, buttonLength, buttonHeight)
    computerInfo = (intSize + 45 + buttonLength * 2, 45, buttonLength, buttonHeight)

    # starting position of piece being moved
    oldX, oldY = 0, 0

    # main loop
    while True:
        tempPiece, x, y = getPiece(board, pSize, size)  # checks if there is a piece under the mouse
        for event in pygame.event.get():

            # exit button pressed
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            # if left mouse button is pressed
            if event.type == pygame.MOUSEBUTTONDOWN:

                # restarts program
                if button(1, restartInfo):
                    pygame.quit()
                    main()
                    return

                #  two player mode
                elif button(2, twoPlayerInfo):
                    print("Two Player")

                # vs Computer
                elif button(3, computerInfo):
                    print("Computer")

                # checks if a piece has been selected
                elif tempPiece != 10 and playerTurn(pieceColour(tempPiece), turn):
                    selected = tempPiece, x, y  # piece is selected, toggles selected variable
                    board[y][x] = 0  # remove piece from board
                    pygame.draw.rect(boardSurface, (244, 246, 128, 50), ((x * pSize) + 25, (y * pSize) + 25, pSize, pSize), 5)  # outline old space
                    piecesSurface = drawPieces(board, pSize, size, turn)
                    oldX, oldY = x, y

            # mouse button is released
            if event.type == pygame.MOUSEBUTTONUP:
                # A piece was selected
                if selected != None:
                    piece = selected[0]
                    newX, newY = getPos(pSize, size)

                    tempBoard = [row[:] for row in board]
                    tempBoard[newY][newX] = piece
                    moveList = computeAll(piece, tempBoard)

                    if castle(piece, board, oldY, oldX, pSize, size, moveList, tempBoard):
                        turn = -turn

                    # piece is moved to a valid position
                    elif newX != 10 and move(piece, newY, newX, oldY, oldX, board) and (newY, newX) != (oldY, oldX):
                        firstMove(piece, tempBoard, newY, newX)

                        # king is in check after move
                        if kingCoord(piece, tempBoard) in moveList:
                            board[oldY][oldX] = piece

                        else:
                            board[newY][newX] = piece
                            firstMove(piece, board, newY, newX)
                            turn = -turn

                            # rotates the pieces on the board for 2 player mode
                            # problems with check case when rotation
                            # board = numpy.rot90(board, 2)

                    # piece moved to invalid position
                    else:
                        board[oldY][oldX] = piece

                # redraw surfaces, reset temp variables
                boardSurface = createBoard(size, pSize)
                buttonSurface = buttons(size)
                piecesSurface = drawPieces(board, pSize, size, turn)
                selected = None
                oldY, oldX = 0, 0

        # add surfaces to screen
        screen.blit(boardSurface, (0, 0))
        screen.blit(buttonSurface, (0, 0))
        screen.blit(piecesSurface, (0, 0))

        numBoard(screen)

        # creates 'dragging' animation for pieces
        drag(screen, selected, pSize, size)

        # update display
        pygame.display.flip()


# evaluates if a button is pressed
def button(selection, info):

    # Restart
    if selection == 1:
        return pygame.mouse.get_pos()[0] in range(info[0], info[2] + info[0]) and pygame.mouse.get_pos()[1] in range(info[1], info[3] + info[1])

    # Two Player
    elif selection == 2:
        return pygame.mouse.get_pos()[0] in range(info[0], info[2] + info[0]) and pygame.mouse.get_pos()[1] in range(info[1], info[3] + info[1])

    # Computer
    elif selection == 3:
        return pygame.mouse.get_pos()[0] in range(info[0], info[2] + info[0]) and pygame.mouse.get_pos()[1] in range(info[1], info[3] + info[1])


if __name__ == '__main__':
    main()
