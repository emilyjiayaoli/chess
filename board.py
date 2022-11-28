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

    def movePiece(self, app, oldRow, oldCol, newRow, newCol):
        # moves piece if movable

        piece = app.selectedPiece

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
                    # update king's row and col attributes
                    self.board[newRow][newCol].row = newRow
                    self.board[newRow][newCol].col = newCol

                    # changes rook position
                    self.board[newRow][3] = self.board[newRow][0]
                    self.board[newRow][0] = None
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
                    # update king's row and col attributes
                    self.board[newRow][newCol].row = newRow
                    self.board[newRow][newCol].col = newCol

                    # changes rook position
                    self.board[newRow][5] = self.board[newRow][7]
                    self.board[newRow][7] = None
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

                #changes the piece attribute
                piece.row = newRow
                piece.col = newCol

            piece.legalMoves = set()
            return "success"

        return "failure"

    
    def drawBoard(self, app, canvas):
        #print(repr2dList(self.board))
        # if self.board[0][3] != None:
        #     print("king spot", self.board[0][3].name, self.board[0][3].isWhite)
        # else: print("king spot None")
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
                    

                piece = self.board[r][c]
                if piece != None:
                    piece.drawPiece(app, canvas)

                if app.isSelected and app.selectedPiece != None:
                    app.selectedPiece.drawHint(app, canvas)
    
    def isCheck(self):
        pass

    def isCheckmate(self):
        pass

    def __repr__(self):
        return repr2dList(self.board)