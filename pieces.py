from cmu_112_graphics import *
from helper import *
#notes:
    # check if there are pieces to the foward diagonal of pawns
    # 

class Piece:
    def __init__(self, app, name, isWhite, row, col):
        self.name = name
        self.moves = regularMoves[name]
        self.isWhite = isWhite
        self.row = row
        self.col = col
        self.imagePath = '/Users/emily/Desktop/15-112_Programming/chess-ai/pieces_sprite.png'
        self.entireImage = app.scaleImage(app.loadImage(self.imagePath), 1/5)
        self.imageWidth = 64.5
        self.image = self.getImage(self.name, self.isWhite)

        self.legalMoves = None #set of legal moves
        self.showLegalMoves = True
        self.isCaptured = False

    def getLegalMoves(self, board):
        if self.name == "pawn":
            legalMoves = regularMoves["pawn"] #set
            print(self.isWhite)
            if not self.isWhite:
                
                otherMoves = [(-1, -1), (-1, 1)]
            else:
                otherMoves = [(1, -1), (1, 1)]
            for (drow, dcol) in otherMoves:
                tempRow, tempCol = self.row + drow, self.col + dcol
                if 0 <= tempRow <= 7 and 0 <= tempCol <= 7:
                    # add diagonal capture move if there are pieces
                    if board[tempRow][tempCol] != None \
                        and board[tempRow][tempCol].isWhite != self.isWhite:
                        legalMoves.add((drow, dcol))
            return legalMoves
        #returns a set of legal moves for bishop, queen, rook
        legalMoves = set()
        for path in regularMoves[self.name]:
            for (drow, dcol) in path:
                tempRow, tempCol = self.row + drow, self.col + dcol
                # check in bounds
                if 0 <= tempRow <= 7 and 0 <= tempCol <= 7:
                    if board[tempRow][tempCol] == None:
                        legalMoves.add((drow, dcol))
                    elif board[tempRow][tempCol] != None:
                        # check if different colors
                        if board[tempRow][tempCol].isWhite != self.isWhite:
                            legalMoves.add((drow, dcol)) #capture move
                        # current path is blocked by same colored piece
                        # move onto next path
                        break
        return legalMoves

    def getImage(self, name, isWhite):
        # returns image of specified piece and color
        w = self.imageWidth
        if isWhite: # white pieces
            if name == "king": 
                i, j = 0, 0
            elif name == "queen":
                i, j = 1, 0
            elif name == "bishop":
                i, j = 2, 0
            elif name == "knight":
                i, j = 3, 0
            elif name == "rook":
                i, j = 4, 0
            elif name == "pawn":
                i, j = 5, 0
        else: #black pieces
            if name == "king": 
                i, j = 0, 1
            elif name == "queen":
                i, j = 1, 1
            elif name == "bishop":
                i, j = 2, 1
            elif name == "knight":
                i, j = 3, 1
            elif name == "rook":
                i, j = 4, 1
            elif name == "pawn":
                i, j = 5, 1
        return self.entireImage.crop((w*i, w*j, w+w*i, w+w*j))

    def __repr__(self):
        if self.isWhite:
            return 'w_' + self.name
        else:
            return 'b_' + self.name

    def drawPiece(self, app, canvas):
        x0, y0, x1, y1 = getCellBounds(app, self.row, self.col)
        cx = (x1+x0)//2
        cy = (y1+y0)//2
        canvas.create_image(cx, cy, image=ImageTk.PhotoImage(self.image))

        if app.isSelected and self.legalMoves != None and self.showLegalMoves:
            for (drow, dcol) in self.legalMoves:
                x0, y0, x1, y1 = getCellBounds(app, self.row+drow, self.col+dcol)
                cx = (x1+x0)//2
                cy = (y1+y0)//2
                radius = 3
                canvas.create_oval(cx-radius, cy-radius, cx+radius, cy+radius, fill = 'pink')

regularMoves = {
    # 'rook': [[(1,0), (-1,0), (0,1), (0,-1)],
    #         [(2,0), (-2,0), (0,2), (0,-2)],
    #         [(3,0), (-3,0), (0,3), (0,-3)],
    #         [(4,0), (-4,0), (0,4), (0,-4)],
    #         [(5,0), (-5,0), (0,5), (0,-5)],
    #         [(6,0), (-6,0), (0,6), (0,-6)],
    #         [(7,0), (-7,0), (0,7), (0,-7)],
    #], 
    'rook':[[(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)], #one path
            [(-1, 0), (-2, 0), (-3, 0), (-4, 0), (-5, 0), (-6, 0), (-7, 0)], #another path
            [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7)], 
            [(0, -1), (0, -2), (0, -3), (0, -4), (0, -5), (0, -6), (0, -7)]],
    'king': [[(1,1), (-1,-1), (-1,1), (1,-1), #diagonal
                (1,0), (-1,0), (0,1), (0,-1)]], #up, down, left, right
    'queen': [
            #up, down, left, right
            [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)], 
            [(-1, 0), (-2, 0), (-3, 0), (-4, 0), (-5, 0), (-6, 0), (-7, 0)], 
            [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7)], 
            [(0, -1), (0, -2), (0, -3), (0, -4), (0, -5), (0, -6), (0, -7)],
            
            
            #diagonal #need to keep going
            [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)], 
            [(-1, -1), (-2, -2), (-3, -3), (-4, -4), (-5, -5), (-6, -6), (-7, -7)], 
            [(-1, 1), (-2, 1), (-3, 3), (-4, 4), (-5, 5), (-6, 6), (-7, 7)], 
            [(1, -1), (2, -2), (3, -3), (4, -4), (5, -5), (6, -6), (7, -7)],
    ],
    'pawn': {(-1, 0)}, # pawn could move diagonal if want to capture someone
    # 'bishop': [[(1,1), (-1,-1), (-1,1), (1,-1)], 
    #             [(2,2), (-2,-2), (-2,1), (2,-2)],
    #             [(3,3), (-3,-3), (-3,3), (3,-3)],
    #             [(4,4), (-4,-4), (-4,4), (4,-4)],
    #             [(5,5), (-5,-5), (-5,5), (5,-5)],
    #             [(6,6), (-6,-6), (-6,6), (6,-6)],
    #             [(7,7), (-7,-7), (-7,7), (7,-7)],], 
                
    'bishop':[[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)], 
              [(-1, -1), (-2, -2), (-3, -3), (-4, -4), (-5, -5), (-6, -6), (-7, -7)], 
              [(-1, 1), (-2, 1), (-3, 3), (-4, 4), (-5, 5), (-6, 6), (-7, 7)], 
              [(1, -1), (2, -2), (3, -3), (4, -4), (5, -5), (6, -6), (7, -7)]],
    
    'knight': [[(-2,-1), (-1,-2), (2,1), (1,2), (-2,1), (-1,2), (2,-1), (1,-2)]]
}


# def transpose(L):
#     rowNum = len(L)
#     colNum = len(L[0])

#     result = [[None]*rowNum for i in range(colNum)]

#     for r in range(rowNum):
#         for c in range(colNum):
#             result[c][r] = L[r][c]
#     return result

# print(transpose(regularMoves['bishop']))