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


# helper function: prints the numbers of the board
def numBoard(screen):

    # font
    font = pygame.font.SysFont('Comic Sans MS', 25)

    # numbers
    white = (255, 255, 255)
    zero = font.render('0', True, white)
    one = font.render('1', False, white)
    two = font.render('2', False, white)
    three = font.render('3', False, white)
    four = font.render('4', False, white)
    five = font.render('5', False, white)
    six = font.render('6', False, white)
    seven = font.render('7', False, white)

    x = 5
    a = 60
    y = 930
    b = 70

    # left hand side
    screen.blit(zero, (x, a))
    screen.blit(one, (x, a + 120))
    screen.blit(two, (x, a + 225))
    screen.blit(three, (x, a + 340))
    screen.blit(four, (x, a + 455))
    screen.blit(five, (x, a + 570))
    screen.blit(six, (x, a + 685))
    screen.blit(seven, (x, a + 800))

    # bottom
    screen.blit(zero, (b, y))
    screen.blit(one, (b + 120, y))
    screen.blit(two, (b + 225, y))
    screen.blit(three, (b + 340, y))
    screen.blit(four, (b + 455, y))
    screen.blit(five, (b + 570, y))
    screen.blit(six, (b + 686, y))
    screen.blit(seven, (b + 800, y))


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


# outlines the promotion buttons when pawn promotion is applicable
def promoOutline(screen, size, toggle):

    if toggle:
        pSize = ((size/1.9)-25)/4 - 15
        buttonHeight = (size - 45)/6

        pygame.draw.rect(screen, (255, 0, 0, 50), (size + 15, 45 + pSize + buttonHeight, pSize, pSize), 5, 0, 12, 12, 12, 12)
        pygame.draw.rect(screen, (255, 0, 0, 50), (size + 25 + pSize, 45 + pSize + buttonHeight, pSize, pSize), 5, 0, 12, 12, 12, 12)
        pygame.draw.rect(screen, (255, 0, 0, 50), (size + 35 + pSize * 2, 45 + pSize + buttonHeight, pSize, pSize), 5, 0, 12, 12, 12, 12)
        pygame.draw.rect(screen, (255, 0, 0, 50), (size + 45 + pSize * 3, 45 + pSize + buttonHeight, pSize, pSize), 5, 0, 12, 12, 12, 12)


# side window and button control
def buttons(size):

    # buttons surface, transparent background
    buttonSurface = pygame.Surface((size + size/1.9, size), pygame.SRCALPHA, 32).convert_alpha()

    # draw side window
    pygame.draw.rect(buttonSurface, (33, 32, 29), (size, 25, (size/1.9)-25, size - 50), 0, 0, 12, 12, 12, 12)

    # button attributes
    buttonLength = ((size/1.9)-25 - 60)/3
    buttonHeight = (size - 45)/6
    green = (104, 136, 80)
    black = (0, 0, 0)
    font = pygame.font.SysFont('Comic Sans MS', 25)
    pSize = ((size/1.9)-25)/4 - 15
    dSize = (pSize, pSize)

    # draw gamemode buttons
    pygame.draw.rect(buttonSurface, green, (size + 15, 45, buttonLength, buttonHeight), 0, 0, 12, 12, 12, 12)
    pygame.draw.rect(buttonSurface, green, (size + 30 + buttonLength, 45, buttonLength, buttonHeight), 0, 0, 12, 12, 12, 12)
    pygame.draw.rect(buttonSurface, green, (size + 45 + buttonLength * 2, 45, buttonLength, buttonHeight), 0, 0, 12, 12, 12, 12)

    restart = pygame.transform.scale(pygame.image.load('Assets\Restart.png'), (buttonLength-15, buttonLength-15)).convert_alpha()
    twoPlayer = pygame.transform.scale(pygame.image.load('Assets\TPlayer.png'), (buttonLength, buttonLength)).convert_alpha()
    computer = pygame.transform.scale(pygame.image.load('Assets\Computer.png'), (buttonLength, buttonLength)).convert_alpha()

    # draw promotion buttons
    pygame.draw.rect(buttonSurface, green, (size + 15, 90 + buttonHeight, buttonLength * 3 + 30, buttonHeight/3), 0, 0, 12, 12, 12, 12)
    pygame.draw.rect(buttonSurface, green, (size + 15, 45 + pSize + buttonHeight, pSize, pSize), 0, 0, 12, 12, 12, 12)
    pygame.draw.rect(buttonSurface, green, (size + 25 + pSize, 45 + pSize + buttonHeight, pSize, pSize), 0, 0, 12, 12, 12, 12)
    pygame.draw.rect(buttonSurface, green, (size + 35 + pSize * 2, 45 + pSize + buttonHeight, pSize, pSize), 0, 0, 12, 12, 12, 12)
    pygame.draw.rect(buttonSurface, green, (size + 45 + pSize * 3, 45 + pSize + buttonHeight, pSize, pSize), 0, 0, 12, 12, 12, 12)
    promotion = font.render('Pawn Promotion', True, black)
    promotionRect = promotion.get_rect(center=(size + 15 + (buttonLength * 3 + 30)/2, 90 + buttonHeight + buttonHeight/6))

    # icons
    bishop = pygame.transform.scale(pygame.image.load('Assets\BishopIcon.png'), dSize).convert_alpha()
    knight = pygame.transform.scale(pygame.image.load('Assets\KnightIcon.png'), dSize).convert_alpha()
    rook = pygame.transform.scale(pygame.image.load('Assets\RookIcon.png'), dSize).convert_alpha()
    queen = pygame.transform.scale(pygame.image.load('Assets\QueenIcon.png'), dSize).convert_alpha()

    # add to surface
    buttonSurface.blit(restart, (size + 15*1.5, 60))
    buttonSurface.blit(twoPlayer, (size + 30 + buttonLength, 45*1.175))
    buttonSurface.blit(computer, (size + 45 + buttonLength * 2, 45*1.1))
    buttonSurface.blit(promotion, promotionRect)
    buttonSurface.blit(bishop, (size + 15, 45 + pSize + buttonHeight))
    buttonSurface.blit(knight, (size + 25 + pSize, 45 + pSize + buttonHeight))
    buttonSurface.blit(rook, (size + 35 + pSize * 2, 45 + pSize + buttonHeight))
    buttonSurface.blit(queen, (size + 45 + pSize * 3, 45 + pSize + buttonHeight))

    return buttonSurface


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

        if piece in {1, 11}:  # black pawn
            bPawn = pygame.transform.scale(pygame.image.load('Assets\Pawn.png'), dSize).convert_alpha()
            screen.blit(bPawn, mouseLocation)

        elif piece == 3:  # black knight
            bKnight = pygame.transform.scale(pygame.image.load('Assets\Knight.png'), dSize).convert_alpha()
            screen.blit(bKnight, mouseLocation)

        elif piece == 4:  # black bishop
            bBishop = pygame.transform.scale(pygame.image.load('Assets\Bishop.png'), dSize).convert_alpha()
            screen.blit(bBishop, mouseLocation)

        elif piece in {5, 55}:  # black rook
            bRook = pygame.transform.scale(pygame.image.load('Assets\Rook.png'), dSize).convert_alpha()
            screen.blit(bRook, mouseLocation)

        elif piece == 7:  # black queen
            bQueen = pygame.transform.scale(pygame.image.load('Assets\Queen.png'), dSize).convert_alpha()
            screen.blit(bQueen, mouseLocation)

        elif piece in {9, 99}:  # black king
            bKing = pygame.transform.scale(pygame.image.load('Assets\King.png'), dSize).convert_alpha()
            screen.blit(bKing, mouseLocation)

        elif piece in {-1, -11}:  # white pawn
            wPawn = pygame.transform.scale(pygame.image.load('Assets\wPawn.png'), dSize).convert_alpha()
            screen.blit(wPawn, mouseLocation)

        elif piece == -3:  # white knight
            wKnight = pygame.transform.scale(pygame.image.load('Assets\wKnight.png'), dSize).convert_alpha()
            screen.blit(wKnight, mouseLocation)

        elif piece == -4:  # white bishop
            wBishop = pygame.transform.scale(pygame.image.load('Assets\wBishop.png'), dSize).convert_alpha()
            screen.blit(wBishop, mouseLocation)

        elif piece in {-5, -55}:  # white rook
            wRook = pygame.transform.scale(pygame.image.load('Assets\wRook.png'), dSize).convert_alpha()
            screen.blit(wRook, mouseLocation)

        elif piece == -7:  # white queen
            wQueen = pygame.transform.scale(pygame.image.load('Assets\wQueen.png'), dSize).convert_alpha()
            screen.blit(wQueen, mouseLocation)

        elif piece in {-9, -99}:  # white king
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
def drawPieces(board, pSize, size, turn):

    if turn == -1:
        rotate = 0
    else:
        rotate = 0

    # create default size and transparent surface for pieces
    dSize = (pSize, pSize)
    pieces = pygame.Surface((size + size/1.9, size), pygame.SRCALPHA, 32).convert_alpha()

    # load & scale all pieces
    bPawn = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('Assets\Pawn.png'), dSize).convert_alpha(), rotate)
    bBishop = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('Assets\Bishop.png'), dSize).convert_alpha(), rotate)
    bKnight = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('Assets\Knight.png'), dSize).convert_alpha(), rotate)
    bRook = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('Assets\Rook.png'), dSize).convert_alpha(), rotate)
    bQueen = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('Assets\Queen.png'), dSize).convert_alpha(), rotate)
    bKing = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('Assets\King.png'), dSize).convert_alpha(), rotate)
    wPawn = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('Assets\wPawn.png'), dSize).convert_alpha(), rotate)
    wBishop = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('Assets\wBishop.png'), dSize).convert_alpha(), rotate)
    wKnight = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('Assets\wKnight.png'), dSize).convert_alpha(), rotate)
    wRook = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('Assets\wRook.png'), dSize).convert_alpha(), rotate)
    wQueen = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('Assets\wQueen.png'), dSize).convert_alpha(), rotate)
    wKing = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('Assets\wKing.png'), dSize).convert_alpha(), rotate)

    # indexes of 2D array
    x = y = -1

    # loop through the 2D array, '_' is each item in the board array (A.K.A each sub array)
    for _ in board:
        y += 1
        for n in _:
            x += 1

            if n in {1, 11}:  # black pawn
                pieces.blit(bPawn, location(x, y, pSize))

            elif n == 3:  # black knight
                pieces.blit(bKnight, location(x, y, pSize))

            elif n == 4:  # black bishop
                pieces.blit(bBishop, location(x, y, pSize))

            elif n in {5, 55}:  # black rook
                pieces.blit(bRook, location(x, y, pSize))

            elif n == 7:  # black queen
                pieces.blit(bQueen, location(x, y, pSize))

            elif n in {9, 99}:  # black king
                pieces.blit(bKing, location(x, y, pSize))

            elif n in {-1, -11}:  # white pawn
                pieces.blit(wPawn, location(x, y, pSize))

            elif n == -3:  # white knight
                pieces.blit(wKnight, location(x, y, pSize))

            elif n == -4:  # white bishop
                pieces.blit(wBishop, location(x, y, pSize))

            elif n in {-5, -55}:  # white rook
                pieces.blit(wRook, location(x, y, pSize))

            elif n == -7:  # white queen
                pieces.blit(wQueen, location(x, y, pSize))

            elif n in {-9, -99}:  # white king
                pieces.blit(wKing, location(x, y, pSize))

            else:  # empty space
                pass
        x = -1

    return pygame.transform.rotate(pieces, rotate)
