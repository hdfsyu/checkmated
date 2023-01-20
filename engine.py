#this file stores all the info for the current game, such as possible moves, or already played moves
class GameState():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]#8x8 2d list, the name of the element in the list is the name of the png, "--" is blank, b or w for the color, and r,n,b,q,k,p for the type
        self.whiteToMove = True #is it white's turn?
        self.moveLog = [] #moves that players have done
    def makeMove(self, move):
        self.board[move.startR][move.startC] = "--"
        self.board[move.endR][move.endC] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove #change turn

class Move():
    #a bunch of dictionaries i actually just copied and pasted this idk what i did
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}
    def __init__(self, startSq, endSq, board):
        self.startR = startSq[0]
        self.startC = startSq[1]
        self.endR = endSq[0]
        self.endC = endSq[1]
        self.pieceMoved = board[self.startR][self.startC]
        self.pieceCaptured = board[self.endR][self.endC]
    def getChessNotation(self):
        return self.getRankFile(self.startR, self.startC) + self.getRankFile(self.endR, self.endC)
    def getRankFile(self,r,c):
        return self.colsToFiles[c] + self.rowsToRanks[r]