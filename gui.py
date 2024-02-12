import pygame

"""
========================
=== NOTES FOR VIEWER ===
========================
• Each sub array in the board array is a row in the board
• The elements in each sub array are the individual spaces on the board in that row
• Initialized to the starting position of the board
• Black is positive, white is negative, 10 is an empty space
• Index starts at [0][0], in the following format: [y][x]
• Values '10' or 'None' is used for null cases
"""


# toggles the turn
def playerTurn(colour, turn):
    if colour == "Black" and turn == 1:
        return True
    elif colour == "White" and turn == 1:
        return False
    elif colour == "Black" and turn == -1:
        return False
    elif colour == "White" and turn == -1:
        return True


# helper function: prints the state of the board
def testBoard(board):
    x = 0
    while x < 8:
        print(board[x])
        x += 1

    print("--------------------------------")


# gets the position of the mouse in terms of the board tile coordinates
def getPos(pSize, size):
    mX, mY = pygame.mouse.get_pos()

    if mX >= (size-25) or mY >= (size-25) or mX < 25 or mY < 25:
        return 10, 10  # out of bounds

    else:
        x = int((mX-25) / pSize)
        y = int((mY-25) / pSize)
        return x, y


# creates board surface
def createBoard(size, pSize):

    # create board surface
    tempBoard = pygame.Surface((size + size/1.9, size))

    # board colours
    green = (119, 149, 86)
    white = (235, 236, 208)
    gray = (48, 46, 43)

    # draw background
    pygame.draw.rect(tempBoard, gray, (0, 0, size + size/1.9, size))

    # draw rounded corners
    pygame.draw.rect(tempBoard, white, (25, 25, pSize, pSize), 0, 0, 12)
    pygame.draw.rect(tempBoard, green, (pSize*7 + 25, 25, pSize, pSize), 0, 0, 0, 12)
    pygame.draw.rect(tempBoard, green, (25, pSize*7 + 25, pSize, pSize), 0, 0, 0, 0, 12)
    pygame.draw.rect(tempBoard, white, (pSize*7 + 25, pSize*7 + 25, pSize, pSize), 0, 0, 0, 0, 0, 12)

    for i in range(1, 7, 2):
        pygame.draw.rect(tempBoard, white, (25 + pSize * (i + 1), 25, pSize, pSize))
        pygame.draw.rect(tempBoard, green, (25 + pSize * i, 25, pSize, pSize))

    for n in range(1, 7, 2):
        pygame.draw.rect(tempBoard, green, (25 + pSize * (n + 1), pSize * 7 + 25, pSize, pSize))
        pygame.draw.rect(tempBoard, white, (25 + pSize * n, pSize * 7 + 25, pSize, pSize))

    # draw middle of board
    for y in range(1, 6, 2):
        for x in range(0, 8, 2):
            pygame.draw.rect(tempBoard, green, (25 + pSize * x, pSize * y + 25, pSize, pSize))
            pygame.draw.rect(tempBoard, white, (25 + pSize * (x + 1), pSize * y + 25, pSize, pSize))
            pygame.draw.rect(tempBoard, green, (25 + pSize * (x + 1), pSize * (y + 1) + 25, pSize, pSize))
            pygame.draw.rect(tempBoard, white, (25 + pSize * x, pSize * (y + 1) + 25, pSize, pSize))

    return tempBoard


# side window and button control
def buttons(tempBoard, size):

    # draw side window
    pygame.draw.rect(tempBoard, (33, 32, 29), (size, 25, (size/1.9)-25, size - 50), 0, 0, 12, 12, 12, 12)

    buttonSize = ((size/1.9)-25 - 60)/3
    green = (104, 136, 80)

    # draw buttons
    pygame.draw.rect(tempBoard, green, (size + 15, 45, buttonSize, (size - 45)/6), 0, 0, 12, 12, 12, 12)
    pygame.draw.rect(tempBoard, green, (size + 30 + buttonSize, 45, buttonSize, (size - 45)/6), 0, 0, 12, 12, 12, 12)
    pygame.draw.rect(tempBoard, green, (size + 45 + buttonSize * 2, 45, buttonSize, (size - 45)/6), 0, 0, 12, 12, 12, 12)

    restart = pygame.transform.scale(pygame.image.load('Assets\Restart.png'), (buttonSize-15, buttonSize-15)).convert_alpha()
    twoPlayer = pygame.transform.scale(pygame.image.load('Assets\TPlayer.png'), (buttonSize, buttonSize)).convert_alpha()
    computer = pygame.transform.scale(pygame.image.load('Assets\Computer.png'), (buttonSize, buttonSize)).convert_alpha()

    tempBoard.blit(restart, (size + 15*1.5, 60))
    tempBoard.blit(twoPlayer, (size + 30 + buttonSize, 45*1.175))
    tempBoard.blit(computer, (size + 45 + buttonSize * 2, 45*1.1))

    return tempBoard


# computes the location from the array indexes
def location(a, b, pSize):
    return (25 + (a*pSize), 25 + (b * pSize))


# creates a 'dragging' animation for the pieces
def drag(screen, selected, pSize, size):
    if selected != None:
        half = pSize/2
        piece = selected[0]
        dSize = (pSize, pSize)
        mX, mY = pygame.mouse.get_pos()
        mouseLocation = (mX - half, mY - half)
        x, y = getPos(pSize, size)

        # draw where piece will land according to mouse location
        pygame.draw.rect(screen, (3, 80, 200, 50), ((x * pSize)+25, (y * pSize)+25, pSize, pSize), 5)

        if piece == 1 or piece == 11:  # black pawn
            bPawn = pygame.transform.scale(pygame.image.load('Assets\Pawn.png'), dSize).convert_alpha()
            screen.blit(bPawn, mouseLocation)

        elif piece == 3:  # black knight
            bKnight = pygame.transform.scale(pygame.image.load('Assets\Knight.png'), dSize).convert_alpha()
            screen.blit(bKnight, mouseLocation)

        elif piece == 4:  # black bishop
            bBishop = pygame.transform.scale(pygame.image.load('Assets\Bishop.png'), dSize).convert_alpha()
            screen.blit(bBishop, mouseLocation)

        elif piece == 5:  # black rook
            bRook = pygame.transform.scale(pygame.image.load('Assets\Rook.png'), dSize).convert_alpha()
            screen.blit(bRook, mouseLocation)

        elif piece == 7:  # black queen
            bQueen = pygame.transform.scale(pygame.image.load('Assets\Queen.png'), dSize).convert_alpha()
            screen.blit(bQueen, mouseLocation)

        elif piece == 9:  # black king
            bKing = pygame.transform.scale(pygame.image.load('Assets\King.png'), dSize).convert_alpha()
            screen.blit(bKing, mouseLocation)

        elif piece == -1 or piece == -11:  # white pawn
            wPawn = pygame.transform.scale(pygame.image.load('Assets\wPawn.png'), dSize).convert_alpha()
            screen.blit(wPawn, mouseLocation)

        elif piece == -3:  # white knight
            wKnight = pygame.transform.scale(pygame.image.load('Assets\wKnight.png'), dSize).convert_alpha()
            screen.blit(wKnight, mouseLocation)

        elif piece == -4:  # white bishop
            wBishop = pygame.transform.scale(pygame.image.load('Assets\wBishop.png'), dSize).convert_alpha()
            screen.blit(wBishop, mouseLocation)

        elif piece == -5:  # white rook
            wRook = pygame.transform.scale(pygame.image.load('Assets\wRook.png'), dSize).convert_alpha()
            screen.blit(wRook, mouseLocation)

        elif piece == -7:  # white queen
            wQueen = pygame.transform.scale(pygame.image.load('Assets\wQueen.png'), dSize).convert_alpha()
            screen.blit(wQueen, mouseLocation)

        elif piece == -9:  # white king
            wKing = pygame.transform.scale(pygame.image.load('Assets\wKing.png'), dSize).convert_alpha()
            screen.blit(wKing, mouseLocation)


# gets the piece of the current mouse position
def getPiece(board, pSize, size):
    x, y = getPos(pSize, size)
    if x != 10 and board[y][x] != 0:
        return board[y][x], x, y
    else:
        return 10, 10, 10  # no piece


# draws the pieces in their positions according to the 2D board array
def drawPieces(board, pSize, size):
    # create default size and transparent surface for pieces
    dSize = (pSize, pSize)
    pieces = pygame.Surface((size-50, size), pygame.SRCALPHA, 32).convert_alpha()

    # load & scale all pieces
    bPawn = pygame.transform.scale(pygame.image.load('Assets\Pawn.png'), dSize).convert_alpha()
    bBishop = pygame.transform.scale(pygame.image.load('Assets\Bishop.png'), dSize).convert_alpha()
    bKnight = pygame.transform.scale(pygame.image.load('Assets\Knight.png'), dSize).convert_alpha()
    bRook = pygame.transform.scale(pygame.image.load('Assets\Rook.png'), dSize).convert_alpha()
    bQueen = pygame.transform.scale(pygame.image.load('Assets\Queen.png'), dSize).convert_alpha()
    bKing = pygame.transform.scale(pygame.image.load('Assets\King.png'), dSize).convert_alpha()
    wPawn = pygame.transform.scale(pygame.image.load('Assets\wPawn.png'), dSize).convert_alpha()
    wBishop = pygame.transform.scale(pygame.image.load('Assets\wBishop.png'), dSize).convert_alpha()
    wKnight = pygame.transform.scale(pygame.image.load('Assets\wKnight.png'), dSize).convert_alpha()
    wRook = pygame.transform.scale(pygame.image.load('Assets\wRook.png'), dSize).convert_alpha()
    wQueen = pygame.transform.scale(pygame.image.load('Assets\wQueen.png'), dSize).convert_alpha()
    wKing = pygame.transform.scale(pygame.image.load('Assets\wKing.png'), dSize).convert_alpha()

    # indexes of 2D array
    x = y = -1

    # loop through the 2D array, '_' is each item in the board array (A.K.A each sub array)
    for _ in board:
        y += 1
        for n in _:
            x += 1

            if n == 1 or n == 11:  # black pawn
                pieces.blit(bPawn, location(x, y, pSize))

            elif n == 3:  # black knight
                pieces.blit(bKnight, location(x, y, pSize))

            elif n == 4:  # black bishop
                pieces.blit(bBishop, location(x, y, pSize))

            elif n == 5:  # black rook
                pieces.blit(bRook, location(x, y, pSize))

            elif n == 7:  # black queen
                pieces.blit(bQueen, location(x, y, pSize))

            elif n == 9:  # black king
                pieces.blit(bKing, location(x, y, pSize))

            elif n == -1 or n == -11:  # white pawn
                pieces.blit(wPawn, location(x, y, pSize))

            elif n == -3:  # white knight
                pieces.blit(wKnight, location(x, y, pSize))

            elif n == -4:  # white bishop
                pieces.blit(wBishop, location(x, y, pSize))

            elif n == -5:  # white rook
                pieces.blit(wRook, location(x, y, pSize))

            elif n == -7:  # white queen
                pieces.blit(wQueen, location(x, y, pSize))

            elif n == -9:  # white king
                pieces.blit(wKing, location(x, y, pSize))

            else:  # empty space
                pass
        x = -1

    return pieces
