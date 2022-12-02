from cmu_112_graphics import *
from pieces import *
from helper import *
from pandas import *
import copy

class Board:
    def __init__(self, app):
        self.rows = app.rows
        self.cols = app.cols
    
        self.board = self.setUpBoard(app) # initializes board

        # style
        # self.color1 = rgbString(252, 251, 232) #light yellow
        # self.color2 = rgbString(191, 117, 124) #maroon

        self.color1 = rgbString(238, 240, 245)
        self.color2 = rgbString(99, 149, 255)
        # self.w_kingRow = 0
        # self.w_kingCol = 3
        # self.b_kingRow = 7
        # self.b_kingCol = 3

        # self.w_king = self.board[0][4] # attatched to the object
        
        # self.b_king = self.board[7][4]
        self.w_king = self.getKingPiece(isWhite=True) # attatched to the object
        #self.w_kingCol = self.board[0][3].col
        self.b_king = self.getKingPiece(isWhite=False)

        self.whiteTurn = True

        # Pawn Promotion
        self.isPawnPromoNow = False
        self.curPawnProm = None

        self.whiteAlreadyCastled = False
        self.blackAlreadyCastled = False

        self.whiteKingAlreadyMoved = False
        self.whiteLeftRookAlreadyMoved = False
        self.whiteRightRookAlreadyMoved = False

        self.blackKingAlreadyMoved = False
        self.blackLeftRookAlreadyMoved = False
        self.blackRightRookAlreadyMoved = False

        self.isCheck = False
        self.colorChecking = None
        self.isCheckmate = False

        self.mode = "regular"
        self.devilPiece = "none"
        self.devilColor = "idk"

        self.justMoved = []

    def getAllLegalMoves(self):
        # gets legal moves for all pieces
        for r in range(len(self.board)):
            for c in range(len(self.board[0])):
                piece = self.board[r][c]
                if piece != None:
                    piece.legalMoves = piece.getLegalMoves(self.board)
                    if piece.name == "king" and self.mode != "pseudo":
                        # adds castling move
                        piece.addCastleMoves(self)
                    
                    # if self.isPieceCheck(piece):
                    #     self.isCheck = True
                    #     if piece.isWhite:
                    #         self.colorChecking = "whiteChecking"
                    #         print("whiteChecking")
                    #     else:
                    #         self.colorChecking = "blackChecking"
                    #         print("blackChecking")
                    #     if self.isPieceCheckmate():
                    #         self.isCheckmate = True
    def isCheckNow(self):
        oneCheck = False
        for r in range(len(self.board)):
            for c in range(len(self.board[0])):
                piece = self.board[r][c]
                if piece != None:
                    if self.isPieceCheck(piece):
                        oneCheck = True
                        if piece.isWhite:
                            self.colorChecking = "whiteChecking"
                            print("whiteChecking")
                        else:
                            self.colorChecking = "blackChecking"
                            print("blackChecking")
        if oneCheck:
            self.isCheck = True
        else:
            self.isCheck = False
    
       # iterates board to check if there is a checking move made by any side or pieces, if so, return True
    def isPieceCheck(self, piece):
        # check every piece's legal move & it's change to the opposite color king
        isWhite = not piece.isWhite
        kingPiece = self.getKingPiece(isWhite=isWhite)
        kingRow, kingCol = kingPiece.row, kingPiece.col
        #if piece.name == "king": print("king is at isPieceCheck() in board.py row, col", kingRow, kingCol)
        dRowToKing = kingRow - piece.row
        dColToKing = kingCol - piece.col

        if kingPiece == None: # shouldn't happen
            print(repr2dList(self.board))
            print(self.b_king.row, self.w_king)

        if (dRowToKing, dColToKing) in piece.legalMoves:
            self.devilPiece = piece.name
            self.devilIsWhite = piece.isWhite
            return True
        else:
            return False

    def isPieceCheckmate(self,):
        if self.colorChecking == "whiteChecking":
            kingPiece = self.getKingPiece(isWhite=False)
            hasMoves, kingLegalMoves = kingPiece.hasNoMoves(self)
            if hasMoves:
                print("whiteWon")
        elif self.colorChecking == "blackChecking":
            kingPiece = self.getKingPiece(isWhite=True)
            hasMoves, kingLegalMoves = kingPiece.hasNoMoves(self)
            if hasMoves:
                print("blackWon")
                return True
        return False


    def getKingPiece(self, isWhite):
        for r in range(len(self.board)):
            for c in range(len(self.board[0])):
                if self.board[r][c] != None:
                    if self.board[r][c].name == "king":
                        if self.board[r][c].isWhite == isWhite:
                            return self.board[r][c]
        raise AssertionError("lost the king")
        
    def setUpBoard(self, app):
        # returns 2d list with pieces set up at inital positions
        newBoard = [[None]*self.cols for i in range(self.rows)]
        pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
        for p in range(len(pieces)):
            # white pieces
            newBoard[0][p] = Piece(app, pieces[p], True, 0, p)
            newBoard[1][p] = Piece(app, 'pawn', True, 1, p)

            # black pieces
            newBoard[6][p] = Piece(app, 'pawn', False, 6, p)
            newBoard[7][p] = Piece(app, pieces[p], False, 7, p)
        return newBoard

    def updateKingAndRookStatus(self, piece):
    # Helper function detects and updates if rooks and king have been moved
        if piece.isWhite:
            if piece.name == "king":
                self.whiteKingAlreadyMoved = True
            if piece.name == "rook":
                print("piece.colBef white", piece.colBef)
                if piece.colBef == 0 and piece.rowBef == 0:
                    self.whiteLeftRookAlreadyMoved = True
                elif piece.colBef == 7 and piece.rowBef == 0:
                    self.whiteRightRookAlreadyMoved = True
        else:
            if piece.name == "king":
                self.blackKingAlreadyMoved = True
            if piece.name == "rook":
                print("piece.colBef black", piece.colBef)
                if piece.colBef == 0 and piece.rowBef == 7:
                    self.blackLeftRookAlreadyMoved = True
                elif piece.colBef == 7 and piece.rowBef == 7:
                    self.blackRightRookAlreadyMoved = True


    def forceMovePiece(self, piece, oldRow, oldCol, newRow, newCol, internalOnly=False):
        drow = newRow-oldRow
        dcol = newCol-oldCol


    def movePiece(self, piece, oldRow, oldCol, newRow, newCol, internalOnly=False):
        # moves piece if movable

        # for queens, bishop, and rook, nothing can be blocking the way
        #if new move is not out of bounds

        drow = newRow-oldRow
        dcol = newCol-oldCol
        #piece.legalMoves = piece.getLegalMoves(self.board)

        if (drow, dcol) in piece.legalMoves:
            piece.rowBef, piece.colBef = oldRow, oldCol
            if piece.name == "king" and piece.canCastleLeft and ((drow, dcol) == (0, -2)):
                    print("castling left!")
                    # changes king position

                    self.board[newRow][newCol] = self.board[oldRow][oldCol]
                    self.board[oldRow][oldCol] = None

                    #assert(king == self.board[newRow][newCol])

                    if not internalOnly:
                        # update king's row and col attributes
                        self.board[newRow][newCol].row = newRow
                        self.board[newRow][newCol].col = newCol

                    # changes rook position
                    self.board[newRow][3] = self.board[newRow][0]
                    self.board[newRow][0] = None
                    if not internalOnly:
                        # update rook's row and col attributes
                        self.board[newRow][3].row = newRow
                        self.board[newRow][3].col = 3

                    piece.canCastleLeft = False
                    if piece.isWhite:
                        self.whiteAlreadyCastled = True
                    else:
                        self.blackAlreadyCastled = True

                    print("castled left")


            elif piece.name == "king" and piece.canCastleRight and ((drow, dcol) == (0, 2)):
                    # castle right

                    self.board[newRow][newCol] = self.board[oldRow][oldCol]
                    #
                    king = self.board[oldRow][oldCol]
                    assert(king == self.board[newRow][newCol])
                    self.board[oldRow][oldCol] = None

                    # king = self.board[oldRow][oldCol]
                    # self.board[newRow][newCol] = king
                    # self.board[oldRow][oldCol] = None

                    if not internalOnly:
                        # update king's row and col attributes
                        self.board[newRow][newCol].row = newRow
                        self.board[newRow][newCol].col = newCol

                    # changes rook position
                    self.board[newRow][5] = self.board[newRow][7]
                    self.board[newRow][7] = None
                    if not internalOnly:
                        # update rook's row and col attributes
                        self.board[newRow][5].row = newRow
                        self.board[newRow][5].col = 5
                
                    piece.canCastleRight = False
                    if piece.isWhite:
                        self.whiteAlreadyCastled = True
                    else:
                        self.blackAlreadyCastled = True
                    
                    print("castled right")
                    
            else:
                #changes the internal board
                self.board[newRow][newCol] = piece
                self.board[oldRow][oldCol] = None

                if not internalOnly:
                    #changes the piece attribute
                    self.board[newRow][newCol].row = newRow
                    self.board[newRow][newCol].col = newCol

            self.justMoved.append((piece.name,(drow, dcol)))

            #piece.legalMoves = set()
            return "success"
        else:
            return "failure"

    #only function that passes in app other than draw in baord.py
    def promotePawn(self, app, newPieceName):
        newPieceRow = self.curPawnProm.row
        newPieceCol = self.curPawnProm.col
        # creates a new piece according to choice
        self.board[newPieceRow][newPieceCol] = Piece(app, newPieceName, self.curPawnProm.isWhite, newPieceRow, newPieceCol)
        
        # Reset to default after pawn promotion
        self.isPawnPromoNow = False 
        self.curPawnProm = None
    
    def drawBoard(self, app, canvas):

        # Iterates through board 2d list and draws each piece
        for r in range(len(self.board)):
            for c in range(len(self.board[0])):

                # draw background color
                if r % 2 == 0:
                    if c % 2 == 0:
                        x0, y0, x1, y1 = getCellBounds(app, r, c)
                        canvas.create_rectangle(x0, y0, x1, y1, fill=self.color1, width = 0)
                    else:
                        x0, y0, x1, y1 = getCellBounds(app, r, c)
                        canvas.create_rectangle(x0, y0, x1, y1, fill=self.color2, width = 0)
                else:
                    if c % 2 == 1:
                        x0, y0, x1, y1 = getCellBounds(app, r, c)
                        canvas.create_rectangle(x0, y0, x1, y1, fill=self.color1, width = 0)
                    else:
                        x0, y0, x1, y1 = getCellBounds(app, r, c)
                        canvas.create_rectangle(x0, y0, x1, y1, fill=self.color2, width = 0)
                    

                # draws each piece
                piece = self.board[r][c]
                if piece != None:
                    piece.drawPiece(app, canvas)
                
                # draws hint circles for selected piece
                if app.isSelected and app.selectedPiece != None:
                    app.selectedPiece.drawHint(app, canvas)



    # iterates board to check if there is a checking move made by any side or pieces, if so, return True
    def isCheckNowV1(self):
        # check every piece's legal move & it's change to the opposite color king
        for r in range(len(self.board)):
            for c in range(len(self.board[0])):
                piece = self.board[r][c]
                if piece != None:
                    #if piece.name == "bishop" and not piece.isWhite: print()
                    piece.legalMoves = piece.getLegalMoves(self.board)
                    if piece.isWhite:
                        # kingRow = self.b_king.row #opposite color king's position
                        # kingCol = self.b_king.col
                        kingPiece = self.getKingPiece(isWhite=False)
                        if kingPiece == None:
                            print(repr2dList(self.board))
                            print(self.b_king.row, self.w_king)
                        kingRow = kingPiece.row
                        kingCol = kingPiece.col

                        dRowToKing = kingRow - piece.row
                        dColToKing = kingCol - piece.col
                        #if piece.name == "bishop": print("white", piece.legalMoves, kingRow, kingCol)
                        #print("kingRow, kingCol", kingRow, kingCol)
                        if (dRowToKing, dColToKing) in piece.legalMoves :
                            # print("piece.name checking",piece.name, "piece.row", piece.row, "piece.col", piece.col, \
                            #     "dRowToKing", dRowToKing, "dColToKing", dColToKing)
                            return True, "whiteChecking"
                    else:
                        # kingRow = self.w_king.row #opposite color king's position
                        # kingCol = self.w_king.col
                        kingPiece = self.getKingPiece(isWhite=True)
                        kingRow = kingPiece.row
                        kingCol = kingPiece.col
                        if kingPiece == None:
                            print(repr2dList(self.board))
                            print(self.w_king.row, self.w_king)

                        dRowToKing = kingRow - piece.row
                        dColToKing = kingCol - piece.col
                        #print("kingRow, kingCol", kingRow, kingCol)
                        #if piece.name == "bishop": print("black bishop legalMoves:", piece.legalMoves, dRowToKing, dColToKing, kingRow, kingCol)
                        if (dRowToKing, dColToKing) in piece.legalMoves and piece.isWhite != self.w_king.isWhite:
                            # print("piece.name checking",piece.name, "piece.row", piece.row, "piece.col", piece.col, \
                            #     "dRowToKing", dRowToKing, "dColToKing", dColToKing)
                            return True, "blackChecking"
        return False, None



    def isCheckmateNow(self):
        # if is check and the king has no legal moves
        if self.isCheck:
            if self.colorChecking == "whiteChecking":
                kingPiece = self.getKingPiece(isWhite=False)
                hasMoves, kingLegalMoves = kingPiece.hasNoMoves(self)
                if hasMoves:
                    print("whiteWon")
                    return True, "whiteWon"
            elif self.colorChecking == "blackChecking":
                kingPiece = self.getKingPiece(isWhite=True)
                hasMoves, kingLegalMoves = kingPiece.hasNoMoves(self)
                if hasMoves:
                    print("blackWon")
                    return True, "blackWon"

            #assert(self.board[0][4] == kingPiece)
            #print("self.kingPiece's legal moves", kingPiece.legalMoves)
            #print("self(board)'s legal moves", self.board[0][4].legalMoves)
            #print(repr2dList(self.board))
        return False, None

    def __repr__(self):
        return repr2dList(self.board)
