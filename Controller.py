import pygame
from random import choice
from GUI import getPiece, getPos, addText, testBoard
from Main import PIECE

BLACK = -1
WHITE = 1


# toggles turn
def playerTurn(colour, turn, player):
    return (colour == BLACK) == (turn == 1) and (player == turn or player == None)


# determines if a set of coordinates are in the bounds of the board
def inBounds(newX, newY):
    return 0 <= newX <= 7 and 0 <= newY <= 7


# checks if space is in bounds and if the space is empty or has an emeny piece
def spaceCheck(piece, board, newY, newX):
    return inBounds(newX, newY) and (board[newY][newX] == 0 or pieceColour(board[newY][newX]) == pieceColour(-piece))


# returns a random turn for the user
def randomTurn():
    return choice((BLACK, WHITE))


# determines if the pawn moved two spaces in first turn
def pawnFirst(piece, newY, newX, oldY, oldX, computer, turn):
    y = oldY - 2 if computer != turn else oldY + 2
    return piece in {-11, 11} and newX == oldX and newY == y


# toggles first move ability of pawn and determines king's ability to castle
def firstMove(tempPiece, board, newY, newX):
    if tempPiece in {11, -11}:
        board[newY][newX] = tempPiece // 11
    elif tempPiece in {-9, 9, -5, 5}:
        board[newY][newX] = tempPiece * 11


# finds the opposite colour of the piece
def pieceColour(piece):
    if piece < 0:
        return BLACK
    elif piece == 0:
        return 0
    else:
        return WHITE


# checks if the opposite king is in check after the move
def isCheck(end, piece, board, opposite, canPassant, text, computer):
    if not end:
        moveList = computeAll(-piece, board, 0, opposite, canPassant, computer)
        if kingCoord(-piece, board) in moveList:
            inCheck = "    White king in check" if -piece < 0 else "    Black king in check"
            addText(text, inCheck, 0, 0, 0)


# computes the board position of the piece
def computePos(piece, computer, player, newY, newX):
    if (pieceColour(-piece) == -1 and computer is None) or (computer == 1 and player == -1):
        num, alph = newY + 1,  8 - newX
    else:
        num, alph = 8 - newY, newX + 1
    return num, alph


# returns the coordinates of the piece's colour king
def kingCoord(piece, board):
    king = {-9, -99} if piece < 0 else {9, 99}
    for y, row in enumerate(board):
        for x, z in enumerate(row):
            if z in king:
                return y, x


# determine if move is legal during check or if it prevents check
def checkMove(piece, newY, newX, oldY, oldX, board, canPassant, computer):
    newPiece = board[newY][newX]
    board[oldY][oldX] = 0
    board[newY][newX] = piece
    moveList = computeAll(piece, board, 0, 0, canPassant, computer)

    if (kingCoord(piece, board) in moveList):
        undo(board, piece, newPiece, newY, newX, oldY, oldX)
        return False
    else:
        undo(board, piece, newPiece, newY, newX, oldY, oldX)
        return True


# determines if move is legal or not
# if the new position is in the list of legal moves, return true
def move(piece, newY, newX, oldY, oldX, board, canPassant, computer):

    if piece in {-11, 11, 1, -1}:
        moves = pawnMove(piece, oldY, oldX, board, 0, canPassant, computer)

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


# computes legal pawn moves
def pawnMove(piece, y, x, board, opposite, canPassant, computer):

    moves = set()
    a = -1 if opposite == 1 else 1
    b = a * 2

    if spaceCheck(piece, board, y - a, x) and board[y - a][x] == 0:
        moves.add((y - a, x))  # forward one space

    if spaceCheck(piece, board, y - b, x) and piece in {-11, 11}:
        if board[y - b][x] == 0 and board[y - a][x] == 0:  # first move
            moves.add((y - b, x))

    if spaceCheck(piece, board, y - a, x + 1) and board[y - a][x + 1] != 0:  # right capture
        moves.add((y - a, x + 1))

    if spaceCheck(piece, board, y - a, x - 1) and board[y - a][x - 1] != 0:  # left capture
        moves.add((y - a, x - 1))

    if computer == None:
        coord = (7 - y, 7 - x)
        p, m = 1, -1
    else:
        coord = (y, x)
        m, p = 1, -1

    if coord in canPassant:  # LH and RH en passant
        if coord[1] - 1 == canPassant[0][1]:
            moves.add((y - a, x + p))
        else:
            moves.add((y - a, x + m))
    return moves


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


# removes the pawn captured through en passant
# special because the pawn doesn't overtake the captured pawn's space
def enPassantCapture(piece, board, newY, newX, oldY, oldX, isPawn, canPassant, text, computer, turn, noPrint):
    coord = (7 - oldY, 7 - oldX) if computer == None else (oldY, oldX)
    add = 1

    if computer == None:
        newCoord = (6 - newY, 7 - newX)

    elif computer == turn:
        newCoord = (newY - 1, newX)
        add = -1

    else:  # not computers turn
        newCoord = (newY + 1, newX)

    if isPawn and coord in canPassant and piece in {-1, 11, -11, 1} and spaceCheck(piece, board, newY, newX) and newCoord == canPassant[0]:
        board[newY + add][newX] = 0
        if not noPrint:
            addText(text, PIECE[piece] + " en passant capture", 0, 0, 0)


# determines if en passant is a possible move
# appends the piece that is able to perform en passant
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


# computes all possible moves for the piece's opposite colour
# kingPass is to ignore the kings movements
# used when determining checkmate to avoid infinite recursion
# meant for fast move validation
def computeAll(king, board, kingPass, opposite, canPassant, computer):
    moves = set()
    colour = pieceColour(king)

    for y, row in enumerate(board):
        for x, n in enumerate(row):
            if pieceColour(-n) == colour:

                if n in {-1, 1, 11, -11}:
                    moves |= pawnMove(n, y, x, board, opposite, canPassant, computer)

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


# similar to compute all
# except will compute the piece type, and old position
# meant for checkmate determination and computer move computations
def specificCompute(piece, board, canPassant, computer, opposite):
    moves = []
    colour = pieceColour(piece)
    i = -1

    for y, row in enumerate(board):
        for x, n in enumerate(row):
            if pieceColour(-n) == colour:

                i += 1
                moves.append([])
                moves[i].append(n)
                moves[i].append((y, x))

                if n in {-1, 1, 11, -11}:
                    moves[i].append(list(pawnMove(n, y, x, board, opposite, canPassant, computer)))

                elif n in {5, -5, 55, -55}:
                    moves[i].append(list(rookMove(n, y, x, board)))

                elif n in {3, -3}:
                    moves[i].append(list(knightMove(n, y, x, board)))

                elif n in {4, -4}:
                    moves[i].append(list(bishopMove(n, y, x, board)))

                elif n in {7, -7}:
                    moves[i].append(list(queenMove(n, y, x, board)))

                elif n in {9, -9, 99, -99}:
                    moves[i].append(list(kingMove(n, y, x, board)))

                if len(moves[i][2]) == 0:
                    i -= 1
                    moves.pop()
    return moves, i


# computes if the computer can castle
def computerCastle(piece, board, moves, i, canPassant, computer):
    moveList = computeAll(piece, board, 0, 0, canPassant, computer)
    piece = -9 if piece < 0 else 9
    oldY, oldX = kingCoord(piece, board)

    if not (oldY, oldX) in moveList and piece in {-9, 9}:  # not in check or king moved
        rookCoord = [0, 7]
        for n, x in enumerate(rookCoord):
            if board[0][x] in {5, -5}:  # rook unmoved
                temp = 1 if n == 0 else -1
                tempX = x

                while (tempX != oldX):
                    if board[0][tempX + temp] != 0:
                        break
                    tempX += temp

                tempX += temp
                kingX = oldX - 2 * temp
                rookX = kingX + temp
                if ((oldY, kingX) in moveList or tempX != oldX):  # kingn in check after castle
                    pass
                else:
                    side = " leftwards castle" if n == 1 else " rightwards castle"
                    i += 1
                    moves.append([])
                    moves[i].append(10)
                    moves[i].append((oldY, oldX))
                    moves[i].append([kingX, rookX, side, piece, x])
    return moves


# determines if the king can castle
# returns true to castle the king
def castle(piece, board, oldY, oldX, pSize, size, moveList, text, count):
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
                return False, count
            mX += temp

        # check if king in check before or after castle
        if (oldY, oldX) in moveList or (oldY, kingX) in moveList:
            return False, count
        else:
            board[oldY][kingX] = piece
            board[oldY][rookX] = rook
            firstMove(piece, board, oldY, kingX)
            firstMove(rook, board, oldY, rookX)
            board[mY][tempX] = 0
            count = addText(text, str(PIECE[piece]) + str(side), count, 0, 0)
            return True, count
    return False, count


# evaluates if a button is pressed
# also dictates pawn promotion behaviour
def button(selection, info, promotedPiece, board, text, count, length, font):
    pressed = pygame.mouse.get_pos()[0] in range(info[0], info[2] + info[0]) and pygame.mouse.get_pos()[1] in range(info[1], info[3] + info[1])
    pawn = "Black"

    # promotion buttonss
    if pressed and selection != 0:
        piece, y, x = promotedPiece
        pieceMap = {1: 4, 2: 3, 3: 55, 4: 7}
        newPiece = pieceMap.get(selection, None)

        if piece < 0:
            newPiece = -newPiece
            pawn = "White"
        board[y][x] = newPiece
        addText(text, pawn + " pawn promoted to", 0, 0, font)
        addText(text, "    " + str(PIECE[newPiece]), 0, length, font)

    if count == 0:
        return pressed
    else:
        return pressed, count


# evaluates true if king is in checkmate
def checkmate(king, board, canPassant, opposite, computer):
    canMove = False
    opposite = 1 if (opposite == 0 and computer == None) else 0
    moveList = specificCompute(-king, board, canPassant, computer, opposite)[0]

    # goes through each list in moveList
    for i, _ in enumerate(moveList):
        n = moveList[i][0]
        oldY, oldX = moveList[i][1]
        board[oldY][oldX] = 0

        # goes through each sublist
        for (newY, newX) in moveList[i][2]:
            if spaceCheck(n, board, newY, newX):
                newPiece = board[newY][newX]
                board[newY][newX] = n
                tempMoveList = computeAll(king, board, 0, opposite, canPassant, computer)
                if kingCoord(king, board) not in tempMoveList:  # king not in check after move
                    canMove = True
                    undo(board, 0, newPiece, newY, newX, oldY, oldX)
                    break
                undo(board, 0, newPiece, newY, newX, oldY, oldX)
        board[oldY][oldX] = n
    return not canMove


# undos the move to prevent deep copying the list
def undo(board, oldPiece, newPiece, newY, newX, oldY, oldX):
    board[newY][newX] = newPiece
    board[oldY][oldX] = oldPiece


# determines if the game has ended through checkmate or stalemate
def gameEnd(board, turn, pieceMoving, start, outline, canPassant, opposite, text, computer):
    if outline or not start or pieceMoving:
        return False
    else:
        if computer != None:
            opposite = 0 if computer == turn else 1

        kY, kX = kingCoord(-turn, board)
        king = board[kY][kX]
        moveList = computeAll(king, board, 0, opposite, canPassant, computer)
        emptySpace, knight, bishop = 0, 0, []

        for y, row in enumerate(board):
            for x, piece in enumerate(row):
                if piece == 0:
                    emptySpace += 1
                elif (piece in {-11, -1} and y > 1 and board[y-1][x] in {11, 1}):
                    if inBounds(y-1, x-1) and board[y-1][x-1] not in {11, 1} and inBounds(y-1, x + 1) and board[y-1][x+1] not in {11, 1}:
                        emptySpace += 2
                elif piece in {-3, 3}:
                    knight += 1
                elif piece in {-4, 4}:
                    bishop.append([piece, y, x])

        # stalemate cases
        if emptySpace == 62:  # king vs king
            addText(text, "Stalemate: Insufficient material.", 0, 0, 0)
            addText(text, "Press restart or exit the game.", 0, 0, 0)
            return True
        elif emptySpace == 61 and ((len(bishop) == 1 and knight == 0) or (knight == 1 and len(bishop) == 0)):  # 1 bishop/knight vs king
            addText(text, "Stalemate: Insufficient material.", 0, 0, 0)
            addText(text, "Press restart or exit the game.", 0, 0, 0)
            return True
        elif emptySpace == 60 and len(bishop) == 2:  # 1 bishop vs 1 bishop, same colour
            b1, b2 = bishop[0][0], bishop[1][0]
            i1, i2 = (bishop[0][1] * 8) + bishop[0][2], (bishop[1][1] * 8) + bishop[1][2]
            y1, y2, = bishop[0][1], bishop[1][1]
            if b1 != b2 and y1 % 2 == i1 % 2 and y2 % 2 == i2 % 2:
                addText(text, "Stalemate: Insufficient material.", 0, 0, 0)
                addText(text, "Press restart or exit the game.", 0, 0, 0)
                return True

        if checkmate(king, board, canPassant, opposite, computer):  # cannot move
            winner = {-9: "Black", -99: "Black", 99: "White", 9: "White"}
            if kingCoord(king, board) in moveList:  # king in check
                addText(text, "Checkmate: " + str(winner[king]) + " won!", 0, 0, 0)
            else:  # no possible moves, stalemate
                addText(text, "Stalemate: " + str(winner[-king]) + " cannot move.", 0, 0, 0)
            addText(text, "Press restart or exit the game.", 0, 0, 0)
            return True
        else:
            return False


# determines if the current board state is at checkmate
def gameOver(computer, turn, board, canPassant):
    opposite = 0 if computer == turn else 1
    kY, kX = kingCoord(-turn, board)
    king = board[kY][kX]
    return checkmate(king, board, canPassant, opposite, computer)
