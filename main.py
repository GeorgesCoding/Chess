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
    screen = pygame.display.set_mode((size, size))

    # customize window
    pygame.display.set_caption("Chess")
    icon = pygame.image.load('Assets\icon.png')
    pygame.display.set_icon(icon)

    # 2D array to represent state of board
    board = [[5, 3, 4, 7, 9, 4, 3, 5], [11]*8, [0]*8, [0]*8, [0]*8, [0]*8, [-11]*8, [-5, -3, -4, -7, -9, -4, -3, -5]]

    # draw board & pieces
    boardSurface = createBoard(size, pSize)
    piecesSurface = drawPieces(board, pSize, size)

    # selected piece variable
    selected = None

    # starting position of piece being moved
    oldX, oldY = 0, 0

    # main loop
    while True:
        tempPiece, x, y = getPiece(board, pSize, size)  # checks if there is a piece under the mouse
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if tempPiece != 10:
                    selected = tempPiece, x, y  # piece is selected, toggles selected variable
                    board[y][x] = 0  # remove piece from board
                    pygame.draw.rect(boardSurface, (244, 246, 128, 50), ((x * pSize) + 25, (y * pSize) + 25, pSize, pSize), 5)  # outline old space
                    piecesSurface = drawPieces(board, pSize, size)
                    oldX, oldY = x, y

            if event.type == pygame.MOUSEBUTTONUP:
                if selected != None:
                    piece = selected[0]
                    newX, newY = getPos(pSize, size)

                    if newX != 10 and move(piece, newY, newX, oldY, oldX, board):  # mouse in bounds of board
                        board[newY][newX] = piece
                        firstMove(piece, board, newY, newX)

                    else:
                        board[oldY][oldX] = piece

                boardSurface = createBoard(size, pSize)
                piecesSurface = drawPieces(board, pSize, size)
                selected = None
                oldY, oldX = 0, 0

        # add surfaces to screen
        screen.blit(boardSurface, (0, 0))
        screen.blit(piecesSurface, (0, 0))

        # creates 'dragging' animation for pieces
        drag(screen, selected, pSize, size)

        # update display
        pygame.display.flip()


if __name__ == '__main__':
    main()
