import pygame
from gui import *
import sys

""" 
========================
=== NOTES FOR VIEWER ===
========================
• All legal moves are computed in terms of a list
• If the new position is in that list, then the move is legal
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


# determines if move is legal or not
# if the new position is in the lis t of legal moves, return true
def move(piece, newY, newX, oldY, oldX, board):

    # lists for piece identification
    pawn = -11, 11, 1, -1
    rook = 5, -5, 55, -55
    knight = 3, -3
    bishop = 4, -4
    queen = 7, -7
    king = 9, -9, -99, 99

    if piece in pawn:
        moves = pawnMove(piece, oldY, oldX, board)
        return ((newY, newX) in moves)

    elif piece in rook:
        moves = rookMove(piece, oldY, oldX, board)
        return ((newY, newX) in moves)

    elif piece in knight:
        moves = knightMove(piece, oldY, oldX, board)
        return ((newY, newX) in moves)

    elif piece in bishop:
        moves = bishopMove(piece, oldY, oldX, board)
        return ((newY, newX) in moves)

    elif piece in queen:
        moves = queenMove(piece, oldY, oldX, board)
        return ((newY, newX) in moves)

    elif piece in king:
        moves = kingMove(piece, oldY, oldX, board)
        return ((newY, newX) in moves)


# determines if a set of coordinates are in bounds
def inBounds(newX, newY):
    if newX < 0 or newX > 7 or newY < 0 or newY > 7:
        return False
    else:
        return True


# the default check for computing legal moves
# True for valid space, false for invalid
def spaceCheck(piece, board, newY, newX):
    if inBounds(newX, newY):
        if board[newY][newX] == 0:
            return True
        elif pieceColour(board[newY][newX]) == pieceColour(-piece):
            return True
        else:
            return False
    else:
        return False


# toggles first move ability of pawn
# also determines if king can castle
def firstMove(tempPiece, board, newY, newX):

    if tempPiece == 11:
        board[newY][newX] = 1

    elif tempPiece == -11:
        board[newY][newX] = -1

    elif tempPiece == -9:
        board[newY][newX] = -99

    elif tempPiece == 9:
        board[newY][newX] = 99

    elif tempPiece == -5:
        board[newY][newX] = -55

    elif tempPiece == 5:
        board[newY][newX] = 55


# finds the opposite colour of the piece
def pieceColour(piece):
    if piece < 0:
        return "Black"
    else:
        return "White"


# computes legal pawn moves
def pawnMove(piece, y, x, board):

    moves = []

    if piece > 0:  # black piece
        if board[y+1][x] == 0:
            moves.append((y+1, x))  # forward one space

        if piece == 11 and board[y+2][x] == 0:  # first move
            moves.append((y+2, x))

        if spaceCheck(piece, board, y + 1, x + 1) and board[y+1][x+1] != 0:  # right capture
            moves.append((y+1, x+1))

        if spaceCheck(piece, board, y + 1, x - 1) and board[y+1][x-1] != 0:  # left capture
            moves.append((y+1, x-1))

        return moves

    else:  # white piece

        if board[y-1][x] == 0:
            moves.append((y-1, x))  # forward one space

        if piece == -11 and board[y-2][x] == 0:  # first move
            moves.append((y-2, x))

        if spaceCheck(piece, board, y - 1, x + 1) and board[y-1][x+1] != 0:  # right capture
            moves.append((y-1, x+1))

        if spaceCheck(piece, board, y - 1, x - 1) and board[y-1][x-1] != 0:  # left capture
            moves.append((y-1, x-1))

        return moves


# computes legal rook moves
def rookMove(piece, y, x, board):
    moves = []
    tempY = y
    tempX = x

    # up
    while (spaceCheck(piece, board, tempY + 1, x)):
        moves.append((tempY + 1, x))
        if board[tempY + 1][x] != 0:
            break
        tempY += 1

    tempY = y

    # right
    while (spaceCheck(piece, board, y, tempX + 1)):
        moves.append((y, tempX + 1))
        if board[y][tempX + 1] != 0:
            break
        tempX += 1

    tempX = x

    # down
    while (spaceCheck(piece, board, tempY - 1, x)):
        moves.append((tempY - 1, x))
        if board[tempY - 1][x] != 0:
            break
        tempY += -1

    # left
    while (spaceCheck(piece, board, y, tempX - 1)):
        moves.append((y, tempX - 1))
        if board[y][tempX - 1] != 0:
            break
        tempX += -1

    return moves


# computes legal knight moves
def knightMove(piece, y, x, board):
    moves = []
    i = 0
    xMove = -2, -1, 1, 2
    yMove = 1, 2, 2, 1

    while i < 4:

        if spaceCheck(piece, board, (y + yMove[i]), (x + xMove[i])):
            moves.append(((y + yMove[i]), (x + xMove[i])))

        if spaceCheck(piece, board, (y - yMove[i]), (x + xMove[i])):
            moves.append(((y - yMove[i]), (x + xMove[i])))

        i += 1

    return moves


# computes legal bishop moves
def bishopMove(piece, y, x, board):
    moves = []
    tempY = y
    tempX = x

    # up right
    while (spaceCheck(piece, board, tempY + 1, tempX + 1)):
        moves.append((tempY + 1, tempX + 1))
        if board[tempY + 1][tempX + 1] != 0:
            break
        tempY += 1
        tempX += 1

    tempY = y
    tempX = x

    # up left
    while (spaceCheck(piece, board, tempY + 1, tempX - 1)):
        moves.append((tempY + 1, tempX - 1))
        if board[tempY + 1][tempX - 1] != 0:
            break
        tempY += 1
        tempX -= 1

    tempY = y
    tempX = x

    # down right
    while (spaceCheck(piece, board, tempY - 1, tempX + 1)):
        moves.append((tempY - 1, tempX + 1))
        if board[tempY - 1][tempX + 1] != 0:
            break
        tempY -= 1
        tempX += 1

    tempY = y
    tempX = x

    # down left
    while (spaceCheck(piece, board, tempY - 1, tempX - 1)):
        moves.append((tempY - 1, tempX - 1))
        if board[tempY - 1][tempX - 1] != 0:
            break
        tempY -= 1
        tempX -= 1

    return moves


# computes legal queen moves
def queenMove(piece, y, x, board):
    moves = []
    moves = bishopMove(piece, y, x, board) + rookMove(piece, y, x, board)

    return moves


# computes possible king moves
def kingMove(piece, y, x, board):
    moves = []
    moveX = 1, 0, -1
    moveY = 1, 0, -1

    for i in moveX:
        for n in moveY:
            if spaceCheck(piece, board, y + moveY[n], x + moveX[i]):
                moves.append((y + moveY[n], x + moveX[i]))

    return moves


# computes all possible moves for the piece's opposite colour
# kingPass is to ignore the kings movements
# used when determining checkmate to avoid infinite recursion
def computeAll(king, board, kingPass):
    moves = []
    y = x = -1
    colour = pieceColour(king)

    for _ in board:
        y += 1
        for n in _:
            x += 1

            if pieceColour(-n) == colour:

                if n in {-1, 1, 11, -11}:
                    moves = moves + pawnMove(n, y, x, board)
                    # print((y, x), ":", pawnMove(n, y, x, board))

                elif n in {5, -5, 55, -55}:
                    moves = moves + rookMove(n, y, x, board)
                    # print((y, x), ":", rookMove(n, y, x, board))

                elif n in {3, -3}:
                    moves = moves + knightMove(n, y, x, board)
                    # print((y, x), ":", knightMove(n, y, x, board))

                elif n in {4, -4}:
                    moves = moves + bishopMove(n, y, x, board)
                    # print((y, x), ":", bishopMove(n, y, x, board))

                elif n in {7, -7}:
                    moves = moves + queenMove(n, y, x, board)
                    # print((y, x), ":", queenMove(n, y, x, board))

                elif n in {9, -9, 99, -99}:
                    if kingPass == 1:
                        pass
                    else:
                        moves = moves + kingMove(n, y, x, board)
                        # print((y, x), ":", kingMove(n, y, x, board))

        x = -1
    # print("-------------------------------------------------------------")
    return moves


# returns the coordinates of the piece's colour king
def kingCoord(piece, board):
    y = x = -1

    if piece < 0:
        king = -9, -99
    else:
        king = 9, 99

    for _ in board:
        y += 1
        for n in _:
            x += 1
            if (n in king):
                return (y, x)
        x = -1


# determines if the king can castle
# returns true to castle the king
def castle(piece, board, oldY, oldX, pSize, size, moveList, tempBoard):
    mX, mY = getPos(pSize, size)
    tempX = mX
    rook = getPiece(board, pSize, size)[0]

    if piece in {9, -9}:  # king unmoved
        if rook in {5, -5}:  # rook unmoved

            if mX == 0:
                kingX = oldX - 2
                rookX = kingX + 1
                while (mX != oldX):
                    if board[oldY][mX + 1] == 0:
                        empty = True
                        mX += 1
                    else:
                        empty = False
                        break
            else:
                kingX = oldX + 2
                rookX = kingX - 1
                while (mX != oldX):
                    if board[oldY][mX - 1] == 0:
                        empty = True
                        mX -= 1
                    else:
                        empty = False
                        break

            if empty:  # empty inbetween spaces
                if kingCoord(piece, tempBoard) in moveList:  # check if king in check
                    return False
                else:
                    board[oldY][kingX] = piece
                    board[oldY][rookX] = rook
                    firstMove(piece, board, oldY, kingX)
                    firstMove(rook, board, oldY, rookX)
                    board[mY][tempX] = 0

                    return True


# determines end pawn promotion
def endPawn(piece, board, newY, newX):
    if piece == -1:
        if newY == 0:
            return True

    elif piece == 1:
        if newY == 7:
            return True


# evaluates if a button is pressed
# also dictates pawn promotion behaviour
def button(selection, info, promotedPiece, board):

    pressed = pygame.mouse.get_pos()[0] in range(info[0], info[2] + info[0]) and pygame.mouse.get_pos()[1] in range(info[1], info[3] + info[1])

    # promotion buttonss
    if pressed and selection != 0:
        piece, y, x = promotedPiece

        # Bishop
        if selection == 1:
            newPiece = 4

        # Knight
        elif selection == 2:
            newPiece = 3

        # Rook
        elif selection == 3:
            newPiece = 55

        # Queen
        elif selection == 4:
            newPiece = 7

        if piece > 0:
            pass
        else:
            newPiece = -newPiece

        board[y][x] = newPiece

    return pressed


# evaluates if king is in checkmate
# False for no, true for yes
def checkmate(king, board, x, y):
    moveList = computeAll(king, board, 0)

    # check if the king is the only piece and it cannot move

    if kingCoord(king, board) in moveList:  # king in check
        kingsList = kingMove(king, y, x, board)
        tempBoard = [row[:] for row in board]
        canMove = False

        n = -1
        for _ in kingsList:
            n += 1
            newY, newX = kingsList[n]
            tempBoard[newY][newX] = king

            if kingCoord(king, tempBoard) in moveList:  # king still in check after move
                pass
            else:  # king can move
                canMove = True

            # resets tempBoard
            tempBoard = [row[:] for row in board]

        if canMove:
            return False
        else:
            moveList = computeAll(-king, board, 1)

            if king < 0:
                tempPiece = -1
            else:
                tempPiece = 1

            n = -1
            for _ in moveList:
                n += 1
                newY, newX = moveList[n]
                tempBoard[newY][newX] = tempPiece
                tempMoveList = computeAll(king, tempBoard, 0)

                if kingCoord(king, tempBoard) in tempMoveList:  # king still in check after move
                    pass
                else:  # piece prevents check
                    canMove = True

                # resets tempBoard
                tempBoard = [row[:] for row in board]

            return not canMove

    else:
        return False
