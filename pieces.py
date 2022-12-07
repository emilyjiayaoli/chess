from cmu_112_graphics import *
from helper import *
import copy

class Piece:
    def __init__(self, app, name, isWhite, row, col):
        self.name = name
        self.isWhite = isWhite
        
        self.row = row
        self.col = col

        self.rowBef = None
        self.colBef = None

        # Sprite sheet taken from https://www.kindpng.com/imgv/hxbhmb_chess-pieces-png-chess-pieces-sprite-sheet-transparent/
        self.imagePath = './pieces_sprite.png'
        self.entireImage = app.scaleImage(app.loadImage(self.imagePath), 1/5)
        self.imageWidth = 64.5
        self.image = self.getImage(self.name, self.isWhite)

        self.legalMoves = set() # store legalMoves as a set for easy membership check :)
        self.showLegalMoves = True
        self.isCaptured = False
        self.leftEnPassant, self.rightEnPassant = False, False

        if self.name == "pawn":
            self.enPassant = set()

        if self.name == "king":
            self.canCastleLeft = False
            self.canCastleRight = False
        else:
            self.protectiveMoves = "not applicable"

    def getPawnLegalMoves(self, board, permission=False):
        # check if in initial position, allowed to make two moves
        if self.isWhite: # piece is black
            legalMoves = regularMoves["pawn_w"].copy() #set
            captureMoves = [(1, -1), (1, 1)]

            # basic pawn moves
            if self.hasAnotherColoredPieceInFront(board, 1):
                legalMoves.remove((1, 0))
            elif (self.isInitialPawnPosition() and not self.hasAnotherColoredPieceInFront(board, 2)) or permission: 
                # Double move at initial position
                legalMoves.add((2, 0))
            
            if self.row == 4: #could only enpassant on 4th row
                if board.blackPawnMovedTwoStep:
                    assert(board.blackPawnMovedTwoStepCol != None)
                    if board.blackPawnMovedTwoStepCol - self.col == 1:
                        legalMoves.add((1, 1)) #white right enpassant
                        board.canEnPassant = True
                    elif board.blackPawnMovedTwoStepCol - self.col == -1:
                        legalMoves.add((1, -1)) #white left enpassant
                        board.canEnPassant = True
        else: # piece is black
            legalMoves = regularMoves["pawn_b"].copy() #set
            captureMoves = [(-1, -1), (-1, 1)]
            
             # basic pawn moves
            if self.hasAnotherColoredPieceInFront(board, 1):
                legalMoves.remove((-1, 0))
            elif self.isInitialPawnPosition() and not self.hasAnotherColoredPieceInFront(board, 2): 
                # Double move at initial position
                legalMoves.add((-2, 0))
            
            if self.row == 3: #could only enpassant on 4th row
                if board.whitePawnMovedTwoStep:
                    #print("on third row and whitePawnMovedTwoStep")
                    assert(board.whitePawnMovedTwoStepCol != None)
                    if board.whitePawnMovedTwoStepCol - self.col == 1:
                        legalMoves.add((-1, 1)) #black right enpassant
                        board.canEnPassant = True
                    elif board.whitePawnMovedTwoStepCol - self.col == -1:
                        legalMoves.add((-1, -1)) #white left enpassant
                        board.canEnPassant = True

        for (drow, dcol) in captureMoves:
            tempRow, tempCol = self.row + drow, self.col + dcol
            if 0 <= tempRow <= 7 and 0 <= tempCol <= 7:
                # add diagonal capture move if there are pieces
                if board.board[tempRow][tempCol] != None \
                    and board.board[tempRow][tempCol].isWhite != self.isWhite:
                    legalMoves.add((drow, dcol))
        return legalMoves

    
    def hasAnotherColoredPieceInFront(self, board, steps):
        # returns True if pawn has another piece in front, False other
        if self.isWhite:
            if not (0 <= self.row+steps <= 7):
                return True
            if board.board[self.row+steps][self.col] != None:
                return True
            else: 
                return False
        else:
            if not (0 <= self.row-steps <= 7):
                return True
            if board.board[self.row-steps][self.col] != None:
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
        # returns image of specified piece, color that has been cropped correctly

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
        # Returns convenient string representation of pieces' names
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
        # Returns the color of piece
        if self.isWhite:
            return "white"
        else:
            return "black"

    def getCastleMoves(self, board):
        # Helper function that adds castle moves to selected piece if it is castle-ble

        moves = set()
        # checks if color can castle
        whiteTurn = self.isWhite
        if whiteTurn and not board.whiteAlreadyCastled and not board.whiteKingAlreadyMoved:
            canCastle = True
        elif not whiteTurn and not board.blackAlreadyCastled and not board.blackKingAlreadyMoved:
            canCastle = True
        else:
            canCastle = False

        # Retrieves proper castling moves via helper
        if canCastle:
            castleDir = self.getValidCastling(board.board)

            # if castleable, add castle left to legal moves, e.g set piece.canCastleLeft = True 
            if castleDir != set():
                if self.isWhite:
                    if "left" in castleDir and not board.whiteLeftRookAlreadyMoved:
                        moves.add((0, -2))
                        self.canCastleLeft = True
                    if "right" in castleDir and not board.whiteRightRookAlreadyMoved:
                        moves.add((0, 2))
                        self.canCastleRight = True
                else:
                    if "left" in castleDir and not board.blackLeftRookAlreadyMoved:
                        moves.add((0, -2))
                        self.canCastleLeft = True
                    if "right" in castleDir and not board.blackRightRookAlreadyMoved:
                        moves.add((0, 2))
                        self.canCastleRight = True
        return moves

    def getPieceMovesDurCheck(self, board, isCheck=True):
        # Returns the appropriate moves during check by simulating all the future legal moves

        legalMoves = set()
        origLegalMoves = self.getLegalMoves(board) # retrieve baseline legalMoves

        # Simulates future legal moves creating a copy of board, named "pseudo"
        boardObj = copy.deepcopy(board)
        boardObj.mode = "pseudo"
        boardObj.isCheck = False
        pieceObj = boardObj.board[self.row][self.col]
        pieceObjInitRow, pieceObjInitCol = self.row, self.col # will always return to this pos

        # Attempt each move in the original set of LegalMoves
        for (dr, dc) in origLegalMoves:

            pieceObjNewRow, pieceObjNewCol = pieceObjInitRow + dr, pieceObjInitCol + dc 
            
            # check if check
            boardObj.getAllLegalMovesPseudo()
            if pieceObj.name == "pawn":
                moves1 = pieceObj.getPawnLegalMoves(boardObj)
            else:
                moves1 = pieceObj.getLegalMoves(boardObj)

            status = boardObj.movePiece(pieceObj, pieceObjInitRow, pieceObjInitCol, pieceObjNewRow, pieceObjNewCol, moves1)
            
            boardObj.getAllLegalMovesPseudo()

            infoAbtCheckPiece = boardObj.updateIsCheck()

            if not boardObj.isCheck:
                legalMoves.add((dr, dc)) # since new position is not in check, add to legalMoves
            
            
             # switch check back to false, not adding into legalmoves
            boardObj.isCheck = False
            
            moves = pieceObj.getLegalMoves(boardObj)
            # move back to original position to try the next move
            status2 = boardObj.movePiece(pieceObj, pieceObjNewRow, pieceObjNewCol, pieceObjInitRow, pieceObjInitCol, defaultLegalMoves=moves)

        #if self.isWhite: print(legalMoves, self.isWhite, " finished ")
        return legalMoves 


    def getKingMoves(self, board, isCheck):
        legalMoves = set()
        origLegalMoves = self.getLegalMoves(board) # retrieve baseline legalMoves
        
        boardObj = copy.deepcopy(board)
        boardObj.mode = "pseudo"
        boardObj.isCheck = False
        kingObj = boardObj.board[self.row][self.col] # right unless self.row, col are incorrect
        kingObjInitRow, kingObjInitCol = self.row, self.col # will always return to this pos

        # Iterates through king's possible legal moves
        for (dr, dc) in origLegalMoves:

            # try moves
            kingObjNewRow, kingObjNewCol = kingObjInitRow + dr, kingObjInitCol + dc #calc pos to move to
            
            # check if check
            moves1 = kingObj.getLegalMoves(boardObj)
            #print("kingObj.legalMoves", moves1, kingObjNewRow-kingObjInitRow, kingObjNewCol-kingObjInitCol)

            status = boardObj.movePiece(kingObj, kingObjInitRow, kingObjInitCol, kingObjNewRow, kingObjNewCol, moves1)
            
            #print("white king position is", kingObj.row, kingObj.col, kingObjNewRow, kingObjNewCol, status, kingObj.legalMoves)
            boardObj.updateIsCheck()
            if not boardObj.isCheck:
                legalMoves.add((dr, dc)) # since new position is not in check, good to add to legalMoves
                 # switch back to false, not adding into legalmoves

            boardObj.isCheck = False
            
            moves = kingObj.getLegalMoves(boardObj)
            # move back to original position to try the next move
            status2 = boardObj.movePiece(kingObj, kingObjNewRow, kingObjNewCol, kingObjInitRow, kingObjInitCol, defaultLegalMoves=moves)

        # good place to check if there are moves in legalMoves that lead to check, answer should be no

        if board.mode != "pseudo" and not isCheck: #note that it is original board
            # adds castling move
            castleMoves = self.getCastleMoves(board)
            legalMoves = legalMoves.union(castleMoves)
        #if self.isWhite: print(legalMoves, self.isWhite, " finished ")
        return legalMoves 
    
    def getLegalMoves(self, board):
        legalMoves = set()
        if self.name == "pawn":
            legalMoves = self.getPawnLegalMoves(board)
            return legalMoves
        
        #returns a set of legal moves for bishop, queen, rook, king
        for path in regularMoves[self.name]:
            for (drow, dcol) in path:
                tempRow, tempCol = self.row + drow, self.col + dcol

                # check in bounds
                if 0 <= tempRow <= 7 and 0 <= tempCol <= 7:
                    if board.board[tempRow][tempCol] == None:
                        legalMoves.add((drow, dcol))
                    else:

                        # check if different colors
                        if board.board[tempRow][tempCol].isWhite != self.isWhite:
                            legalMoves.add((drow, dcol)) #capture move
                        # current path is blocked by same colored piece
                        # move onto next path
                        break

        return legalMoves

    def getLegalMovesDuringCheck(self, boardObj, fullMoves):
        # returns the set of moves that protect the same colored king 

        assert(self.name != "king")
        piece = boardObj.board[self.row][self.col] # get corresponding piece in copy of board
        oldRow, oldCol = piece.row, piece.col
        protectiveMoves = set()

        for (drow, dcol) in fullMoves:

            #print("before moving", piece.name, oldRow, oldCol,repr2dList(boardObj.board))
            newRow, newCol = oldRow + drow, oldCol + dcol
            status = boardObj.movePiece(piece, oldRow, oldCol, newRow, newCol)
            boardObj.getAllLegalMoves()
            # boardObj.getAllLegalMovesInPseudo()
            #print(status, "after", repr2dList(boardObj.board))
            if not boardObj.isCheckNow():
                protectiveMoves.add((drow, dcol)) #add to objs in original board
            else:
                #print("still is check")
                boardObj.isCheck = False
            boardObj.movePiece(piece, newRow, newCol, oldRow, oldCol)
        return protectiveMoves


    def drawPiece(self, app, canvas):
        x0, y0, x1, y1 = getCellBounds(app, self.row, self.col)
        cx = (x1+x0)//2
        cy = (y1+y0)//2
        canvas.create_image(cx, cy, image=ImageTk.PhotoImage(self.image))

    def drawHint(self, app, canvas):
        
        if self.name == app.selectedPiece.name and self.showLegalMoves and isinstance(self.legalMoves, set):
            for (drow, dcol) in self.legalMoves:
                #print(self.row+drow,  self.col+dcol)
                x0, y0, x1, y1 = getCellBounds(app, self.row+drow, self.col+dcol)
                cx = x0 + abs(x1-x0)//2
                cy = y0 + abs(y1-y0)//2
                radius = 5
                canvas.create_oval(cx-radius, cy-radius, cx+radius, cy+radius, fill = 'blue')
            if self.name != "king" and isinstance(self.protectiveMoves, set):
                for (drow, dcol) in self.protectiveMoves:
                    x0, y0, x1, y1 = getCellBounds(app, self.row+drow, self.col+dcol)
                    cx = x0 + abs(x1-x0)//2
                    cy = y0 + abs(y1-y0)//2
                    radius = 5
                    canvas.create_oval(cx-radius-5, cy-radius-5, cx+radius, cy+radius, fill = 'blue')

# Stores all the possible moves various pieces could make
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