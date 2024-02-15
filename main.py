import pygame
from gui import *
from rules import *


""" 
========================
=== NOTES FOR VIEWER ===
========================
• This file is responsible for running the entire game
• Make sure 'pygame' module is installed prior to running file
    - Using pip: pip install pygame
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

    # draw board, pieces and side bar
    boardSurface = createBoard(size, pSize)
    boardSurface = buttons(boardSurface, size)
    piecesSurface = drawPieces(board, pSize, size)

    # selected and turn variable
    selected = None
    turn = 1

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

            if event.type == pygame.QUIT:
                pygame.quit()
                return

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

                elif tempPiece != 10 and playerTurn(pieceColour(tempPiece), turn):
                    if tempPiece in {9, -9}:
                        moveList = computeAll(tempPiece, board)

                    selected = tempPiece, x, y  # piece is selected, toggles selected variable
                    board[y][x] = 0  # remove piece from board
                    pygame.draw.rect(boardSurface, (244, 246, 128, 50), ((x * pSize) + 25, (y * pSize) + 25, pSize, pSize), 5)  # outline old space
                    piecesSurface = drawPieces(board, pSize, size)
                    oldX, oldY = x, y

            if event.type == pygame.MOUSEBUTTONUP:
                if selected != None:
                    piece = selected[0]
                    newX, newY = getPos(pSize, size)

                    if piece in {9, -9} and (newY, newX) in moveList:
                        print("A")
                        board[oldY][oldX] = piece

                    elif newX != 10 and move(piece, newY, newX, oldY, oldX, board) and (newY, newX) != (oldY, oldX):  # mouse in bounds of board
                        print("B")
                        board[newY][newX] = piece
                        firstMove(piece, board, newY, newX)
                        turn = -turn
                    else:
                        print("C")
                        board[oldY][oldX] = piece

                boardSurface = createBoard(size, pSize)
                boardSurface = buttons(boardSurface, size)
                piecesSurface = drawPieces(board, pSize, size)
                selected = None
                oldY, oldX = 0, 0

        # add surfaces to screen
        screen.blit(boardSurface, (0, 0))
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
