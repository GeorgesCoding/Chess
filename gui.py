import pygame


# main control function
def main():

    # initialize window
    screen = pygame.display.set_mode((1250, 1250))

    # customize window
    pygame.display.set_caption("Chess")
    programIcon = pygame.image.load('Assets\icon.png')
    pygame.display.set_icon(programIcon)
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
    boardSurface = createBoard()
    piecesSurface = drawPieces(board)

    # selected piece variable
    selected = None

    # main loop
    while True:
        piece, x, y = getPiece(board)  # checks if there is a piece under the mouse
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if piece != 10:
                    selected = piece, x, y  # piece is selected, toggles selected variable
                    board[y][x] = 0  # remove piece from board
                    pygame.draw.rect(boardSurface, (244, 246, 128, 50), ((x * 150), (y * 150), 150, 150), 5)  # outline old space
                    piecesSurface = drawPieces(board)

            if event.type == pygame.MOUSEBUTTONUP:
                if selected != None:
                    tempPiece = selected[0]
                    newX, newY = getPos()
                    board[newY][newX] = tempPiece
                    boardSurface = createBoard()
                    piecesSurface = drawPieces(board)
                    selected = None

        # add surfaces to screen
        screen.blit(boardSurface, (25, 25))
        screen.blit(piecesSurface, (0, 0))

        # creates 'dragging' animation for pieces
        drag(screen, selected, boardSurface)

        # update display
        pygame.display.flip()


# gets the position of the mouse in terms of the board tile coordinates
def getPos():
    mX, mY = pygame.mouse.get_pos()

    if mX >= 1225 or mY >= 1225 or mX < 25 or mY < 25:
        return 10, 10  # out of bounds

    else:
        x = int((mX-25) / 150)
        y = int((mY-25) / 150)
        return x, y


# creates board surface
def createBoard():

    # create board surface
    tempBoard = pygame.Surface((1200, 1200))

    # board colours
    green = (119, 149, 86)
    white = (235, 236, 208)

    # draw boards
    for y in range(0, 8, 2):
        for x in range(0, 8, 2):
            pygame.draw.rect(tempBoard, white, (150*x, 150*y, 150, 150))
            pygame.draw.rect(tempBoard, green, ((x + 1)*150, 150*y, 150, 150))
            pygame.draw.rect(tempBoard, white, ((x + 1)*150, (y + 1)*150, 150, 150))
            pygame.draw.rect(tempBoard, green, (150*x, (y + 1)*150, 150, 150))

    return tempBoard


# computes the location from the array indexes
def location(a, b):
    return (25 + (a * 150), 25 + (b * 150))


# creates a 'dragging' animation for the pieces
def drag(screen, selected, boardSurface):
    if selected != None:

        piece = selected[0]
        size = (150, 150)
        mX, mY = pygame.mouse.get_pos()
        mouseLocation = (mX - 75, mY - 75)

        x, y = getPos()
        if x != 10:
            pygame.draw.rect(screen, (3, 80, 200, 50), ((x * 150)+25, (y * 150)+25, 150, 150), 5)

        if piece == 1:  # black pawn
            bPawn = pygame.transform.scale(pygame.image.load('Assets\Pawn.png'), size).convert_alpha()
            screen.blit(bPawn, mouseLocation)

        elif piece == 3:  # black knight
            bKnight = pygame.transform.scale(pygame.image.load('Assets\Knight.png'), size).convert_alpha()
            screen.blit(bKnight, mouseLocation)

        elif piece == 4:  # black bishop
            bBishop = pygame.transform.scale(pygame.image.load('Assets\Bishop.png'), size).convert_alpha()
            screen.blit(bBishop, mouseLocation)

        elif piece == 5:  # black rook
            bRook = pygame.transform.scale(pygame.image.load('Assets\Rook.png'), size).convert_alpha()
            screen.blit(bRook, mouseLocation)

        elif piece == 7:  # black queen
            bQueen = pygame.transform.scale(pygame.image.load('Assets\Queen.png'), size).convert_alpha()
            screen.blit(bQueen, mouseLocation)

        elif piece == 9:  # black king
            bKing = pygame.transform.scale(pygame.image.load('Assets\King.png'), size).convert_alpha()
            screen.blit(bKing, mouseLocation)

        elif piece == -1:  # white pawn
            wPawn = pygame.transform.scale(pygame.image.load('Assets\wPawn.png'), size).convert_alpha()
            screen.blit(wPawn, mouseLocation)

        elif piece == -3:  # white knight
            wKnight = pygame.transform.scale(pygame.image.load('Assets\wKnight.png'), size).convert_alpha()
            screen.blit(wKnight, mouseLocation)

        elif piece == -4:  # white bishop
            wBishop = pygame.transform.scale(pygame.image.load('Assets\wBishop.png'), size).convert_alpha()
            screen.blit(wBishop, mouseLocation)

        elif piece == -5:  # white rook
            wRook = pygame.transform.scale(pygame.image.load('Assets\wRook.png'), size).convert_alpha()
            screen.blit(wRook, mouseLocation)

        elif piece == -7:  # white queen
            wQueen = pygame.transform.scale(pygame.image.load('Assets\wQueen.png'), size).convert_alpha()
            screen.blit(wQueen, mouseLocation)

        elif piece == -9:  # white king
            wKing = pygame.transform.scale(pygame.image.load('Assets\wKing.png'), size).convert_alpha()
            screen.blit(wKing, mouseLocation)


# gets the piece of the current mouse position
def getPiece(board):
    x, y = getPos()
    if x != 10:
        if board[y][x] != 0:
            return board[y][x], x, y
        else:
            return 10, 10, 10
    else:
        return 10, 10, 10


# draws the pieces in their positions according to the 2D board array
def drawPieces(board):

    # create default size and transparent surface for pieces
    size = (150, 150)
    pieces = pygame.Surface((1200, 1250), pygame.SRCALPHA, 32).convert_alpha()

    # load & scale all pieces
    bPawn = pygame.transform.scale(pygame.image.load('Assets\Pawn.png'), size).convert_alpha()
    bBishop = pygame.transform.scale(pygame.image.load('Assets\Bishop.png'), size).convert_alpha()
    bKnight = pygame.transform.scale(pygame.image.load('Assets\Knight.png'), size).convert_alpha()
    bRook = pygame.transform.scale(pygame.image.load('Assets\Rook.png'), size).convert_alpha()
    bQueen = pygame.transform.scale(pygame.image.load('Assets\Queen.png'), size).convert_alpha()
    bKing = pygame.transform.scale(pygame.image.load('Assets\King.png'), size).convert_alpha()
    wPawn = pygame.transform.scale(pygame.image.load('Assets\wPawn.png'), size).convert_alpha()
    wBishop = pygame.transform.scale(pygame.image.load('Assets\wBishop.png'), size).convert_alpha()
    wKnight = pygame.transform.scale(pygame.image.load('Assets\wKnight.png'), size).convert_alpha()
    wRook = pygame.transform.scale(pygame.image.load('Assets\wRook.png'), size).convert_alpha()
    wQueen = pygame.transform.scale(pygame.image.load('Assets\wQueen.png'), size).convert_alpha()
    wKing = pygame.transform.scale(pygame.image.load('Assets\wKing.png'), size).convert_alpha()

    # indexes of 2D array
    x = y = -1

    # loop through the 2D array, '_' is each item in the board array (A.K.A each sub array)
    for _ in board:
        y += 1
        for n in _:
            x += 1

            if n == 1:  # black pawn
                pieces.blit(bPawn, location(x, y))

            elif n == 3:  # black knight
                pieces.blit(bKnight, location(x, y))

            elif n == 4:  # black bishop
                pieces.blit(bBishop, location(x, y))

            elif n == 5:  # black rook
                pieces.blit(bRook, location(x, y))

            elif n == 7:  # black queen
                pieces.blit(bQueen, location(x, y))

            elif n == 9:  # black king
                pieces.blit(bKing, location(x, y))

            elif n == -1:  # white pawn
                pieces.blit(wPawn, location(x, y))

            elif n == -3:  # white knight
                pieces.blit(wKnight, location(x, y))

            elif n == -4:  # white bishop
                pieces.blit(wBishop, location(x, y))

            elif n == -5:  # white rook
                pieces.blit(wRook, location(x, y))

            elif n == -7:  # white queen
                pieces.blit(wQueen, location(x, y))

            elif n == -9:  # white king
                pieces.blit(wKing, location(x, y))

            else:  # empty space
                pass
        x = -1

    return pieces


if __name__ == '__main__':
    main()
