import pygame


# dictionary constant of the paths of the image of the pieces
IMAGEPATH = {
    1: 'Assets\Pawn.png', 11: 'Assets\Pawn.png', 3: 'Assets\Knight.png',
    4: 'Assets\Bishop.png', 5: 'Assets\Rook.png', 55: 'Assets\Rook.png',
    7: 'Assets\Queen.png', 9: 'Assets\King.png', 99: 'Assets\King.png',
    -1: 'Assets\wPawn.png', -11: 'Assets\wPawn.png', -3: 'Assets\wKnight.png',
    -4: 'Assets\wBishop.png', -5: 'Assets\wRook.png',  -55: 'Assets\wRook.png',
    -7: 'Assets\wQueen.png',   -9: 'Assets\wKing.png',   -99: 'Assets\wKing.png'
}


# helper function: prints the state of the board
def testBoard(board):
    for row in board:
        print(row)
    print("--------------------------------")


# prints the numbers of the board
def numBoard(screen, pSize, turn, computer, switch):

    # font
    font = pygame.font.SysFont('Comic Sans MS', 20)

    # coordinates
    w = 10 + pSize/2
    x = 5
    y = 20 + pSize * 8
    z = 20 + pSize/2

    # coordinate lists
    numCoord = [w + i * pSize for i in range(8)]
    alphaCoord = [z + i * pSize for i in range(8)]

    # turn switch
    if computer == 1 or (turn == -1 and computer is None):
        numCoord.reverse()
        alphaCoord.reverse()

    # blit to screen
    for i, (num, alpha) in enumerate(zip(['8', '7', '6', '5', '4', '3', '2', '1'], ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])):
        screen.blit(font.render(num, False, (255, 255, 255)), (x, numCoord[i]))
        screen.blit(font.render(alpha, False, (255, 255, 255)), (alphaCoord[i], y))

    return switch


# gets the position of the mouse in terms of the board tile coordinates
def getPos(pSize, size):
    mX, mY = pygame.mouse.get_pos()

    if not (25 <= mX < size - 25) or not (25 <= mY < size - 25):
        return 10, 10  # out of bounds

    else:
        return int((mX - 25) / pSize), int((mY - 25) / pSize)


# creates board surface
def createBoard(size, pSize):

    # create board surface
    tempBoard = pygame.Surface((size + size/1.9, size))

    # board colours
    green = (119, 149, 86)
    white = (235, 236, 208)
    gray = (48, 46, 43)

    # draw background
    tempBoard.fill(gray)

    # draw rounded corners
    pygame.draw.rect(tempBoard, white, (25, 25, pSize, pSize), 0, 0, 12)
    pygame.draw.rect(tempBoard, green, (pSize*7 + 25, 25, pSize, pSize), 0, 0, 0, 12)
    pygame.draw.rect(tempBoard, green, (25, pSize*7 + 25, pSize, pSize), 0, 0, 0, 0, 12)
    pygame.draw.rect(tempBoard, white, (pSize*7 + 25, pSize*7 + 25, pSize, pSize), 0, 0, 0, 0, 0, 12)

# Draw squares and rounded corners
    for y in range(8):
        for x in range(8):
            rect_color = white if (x + y) % 2 == 0 else green
            pygame.draw.rect(tempBoard, rect_color, (25 + x * pSize, 25 + y * pSize, pSize, pSize))

    return tempBoard


# toggles a tooltip at the mouse position when idle for 3 seconds
def tooltip(screen):
    x, y = pygame.mouse.get_pos()
    pygame.draw.rect(screen, (200, 0, 0), (x, y, 200, 200))


# outlines the promotion buttons when pawn promotion is applicable
def promoOutline(screen, size, toggle):

    if toggle:
        pSize = ((size/1.9)-25)/4 - 15
        buttonHeight = (size - 45)/6

        colour = (200, 0, 0, 50)
        pygame.draw.rect(screen, colour, (size + 15, 115 + buttonHeight + buttonHeight/3, pSize, pSize), 5, 0, 12, 12, 12, 12)
        pygame.draw.rect(screen, colour, (size + 25 + pSize, 115 + buttonHeight + buttonHeight/3, pSize, pSize), 5, 0, 12, 12, 12, 12)
        pygame.draw.rect(screen, colour, (size + 35 + pSize * 2, 115 + buttonHeight + buttonHeight/3, pSize, pSize), 5, 0, 12, 12, 12, 12)
        pygame.draw.rect(screen, colour, (size + 45 + pSize * 3, 115 + buttonHeight + buttonHeight/3, pSize, pSize), 5, 0, 12, 12, 12, 12)


# adds additional dialouge into the list
def addText(array, text):
    try:
        index = array.index("")
        array[index] = text
    except ValueError:
        array.pop(0)
        array.append(text)


# clears the dialouge list
def clearText(array):

    for i in range(len(array)):
        array[i] = ""
    return array


# states the move of the board
# also display check, checkmate, castle and winner
def dialouge(size, text):
    # buttons surface, transparent background
    dialougeSurf = pygame.Surface((size + size/1.9, size), pygame.SRCALPHA, 32).convert_alpha()
    buttonHeight = (size - 45)/6
    black = (0, 0, 0)
    font = pygame.font.SysFont('Comic Sans MS', 27)
    white = (255, 255, 255)

    # Calculate dimensions for the rectangle
    x = size + 15
    y = 115 + 2 * buttonHeight + buttonHeight/3
    w = (size/1.9) - 55
    h = size - (165 + 2 * buttonHeight + buttonHeight/3)

    # Draw the rectangle
    pygame.draw.rect(dialougeSurf, black, (x, y, w, h), 0, 0, 12, 12, 12, 12)

    # Render and blit text
    for i, txt in enumerate(text):
        render = font.render(txt, False, white)
        height = 130 + 2 * buttonHeight + buttonHeight/3 + 45 * i
        dialougeSurf.blit(render, (size + 30, height))

    return dialougeSurf


# side window and button control
def buttons(size):

    # buttons surface, transparent background
    buttonSurface = pygame.Surface((size + size/1.9, size), pygame.SRCALPHA, 32).convert_alpha()

    # draw side window
    pygame.draw.rect(buttonSurface, (33, 32, 29), (size, 25, (size/1.9)-25, size - 50), 0, 0, 12, 12, 12, 12)

    # button attributes
    buttonLength = ((size/1.9)-25 - 60)/3
    buttonHeight = (size - 45)/6
    brown = (129, 95, 71)
    black = (0, 0, 0)
    font = pygame.font.SysFont('Comic Sans MS', int((size / 960) * 25))
    pSize = ((size/1.9)-25)/4 - 15
    dSize = (pSize, pSize)

    # draw gamemode buttons
    for i in range(3):
        pygame.draw.rect(buttonSurface, brown, (size + 15 + (buttonLength + 15) * i, 45, buttonLength, buttonHeight), 0, 0, 12, 12, 12, 12)

    restart = pygame.transform.scale(pygame.image.load('Assets\Restart.png'), (buttonLength-45, buttonLength-45)).convert_alpha()
    twoPlayer = pygame.transform.scale(pygame.image.load('Assets\TPlayer.png'), (buttonLength, buttonLength)).convert_alpha()
    computer = pygame.transform.scale(pygame.image.load('Assets\Computer.png'), (buttonLength, buttonLength)).convert_alpha()

    # draw promotion buttons
    for i in range(4):
        pygame.draw.rect(buttonSurface, brown, (size + 15 + (pSize + 10) * i, 115 + buttonHeight + buttonHeight/3, pSize, pSize), 0, 0, 12, 12, 12, 12)

    promotion = font.render('Pawn Promotion', True, black)
    promotionRect = promotion.get_rect(center=(size + 15 + (buttonLength * 3 + 30)/2, 105 + buttonHeight + buttonHeight/6))

    s = pygame.Rect(size + 15, 105 + buttonHeight, promotionRect.width + 40, buttonHeight/3)
    s.center = promotionRect.center
    pygame.draw.rect(buttonSurface, brown, s, 0, 0, 12, 12, 12, 12)

    # icons
    bishop = pygame.transform.scale(pygame.image.load('Assets\BishopIcon.png'), dSize).convert_alpha()
    knight = pygame.transform.scale(pygame.image.load('Assets\KnightIcon.png'), dSize).convert_alpha()
    rook = pygame.transform.scale(pygame.image.load('Assets\RookIcon.png'), dSize).convert_alpha()
    queen = pygame.transform.scale(pygame.image.load('Assets\QueenIcon.png'), dSize).convert_alpha()

    # add to surface
    buttonSurface.blit(restart, (size + 22.5*1.5, 75))
    buttonSurface.blit(twoPlayer, (size + 30 + buttonLength, 45*1.175))
    buttonSurface.blit(computer, (size + 45 + buttonLength * 2, 45*1.1))
    buttonSurface.blit(promotion, promotionRect)
    buttonSurface.blit(bishop, (size + 15, 115 + buttonHeight + buttonHeight/3))
    buttonSurface.blit(knight, (size + 25 + pSize, 115 + buttonHeight + buttonHeight/3))
    buttonSurface.blit(rook, (size + 35 + pSize * 2, 115 + buttonHeight + buttonHeight/3))
    buttonSurface.blit(queen, (size + 45 + pSize * 3, 115 + buttonHeight + buttonHeight/3))

    return buttonSurface


# computes the location from the array indexes
def location(a, b, pSize):
    return (25 + (a*pSize), 25 + (b * pSize))


# rotates board
def rotate(board, computer):
    if computer == None:
        return [x[::-1] for x in board[::-1]]
    else:
        return board


# creates a 'dragging' animation for the pieces
def drag(screen, selected, pSize, size):
    if selected != None:
        piece = selected[0]
        dSize = (pSize, pSize)
        mX, mY = pygame.mouse.get_pos()
        mouseLocation = (mX - pSize/2, mY - pSize/2)
        x, y = getPos(pSize, size)

        # draw where piece will land according to mouse location
        pygame.draw.rect(screen, (3, 80, 200, 50), ((x * pSize)+25, (y * pSize)+25, pSize, pSize), 5)

        # Load and scale piece images
        path = IMAGEPATH[piece]
        image = pygame.transform.scale(pygame.image.load(path), dSize).convert_alpha()
        screen.blit(image, mouseLocation)


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
    pieces = pygame.Surface((size + size/1.9, size), pygame.SRCALPHA, 32).convert_alpha()

    # Load and scale piece images
    image = {key: pygame.transform.scale(pygame.image.load(path), dSize).convert_alpha() for key, path in IMAGEPATH.items()}

    # indexes of 2D array
    x = y = -1

    # loop through the 2D array, '_' is each item in the board array (A.K.A each sub array)
    for row in board:
        y += 1
        for piece in row:
            x += 1
            if piece in image:
                pieces.blit(image[piece], location(x, y, pSize))
        x = -1

    return pieces
