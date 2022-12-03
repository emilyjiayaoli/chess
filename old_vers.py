
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
    
    