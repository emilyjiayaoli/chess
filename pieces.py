from cmu_112_graphics import *
from helper import *
import copy
#notes:
    # check if there are pieces to the foward diagonal of pawns
    # 

class Piece:
    def __init__(self, app, name, isWhite, row, col):
        self.name = name
        self.isWhite = isWhite
        self.row = row
        self.col = col
        self.rowBef = None
        self.colBef = None
        self.imagePath = '/Users/emily/Desktop/15-112_Programming/chess-ai/pieces_sprite.png'
        self.entireImage = app.scaleImage(app.loadImage(self.imagePath), 1/5)
        self.imageWidth = 64.5
        self.image = self.getImage(self.name, self.isWhite)

        self.legalMoves = set() #set of legal moves
        self.showLegalMoves = True
        self.isCaptured = False
        self.leftEnPassant, self.rightEnPassant = False, False


        if self.name == "pawn":
            self.enPassant = set()

        if self.name == "king":
            self.canCastleLeft = False
            self.canCastleRight = False
            # self.alreadyCastled = False

    def getLegalMoves(self, board):
        if self.name == "pawn":
            return self.getPawnLegalMoves(board)
        
        #returns a set of legal moves for bishop, queen, rook, king
        legalMoves = set()
        for path in regularMoves[self.name]:
            for (drow, dcol) in path:
                tempRow, tempCol = self.row + drow, self.col + dcol
                # check in bounds
                if 0 <= tempRow <= 7 and 0 <= tempCol <= 7:
                    if board[tempRow][tempCol] == None:
                        legalMoves.add((drow, dcol))
                    else:
                        # check if different colors
                        if board[tempRow][tempCol].isWhite != self.isWhite:
                            legalMoves.add((drow, dcol)) #capture move
                        # current path is blocked by same colored piece
                        # move onto next path
                        break
        return legalMoves

    def getPawnLegalMoves(self, board):
        # check if in initial position, allowed to make two moves
        if self.isWhite:
            legalMoves = regularMoves["pawn_w"].copy() #set
            captureMoves = [(1, -1), (1, 1)]

            # basic pawn moves
            if self.hasAnotherColoredPieceInFront(board):
                legalMoves.remove((1, 0))
            elif self.isInitialPawnPosition(): # Double move at initial position
                legalMoves.add((2, 0))

            #add in later
            # self.enPassant = self.getEnPassant(board)
            # if 'left' in self.enPassant:
            #     legalMoves.add((1, -1))
            #     self.leftEnPassant = (1, -1)
            # if 'right' in self.enPassant:
            #     legalMoves.add((1, 1))
            #     self.rightEnPassant = (1, 1)
                
        else:
            legalMoves = regularMoves["pawn_b"].copy() #set
            captureMoves = [(-1, -1), (-1, 1)]
            
            #print(legalMoves)

             # basic pawn moves
            if self.hasAnotherColoredPieceInFront(board):
                legalMoves.remove((-1, 0))
            elif self.isInitialPawnPosition(): # Double move at initial position
                legalMoves.add((-2, 0))
            
            #add in later
            # self.enPassant = self.getEnPassant(board)
            # if 'left' in self.enPassant:
            #     legalMoves.add((-1, -1))
            #     self.leftEnPassant = (-1, -1)
            # if 'right' in self.enPassant:
            #     legalMoves.add((-1, 1))
            #     self.rightEnPassant = (-1, 1)
        

        for (drow, dcol) in captureMoves:
            tempRow, tempCol = self.row + drow, self.col + dcol
            if 0 <= tempRow <= 7 and 0 <= tempCol <= 7:
                # add diagonal capture move if there are pieces
                if board[tempRow][tempCol] != None \
                    and board[tempRow][tempCol].isWhite != self.isWhite:
                    legalMoves.add((drow, dcol))
        return legalMoves
    
    def hasAnotherColoredPieceInFront(self, board):
        # returns True if pawn has another piece in front, False other
        if self.isWhite:
            if board[self.row+1][self.col] != None:
                return True
            else: 
                return False
        else:
            if board[self.row-1][self.col] != None:
                return True
            else: 
                return False

    def isInitialPawnPosition(self):
        # Returns True if pawn is in initial position, False otherwise
        if self.isWhite:
            if self.row == 1:
                return True
            else: 
                return False
        else:
            if self.row == 6:
                return True
            else: 
                return False
    
    def getEnPassant(self, board):
        # Returns a set specifying if enpasant exists to the left, right, both, or neither {'left', 'right'}
        enPassant = set()
        if self.isWhite:
            if board[self.row][self.col-1] != None and not board[self.row][self.col-1].isWhite:
                enPassant.add('left')
            if board[self.row][self.col+1] != None and not board[self.row][self.col+1].isWhite:
                enPassant.add('right')
        else: #black pieces
            if board[self.row][self.col-1] != None and board[self.row][self.col-1].isWhite:
                enPassant.add('left')
            if board[self.row][self.col+1] != None and board[self.row][self.col+1].isWhite:
                enPassant.add('right')
        return enPassant


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
    
    def isValidPawnPromotion(self):
        # Returns true if a pawn has reached the other end of board
        if self.name != "pawn":
            return False
        else:
            if self.isWhite:
                if self.row == 7: 
                    return True
                else: 
                    return False
            else: #black pawn
                if self.row == 0: 
                    return True
                else: 
                    return False

    def getValidCastling(self, board):
        # returns set containing "left" and "right" if castle-able, empty set if not
        assert(self.name == "king")

        castleDir = set()
        if self.isWhite:
            castleRow = board[0]
        else: # black side
            castleRow = board[7]
        #left castle
        if castleRow[0] != None and castleRow[0].name == "rook" and castleRow[4].name == "king" \
            and self.isNothingBetween(castleRow, 1, 4):
            castleDir.add("left")
        #right castle
        if castleRow[7] != None and castleRow[7].name == "rook" and castleRow[4].name == "king" \
            and self.isNothingBetween(castleRow, 5, 7):
            castleDir.add("right")
        return castleDir
    
    def isNothingBetween(self, row:list, start, end):
        # Helper function that returns true if there are no pieces between two indices in a row.
        # (inclusive, non-inclusive)
        for piece in row[start:end]:
            if piece != None:
                return False
        return True

    def getColor(self):
        if self.isWhite:
            return "white"
        else:
            return "black"

    def addCastleMoves(self, board):
    # Helper function that adds castle moves to selected piece if it is castle-ble

        # checks if color can castle
        whiteTurn = self.isWhite
        if whiteTurn and not board.whiteAlreadyCastled and not board.whiteKingAlreadyMoved:
            canCastle = True
        elif not whiteTurn and not board.blackAlreadyCastled and not board.blackKingAlreadyMoved:
            canCastle = True
        else:
            canCastle = False

        if canCastle:
            castleDir = self.getValidCastling(board.board)
            #print("castleDir:", castleDir)

            # if castleable
            if castleDir != set():
                if self.isWhite:
                    if "left" in castleDir and not board.whiteLeftRookAlreadyMoved:
                        self.legalMoves.add((0, -2))
                        self.canCastleLeft = True
                        #add castle left to legal moves, set piece.canCastleLeft = True 

                    if "right" in castleDir and not board.whiteRightRookAlreadyMoved:
                        self.legalMoves.add((0, 2))
                        self.canCastleRight = True
                        #add castle right to legal moves, set piece.canCastleRight = True
                else:
                    if "left" in castleDir and not board.blackLeftRookAlreadyMoved:
                        self.legalMoves.add((0, -2))
                        self.canCastleLeft = True
                        #add castle left to legal moves, set piece.canCastleLeft = True 

                    if "right" in castleDir and not board.blackRightRookAlreadyMoved:
                        self.legalMoves.add((0, 2))
                        self.canCastleRight = True
                        #add castle right to legal moves, set piece.canCastleRight = True

    def hasNoMoves(self, board):
        assert(self.name == "king")
        boardObj = copy.deepcopy(board)
        boardObj.mode = "pseudo"

        kingObj = boardObj.board[self.row][self.col]
        
        kingObjInitRow = self.row
        kingObjInitCol = self.col
        print("king's init pos",kingObjInitRow, kingObjInitCol)

        boardObj.getAllLegalMoves()
        legalMovesList = list(kingObj.legalMoves)
        print("legalMovesList", legalMovesList)

        counter = 0
        print("king's (initial) legalmovelist (pieces.py)", legalMovesList)        
        # removes each move that will still be in check
        print(repr2dList(boardObj.board))
        while 0 <= counter < len(legalMovesList):
            (dr, dc) = legalMovesList[counter]
            oldRow, oldCol = kingObjInitRow, kingObjInitCol
            newRow, newCol= oldRow + dr, oldCol + dc

            pieceTaken = copy.deepcopy(boardObj.board[newRow][newCol])
    
            boardObj.movePiece(kingObj, kingObj.row, kingObj.col, newRow, newCol)
            print("= moved king to ", newRow, newCol)
            print(repr2dList(boardObj.board))

            #isChecking, colorChecking = boardObj.isCheckNow()
            boardObj.isCheckNow()
            if boardObj.isCheck and (boardObj.colorChecking != (kingObj.getColor() + "Checking")):
                print("== still in check by ",boardObj.devilPiece, boardObj.devilIsWhite," after move", (dr, dc), "from", oldRow, oldCol, "so going back..")
                legalMovesList.remove((dr, dc))
                print("=== removed invalid move from legalMoveList", (dr, dc))
            else:
                counter += 1
                print("---- move valid!")    

             #restore
            boardObj.getAllLegalMoves()
            print(boardObj.board[0][4])
            #kingObj.legalMoves = kingObj.getLegalMoves(boardObj.board) #retrieves new king obj.legal moves at new position before moving back to old pos
            print(kingObj.legalMoves, "kingObj cur row, col", kingObj.row, kingObj.col)
            status = boardObj.movePiece(kingObj, newRow, newCol, oldRow, oldCol)
            boardObj.board[newRow][newCol] = pieceTaken
            print(status, "==== resetted - moved king back to original ", oldRow, oldCol, "onto next move!")
            
            
        legalMoves = set(legalMovesList)
        print("king's old legalMoves", self.legalMoves)
        self.legalMoves = legalMoves
        print("king's new legalMoves", self.legalMoves, counter)

        if len(self.legalMoves) == 0:
            print("no more moves :((")
            return True, legalMoves
        else:
            print("legalMoves not 0 yet, could still move!")
            return False, legalMoves


    def hasNoMovesV1(self, board):
        assert(self.name == "king")
        boardObj = copy.deepcopy(board)
        kingObj = copy.deepcopy(self)

        #legalMoves = kingObj.getLegalMoves(boardObj.board)
        #legalMoves = kingObj.legalMoves
        legalMovesList = list(kingObj.legalMoves)
        counter = 0
        print("king's (initial) legalmovelist (pieces.py)", legalMovesList)        
        # removes each move that will still be in check
        while 0 <= counter < len(legalMovesList):
            # print("king's legalMovesList", legalMovesList, "counter", counter)
            (dr, dc) = legalMovesList[counter]
            # psudomoving piece
            oldRow, oldCol = kingObj.row, kingObj.col
            newRow, newCol= oldRow + dr, oldCol + dc
            
            pieceTaken = copy.deepcopy(boardObj.board[newRow][newCol])
    
            boardObj.movePiece(kingObj, kingObj.row, kingObj.col, newRow, newCol)
            print("= moved king to ", newRow, newCol)
            # kingObj.row = newRow
            # kingObj.col = newCol

            isChecking, colorChecking = boardObj.isCheckNow()
            #print(repr2dList(boardObj.board), colorChecking, "isChecking")
            
            if isChecking and (colorChecking != (kingObj.getColor() + "Checking")):

                print("== king still in check after move", (dr, dc), "from", oldRow, oldCol, "so going back..")
                # # bad move, so step back and undo move
                # boardObj.movePiece(app, kingObj, newRow, newCol, oldRow, oldCol)
                # boardObj.board[newRow][newCol] = pieceTaken
                #assert(boardObj.board[newRow][newCol] == board.board[newRow][newCol])

                legalMovesList.remove((dr, dc))
                print("=== removed invalid move from legalMoveList", (dr, dc))

            # elif not isChecking:
            else:
                counter += 1
                print("---- move valid!")

            boardObj.movePiece(kingObj, newRow, newCol, oldRow, oldCol)


            # kingObj.row = oldRow
            # kingObj.col = oldCol

            boardObj.board[newRow][newCol] = pieceTaken
                #assert(boardObj.board[newRow][newCol] == board.board[newRow][newCol])
            #counter += 1
            print("==== resetted - moved king back to original ", oldRow, oldCol, "onto next move!")
            
        legalMoves = set(legalMovesList)
        print("king's old legalMoves", self.legalMoves)
        self.legalMoves = legalMoves
        print("king's new legalMoves", self.legalMoves)

        print("king's legalMovesList", legalMovesList, "counter", counter)
        if len(self.legalMoves) == 0:
            print("no more moves :((")
            return True, legalMoves
        else:
            print("updated moves! could still move!")
            return False, legalMoves
    
    # king can't walk into a checking move

    def drawPiece(self, app, canvas):
        x0, y0, x1, y1 = getCellBounds(app, self.row, self.col)
        cx = (x1+x0)//2
        cy = (y1+y0)//2
        canvas.create_image(cx, cy, image=ImageTk.PhotoImage(self.image))

    def drawHint(self, app, canvas):
        
        if self.name == app.selectedPiece.name and self.showLegalMoves and isinstance(self.legalMoves, set):
            # counter = 0
            #if self.name == "king": print("king's legalMoves in draw", self.legalMoves)
            for (drow, dcol) in self.legalMoves:
                #print(self.row+drow,  self.col+dcol)
                x0, y0, x1, y1 = getCellBounds(app, self.row+drow, self.col+dcol)
                cx = x0 + abs(x1-x0)//2
                cy = y0 + abs(y1-y0)//2
                radius = 5
                canvas.create_oval(cx-radius, cy-radius, cx+radius, cy+radius, fill = 'pink')
                #counter += 1

regularMoves = {
    'rook':[[(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)], #one path
            [(-1, 0), (-2, 0), (-3, 0), (-4, 0), (-5, 0), (-6, 0), (-7, 0)], #another path
            [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7)], 
            [(0, -1), (0, -2), (0, -3), (0, -4), (0, -5), (0, -6), (0, -7)]],
    'king': [[(1,1)], [(-1,-1)], [(-1,1)], [(1,-1)], #diagonal
                [(1,0)], [(-1,0)], [(0,1)], [(0,-1)]], #up, down, left, right
    'queen': [
            #up, down, left, right
            [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)], 
            [(-1, 0), (-2, 0), (-3, 0), (-4, 0), (-5, 0), (-6, 0), (-7, 0)], 
            [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7)], 
            [(0, -1), (0, -2), (0, -3), (0, -4), (0, -5), (0, -6), (0, -7)],
            
            
            #diagonal #need to keep going
            [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)], 
            [(-1, -1), (-2, -2), (-3, -3), (-4, -4), (-5, -5), (-6, -6), (-7, -7)], 
            [(-1, 1), (-2, 2), (-3, 3), (-4, 4), (-5, 5), (-6, 6), (-7, 7)], 
            [(1, -1), (2, -2), (3, -3), (4, -4), (5, -5), (6, -6), (7, -7)],
    ],
    'pawn_w': {(1, 0)}, # default pawn movement
    'pawn_b': {(-1, 0)},
    'bishop':[[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)], 
              [(-1, -1), (-2, -2), (-3, -3), (-4, -4), (-5, -5), (-6, -6), (-7, -7)], 
              [(-1, 1), (-2, 2), (-3, 3), (-4, 4), (-5, 5), (-6, 6), (-7, 7)], 
              [(1, -1), (2, -2), (3, -3), (4, -4), (5, -5), (6, -6), (7, -7)]],
    
    'knight': [[(-2,-1)], [(-1,-2)], [(2,1)], [(1,2)], [(-2,1)], [(-1,2)], [(2,-1)], [(1,-2)]]
}