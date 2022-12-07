from cmu_112_graphics import *
from pieces import *
from helper import *
from pandas import *
import copy

class Board:
    def __init__(self, app):
        self.rows = app.rows
        self.cols = app.cols
    
        # Initialize board
        self.board = self.setUpBoard(app) 

        self.color1 = rgbString(238, 240, 245)
        self.color2 = rgbString(146, 182, 232)
        
        #self.color2 = rgbString(99, 149, 255)

        self.w_king = self.getKingPiece(isWhite=True)
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

        self.canEnPassant = False

        self.whitePawnMovedTwoStep = False
        self.whitePawnMovedTwoStepCol = None
        self.blackPawnMovedTwoStep = False
        self.blackPawnMovedTwoStepCol = None

        self.isCheck = False
        self.colorChecking = None
        self.isCheckmate = False
        self.winner = None

        self.mode = "regular"
        self.justMoved = []

    def isWhiteDuringCheck(self):
        # returns True if the color checking if white, False if black
        assert(self.isCheck == True)
        if self.colorChecking == "whiteChecking":
            return True
        else: return False

    def getAllLegalMovesDurCheck(self):
        # Updates piece.legalMoves for each valid piece in the entire board during check
        for r in range(len(self.board)):
            for c in range(len(self.board[0])):
                piece = self.board[r][c]
                if piece != None:
                    if self.colorChecking == "whiteChecking": # white is checking black
                        if not piece.isWhite:
                            if piece.name == "king":
                                piece.legalMoves = piece.getKingMoves(self, isCheck=True)
                            else:
                                piece.legalMoves = piece.getPieceMovesDurCheck(self, isCheck=True)
                        else:
                            piece.legalMoves = piece.getLegalMoves(self)
                    elif self.colorChecking == "blackChecking": # black is checking white
                        if piece.isWhite:
                            if piece.name == "king":
                                piece.legalMoves = piece.getKingMoves(self, isCheck=True)
                            else:
                                piece.legalMoves = piece.getPieceMovesDurCheck(self, isCheck=True)
                        else:
                            piece.legalMoves = piece.getLegalMoves(self)
                    else:
                        raise AssertionError("Neither color checking in getAllLegalMovesDurCheck")


    def getAllLegalMovesRegular(self):
        # Updates piece.legalMoves for each valid piece in the entire board when not in check
        for r in range(len(self.board)):
            for c in range(len(self.board[0])):
                piece = self.board[r][c]
                if piece != None:
                    if piece.name == "king":
                        #print(piece.legalMoves, piece.isWhite)
                        piece.legalMoves = piece.getKingMoves(self, isCheck=False)
                    else:
                        piece.legalMoves = piece.getLegalMoves(self)

    def getAllLegalMovesPseudo(self):
        assert(self.mode == "pseudo")
        # Updates piece.legalMoves for each valid piece in the pseudo board
        for r in range(len(self.board)):
            for c in range(len(self.board[0])):
                piece = self.board[r][c]
                if piece != None:
                    #if piece.name != "king": #skip king
                        piece.legalMoves = piece.getLegalMoves(self)
                        #print("updated pseudo moves ", piece.legalMoves)
                        
    def updateIsCheck(self):
        # Iterates through board to check if any piece is currently checking the opposite color king
        # if so, sets self.isCheck to True and modifies self.colorChecking.
        existsOneCheck = False
        infoAbtCheckPiece = ()
        for r in range(len(self.board)):
            for c in range(len(self.board[0])):
                piece = self.board[r][c]
                if piece != None:
                    # checks if each piece is checking the opposite side's king
                    if self.isPieceCheck(piece):
                        existsOneCheck = True
                        infoAbtCheckPiece = (piece.name, r, c)
                        if piece.isWhite:
                            self.colorChecking = "whiteChecking"
                        else:
                            self.colorChecking = "blackChecking"
        # Updates board.isCheck if at least one piece is checking 
        if existsOneCheck:
            self.isCheck = True
            if infoAbtCheckPiece!= (): 
                return infoAbtCheckPiece
            else: 
                return None
        else:
            self.isCheck = False
            if infoAbtCheckPiece!= (): 
                return infoAbtCheckPiece
            else: 
                return None

    def isPieceCheck(self, piece):
        # returns True if piece's move to the king is in the set of legalMoves
        isWhite = not piece.isWhite
        kingPiece = self.getKingPiece(isWhite=isWhite)
        kingRow, kingCol = kingPiece.row, kingPiece.col
        dRowToKing = kingRow - piece.row
        dColToKing = kingCol - piece.col
        if (dRowToKing, dColToKing) in piece.legalMoves:
            return True
        else:
            return False

    def getKingPiece(self, isWhite):
        # Iterates though board to find the king object, returns the king object based on color
        for r in range(len(self.board)):
            for c in range(len(self.board[0])):
                if self.board[r][c] != None:
                    if self.board[r][c].name == "king":
                        if self.board[r][c].isWhite == isWhite:
                            return self.board[r][c]
        raise AssertionError("Lost the king :<")
        
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
        # Helper function detects and updates if rooks and king have been moved; Modifies appropriate attributes
        # Used in castling detection and feature
        if piece.isWhite:
            if piece.name == "king":
                self.whiteKingAlreadyMoved = True
            if piece.name == "rook":
                if piece.colBef == 0 and piece.rowBef == 0:
                    self.whiteLeftRookAlreadyMoved = True
                elif piece.colBef == 7 and piece.rowBef == 0:
                    self.whiteRightRookAlreadyMoved = True
        else: # piece is black
            if piece.name == "king":
                self.blackKingAlreadyMoved = True
            if piece.name == "rook":
                #print("piece.colBef black", piece.colBef)
                if piece.colBef == 0 and piece.rowBef == 7:
                    self.blackLeftRookAlreadyMoved = True
                elif piece.colBef == 7 and piece.rowBef == 7:
                    self.blackRightRookAlreadyMoved = True

    def movePiece(self, piece, oldRow, oldCol, newRow, newCol, defaultLegalMoves=None, internalOnly=False):
        # Moves piece on the internal board (self.board) if legal

        # calculates rowChange
        drow = newRow-oldRow
        dcol = newCol-oldCol

        # set default legalMoves
        if defaultLegalMoves == None:
            legalMoves = piece.legalMoves
        else:
            legalMoves = defaultLegalMoves
        
        if (drow, dcol) in legalMoves:
            piece.rowBef, piece.colBef = oldRow, oldCol

            # castles left
            if piece.name == "king" and piece.canCastleLeft and ((drow, dcol) == (0, -2)):
                    
                    # changes king position
                    self.board[newRow][newCol] = self.board[oldRow][oldCol]
                    self.board[oldRow][oldCol] = None

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

                    # updates castling attributes of the board
                    piece.canCastleLeft = False
                    if piece.isWhite:
                        self.whiteAlreadyCastled = True
                    else:
                        self.blackAlreadyCastled = True

                    print("castled left!")

            # castles right
            elif piece.name == "king" and piece.canCastleRight and ((drow, dcol) == (0, 2)):
                    

                    self.board[newRow][newCol] = self.board[oldRow][oldCol]
                    self.board[oldRow][oldCol] = None

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
                
                    # updates castling attributes of the board
                    piece.canCastleRight = False
                    if piece.isWhite:
                        self.whiteAlreadyCastled = True
                    else:
                        self.blackAlreadyCastled = True
                    
                    print("castled right!")
                    
            # En Passant move
            elif piece.name == "pawn" and self.canEnPassant:
                # Internally modifies board
                self.board[newRow][newCol] = piece
                self.board[oldRow][oldCol] = None

                self.board[newRow][newCol].row = newRow
                self.board[newRow][newCol].col = newCol

                # Performs En Passant move based on appropriate color
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
            else:

                #changes the internal board
                self.board[newRow][newCol] = piece
                self.board[oldRow][oldCol] = None

                if not internalOnly:
                    #changes the piece attribute
                    self.board[newRow][newCol].row = newRow
                    self.board[newRow][newCol].col = newCol

            self.justMoved.append((piece.name,(drow, dcol)))

            # updates if the pawn has already moved since if so, en passant will be disabled
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

    def promotePawn(self, app, newPieceName):
        # Modifies board based upon piece chosen in pawn promotion
        newPieceRow = self.curPawnProm.row
        newPieceCol = self.curPawnProm.col

        # creates a new piece according to choice
        self.board[newPieceRow][newPieceCol] = Piece(app, newPieceName, self.curPawnProm.isWhite, newPieceRow, newPieceCol)
        
        # Reset to default after pawn promotion
        self.isPawnPromoNow = False 
        self.curPawnProm = None

    def isCheckmateNow(self):
        # Returs True if board is in Checkmate and False if not
        # Modifies board attributes such as winner
        if self.isCheck:
            if self.colorChecking == "whiteChecking":
                # Checkmate is only valid when if one side is in check and the side in check has no valid move
                if self.noMoves(isWhite=False):
                    self.isCheckmate = True
                    self.winner = "white"
                    return True
            elif self.colorChecking == "blackChecking":
                if self.noMoves(isWhite=True):
                    self.isCheckmate = True
                    self.winner = "black"
                    return True

        return False

    def noMoves(self, isWhite):
        # Returns True if there are no valid moves on the specified side, False otherwise
        for r in range(len(self.board)):
            for c in range(len(self.board[0])):
                piece = self.board[r][c]
                if piece != None:
                    if piece.isWhite == isWhite:
                        if len(piece.legalMoves) != 0:
                            #print(piece.name, "still have move", piece.legalMoves)
                            return False
        return True

    def __repr__(self): 
        # Returns a great representation of 2D board used for debuggung
        return repr2dList(self.board)
    
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
