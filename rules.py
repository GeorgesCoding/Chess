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
    pawn = -11, 11, 1, -1

    if piece in pawn:
        moves = pawnMove(piece, oldY, oldX, board)
        return ((newY, newX) in moves)


# determines if a set of coordinates are in bounds
def inBounds(x, y):
    if x < 0 or x > 7 or y < 0 or y > 7:
        return False
    else:
        return True


# computes pawn movement
def pawnMove(piece, y, x, board):

    moves = [None]*3

    if piece > 0:  # black piece
        if board[y+1][x] == 0:
            moves.append((y+1, x))

        if board[y+2][x] == 0 and piece == 11:
            moves.append((y+2, x))

        if board[y+1][x+1] != 0 and inBounds(y+1, x+1):
            moves.append((y+1, x+1))

        if board[y+1][x-1] != 0 and inBounds(y+1, x-1):
            moves.append((y+1, x-1))

        return moves

    else:  # white piece
        if board[y-1][x] == 0:
            moves.append((y-1, x))

        if board[y-2][x] == 0 and piece == -11:
            moves.append((y-2, x))

        if board[y-1][x+1] != 0 and inBounds(y-1, x+1):
            moves.append((y-1, x+1))

        if board[y-1][x-1] != 0 and inBounds(y-1, x-1):
            moves.append((y-1, x-1))

        return moves


# toggles first move ability of pawn
def firstMove(tempPiece, board, newY, newX):

    if tempPiece == 11:
        board[newY][newX] = 1

    if tempPiece == -11:
        board[newY][newX] = -1
