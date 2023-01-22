#this file stores all the info for the current game, such as possible moves, or already played moves
class GameState:
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
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves, 'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whiteToMove = True #is it white's turn?
        self.whiteKingLoc = (7,4)
        self.blackKingLoc = (0,4)
        self.inCheck = False
        self.pins = []
        self.checks = []
        self.moveLog = [] #moves that players have done
    #executes move (will not work for castling, pawn promotion and en passant)
    def makeMove(self, move):
        self.board[move.startR][move.startC] = "--"
        self.board[move.endR][move.endC] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove #change turn
        if move.pieceMoved == "wK":
            self.whiteKingLoc = (move.endR, move.endC)
        elif move.pieceMoved == "bK":
            self.blackKingLoc = (move.endR, move.endC)
    #undo last move
    def undoMove(self):
        if len(self.moveLog) != 0: #make sure that we can actually undo a move
            move = self.moveLog.pop()
            self.board[move.startR][move.startC] = move.pieceMoved
            self.board[move.endR][move.endC] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove #switch turns back
            if move.pieceMoved == "wK":
                self.whiteKingLoc = (move.startR, move.startC)
            elif move.pieceMoved == "bK":
                self.blackKingLoc = (move.startR, move.startC)
            print("undo")
    #get a valid move
    def getValidMoves(self):
        moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.whiteToMove:
            kingR = self.whiteKingLoc[0]
            kingC = self.whiteKingLoc[1]
        else:
            kingR = self.blackKingLoc[0]
            kingC = self.blackKingLoc[1]
        if self.inCheck:
            if len(self.checks) == 1:
                moves = self.getPossibleMoves()
                check = self.checks[0]
                checkR = check[0]
                checkC = check[1]
                pieceChecking = self.board[checkR][checkC]
                validSquares = []
                if pieceChecking[1] == 'N':
                    validSquares = [(checkR, checkC)]
                else:
                    for i in range(1,8):
                        validSquare = (kingR + check[2] * i, kingC + check[3] * i)
                        validSquares.append(validSquare)
                        if validSquare[0] == checkR and validSquare[1] == checkC:
                            break
                for i in range(len(moves) - 1, -1, -1):
                    if moves[i].piecedMoved[1] != 'K':
                        if not(moves[i].endRow,moves[i].endCol) in validSquares:
                            moves.remove(moves[i])
            else:
                self.getKingMoves(kingR,kingC,moves)
        else:
            moves = self.getPossibleMoves()
        return moves
    #get a valid move BUT without considering checkmate
    def getPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn=='w' and self.whiteToMove) or (turn=='b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r,c,moves)
        return moves
    #get pawn moves
    def getPawnMoves(self,r,c,moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        if self.whiteToMove:
            if self.board[r-1][c] == '--': #1 square pawn move
                if not piecePinned or pinDirection == (-1,0):
                    moves.append(Move((r, c), (r - 1, c), self.board))
                    if r == 6 and self.board[r - 2][c] == "--":  # 2 square pawn move
                        moves.append(Move((r, c), (r - 2, c), self.board))
            if c - 1 >= 0: # we dont wanna go to column -1
                if self.board[r-1][c-1][0] == 'w': #is there a black piece?
                    if not piecePinned or pinDirection == (-1,-1):
                        moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if c+1 <= 7:
                if self.board[r-1][c+1][0] == 'w':
                    if not piecePinned or pinDirection == (-1,1):
                        moves.append(Move((r, c), (r - 1, c + 1), self.board))
        else:
            if self.board[r+1][c] == '--': #1 square pawn move
                if not piecePinned or pinDirection == (1,0):
                    moves.append(Move((r, c), (r + 1, c), self.board))
                    if r == 1 and self.board[r + 2][c] == "--":  # 2 square pawn move
                        moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0: # we dont wanna go to column -1
                if self.board[r+1][c-1][0] == 'w': #is there a black piece?
                    if not piecePinned or pinDirection == (1,-1):
                        moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if c+1 <= 7:
                if self.board[r+1][c+1][0] == 'w':
                    if not piecePinned or pinDirection == (1,1):
                        moves.append(Move((r, c), (r + 1, c + 1), self.board))
    #get rook moves
    def getRookMoves(self,r,c,moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != 'Q':
                    self.pins.remove(self.pins[i])
                break
        directions = ((-1,0),(0,-1),(1,0),(0,1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1,8):
                endR = r + d[0] * i
                endC = c+d[1]*i
                if 0 <= endR < 8 and 0 <= endC < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0],-d[1]):
                        endPiece = self.board[endR][endC]
                        if endPiece == "--":
                            moves.append(Move((r, c), (endR, endC), self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((r, c), (endR, endC), self.board))
                            break
                        else:
                            break
                else:
                    break
    #get possible moves for all other pieces
    def getKingMoves(self,r,c,moves):
        rMoves = (-1,-1,-1,0,0,1,1,1)
        cMoves = (-1,0,1,-1,1,-1,0,1)
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endR = r + rMoves[i]
            endC = c + cMoves[i]
            if 0 <= endR < 8 and 0 <= endC < 8:
                endPiece = self.board[endR][endC]
                if endPiece[0] != allyColor:
                    if allyColor == 'w':
                        self.whiteKingLoc = (endR, endC)
                    else:
                        self.blackKingLoc = (endR, endC)
                    inCheck, pins, checks = self.checkForPinsAndChecks()
                    if not inCheck:
                        moves.append(Move((r, c), (endR, endC), self.board))
                    if allyColor == 'w':
                        self.whiteKingLoc = (r,c)
                    else:
                        self.blackKingLoc = (r,c)
    def getKnightMoves(self,r,c,moves):
        piecePinned = False
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break
        knightMoves = ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endR = r + m[0]
            endC = c+m[1]
            if 0 <= endR < 8 and 0 <= endC < 8:
                if not piecePinned:
                    endPiece = self.board[endR][endC]
                    if endPiece[0] != allyColor:
                        moves.append(Move((r, c), (endR, endC), self.board))
    def getBishopMoves(self,r,c,moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        directions = ((-1,-1),(-1,1),(1,-1),(1,1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1,8):
                endR = r + d[0] * i
                endC = c+d[1]*i
                if 0 <= endR < 8 and 0 <= endC < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endR][endC]
                        if endPiece == "--":
                            moves.append(Move((r, c), (endR, endC), self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((r, c), (endR, endC), self.board))
                            break
                        else:
                            break
                else:
                    break
    def getQueenMoves(self,r,c,moves):
        self.getRookMoves(r,c,moves)
        self.getBishopMoves(r,c,moves)
    def checkForPinsAndChecks(self):
        pins = []
        checks = []
        inCheck = False
        if self.whiteToMove:
            enemyColor = "b"
            allyColor = "w"
            startR = self.whiteKingLoc[0]
            startC = self.whiteKingLoc[1]
        else:
            enemyColor = "w"
            allyColor = "b"
            startR = self.blackKingLoc[0]
            startC = self.blackKingLoc[1]
        directions = ((-1,0),(0,-1),(1,0),(0,1),(-1,-1),(-1,1),(1,-1),(1,1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = ()
            for i in range(1,8):
                endR = startR + d[0] * i
                endC = startC + d[1] * i
                if 0 <= endR < 8 and 0 <= endC < 8:
                    endPiece = self.board[endR][endC]
                    if endPiece[0] == allyColor:
                        if possiblePin == ():
                            possiblePin = (endR, endC, d[0], d[1])
                        else:
                            break
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]
                        if(0 <= j <= 3 and type == 'R') or \
                                (4 <= j <= 7 and type == 'B') or \
                                (i == 1 and type == 'p' and ((enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <=5))) or \
                                (type == 'Q') or (i==1 and type == 'K'):
                            if possiblePin == ():
                                inCheck = True
                                checks.append((endR, endC, d[0], d[1]))
                                break
                            else:
                                pins.append(possiblePin)
                                break
                        else:
                            break
                knightMoves = ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
                for m in knightMoves:
                    endR = startR + m[0]
                    endC = startC + m[1]
                    if 0 <= endR < 8 and 0 <= endC < 8:
                        endPiece = self.board[endR][endC]
                        if endPiece[0] == enemyColor and endPiece[1] == 'N':
                            inCheck = True
                            checks.append((endR,endC,m[0],m[1]))
                return inCheck, pins, checks
class Move:
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
        self.moveID = self.startR * 1000 + self.startC * 100 + self.endR * 10 + self.endC
        print(self.moveID)
    #override equals method
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
    def getChessNotation(self):
        return self.getRankFile(self.startR, self.startC) + self.getRankFile(self.endR, self.endC)
    def getRankFile(self,r,c):
        return self.colsToFiles[c] + self.rowsToRanks[r]