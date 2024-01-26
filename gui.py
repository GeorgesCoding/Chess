import pygame


# main control function
def main():

    # initialize window
    screen = pygame.display.set_mode((1250, 1250))

    # customize window
    pygame.display.set_caption("Chess")
    programIcon = pygame.image.load('icon.png')
    pygame.display.set_icon(programIcon)
    screen.fill(pygame.Color(48, 46, 43))

    clock = pygame.time.Clock()

    # 2D array to represent state of board
    board = [[5, 3, 4, 7, 9, 4, 3, 5], [1]*8, [0]*8, [0]*8, [0]*8, [0]*8, [-1]*8, [-5, -3, -4, -7, -9, -4, -3, -5]]
    """
    Each sub array is a row in the board
    The elements in each sub array are the individual spaces on the board in that row
    Initialized to the starting position of the board
    Black is positive, white is negative, zero is an empty space
    """

    # draw board & pieces
    boardSurface = createBoard()
    piecesSurface = drawPieces(board)

    # variables for moving pieces
    selected = None
    drop = None

    # main loop
    while True:
        piece, x, y = getPiece(board)  # checks if there is a piece under the mouse

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if piece != 10:
                    selected = piece  # piece is selected, toggles 'selected variable

        # add surfaces to screen
        screen.blit(boardSurface, (25, 25))
        screen.blit(piecesSurface, (0, 0))

        # outline mouse
        outline(screen)

        # update display
        pygame.display.flip()
        clock.tick(60)


# gets the position of the mouse in terms of the board tile coordinates
def getPos():
    mX, mY = pygame.mouse.get_pos()

    if mX >= 1225 or mY >= 1225 or mX < 25 or mY < 25:
        return 10, 10  # out of bounds

    else:
        x = int((mX-25) / 150)
        y = int((mY-25) / 150)
        return x, y


# outlines the space where the mouse is
def outline(screen):
    x, y = getPos()
    if x != 10:
        pygame.draw.rect(screen, (255, 0, 0, 50), ((x * 150)+25, (y * 150)+25, 150, 150), 2)


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


# computes the location from the array index
def location(a, b):
    return (25 + (a * 150), 25 + (b * 150))


# creates a 'dragging' animation for the pieces
def drag(screen, selected, board):
    if selected != None:
        piece = getPiece(board)
        x, y = getPos()
        if x != 10:
            pygame.draw.rect(screen, (0, 255, 0, 50), ((x * 150)+25, (y * 150)+25, 150, 150), 2)


# gets the piece of the current mouse position
def getPiece(board):
    x, y = getPos()
    if x != 10:
        if board[x][y] != 0:
            return board[x][y], x, y
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
    bPawn = pygame.transform.scale(pygame.image.load('Pieces\Pawn.png'), size).convert_alpha()
    bBishop = pygame.transform.scale(pygame.image.load('Pieces\Bishop.png'), size).convert_alpha()
    bKnight = pygame.transform.scale(pygame.image.load('Pieces\Knight.png'), size).convert_alpha()
    bRook = pygame.transform.scale(pygame.image.load('Pieces\Rook.png'), size).convert_alpha()
    bQueen = pygame.transform.scale(pygame.image.load('Pieces\Queen.png'), size).convert_alpha()
    bKing = pygame.transform.scale(pygame.image.load('Pieces\King.png'), size).convert_alpha()
    wPawn = pygame.transform.scale(pygame.image.load('Pieces\wPawn.png'), size).convert_alpha()
    wBishop = pygame.transform.scale(pygame.image.load('Pieces\wBishop.png'), size).convert_alpha()
    wKnight = pygame.transform.scale(pygame.image.load('Pieces\wKnight.png'), size).convert_alpha()
    wRook = pygame.transform.scale(pygame.image.load('Pieces\wRook.png'), size).convert_alpha()
    wQueen = pygame.transform.scale(pygame.image.load('Pieces\wQueen.png'), size).convert_alpha()
    wKing = pygame.transform.scale(pygame.image.load('Pieces\wKing.png'), size).convert_alpha()

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
