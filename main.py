# this file handles user input and renders the board
import pygame as p
from pygame import mixer
import engine
from os import path
p.init()
mixer.init()
if path.exists("config/scaled"):
    WIDTH = 1024
    HEIGHT = 768
else:
    WIDTH = 640
    HEIGHT = 480
DIMENSION = 8  # dimensions of the chess board (8x8)
SQ_SIZE = HEIGHT // DIMENSION  # size of the squares
MAX_FPS = 15  # fps cap (fps cap for animation running at their normal speed)
IMAGES = {

}
# init a global dictionary of images (only called once)
def LoadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']  # dictionary
    if path.exists('config/switched'):# if board has been switched
        for piece in pieces:  # for loop for each piece in the dictionary
            IMAGES[piece] = p.transform.scale(p.image.load("images/medieval/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    else:
        for piece in pieces:  # for loop for each piece in the dictionary
            IMAGES[piece] = p.transform.scale(p.image.load("images/fancy/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
def main():
    screen = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption("checkmated")
    screen.fill(p.Color("black"))
    clock = p.time.Clock()
    gs = engine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False#is a move made?
    #load images
    LoadImages()
    running = True
    sqSelected = ()#keep track of the last click of the player
    playerClicks = [] #keep track of player clicks
    #while loop
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                c = location[0]//SQ_SIZE
                r = location[1]//SQ_SIZE
                if sqSelected == (r,c): #did the player click the same square twice?
                    sqSelected = () #remove all items from sqselected
                    playerClicks = []#clear the track of the player clicks
                else:
                    sqSelected = (r,c)
                    playerClicks.append(sqSelected) #append the first and second clicks to the track
                if len(playerClicks) == 2: #after the second click
                    move = engine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                        sqSelected = ()  # reset the user clicks
                        playerClicks = []
                        mixer.music.load('sounds/move.mp3')
                        mixer.music.set_volume(1)
                        mixer.music.play()
                    else:
                        playerClicks = [sqSelected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_e:
                    gs.undoMove()
                    moveMade = True
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
        drawState(screen,gs)
        clock.tick(MAX_FPS)
        p.display.flip()
#GFX for the game state
def drawState(screen, gs):
    drawBoard(screen) #draw squares on the board
    drawPieces(screen, gs.board) #draw pieces after drawing squares so the pieces can be visible
def drawBoard(screen):
    cols = [p.Color(196,164,132), p.Color(150,75,0)]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            col = cols[((r+c)%2)]# solve corner parities
            p.draw.rect(screen, col, p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))
def drawPieces(screen,board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":#if piece is not empty
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))
if __name__ == "__main__":
    main()
