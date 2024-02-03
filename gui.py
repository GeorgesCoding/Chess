import pygame


# main control function
def main():

    # automatically changes game size according to monitor size
    pygame.init()
    size = pygame.display.Info().current_h
    size = size - 120
    pSize = (size-50)/8
    oldMouse = 0, 0

    # initialize window
    screen = pygame.display.set_mode((size, size))

    # customize window
    pygame.display.set_caption("Chess")
    icon = pygame.image.load('Assets\icon.png')
    pygame.display.set_icon(icon)
    screen.fill(pygame.Color(48, 46, 43))

    # 2D array to represent state of board
    board = [[5, 3, 4, 7, 9, 4, 3, 5], [1]*8, [0]*8, [0]*8, [0]*8, [0]*8, [-1]*8, [-5, -3, -4, -7, -9, -4, -3, -5]]
    """
    Each sub array is a row in the board
    The elements in each sub array are the individual spaces on the board in that row
    Initialized to the starting position of the board
    Black is positive, white is negative, zero is an empty space
    [y][x]
    """

    # draw board & pieces
    boardSurface = createBoard(size, pSize)
    piecesSurface = drawPieces(board, pSize, size)

    # selected piece variable
    selected = None

    # main loop
    while True:
        piece, x, y = getPiece(board, pSize, size)  # checks if there is a piece under the mouse
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if piece != 10:
                    selected = piece, x, y  # piece is selected, toggles selected variable
                    board[y][x] = 0  # remove piece from board
                    pygame.draw.rect(boardSurface, (244, 246, 128, 50), ((x * pSize), (y * pSize), pSize, pSize), 5)  # outline old space
                    piecesSurface = drawPieces(board, pSize, size)

            if event.type == pygame.MOUSEBUTTONUP:
                if selected != None:
                    tempPiece = selected[0]
                    newX, newY = getPos(pSize, size)
                    if newX != 10: # if mouse go outside of board
                        
                        board[newY][newX] = tempPiece
                        boardSurface = createBoard(size, pSize)
                        piecesSurface = drawPieces(board, pSize, size)
                        selected = None
                    else:
                        oldMouse = newX, newY


        # add surfaces to screen
        screen.blit(boardSurface, (25, 25))
        screen.blit(piecesSurface, (0, 0))
        
        # creates 'dragging' animation for pieces
        drag(screen, selected, pSize, size)

        # update display
        pygame.display.flip()


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
    tempBoard = pygame.Surface((size-50, size-50))

    # board colours
    green = (119, 149, 86)
    white = (235, 236, 208)

    # draw boards
    for y in range(0, 8, 2):
        for x in range(0, 8, 2):
            pygame.draw.rect(tempBoard, white, (pSize*x, pSize*y, pSize, pSize))
            pygame.draw.rect(tempBoard, green, ((x + 1)*pSize, pSize*y, pSize, pSize))
            pygame.draw.rect(tempBoard, white, ((x + 1)*pSize, (y + 1)*pSize, pSize, pSize))
            pygame.draw.rect(tempBoard, green, (pSize*x, (y + 1)*pSize, pSize, pSize))

    return tempBoard


# computes the location from the array indexes
def location(a, b, pSize):
    return (25 + (a*pSize), 25 + (b * pSize))


# creates a 'dragging' animation for the pieces
def drag(screen, selected, pSize, size):
    if selected != None:

        piece = selected[0]
        dSize = (pSize, pSize)
        mX, mY = pygame.mouse.get_pos()
        mouseLocation = (mX - (pSize/2), mY - (pSize/2))
        x, y = getPos(pSize, size)

        if x != 10:
            pygame.draw.rect(screen, (3, 80, 200, 50), ((x * pSize)+25, (y * pSize)+25, pSize, pSize), 5)

            if piece == 1:  # black pawn
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

            elif piece == -1:  # white pawn
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
    if x != 10:
        if board[y][x] != 0:
            return board[y][x], x, y
        else:
            return 10, 10, 10
    else:
        return 10, 10, 10


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

            if n == 1:  # black pawn
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

            elif n == -1:  # white pawn
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


if __name__ == '__main__':
    main()
