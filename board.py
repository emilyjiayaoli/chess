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

        self.w_king = self.getKingPiece(isWhite=True) # attatched to the object
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

        # self.whiteEnpassantLeft = False
        # self.whiteEnpassantRight = False
        # self.blackEnpassantLeft = False
        # self.blackEnpassantRight = False

        self.canEnPassant = False

        self.whitePawnMovedTwoStep = False
        self.whitePawnMovedTwoStepCol = None
        self.blackPawnMovedTwoStep = False
        self.blackPawnMovedTwoStepCol = None

        self.isCheck = False
        self.colorChecking = None
        self.isCheckmate = False

        self.mode = "regular"
        self.devilPiece = "none"
        self.devilColor = "idk"

        self.justMoved = []

    def isWhiteDuringCheck(self):
        assert(self.isCheck == True)
        if self.colorChecking == "whiteChecking":
            return True
        else: return False

    def getAllLegalMoves(self):
        # gets legal moves for all pieces
        for r in range(len(self.board)):
            for c in range(len(self.board[0])):
                piece = self.board[r][c]
                if piece != None:
                    piece.legalMoves = piece.getLegalMoves(self)
                    # if piece.name == "king" and self.mode != "pseudo":
                        # get castling move
                        #piece.getCastleMoves(self)

                    # if self.isCheck:# :and self.mode != "pseudo":
                    #     boardObj = copy.deepcopy(self)
                    #     boardObj.isCheck = False # set is check back to false
                    #     boardObj.mode = "pseudo"
                    #     if piece.name != "king":
                    #         if self.colorChecking == "whiteChecking":
                    #             if piece.isWhite:
                    #                 piece.protectiveMoves = piece.getLegalMovesDuringCheck(boardObj)
                    #         elif self.colorChecking == "blackChecking":
                    #             if not piece.isWhite:
                    #                 piece.protectiveMoves = piece.getLegalMovesDuringCheck(boardObj)
                    #         else:
                    #             raise AssertionError("self.colorChecking is neither white or black")
    
                        
    def isCheckNow(self):
        # iterates through board to check if any piece is currently checking the opposite color king
        # if so, sets self.isCheck to True and modifies self.colorChecking.
        existsOneCheck = False
        for r in range(len(self.board)):
            for c in range(len(self.board[0])):
                piece = self.board[r][c]
                if piece != None:
                    if self.isPieceCheck(piece):
                        existsOneCheck = True
                        if piece.isWhite:
                            self.colorChecking = "whiteChecking"
                            print("whiteChecking")
                        else:
                            self.colorChecking = "blackChecking"
                            print("blackChecking")
        if existsOneCheck:
            self.isCheck = True
        else:
            self.isCheck = False
    
    def isPieceCheck(self, piece):
        # returns True if piece's move to the king is in the set of legalMoves
        isWhite = not piece.isWhite
        kingPiece = self.getKingPiece(isWhite=isWhite)
        kingRow, kingCol = kingPiece.row, kingPiece.col
        #if piece.name == "king": print("king is at isPieceCheck() in board.py row, col", kingRow, kingCol)
        dRowToKing = kingRow - piece.row
        dColToKing = kingCol - piece.col

        if (dRowToKing, dColToKing) in piece.legalMoves:
            self.devilPiece = piece.name
            self.devilIsWhite = piece.isWhite
            return True
        else:
            return False

    def isPieceCheckmate(self):
        if self.colorChecking == "whiteChecking":
            kingPiece = self.getKingPiece(isWhite=False)
            hasNoMoves, kingLegalMoves = kingPiece.hasNoMoves(self)
            hasNoProtection = kingPiece.hasNoProtection(self)
            if hasNoMoves and hasNoProtection:
                print("whiteWon")
                return True
        elif self.colorChecking == "blackChecking":
            kingPiece = self.getKingPiece(isWhite=True)
            hasNoMoves, kingLegalMoves = kingPiece.hasNoMoves(self)
            hasNoProtection = kingPiece.hasNoProtection(self)
            if hasNoMoves and hasNoProtection:
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
                #print("piece.colBef white", piece.colBef)
                if piece.colBef == 0 and piece.rowBef == 0:
                    self.whiteLeftRookAlreadyMoved = True
                elif piece.colBef == 7 and piece.rowBef == 0:
                    self.whiteRightRookAlreadyMoved = True
        else:
            if piece.name == "king":
                self.blackKingAlreadyMoved = True
            if piece.name == "rook":
                #print("piece.colBef black", piece.colBef)
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
            elif piece.name == "pawn" and self.canEnPassant:
                self.board[newRow][newCol] = piece
                self.board[oldRow][oldCol] = None

                self.board[newRow][newCol].row = newRow
                self.board[newRow][newCol].col = newCol

                if piece.isWhite:
                    if (drow, dcol) == (1, 1):
                        self.board[newRow-1][newCol] = None
                    elif (drow, dcol) == (1, -1):
                        self.board[newRow-1][newCol] = None
                else:
                    if (drow, dcol) == (-1, 1):
                        self.board[newRow+1][newCol] = None
                    elif (drow, dcol) == (-1, -1):
                        self.board[newRow+1][newCol] = None
                print("En Passant")
            else:
                
                #changes the internal board
                self.board[newRow][newCol] = piece
                self.board[oldRow][oldCol] = None

                if not internalOnly:
                    #changes the piece attribute
                    self.board[newRow][newCol].row = newRow
                    self.board[newRow][newCol].col = newCol

            self.justMoved.append((piece.name,(drow, dcol)))

            # if self.mode != "pseudo" and self.isCheck and self.isWhiteDuringCheck() != piece.isWhite:
            #     raise AssertionError("moved but still in check")

            #piece.legalMoves = set()
            if piece.name == "pawn":
                if (drow, dcol) == (2, 0): #white pawn
                    self.whitePawnMovedTwoStep = True
                    self.whitePawnMovedTwoStepCol = piece.col
                elif (drow, dcol) == (-2, 0): #black pawn
                    self.blackPawnMovedTwoStep = True
                    self.blackPawnMovedTwoStepCol = piece.col
                else:
                    if piece.isWhite:
                        self.whitePawnMovedTwoStep = False
                        self.whitePawnMovedTwoStepCol = None
                    else:
                        self.blackPawnMovedTwoStep = False
                        self.blackPawnMovedTwoStepCol = None

            self.canEnPassant = False
            return "success"
        else:
            self.canEnPassant = False
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
