from cmu_112_graphics import *
from pieces import *
from board import *
import time
import copy

def appStarted(app):
    app.mode = "startScreen"
    app.margin = 10
    app.rightMargin = 260

    app.rows = 8
    app.cols = 8
    app.board = Board(app)
    #print(app.board)
    app.whiteTurn = True
    app.x0, app.y0, app.x1, app.y1 = getBoardBounds(app) # for board
    # print(app.width, app.height)
    # print(app.x0, app.y0, app.x1, app.y1)
    app.isSelected = False
    app.selectedPiece = None
    app.hoverPiece = None

    app.isPawnPromoNow = False
    app.curPawnProm = None

    app.whiteAlreadyCastled = False
    app.blackAlreadyCastled = False

    app.whiteKingAlreadyMoved = False
    app.whiteLeftRookAlreadyMoved = False
    app.whiteRightRookAlreadyMoved = False

    app.blackKingAlreadyMoved = False
    app.blackLeftRookAlreadyMoved = False
    app.blackRightRookAlreadyMoved = False

    app.isCheck = False
    app.colorChecking = None
    app.isCheckmate = False

def getBoardBounds(app):
    upperLeft = getCellBounds(app, 0, 0)
    upperRight = getCellBounds(app, 0, 7)
    lowerLeft = getCellBounds(app, 7, 0)
    lowerRight = getCellBounds(app, 7, 7)
    x0 = upperLeft[0]
    y0 = upperLeft[1]
    x1 = upperRight[2]
    y1 = lowerRight[3]
    return x0, y0, x1, y1

def startScreen_redrawAll(app, canvas):
    # color = rgbString(191, 117, 124)
    # # 158, 68, 77
    # canvas.create_rectangle(0, 0, app.width, app.height, fill=color)
    text = "Welcome to ChessAI"
    canvas.create_text(app.width//2, app.height//2, text=text, font="Courier 35 bold")
    text = "Press B to begin playing 2 Player Mode"
    canvas.create_text(app.width//2, app.height//2 + 40, text=text)
    

# def drawButton(canvas, targetRectTuple, text, color="pink"):
#     (x0, y0, x1, y1) = targetRectTuple
#     canvas.create_rectangle(x0, y0, x1, y1, fill=color)
#     canvas.create_text(x0+(abs(x1-x0)//2), y0+(abs(y1-y0)//2), text=text)

# def getButtonPosition(centerX, centerY, width=40, height=20):
#     return (centerX-width, centerY-height, centerX+width, centerY+height)

# def isButtonClicked(event, targetRectTuple):
#     (x0, y0, x1, y1) = targetRectTuple
#     if x0 < event.x < x1 and y0 < event.y < y1:
#         return True
#     return False

# def startScreen_mousePressed(app, event):
#     # if isButtonClicked(event, app.fourTilesButton):
#     #     app.mode = "main"
#     #     app.colTileNum = 4
#     pass

def startScreen_keyPressed(app, event):
    if (event.key == "b"):
        app.mode = "main"


def main_mousePressed(app, event):
    # print(event.x, event.y)
    # print("app.isPawnPromoNow", app.isPawnPromoNow)
    

    newPieceName = clickButton(app, event.x, event.y)
    print("newPieceName", newPieceName)
    
    # Pawn promotion
    if app.isPawnPromoNow and (newPieceName != None) and (app.curPawnProm != None):
            newPieceRow = app.curPawnProm.row
            newPieceCol = app.curPawnProm.col
            app.board.board[newPieceRow][newPieceCol] = Piece(app, newPieceName, app.curPawnProm.isWhite, newPieceRow, newPieceCol)
            
            # Reset to default after pawn promotion
            app.isPawnPromoNow = False 
            app.curPawnProm = None
        
    # Regular Moves
    if (app.x0 <= event.x <= app.x1) and (app.y0 <= event.y <= app.y1) and not app.isPawnPromoNow:
        row, col = getCell(app, event.x, event.y)
        app.hoverPiece = app.board.board[row][col] # Piece clicked
        
        # Select: only if nothing was selected before
        if app.isSelected == False:
            if app.hoverPiece != None and (app.hoverPiece.isWhite == app.whiteTurn): #select something if turn
                app.isSelected = True
                app.selectedPiece = app.hoverPiece
                app.selectedPiece.legalMoves = app.selectedPiece.getLegalMoves(app.board.board)

                # Adds castle-ble moves if there are any
                addCastleMoves(app)
    
                print("app.selectedPiece.legalMoves", app.selectedPiece.legalMoves)

                ##

                # if no valid moves, reset to not clicked
                if len(app.selectedPiece.legalMoves) == 0:
                    app.isSelected = False
                    app.selectedPiece = None


        # Release: move the selected piece if legal
        else:
             # if moving itself on top of itself, reset to not clicked
            if (app.hoverPiece == app.selectedPiece):
                app.isSelected = False
                app.selectedPiece = None
            
            # move piece if legal
            if (app.selectedPiece != None and app.hoverPiece == None) or\
                (app.selectedPiece != None and app.hoverPiece.isWhite != app.selectedPiece.isWhite):
                status = app.board.movePiece(app, app.selectedPiece, app.selectedPiece.row, app.selectedPiece.col, row, col)
                if status == 'success':
                    app.whiteTurn = not app.whiteTurn # flip turns after moving piece

                    #Detects if rooks and king have been moved
                    updateKingAndRookStatus(app)

                    # checks if pawn promotion is valid
                    if app.selectedPiece.isValidPawnPromotion(): 
                        app.isPawnPromoNow = True
                        app.curPawnProm = app.selectedPiece
                    
                    app.isSelected = False
                    app.selectedPiece = None
                    
                # reset if failed to move piece (e.g target is not a valid move)
                elif status == 'failure':
                    app.isSelected = False
                    app.selectedPiece = None


        #print("app.isSelected", app.isSelected)
        #print("app.selectedPiece", app.selectedPiece)
        #print(repr2dList(app.board.board))

        # app.isCheckmate, winner = app.board.isCheckmate(app)
        # if app.isCheckmate:
        #     print("Game Over!!", winner)

        app.isCheck, app.colorChecking = app.board.isCheck()
        if app.isCheck:
            print("check!", app.colorChecking)

def addCastleMoves(app):
    # Helper function that adds castle moves to selected piece if it is castle-ble
    isWhite = app.selectedPiece.isWhite
    if isWhite and not app.whiteAlreadyCastled and not app.whiteKingAlreadyMoved:
        canCastle = True
    elif not isWhite and not app.blackAlreadyCastled and not app.blackKingAlreadyMoved:
        canCastle = True
    else:
        canCastle = False

    if app.selectedPiece.name == "king" and canCastle:
        castleDir = app.selectedPiece.isValidCastling(app.board.board)
        print("castleDir:", castleDir)
        # if castleable
        if castleDir != None:
            if app.selectedPiece.isWhite:
                if "left" in castleDir and not app.whiteLeftRookAlreadyMoved:
                    app.selectedPiece.legalMoves.add((0, -2))
                    app.selectedPiece.canCastleLeft = True
                    #add castle left to legal moves, set piece.canCastleLeft = True 

                if "right" in castleDir and not app.whiteRightRookAlreadyMoved:
                    app.selectedPiece.legalMoves.add((0, 2))
                    app.selectedPiece.canCastleRight = True
                    #add castle right to legal moves, set piece.canCastleRight = True
            else:
                if "left" in castleDir and not app.blackLeftRookAlreadyMoved:
                    app.selectedPiece.legalMoves.add((0, -2))
                    app.selectedPiece.canCastleLeft = True
                    #add castle left to legal moves, set piece.canCastleLeft = True 

                if "right" in castleDir and not app.blackRightRookAlreadyMoved:
                    app.selectedPiece.legalMoves.add((0, 2))
                    app.selectedPiece.canCastleRight = True
                    #add castle right to legal moves, set piece.canCastleRight = True

        
def updateKingAndRookStatus(app):
    # Helper function detects and updates if rooks and king have been moved
    if app.selectedPiece.isWhite:
        if app.selectedPiece.name == "king":
            app.whiteKingAlreadyMoved = True
        elif app.selectedPiece.name == "rook":
            if app.selectedPiece.col == 0:
                app.whiteLeftRookAlreadyMoved = True
            elif app.selectedPiece.col == 7:
                app.whiteRightRookAlreadyMoved = True
    else:
        if app.selectedPiece.name == "king":
            app.blackKingAlreadyMoved = True
        elif app.selectedPiece.name == "rook":
            if app.selectedPiece.col == 0:
                app.blackLeftRookAlreadyMoved = True
            elif app.selectedPiece.col == 7:
                app.blackRightRookAlreadyMoved = True

def main_keyPressed(app, event):
    if (event.key == "r"):
        appStarted(app)

def main_timerFired(app):
    pass
        
def clickButton(app, x, y):
    center = app.rightMargin//2 + (app.x1)
    buttonWidth = 60
    buttonHeight = 15

    if (center-buttonWidth <= x <= center+buttonWidth) and (160-buttonHeight <= y <= 160+buttonHeight):
        return "queen"
    elif (center-buttonWidth <= x <= center+buttonWidth) and (200-buttonHeight <= y <= 200+buttonHeight):
        return "rook"
    elif (center-buttonWidth <= x <= center+buttonWidth) and (240-buttonHeight <= y <= 240+buttonHeight):
        return "bishop"
    elif (center-buttonWidth <= x <= center+buttonWidth) and (280-buttonHeight <= y <= 280+buttonHeight):
        return "knight"
    return None
    # canvas.create_rectangle(center-buttonWidth, 200-buttonHeight, center+buttonWidth, 200+buttonHeight, fill="pink")
    # canvas.create_text(center, 200, text="rook")

    # canvas.create_rectangle(center-buttonWidth, 240-buttonHeight, center+buttonWidth, 240+buttonHeight, fill="pink")
    # canvas.create_text(center, 240, text="bishop")

    # canvas.create_rectangle(center-buttonWidth, 280-buttonHeight, center+buttonWidth, 280+buttonHeight, fill="pink")
    # canvas.create_text(center, 280, text="knight")

def getTurn(app):
    if app.whiteTurn:
        return "white"
    else:
        return "black"

def main_redrawAll(app, canvas):
    # color = rgbString(158, 68, 77)
    # # 158, 68, 77
    # canvas.create_rectangle(0, 0, app.width, app.height, fill=color)
    app.board.drawBoard(app,canvas)
    canvas.create_text(7*app.width//8 , 7*app.height//8, text=f"Turn: {getTurn(app)}", font="Courier 16 bold")

    if app.isCheck:
        canvas.create_text(7*app.width//8 , 6*app.height//8, text=f"Check!", font="Courier 16 bold")
    
    canvas.create_text(7*app.width//8 , 7.8*app.height//8, text=f"Press r to restart game", font="Courie 14")
    
    
    if app.isPawnPromoNow:
        center = app.rightMargin//2 + (app.x1)
        buttonWidth = 60
        buttonHeight = 15
        canvas.create_text(center, 100, text="Pawn Promotion")
        canvas.create_text(center, 120, text="Choose Piece:")
        
        canvas.create_rectangle(center-buttonWidth, 160-buttonHeight, center+buttonWidth, 160+buttonHeight, fill="pink")
        canvas.create_text(center, 160, text="queen")

        canvas.create_rectangle(center-buttonWidth, 200-buttonHeight, center+buttonWidth, 200+buttonHeight, fill="pink")
        canvas.create_text(center, 200, text="rook")

        canvas.create_rectangle(center-buttonWidth, 240-buttonHeight, center+buttonWidth, 240+buttonHeight, fill="pink")
        canvas.create_text(center, 240, text="bishop")

        canvas.create_rectangle(center-buttonWidth, 280-buttonHeight, center+buttonWidth, 280+buttonHeight, fill="pink")
        canvas.create_text(center, 280, text="knight")
        # canvas.create_rectangle(app.width//2, app.rectangle//2)
        # canvas

runApp(width=940, height=680) # quit still runs next one, exit does not