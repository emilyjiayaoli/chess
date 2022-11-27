from cmu_112_graphics import *
from pieces import *
from helper import *
from pandas import *

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

    def movePiece(self, oldRow, oldCol, newRow, newCol):
        # moves piece if movable

        piece = self.board[oldRow][oldCol]

        # for queens, bishop, and rook, nothing can be blocking the way
        #if new move is not out of bounds

        drow = newRow-oldRow
        dcol = newCol-oldCol

        #piece.legalMoves = piece.getLegalMoves(self.board)

        if (drow, dcol) in piece.legalMoves:
            # changes the internal board
            self.board[newRow][newCol] = piece
            self.board[oldRow][oldCol] = None

            piece.row = newRow
            piece.col = newCol

            return "success"
        return "failure"

    
    def drawBoard(self, app, canvas):
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

    def __repr__(self):
        return repr2dList(self.board)