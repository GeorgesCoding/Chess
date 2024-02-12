import pygame
from gui import *

""" 
========================
=== NOTES FOR VIEWER ===
========================
• All legal moves are computed in terms of a list
• If the new position is in that list, then the move is legal

• Saving the following cases after primary movements are completed:
    - Switching turns, check, pawn at end of board, castle, checkmate
"""


# determines if move is legal or not
# if the new position is in the lis t of legal moves, return true
def move(piece, newY, newX, oldY, oldX, board):

    # lists for piece identification
    pawn = -11, 11, 1, -1
    rook = 5, -5
    knight = 3, -3
    bishop = 4, -4
    queen = 7, -7
    king = 9, -9

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
        return

    elif piece in queen:
        return

    elif piece in king:
        return


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
        elif pieceColour(board[newY][newX]) == pieceColour(piece):
            return False
        else:
            return True
    else:
        return False


# toggles first move ability of pawn
def firstMove(tempPiece, board, newY, newX):

    if tempPiece == 11:
        board[newY][newX] = 1

    if tempPiece == -11:
        board[newY][newX] = -1


# finds the colour of the piece
def pieceColour(piece):
    if piece < 0:
        return "Black"
    else:
        return "White"


# computes legal pawn moves
def pawnMove(piece, y, x, board):

    moves = [None]*3

    if piece > 0:  # black piece
        if board[y+1][x] == 0:
            moves.append((y+1, x))  # forward one space

        if board[y+2][x] == 0 and piece == 11:  # first move
            moves.append((y+2, x))

        if spaceCheck(piece, board, y + 1, x + 1):  # right capture
            moves.append((y+1, x+1))

        if spaceCheck(piece, board, y + 1, x - 1):  # left capture
            moves.append((y+1, x-1))

        return moves

    else:  # white piece
        if board[y-1][x] == 0:
            moves.append((y-1, x))  # forward one space

        if board[y-2][x] == 0 and piece == -11:  # first move
            moves.append((y-2, x))

        if spaceCheck(piece, board, y - 1, x + 1):  # right capture
            moves.append((y-1, x+1))

        if spaceCheck(piece, board, y - 1, x - 1):  # left capture
            moves.append((y-1, x-1))

        return moves


# computes legal rook moves
def rookMove(piece, y, x, board):
    moves = []
    tempY = y
    tempX = x

    # current space
    moves.append((y, x))

    # up
    while (spaceCheck(piece, board, tempY + 1, x)):
        moves.append((tempY + 1, x))
        tempY += 1

    tempY = y

    # right
    while (spaceCheck(piece, board, y, tempX + 1)):
        moves.append((y, tempX + 1))
        tempX += 1

    tempX = x

    # down
    while (spaceCheck(piece, board, tempY - 1, x)):
        moves.append((tempY - 1, x))
        tempY += -1

    # left
    while (spaceCheck(piece, board, y, tempX - 1)):
        moves.append((y, tempX - 1))
        tempX += -1

    return moves


# computes legal knight moves
def knightMove(piece, y, x, board):
    moves = []
    i = 0
    xMove = -2, -1, 1, 2
    yMove = 1, 2, 2, 1

    # current space
    moves.append((y, x))

    while i < 4:

        if spaceCheck(piece, board, (y + yMove[i]), (x + xMove[i])):
            moves.append(((y + yMove[i]), (x + xMove[i])))

        if spaceCheck(piece, board, (y - yMove[i]), (x + xMove[i])):
            moves.append(((y - yMove[i]), (x + xMove[i])))

        i += 1

    return moves
