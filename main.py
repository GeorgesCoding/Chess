import pygame
from gui import *
from rules import *


# Dictionary constant of the names of pieces according to their integer representation
PIECE = {
    1: "Black pawn", 11: "Black pawn", 3: "Black knight", 4: "Black bishop",
    5: "Black rook", 55: "Black rook", 7: "Black queen", 9: "Black king",
    99: "Black king", -1: "White pawn", -11: "White pawn", -3: "White knight",
    -4: "White bishop", -5: "White rook", -55: "White rook", -7: "White queen",
    -9: "White king", -99: "White king"
}

# Dictionary constant of the letters used to represent piece moves
ALPH = {1: "a", 2: "b", 3: "c", 4: "d", 5: "e", 6: "f", 7: "g", 8: "h"}


def main():

    # automatically changes window dimensions according to monitor size
    pygame.init()
    size = pygame.display.Info().current_h
    SIZE = size - 120
    PSIZE = (SIZE-50)/8

    # initialize window
    screen = pygame.display.set_mode((SIZE + SIZE/1.9, SIZE))

    # customize window
    pygame.display.set_caption("Chess")
    icon = pygame.image.load('Assets\icon.png')
    pygame.display.set_icon(icon)

    # 2D array to represent state of board
    board = [
        [5, 3, 4, 7, 9, 4, 3, 5],
        [11] * 8,
        [0] * 8,
        [0] * 8,
        [0] * 8,
        [0] * 8,
        [-11] * 8,
        [-5, -3, -4, -7, -9, -4, -3, -5]
    ]

    # toggable variables
    selected = None
    turn = 1
    outline = False
    promotion = None, None, None
    pieceMoving = False
    colourChoose = False
    computer = None
    start = False
    isPawn = False
    opposite = 1
    switch = True
    end = False  # if true, freezes the game except restart and quit

    # list of all possible enemy piece moves
    moveList = set()

    # list of all pawns that can perform en passant
    canPassant = []

    # an array that holds the dialouge to be displayed
    text = ["", "", "", "", "", "", "", "", ""]

    # draw board, pieces and side bar
    buttonSurface = buttons(SIZE)
    boardSurface = createBoard(SIZE, PSIZE)
    dialougeSurf = dialouge(SIZE, text)
    piecesSurface = drawPieces(board, PSIZE, SIZE)

    # button dimensions
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

            end = gameEnd(board, turn, pieceMoving, start, outline, canPassant, opposite, text)

            # Checks for turn selection
            if colourChoose and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    computer = BLACK
                    player = WHITE
                    clearText(text)
                elif event.key == pygame.K_b:
                    player = BLACK
                    computer = WHITE
                    clearText(text)
                elif event.key == pygame.K_r:
                    computer = randomTurn()
                    player = -computer
                    clearText(text)
                dialougeSurf = dialouge(SIZE, text)

            if start and computer != None and turn == computer:
                pass
                # cY, cX = random.choice(list(computeAll(computer, board, 0, 1, canPassant)))
                # need piece, old and new coordinates
                # for promotion, promotes to random

            # if left mouse button is pressed
            if event.type == pygame.MOUSEBUTTONDOWN:

                # promotion buttons are outlined
                if outline:
                    for i, p in enumerate(promoInfo):
                        if button(i + 1, p, promotion, board, text):
                            outline = False
                            board = rotate(board, computer)
                            turn = -turn
                            break

                # restarts program
                elif button(0, restartInfo, None, None, text):
                    pygame.quit()
                    main()
                    return

                #  two player mode
                elif not colourChoose and button(0, twoPlayerInfo, None, None, text):
                    start = True

                # vs Computer
                elif not start and button(0, computerInfo, None, None, text):
                    addText(text, "Press the Key to Choose a Colour:")
                    addText(text, "W for White")
                    addText(text, "B for Black")
                    addText(text, "R for Random")
                    colourChoose = True

                # checks if a piece has been selected
                elif start and tempPiece != 10 and playerTurn(pieceColour(tempPiece), turn) and not end:
                    selected = tempPiece, x, y  # piece is selected, toggles selected variable
                    board[y][x] = 0  # remove piece from board
                    pygame.draw.rect(boardSurface, (244, 246, 128, 50), ((x * PSIZE) + 25, (y * PSIZE) + 25, PSIZE, PSIZE), 5)  # outline old space
                    piecesSurface = drawPieces(board, PSIZE, SIZE)
                    oldX, oldY = x, y
                    pieceMoving = True

            # mouse button is released
            if event.type == pygame.MOUSEBUTTONUP and not outline and not end:

                # A piece was selected
                if selected != None:
                    pieceMoving = False
                    piece = selected[0]
                    newX, newY = getPos(PSIZE, SIZE)

                    if newX != 10:
                        # creates a board with the temporary state of the board with the moved piece
                        tempBoard = [row[:] for row in board]
                        tempBoard[newY][newX] = piece
                        moveList = computeAll(piece, tempBoard, 0, opposite, canPassant)

                        # king castles
                        if castle(piece, board, oldY, oldX, PSIZE, SIZE, moveList, tempBoard, text):
                            turn = -turn
                            board = rotate(board, computer)

                        # piece is moved to a valid position
                        elif move(piece, newY, newX, oldY, oldX, board, canPassant) and (newY, newX) != (oldY, oldX):
                            firstMove(piece, tempBoard, newY, newX)

                            # king is in check after move
                            if kingCoord(piece, board) in moveList:
                                board[oldY][oldX] = piece
                                inCheck = "White king in check" if piece < 0 else "Black king in check"
                                addText(text, "Invalid move: " + str(inCheck))

                            else:  # legal move
                                enPassantCapture(piece, board, newY, newX, oldY, oldX, isPawn, canPassant)
                                board[newY][newX] = piece
                                isPawn = pawnFirst(piece, newY, newX, oldY, oldX)
                                firstMove(piece, board, newY, newX)
                                canPassant = enPassant(piece, newY, newX, board, isPawn)
                                turn = -turn
                                board = rotate(board, computer)

                                if (pieceColour(-piece) == BLACK and computer is None) or (computer == 1 and player == -1):
                                    num = newY + 1
                                    alph = 8 - newX
                                else:
                                    num = 8 - newY
                                    alph = newX + 1
                                addText(text, str(PIECE[piece]) + " to " + str(ALPH[alph]) + str(num))

                                # pawn at end of board
                                if piece in {-1, 1} and newY == 0:
                                    outline = True
                                    promotion = piece, newY, newX
                                    board = rotate(board, computer)
                                    turn = -turn
                                else:
                                    outline = False
                                    promotion = None, None, None

                                    end = gameEnd(board, turn, pieceMoving, start, outline, canPassant, opposite, text)

                                    if not end:
                                        moveList = computeAll(-piece, board, 0, opposite, canPassant)
                                        if kingCoord(-piece, board) in moveList:
                                            inCheck = "White king in check" if -piece < 0 else "Black king in check"
                                            addText(text, inCheck)

                        else:
                            board[oldY][oldX] = piece
                            if not (newY == oldY and newX == oldX):
                                addText(text, "Invalid Move")

                # redraw surfaces, reset temp variables
                boardSurface = createBoard(SIZE, PSIZE)
                buttonSurface = buttons(SIZE)
                piecesSurface = drawPieces(board, PSIZE, SIZE)
                dialougeSurf = dialouge(SIZE, text)
                selected = None
                oldY, oldX = 0, 0

        # add surfaces to screen
        screen.blit(boardSurface, (0, 0))
        screen.blit(buttonSurface, (0, 0))
        screen.blit(dialougeSurf, (0, 0))

        if start:
            screen.blit(piecesSurface, (0, 0))
        elif computer != None:
            colourChoose = False
            if computer == 1:
                board = rotate(board, None)
            opposite = 0
            piecesSurface = drawPieces(board, PSIZE, SIZE)
            screen.blit(piecesSurface, (0, 0))
            start = True

        # outline promotion buttons
        promoOutline(screen, SIZE, outline)

        # numbers the board
        switch = numBoard(screen, PSIZE, turn, computer, switch)

        # creates "dragging" animation for pieces
        drag(screen, selected, PSIZE, SIZE)

        # update display
        pygame.display.flip()


if __name__ == '__main__':
    main()
