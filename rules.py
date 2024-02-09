import pygame
from gui import *

""" 
all legal moves are computed in terms of a list
if the new position is in that list, then the move is legal

saving switching turns for last
same with external conditions including
check, pawn at end of board, castle, checkmate
focusing soley on movements of pieces
"""


# determines if move is legal or not
# if the new position is in the list of legal moves, return true
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


# determines if a set of coordinates are in bounds
def inBounds(x, y):
    if x < 0 or x > 7 or y < 0 or y > 7:
        return False
    else:
        return True


# computes legal pawn moves
def pawnMove(piece, y, x, board):

    moves = [None]*3

    if piece > 0:  # black piece
        if board[y+1][x] == 0:
            moves.append((y+1, x))  # forward one space

        if board[y+2][x] == 0 and piece == 11:  # first move
            moves.append((y+2, x))

        if inBounds(y+1, x+1) and board[y+1][x+1] != 0:  # right capture
            moves.append((y+1, x+1))

        if inBounds(y+1, x-1) and board[y+1][x-1] != 0:  # left capture
            moves.append((y+1, x-1))

        return moves

    else:  # white piece
        if board[y-1][x] == 0:
            moves.append((y-1, x))  # forward one space

        if board[y-2][x] == 0 and piece == -11:  # first move
            moves.append((y-2, x))

        if inBounds(y-1, x+1) and board[y-1][x+1] != 0:  # right capture
            moves.append((y-1, x+1))

        if inBounds(y-1, x-1) and board[y-1][x-1] != 0:  # left capture
            moves.append((y-1, x-1))

        return moves


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


# computes legal rook moves
def rookMove(piece, y, x, board):
    moves = []
    tempY = y
    tempX = x

    # gets opposite colour of the rook
    colour = pieceColour(-piece)

    # current space
    moves.append((y, x))

    # up
    while (inBounds(x, tempY + 1) and board[tempY + 1][x] == 0):
        moves.append((tempY + 1, x))
        tempY += 1

    # up capture
    if inBounds(x, tempY+1) and pieceColour(board[tempY+1][x]) == colour:
        moves.append((tempY+1, x))

    tempY = y

    # right
    while (inBounds(y, tempX + 1) and board[y][tempX + 1] == 0):
        moves.append((y, tempX + 1))
        tempX += 1

    # rightwards capture
    if inBounds(tempX + 1, y) and pieceColour(board[y][tempX + 1]) == colour:
        moves.append((y, tempX + 1))

    tempX = x

    # down
    while (inBounds(x, tempY - 1) and board[tempY - 1][x] == 0):
        moves.append((tempY - 1, x))
        tempY += -1

    # down capture
    if inBounds(x, tempY-1) and pieceColour(board[tempY-1][x]) == colour:
        moves.append((tempY - 1, x))

    # left
    while (inBounds(y, tempX - 1) and board[y][tempX - 1] == 0):
        moves.append((y, tempX - 1))
        tempX += -1

    # leftwards capture
    if inBounds(tempX - 1, y) and pieceColour(board[y][tempX - 1]) == colour:
        moves.append((y, tempX - 1))

    return moves
