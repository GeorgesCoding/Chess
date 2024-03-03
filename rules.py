import pygame
import random
from gui import getPiece, getPos, addText
from main import PIECE


BLACK = -1
WHITE = 1


# toggles the turn
def playerTurn(colour, turn):
    return (colour == BLACK) == (turn == 1)


# determines if move is legal or not
# if the new position is in the list of legal moves, return true
def move(piece, newY, newX, oldY, oldX, board, canPassant):

    if piece in {-11, 11, 1, -1}:
        moves = pawnMove(piece, oldY, oldX, board, 0, canPassant)

    elif piece in {5, -5, 55, -55}:
        moves = rookMove(piece, oldY, oldX, board)

    elif piece in {3, -3}:
        moves = knightMove(piece, oldY, oldX, board)

    elif piece in {4, -4}:
        moves = bishopMove(piece, oldY, oldX, board)

    elif piece in {7, -7}:
        moves = queenMove(piece, oldY, oldX, board)

    elif piece in {9, -9, -99, 99}:
        moves = kingMove(piece, oldY, oldX, board)

    return ((newY, newX) in moves)


# determines if a set of coordinates are in bounds
def inBounds(newX, newY):
    return 0 <= newX <= 7 and 0 <= newY <= 7


# determines if the pawn moved two spaces in first turn
# used for en passant computations
def pawnFirst(piece, newY, newX, oldY, oldX):
    return piece in {-11, 11} and newX == oldX and newY == oldY - 2


# removes the pawn captured through en passant
# special because the pawn doesn't overtake the captured pawn's space
def enPassantCapture(piece, board, newY, newX, oldY, oldX, isPawn, canPassant):
    if isPawn and (7 - oldY, 7 - oldX) in canPassant and piece in {-1, 11, -11, 1} and spaceCheck(piece, board, newY, newX):
        board[newY + 1][newX] = 0


# the default check for computing legal moves
# True for valid space, false for invalid
def spaceCheck(piece, board, newY, newX):
    return inBounds(newX, newY) and (board[newY][newX] == 0 or pieceColour(board[newY][newX]) == pieceColour(-piece))


# toggles first move ability of pawn
# also determines if king can castle
# returns true if it is a pawn that moved
def firstMove(tempPiece, board, newY, newX):

    if tempPiece in {11, -11}:
        board[newY][newX] = tempPiece // 11

    elif tempPiece in {-9, 9, -5, 5}:
        board[newY][newX] = tempPiece * 11


# determines if en passant is a possible move
# checks when a pawn moves two spaces
def enPassant(piece, y, x, board, isPawn):
    colour = pieceColour(-piece)
    canPassant = []

    if isPawn:
        canPassant.append((y, x))
        if inBounds(x - 1, y) and pieceColour(board[y][x - 1]) == colour:
            canPassant.append((y, x - 1))
        if inBounds(x + 1, y) and pieceColour(board[y][x + 1]) == colour:
            canPassant.append((y, x + 1))

    return canPassant


# finds the opposite colour of the piece
def pieceColour(piece):
    if piece < 0:
        return BLACK
    elif piece == 0:
        return 0
    else:
        return WHITE


# computes legal pawn moves
def pawnMove(piece, y, x, board, opposite, canPassant):

    moves = set()
    a = -1 if opposite == 1 else 1
    b = -2 if opposite == 1 else 2

    if board[y - a][x] == 0:
        moves.add((y - a, x))  # forward one space

    if piece in {-11, 11}:
        if board[y - b][x] == 0:  # first move
            moves.add((y - b, x))

    if spaceCheck(piece, board, y - a, x + 1) and board[y - a][x + 1] != 0:  # right capture
        moves.add((y - a, x + 1))

    if spaceCheck(piece, board, y - a, x - 1) and board[y - a][x - 1] != 0:  # left capture
        moves.add((y - a, x - 1))

    if (7 - y, 7 - x) in canPassant:
        if 7 - canPassant[0][1] - x == 1:
            moves.add((y - a, x + 1))
        else:
            moves.add((y - a, x - 1))

    return moves


# in first array, each index is a seperate array for each piece
# first index in subarray is the piece
# second is the location
# third index is the set of the legal moves
def moveChoose(piece, y, x, board, opposite, canPassant, kingPass):
    specificMoves = []
    colour = pieceColour(piece)
    x = 0

    for b, row in enumerate(board):
        for a, n in enumerate(row):
            if pieceColour(-n) == colour:

                if n in {-1, 1, 11, -11}:
                    specificMoves[x][2] = pawnMove(n, y, x, board, opposite, canPassant)

                elif n in {5, -5, 55, -55}:
                    specificMoves[x][2] = pawnMove(n, y, x, board, opposite, canPassant)

                elif n in {3, -3}:
                    specificMoves[x][2] = pawnMove(n, y, x, board, opposite, canPassant)

                elif n in {4, -4}:
                    specificMoves[x][2] = pawnMove(n, y, x, board, opposite, canPassant)

                elif n in {7, -7}:
                    specificMoves[x][2] = pawnMove(n, y, x, board, opposite, canPassant)

                elif n in {9, -9, 99, -99} and kingPass != 1:
                    specificMoves[x][2] = pawnMove(n, y, x, board, opposite, canPassant)

                specificMoves[x][0] = n
                specificMoves[x][1] = (b, a)
                x += 1


# computes legal knight moves
def knightMove(piece, y, x, board):
    moves = set()
    xMove = [-2, -1, 1, 2]
    yMove = [1, 2, 2, 1]

    for a, b in zip(xMove, yMove):
        if spaceCheck(piece, board, (y + b), (x + a)):
            moves.add((y + b, x + a))

        if spaceCheck(piece, board, (y - b), (x + a)):
            moves.add((y - b, x + a))

    return moves


# general move pattern for bishop & rook
def bishopRookCompute(piece, y, x, board, xMove, yMove):
    moves = set()

    for a, b in zip(xMove, yMove):
        tempX, tempY = x + a, y + b
        while (spaceCheck(piece, board, tempY, tempX)):
            moves.add((tempY, tempX))
            if board[tempY][tempX] != 0:
                break
            tempY += b
            tempX += a

    return moves


# computes legal bishop moves
def bishopMove(piece, y, x, board):
    xMove = [1, 1, -1, -1]
    yMove = [1, -1, 1, -1]

    return bishopRookCompute(piece, y, x, board, xMove, yMove)


# computes legal rook moves
def rookMove(piece, y, x, board):
    xMove = [-1, 1, 0, 0]
    yMove = [0, 0, -1, 1]

    return bishopRookCompute(piece, y, x, board, xMove, yMove)


# computes legal queen moves
def queenMove(piece, y, x, board):
    return bishopMove(piece, y, x, board) | rookMove(piece, y, x, board)


# computes possible king moves
def kingMove(piece, y, x, board):
    moves = set()
    moveX = [1, 0, -1]
    moveY = [1, 0, -1]

    for b in moveY:
        for a in moveX:
            if spaceCheck(piece, board, y + b, x + a):
                moves.add((y + b, x + a))

    return moves


# computes all possible moves for the piece's opposite colour
# kingPass is to ignore the kings movements
# used when determining checkmate to avoid infinite recursion
def computeAll(king, board, kingPass, opposite, canPassant):
    moves = set()
    colour = pieceColour(king)

    for y, row in enumerate(board):
        for x, n in enumerate(row):
            if pieceColour(-n) == colour:
                if n in {-1, 1, 11, -11}:
                    moves |= pawnMove(n, y, x, board, opposite, canPassant)

                elif n in {5, -5, 55, -55}:
                    moves |= rookMove(n, y, x, board)

                elif n in {3, -3}:
                    moves |= knightMove(n, y, x, board)

                elif n in {4, -4}:
                    moves |= bishopMove(n, y, x, board)

                elif n in {7, -7}:
                    moves |= queenMove(n, y, x, board)

                elif n in {9, -9, 99, -99} and kingPass != 1:
                    moves |= kingMove(n, y, x, board)

    return moves


# returns the coordinates of the piece's colour king
def kingCoord(piece, board):
    y = x = -1

    king = {-9, -99} if piece < 0 else {9, 99}

    for y, row in enumerate(board):
        for x, z in enumerate(row):
            if z in king:
                return y, x


# determines if the king can castle
# returns true to castle the king
def castle(piece, board, oldY, oldX, pSize, size, moveList, tempBoard, text):
    mX, mY = getPos(pSize, size)
    tempX = mX
    rook = getPiece(board, pSize, size)[0]

    # pieces unmoved & determines LH or RH castle
    if piece in {9, -9} and rook in {5, -5}:
        temp = 1 if mX == 0 else -1
        kingX = oldX - 2 * temp
        rookX = kingX + temp
        side = " leftwards castle" if temp == 1 else " rightwards castle"

        # empty inbetween spaces
        while (mX != oldX):
            if board[oldY][mX + temp] != 0:
                return False
            mX += temp

        # check if king in check
        if kingCoord(piece, tempBoard) in moveList:
            return False
        else:
            board[oldY][kingX] = piece
            board[oldY][rookX] = rook
            firstMove(piece, board, oldY, kingX)
            firstMove(rook, board, oldY, rookX)
            board[mY][tempX] = 0
            addText(text, str(PIECE[piece]) + str(side))
            return True
    return False


# evaluates if a button is pressed
# also dictates pawn promotion behaviour
def button(selection, info, promotedPiece, board):

    pressed = pygame.mouse.get_pos()[0] in range(info[0], info[2] + info[0]) and pygame.mouse.get_pos()[1] in range(info[1], info[3] + info[1])
    pawn = "Black"

    # promotion buttonss
    if pressed and selection != 0:
        piece, y, x = promotedPiece

        # map selection to newPiece type
        pieceMap = {1: 4, 2: 3, 3: 55, 4: 7}
        newPiece = pieceMap.get(selection, None)

        if piece < 0:
            newPiece = -newPiece
            pawn = "White"

        board[y][x] = newPiece

        print(pawn + " pawn promoted to " + PIECE[newPiece])

    return pressed


# evaluates if king is in checkmate
# False for no, true for yes
def checkmate(king, board, x, y, canPassant, opposite):
    moveList = computeAll(king, board, 0, opposite, canPassant)

    # check if the king is the only piece and it cannot move
    if kingCoord(king, board) in moveList:  # king in check
        kingsList = kingMove(king, y, x, board)
        tempBoard = [row[:] for row in board]
        canMove = False
        for (newY, newX) in kingsList:
            if (newY, newX) not in moveList:  # king still in check after move
                canMove = True
                break
            opposite = 0 if opposite == 1 else 1
        if canMove:
            return False
        else:
            moveList = computeAll(-king, board, 1, opposite, canPassant)
            tempPiece = -1 if king < 0 else 1

            opposite = 0 if opposite == 1 else 1

            for (newY, newX) in moveList:
                tempBoard[newY][newX] = tempPiece
                tempMoveList = computeAll(king, tempBoard, 0, opposite, canPassant)

                if kingCoord(king, tempBoard) not in tempMoveList:  # king not in check after move
                    canMove = True
                    break

                # resets tempBoard
                tempBoard = [row[:] for row in board]

            return not canMove

    else:
        return False


# determines if the game has ended through checkmate
def gameEnd(board, turn, pieceMoving, start, outline, canPassant, opposite, text):
    if outline or (not start and (kingCoord(-turn, board) == None)) or (pieceMoving):
        pass
    else:
        kY, kX = kingCoord(-turn, board)
        king = board[kY][kX]
        if checkmate(king, board, kX, kY, canPassant, opposite):
            winner = "Black" if pieceColour(king) < 0 else "White"
            addText(text, "Checkmate: " + str(winner) + " won!")
            addText(text, "Press restart or exit the game.")
            return True


# temporary function
# randomly decides moves for the computer
def randomMove(king, board, canPassant):
    return


# returns a random turn for the user
def randomTurn():
    return random.choice((BLACK, WHITE))
