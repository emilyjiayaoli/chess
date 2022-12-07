from cmu_112_graphics import *
from pieces import *
from board import *

def appStarted(app):
    app.mode = "startScreen"
    app.margin = 10
    app.rightMargin = 260

    app.rows = 8
    app.cols = 8
    app.board = Board(app) # initializes board

    app.x0, app.y0, app.x1, app.y1 = getBoardBounds(app) # for board

    app.isSelected = False
    app.selectedPiece = None
    app.hoverPiece = None
    app.winner = None
    #app.isCheckmate = False

def getBoardBounds(app):
    # returns cell bounds of the playable region
    upperLeft = getCellBounds(app, 0, 0)
    upperRight = getCellBounds(app, 0, 7)
    lowerLeft = getCellBounds(app, 7, 0)
    lowerRight = getCellBounds(app, 7, 7)
    x0 = upperLeft[0]
    y0 = upperLeft[1]
    x1 = upperRight[2]
    y1 = lowerRight[3]
    return x0, y0, x1, y1

def main_keyPressed(app, event):
    if (event.key == "r"):
        appStarted(app)

def main_timerFired(app):
    if not app.board.isCheck:
        app.board.getAllLegalMovesRegular()

    else:
        app.board.getAllLegalMovesDurCheck()

        isCheckMate = app.board.isCheckmateNow()
        if isCheckMate:
            app.isCheckmate = True
            app.winner = app.board.winner
            print("winner is", app.winner)
    app.board.updateIsCheck()
    

def main_mousePressed(app, event):
    # Pawn promotion
    if app.board.isPawnPromoNow and (app.board.curPawnProm != None):
            newPieceName = pawnPromotionSelection(app, event.x, event.y)
            if newPieceName != None:
                app.board.promotePawn(app, newPieceName)
                
    # Regular Moves
    if (app.x0 <= event.x <= app.x1) and (app.y0 <= event.y <= app.y1) and not app.board.isPawnPromoNow:
        row, col = getCell(app, event.x, event.y)
        app.hoverPiece = app.board.board[row][col] # stores item at clicked cell
        
        # Select: only if nothing was selected before
        if app.isSelected == False:
            if app.hoverPiece != None and (app.hoverPiece.isWhite == app.board.whiteTurn): #select something if turn
                app.isSelected = True
                app.selectedPiece = app.hoverPiece

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
                status = app.board.movePiece(app.selectedPiece, app.selectedPiece.row, app.selectedPiece.col, row, col)
                #print((app.selectedPiece.name, app.selectedPiece.row, app.selectedPiece.col, status))
                if status == 'success':
                    app.board.whiteTurn = not app.board.whiteTurn # flip turns after moving piece

                    #Detects if rooks and king have been moved
                    if app.selectedPiece.name == "rook" or app.selectedPiece.name == "king":
                        app.board.updateKingAndRookStatus(app.selectedPiece)

                    # checks if pawn promotion is valid
                    if app.selectedPiece.isValidPawnPromotion(): 
                        app.board.isPawnPromoNow = True
                        app.board.curPawnProm = app.selectedPiece
                    
                    app.isSelected = False
                    app.selectedPiece = None
                    #print("board after move", repr2dList(app.board.board))

                    #print(app.board.justMoved)
                    
                # reset if failed to move piece (e.g target is not a valid move)
                elif status == 'failure':
                    app.isSelected = False
                    app.selectedPiece = None
    
    
def pawnPromotionSelection(app, x, y):

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

def getTurn(app):
    if app.board.whiteTurn:
        return "white"
    else:
        return "black"

def startScreen_redrawAll(app, canvas):
    text = "Welcome to Chess"
    canvas.create_text(app.width//2, app.height//2, text=text, font="Courier 35 bold")
    text = "Press B to begin playing 2 Player Mode"
    canvas.create_text(app.width//2, app.height//2 + 40, text=text)


def startScreen_keyPressed(app, event):
    if (event.key == "b"):
        app.mode = "main"

def main_redrawAll(app, canvas):
    app.board.drawBoard(app, canvas)
    canvas.create_text(7*app.width//8 , 7*app.height//8, text=f"Turn: {getTurn(app)}", font="Courier 16 bold")


    if app.board.isCheckmate:
        canvas.create_text(7*app.width//8 , 5*app.height//8, text=f"Checkmate!", font="Courier 16 bold")
        canvas.create_text(7*app.width//8 , 5.5*app.height//8, text=f"Winner is {app.winner}", font="Courier 16 bold")
    elif app.board.isCheck:
        canvas.create_text(7*app.width//8 , 6*app.height//8, text=f"Check!", font="Courier 16 bold")

    
    canvas.create_text(7*app.width//8 , 7.8*app.height//8, text=f"Press r to restart game", font="Courie 14")
    
    
    if app.board.isPawnPromoNow:
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

runApp(width=940, height=680) # quit still runs next one, exit does not