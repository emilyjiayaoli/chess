# This demos using image.size

from cmu_112_graphics import *

def appStarted(app):
    url = 'https://tinyurl.com/great-pitch-gif'
    app.image1 = app.loadImage(url)
    app.image2 = app.scaleImage(app.image1, 2/3)

def drawImageWithSizeBelowIt(app, canvas, image, cx, cy):
    canvas.create_image(cx, cy, image=ImageTk.PhotoImage(image))
    imageWidth, imageHeight = image.size
    msg = f'Image size: {imageWidth} x {imageHeight}'
    canvas.create_text(cx, cy + imageHeight/2 + 20,
                       text=msg, font='Arial 20 bold', fill='black')

def redrawAll(app, canvas):
    drawImageWithSizeBelowIt(app, canvas, app.image1, 200, 300)
    drawImageWithSizeBelowIt(app, canvas, app.image2, 500, 300)

runApp(width=700, height=600)