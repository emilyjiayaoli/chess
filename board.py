from cmu_112_graphics import *
from pieces import *
from helper import *
from pandas import *
import copy

class Board:
    def __init__(self, app):
        self.rows = app.rows
        self.cols = app.cols
        self.emptyBoard = [[None]*self.cols for i in range(self.rows)]
        self.board = self.setUpBoard(app)

        # style
        self.color1 = rgbString(252, 251, 232) #light yellow
        self.color2 = rgbString(191, 117, 124) #maroon

        # self.w_kingRow = 0
        # self.w_kingCol = 3
        # self.b_kingRow = 7
        # self.b_kingCol = 3

        self.w_king = self.board[0][4] # attatched to the object
        #self.w_kingCol = self.board[0][3].col
        self.b_king = self.board[7][4]
        #self.b_kingCol = self.board[7][3].col
        
    def setUpBoard(self, app):
        # returns 2d list with pieces set up at their inital positions

        pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
        for p in range(len(pieces)):
            # white pieces
            self.emptyBoard[0][p] = Piece(app, pieces[p], True, 0, p)
            self.emptyBoard[1][p] = Piece(app, 'pawn', True, 1, p)

            # black pieces
            self.emptyBoard[6][p] = Piece(app, 'pawn', False, 6, p)
            self.emptyBoard[7][p] = Piece(app, pieces[p], False, 7, p)
        return self.emptyBoard

    def movePiece(self, app, piece, oldRow, oldCol, newRow, newCol, internalOnly=False):
        # moves piece if movable

        # for queens, bishop, and rook, nothing can be blocking the way
        #if new move is not out of bounds

        drow = newRow-oldRow
        dcol = newCol-oldCol
        #piece.legalMoves = piece.getLegalMoves(self.board)

        if (drow, dcol) in piece.legalMoves:
            if piece.name == "king" and piece.canCastleLeft and ((drow, dcol) == (0, -2)):
                    print("castling left!")
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

                    piece.canCastleLeft = False
                    if piece.isWhite:
                        app.whiteAlreadyCastled = True
                    else:
                        app.blackAlreadyCastled = True

            elif piece.name == "king" and piece.canCastleRight and ((drow, dcol) == (0, 2)):
                    # castle right
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
                
                    piece.canCastleRight = False
                    if piece.isWhite:
                        app.whiteAlreadyCastled = True
                    else:
                        app.blackAlreadyCastled = True
                    #piece.alreadyCastled = True
        
            else:
                #changes the internal board
                self.board[newRow][newCol] = piece
                self.board[oldRow][oldCol] = None

                if not internalOnly:
                    #changes the piece attribute
                    piece.row = newRow
                    piece.col = newCol

            piece.legalMoves = set()
            return "success"

        return "failure"

    
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
    
    # def isCheckHelper(self, app, isWhite):
    #     if isWhite:
    #         kingRow = self.b_king.row
    #         kingCol = self.b_king.col
    #         dRowToKing = kingRow - app.selectedPiece.row
    #         dColToKing = kingCol - app.selectedPiece.col
    #         print("king row, col:", kingRow, kingCol, dRowToKing, dColToKing)
    #     else:
    #         kingRow = self.w_king.row
    #         kingCol = self.w_king.col
    #         dRowToKing = kingRow - app.selectedPiece.row
    #         dColToKing = kingCol - app.selectedPiece.col
    #         print("king row, col:", kingRow, kingCol)
    #     for r in range(len(self.board)):
    #         for c in range(len(self.board[0])):
    #             piece = self.board[r][c]
    #             if piece != None and piece.isWhite != isWhite:
    #                 piece.legalMoves = piece.getLegalMoves(self.board)
    #                 if piece.name == "bishop": print(piece.isWhite, piece.getLegalMoves(self.board))
    #                 if (dRowToKing, dColToKing) in piece.legalMoves:
    #                     return True, isWhite
    #     return False, None


    # iterates board to check if there is a checking move made by any side, if so, return True
    def isCheck(self):
        # check every piece's legal move & it's change to the opposite color king
        for r in range(len(self.board)):
            for c in range(len(self.board[0])):
                piece = self.board[r][c]
                if piece != None:
                    piece.legalMoves = piece.getLegalMoves(self.board)
                    if piece.isWhite:
                        kingRow = self.b_king.row #opposite color king's position
                        kingCol = self.b_king.col
                        dRowToKing = kingRow - piece.row
                        dColToKing = kingCol - piece.col
                        #if piece.name == "bishop": print("white", piece.legalMoves, kingRow, kingCol)
                        if (dRowToKing, dColToKing) in piece.legalMoves:
                            return True, "whiteChecking"
                    else:
                        kingRow = self.w_king.row #opposite color king's position
                        kingCol = self.w_king.col
                        dRowToKing = kingRow - piece.row
                        dColToKing = kingCol - piece.col
                        #if piece.name == "bishop": print("black", piece.legalMoves, kingRow, kingCol)
                        if (dRowToKing, dColToKing) in piece.legalMoves:
                            return True, "blackChecking"
        return False, None


    # outdated version: checks only if king is in direct path
    def isCheckV1(self, app, legalMoves, isWhite):
        
        if isWhite:
            kingRow = self.b_king.row
            kingCol = self.b_king.col
            dRowToKing = kingRow - app.selectedPiece.row
            dColToKing = kingCol - app.selectedPiece.col
            print("king row, col:", kingRow, kingCol)
        else:
            kingRow = self.w_king.row
            kingCol = self.w_king.col
            dRowToKing = kingRow - app.selectedPiece.row
            dColToKing = kingCol - app.selectedPiece.col
            print("king row, col:", kingRow, kingCol)
        
        # if path to king is in currently selected piece's legalMoves, then king is in check
        #if (dRowToKing, dColToKing) in app.selectedPiece.legalMoves:
        if (dRowToKing, dColToKing) in legalMoves:
            return True
        else:
            return False

    def isCheckmate(self, app):
        # if is check and the king has no legal moves
        if app.isCheck:
            if app.colorChecking == "whiteChecking":
                # self.b_king.legalMoves = self.b_king.getLegalMoves(self.board)
                if self.b_king.hasNoMoves(app, app.board): #self.b_king.hasNoProtection(app.board) and 
                #if self.b_king.legalMoves == set():
                    print("whiteWon")
                    return True, "whiteWon"
            elif app.colorChecking == "blackChecking":
                # self.w_king.legalMoves = self.b_king.getLegalMoves(self.board)
                if self.w_king.hasNoMoves(app, app.board): #self.w_king.hasNoProtection(app, app.board) and 
                #if self.w_king.legalMoves == set():
                    print("blackWon")
                    return True, "blackWon"
        return False, None

    def __repr__(self):
        return repr2dList(self.board)