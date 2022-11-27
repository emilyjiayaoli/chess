from cmu_112_graphics import *
from pieces import *
from board import *
import time
import copy

def appStarted(app):
    app.mode = "startScreen"
    app.margin = 0

    app.rows = 8
    app.cols = 8
    app.board = Board(app)
    print(app.board)

    app.isSelected = False
    app.selectedPiece = None
    app.hoverPiece = None


def startScreen_redrawAll(app, canvas):
    text = "Welcome to ChessAI"
    canvas.create_text(app.width//2, app.height//2, text=text)
    

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
    row, col = getCell(app, event.x, event.y)

    app.isSelected = not app.isSelected
    app.hoverPiece = app.board.board[row][col]

    if app.isSelected:
        if app.hoverPiece != None:
            app.selectedPiece = app.hoverPiece
            app.selectedPiece.legalMoves = app.selectedPiece.getLegalMoves(app.board.board)
    else:
        if (app.selectedPiece != None and app.hoverPiece == None) or\
            (app.selectedPiece != None and app.hoverPiece.isWhite != app.selectedPiece.isWhite):
            status = app.board.movePiece(app.selectedPiece.row, app.selectedPiece.col, row, col)



    # if app.hoverPiece == None:
    #     if app.isSelected:
    #         app.selectedPiece = app.board.board[row][col] #pick up
    #         # if app.selectedPiece != None:
    #         app.selectedPiece.legalMoves = app.selectedPiece.getLegalMoves(app.board.board)
    #     else:
    #         if app.selectedPiece != None:
    #             if app.hoverPiece!= None and app.hoverPiece.isWhite != app.selectedPiece.isWhite:
    #                 status = app.board.movePiece(app.selectedPiece.row, app.selectedPiece.col, row, col)
    #                 app.selectedPiece = None
    # elif app.hoverPiece != None:

    print("app.isSelected", app.isSelected)
    print("app.selectedPiece", app.selectedPiece)

    
    # if app.selectedPiece != None:
    #     if app.isSelected:
    #         app.selectedPiece.legalMoves = app.selectedPiece.getLegalMoves(app.board.board)
    #     else:
    #         status = app.board.movePiece(app.selectedPiece.row, app.selectedPiece.col, row, col)
    #         app.selectedPiece = None
    #     app.isSelected = not app.isSelected
    # else:
    #     app.isSelected = False
    # # if app.mouseR:
    #     if app.board.board[row][col] != None:
    #         piece = app.board.board[row][col]
    #         print(piece.row, piece.col)
    #         app.mouseR = False #mouse clicked

    # if not app.mouseR and app.bobard.board[row][col] == None:
    #     piece = app.board.board[row][col]
    #     print(piece.row, piece.col)
    #     piece.row = row
    #     piece.col = col
    #     app.mouseR = True #mouse clicked
    print(app.board)


def main_keyPressed(app, event):
    if (event.key == "r"):
        appStarted(app)

def main_timerFired(app):
    pass

def main_redrawAll(app, canvas):
    app.board.drawBoard(app,canvas)
    
runApp(width=680, height=680) # quit still runs next one, exit does not